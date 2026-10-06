"""HTTP helper for provider adapters (P2-04): retry, error classification, redaction, usage logging."""

from __future__ import annotations

import json
import logging
import random
import re
import socket
import time
import urllib.error
import urllib.request
from typing import Any, Callable, Dict, List, Optional, Tuple

from .provider import ProviderError, ProviderTransportError

logger = logging.getLogger("doccad.ai.http")

RETRYABLE_STATUSES = {429, 500, 502, 503, 504, 529}
TERMINAL_STATUSES = {400, 401, 403, 404}


def sanitize_text(text: str, sensitive_values: Optional[List[str]] = None) -> str:
    """Sanitize and truncate error text, redacting keys and auth headers."""
    if not text:
        return ""
    if sensitive_values:
        for val in sensitive_values:
            if val and len(val) >= 4:
                text = text.replace(val, "[REDACTED]")
    # Redact common auth header patterns
    text = re.sub(r'(?i)(authorization\s*[:=]\s*(?:Bearer\s+)?)[^\s,"\']+', r'\1[REDACTED]', text)
    text = re.sub(r'(?i)(x-api-key\s*[:=]\s*)[^\s,"\']+', r'\1[REDACTED]', text)
    text = re.sub(r'(?i)(x-goog-api-key\s*[:=]\s*)[^\s,"\']+', r'\1[REDACTED]', text)
    # Redact common key patterns
    text = re.sub(r'sk-[a-zA-Z0-9_-]{10,}', '[REDACTED]', text)
    text = re.sub(r'AIza[a-zA-Z0-9_-]{10,}', '[REDACTED]', text)
    return text[:500]


def is_quota_429(status: int, body_text: str, headers: Dict[str, str]) -> bool:
    """Check if 429 response is a non-retryable quota or spend cap limit."""
    if status != 429:
        return False
    lower = body_text.lower()
    if "insufficient_quota" in lower:
        return True
    if "enforced_spend_limit_reached" in lower:
        # Anthropic spend limit reached with no Retry-After
        if not headers.get("retry-after"):
            return True
    return False


def extract_usage_summary(body: Dict[str, Any]) -> str:
    """Extract token and cache usage summary without payloads."""
    usage = body.get("usage") or body.get("usageMetadata") or {}
    parts = []
    for in_key in ("prompt_tokens", "promptTokenCount", "input_tokens"):
        if in_key in usage:
            parts.append(f"in={usage[in_key]}")
            break
    for out_key in ("completion_tokens", "candidatesTokenCount", "output_tokens"):
        if out_key in usage:
            parts.append(f"out={usage[out_key]}")
            break
    for c_key in ("cache_creation_input_tokens", "cache_read_input_tokens", "cachedContentTokenCount"):
        if c_key in usage:
            parts.append(f"{c_key}={usage[c_key]}")
    if "prompt_tokens_details" in usage:
        details = usage["prompt_tokens_details"]
        if isinstance(details, dict) and "cached_tokens" in details:
            parts.append(f"cached_tokens={details['cached_tokens']}")
    return " ".join(parts) if parts else "none"


def http_post_json(
    url: str,
    payload: Dict[str, Any] | str | bytes,
    headers: Dict[str, str],
    timeout: int = 120,
    provider_name: str = "provider",
    max_retries: int = 3,
    backoff_base: float = 0.5,
    sleep_fn: Optional[Callable[[float], None]] = None,
) -> Tuple[Dict[str, Any], Dict[str, str]]:
    """Post JSON payload with retry, error classification, redaction and usage logging.

    Returns (response_body_dict, response_headers_dict).
    """
    if sleep_fn is None:
        sleep_fn = time.sleep

    # Collect sensitive values from auth headers for redaction
    sensitive_values: List[str] = []
    for k, v in headers.items():
        if k.lower() in ("authorization", "x-api-key", "x-goog-api-key") and v:
            sensitive_values.append(v)
            if v.lower().startswith("bearer "):
                sensitive_values.append(v[7:].strip())

    if isinstance(payload, (dict, list)):
        data = json.dumps(payload).encode("utf-8")
    elif isinstance(payload, str):
        data = payload.encode("utf-8")
    else:
        data = payload

    attempt = 0
    while True:
        req = urllib.request.Request(
            url,
            data=data,
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                status = resp.status if hasattr(resp, "status") else 200
                resp_headers = {k.lower(): v for k, v in resp.headers.items()}
                raw_bytes = resp.read()
                try:
                    raw_body = raw_bytes.decode("utf-8")
                except UnicodeDecodeError as e:
                    raise ProviderError(f"{provider_name} response body is not valid UTF-8") from e
                try:
                    body_dict = json.loads(raw_body)
                except json.JSONDecodeError as e:
                    raise ProviderError(
                        f"{provider_name} malformed JSON response: {sanitize_text(raw_body, sensitive_values)}"
                    ) from e
                if not isinstance(body_dict, dict):
                    raise ProviderError(
                        f"{provider_name} JSON response is {type(body_dict).__name__}, expected an object"
                    )

                req_id = (
                    resp_headers.get("x-request-id")
                    or resp_headers.get("request-id")
                    or resp_headers.get("x-goog-request-id")
                    or ""
                )
                usage_summary = extract_usage_summary(body_dict)
                logger.info(
                    "provider=%s status=%d request_id=%s usage=[%s]",
                    provider_name,
                    status,
                    req_id,
                    usage_summary,
                )
                return body_dict, resp_headers

        except urllib.error.HTTPError as e:
            try:
                status = e.code
                resp_headers = {k.lower(): v for k, v in e.headers.items()} if e.headers else {}
                body_text = e.read().decode("utf-8", "replace")
                clean_body = sanitize_text(body_text, sensitive_values)

                # Terminal status
                if status in TERMINAL_STATUSES or is_quota_429(status, body_text, resp_headers):
                    raise ProviderError(
                        f"{provider_name} HTTP {status}: {clean_body}"
                    ) from e

                # Retryable status
                if status in RETRYABLE_STATUSES:
                    if attempt < max_retries:
                        retry_after = resp_headers.get("retry-after")
                        if retry_after:
                            try:
                                delay = float(retry_after)
                            except ValueError:
                                delay = backoff_base * (2 ** attempt) + random.uniform(0, 0.1)
                        else:
                            delay = backoff_base * (2 ** attempt) + random.uniform(0, 0.1)
                        attempt += 1
                        sleep_fn(delay)
                        continue
                    else:
                        raise ProviderTransportError(
                            f"{provider_name} HTTP {status} (retries exhausted after {attempt} attempts): {clean_body}"
                        ) from e

                # Other status
                raise ProviderError(f"{provider_name} HTTP {status}: {clean_body}") from e
            finally:
                e.close()

        except (urllib.error.URLError, TimeoutError, socket.timeout) as e:
            clean_reason = sanitize_text(str(getattr(e, "reason", e)), sensitive_values)
            if attempt < max_retries:
                delay = backoff_base * (2 ** attempt) + random.uniform(0, 0.1)
                attempt += 1
                sleep_fn(delay)
                continue
            raise ProviderTransportError(
                f"{provider_name} transport unreachable ({type(e).__name__}): {clean_reason}"
            ) from e
