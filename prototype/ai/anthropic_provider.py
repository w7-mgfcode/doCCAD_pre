"""Anthropic Messages API adapter — plain HTTPS, no SDK (AD-5)."""

from __future__ import annotations

import json
from typing import Any, Callable, Dict, List, Optional

from .http import http_post_json
from .provider import ProviderContentError, ProviderError, require_env, require_model

API_URL = "https://api.anthropic.com/v1/messages"
API_VERSION = "2023-06-01"


def build_anthropic_request(
    model: str,
    messages: List[Dict[str, str]],
    opts: Dict[str, Any],
    api_key: str,
    params: Optional[Dict[str, Any]] = None,
) -> tuple[Dict[str, str], Dict[str, Any]]:
    """Build Anthropic headers and request payload in one function (P2-02, P2-03)."""
    system = "\n\n".join(m["content"] for m in messages if m["role"] == "system")
    chat = [m for m in messages if m["role"] != "system"]
    payload: Dict[str, Any] = {
        "model": model,
        "max_tokens": int(opts.get("max_tokens", 4096)),
        "messages": chat,
    }
    if system:
        payload["system"] = system

    # Sampling parameters: opt-in only if configured in params (P2-03, KB C2.2)
    if params:
        for k in ("temperature", "top_p", "top_k"):
            if k in params:
                payload[k] = params[k]

    # Structured JSON output via output_config.format (P2-02, KB C1.4)
    if "schema" in opts:
        payload["output_config"] = {
            "format": {
                "type": "json_schema",
                "schema": opts["schema"],
            }
        }

    headers = {
        "content-type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": API_VERSION,
    }
    return headers, payload


class AnthropicProvider:
    name = "anthropic"

    def __init__(self, model: str | None, env_key: str = "ANTHROPIC_API_KEY",
                 timeout: int = 120, base_url: str | None = None,
                 sleep_fn: Optional[Callable[[float], None]] = None,
                 params: Optional[Dict[str, Any]] = None):
        self.model = model
        self.env_key = env_key
        self.timeout = timeout
        self.base_url = base_url or API_URL
        self.sleep_fn = sleep_fn
        self.params = params or {}

    def complete(self, task_meta: Dict[str, Any], messages: List[Dict[str, str]],
                 opts: Dict[str, Any] | None = None) -> Dict[str, Any]:
        opts = opts or {}
        api_key = require_env(self.env_key, self.name)
        model = require_model(self.model, self.name)

        headers, payload = build_anthropic_request(
            model=model,
            messages=messages,
            opts=opts,
            api_key=api_key,
            params=self.params,
        )

        body, resp_headers = http_post_json(
            url=self.base_url,
            payload=payload,
            headers=headers,
            timeout=self.timeout,
            provider_name=self.name,
            sleep_fn=self.sleep_fn,
        )

        stop_reason = body.get("stop_reason")
        if stop_reason == "refusal":
            raise ProviderContentError("anthropic request was refused by model (stop_reason: refusal)")

        text = "".join(b.get("text", "") for b in body.get("content", [])
                       if b.get("type") == "text")
        usage = body.get("usage", {})
        returned_model = body.get("model") or model
        req_id = (
            resp_headers.get("request-id")
            or resp_headers.get("x-request-id")
            or resp_headers.get("x-goog-request-id")
            or None
        )
        return {
            "text": text,
            "usage": {"input_tokens": usage.get("input_tokens", 0),
                      "output_tokens": usage.get("output_tokens", 0)},
            "provider": self.name,
            "model": returned_model,
            "request_id": req_id,
        }
