"""Local OpenAI-compatible endpoint adapter (Ollama, llama.cpp server, vLLM).

Used for privacy-pinned tasks (AD-5 / router privacy rule): no data leaves the
machine. No API key is required by default; if LOCAL_API_KEY is set it is sent as a
bearer token (vLLM deployments sometimes require one).
"""

from __future__ import annotations

import json
import os
from typing import Any, Callable, Dict, List, Optional

from .http import http_post_json
from .provider import ProviderContentError, ProviderError, require_model


API_DEFAULT_ENDPOINT = "http://localhost:11434/v1"


def build_local_request(
    model: str,
    messages: List[Dict[str, str]],
    opts: Dict[str, Any],
    key: str = "",
    params: Optional[Dict[str, Any]] = None,
    token_param: str = "max_tokens",
) -> tuple[Dict[str, str], Dict[str, Any]]:
    """Build OpenAI-compatible request payload for local endpoint (P2-02, P2-03)."""
    max_tokens = int(opts.get("max_tokens", 4096))
    payload: Dict[str, Any] = {
        "model": model,
        "messages": messages,
    }
    if token_param == "max_completion_tokens":
        payload["max_completion_tokens"] = max_tokens
    else:
        payload["max_tokens"] = max_tokens

    # Sampling parameters: opt-in only if configured in params (P2-03, KB C2.2)
    if params:
        for k in ("temperature", "top_p"):
            if k in params:
                payload[k] = params[k]

    # Structured JSON output via response_format strict json_schema (P2-02, KB C1.12)
    if "schema" in opts:
        payload["response_format"] = {
            "type": "json_schema",
            "json_schema": {
                "name": opts.get("schema_name", "output_schema"),
                "strict": True,
                "schema": opts["schema"],
            },
        }

    headers = {"content-type": "application/json"}
    if key:
        headers["authorization"] = f"Bearer {key}"
    return headers, payload


def build_local_native_request(
    model: str,
    messages: List[Dict[str, str]],
    opts: Dict[str, Any],
    key: str = "",
    params: Optional[Dict[str, Any]] = None,
) -> tuple[Dict[str, str], Dict[str, Any]]:
    """Build native Ollama /api/chat payload with stream: false (P2-02, KB C1.11)."""
    payload: Dict[str, Any] = {
        "model": model,
        "messages": messages,
        "stream": False,
    }
    if params:
        payload["options"] = dict(params)

    # Native Ollama structured JSON format (KB C1.11)
    if "schema" in opts:
        payload["format"] = opts["schema"]

    headers = {"content-type": "application/json"}
    if key:
        headers["authorization"] = f"Bearer {key}"
    return headers, payload


class LocalProvider:
    name = "local"

    def __init__(self, model: str | None,
                 endpoint: str = API_DEFAULT_ENDPOINT,
                 env_key: str = "LOCAL_API_KEY", timeout: int = 300,
                 base_url: str | None = None,
                 sleep_fn: Optional[Callable[[float], None]] = None,
                 params: Optional[Dict[str, Any]] = None,
                 token_param: str = "max_tokens"):
        self.model = model
        self.endpoint = endpoint.rstrip("/")
        self.env_key = env_key
        self.timeout = timeout
        self.base_url = base_url
        self.sleep_fn = sleep_fn
        self.params = params or {}
        self.token_param = token_param

    def complete(self, task_meta: Dict[str, Any], messages: List[Dict[str, str]],
                 opts: Dict[str, Any] | None = None) -> Dict[str, Any]:
        opts = opts or {}
        model = require_model(self.model, self.name)
        key = os.environ.get(self.env_key, "").strip()

        is_native = self.endpoint.endswith("/api") or self.endpoint.endswith("/api/chat")
        if is_native:
            headers, payload = build_local_native_request(
                model=model,
                messages=messages,
                opts=opts,
                key=key,
                params=self.params,
            )
            url = self.base_url or (self.endpoint if self.endpoint.endswith("/chat") else f"{self.endpoint}/chat")
            body, _ = http_post_json(
                url=url,
                payload=payload,
                headers=headers,
                timeout=self.timeout,
                provider_name=self.name,
                sleep_fn=self.sleep_fn,
            )
        else:
            headers, payload = build_local_request(
                model=model,
                messages=messages,
                opts=opts,
                key=key,
                params=self.params,
                token_param=self.token_param,
            )
            url = self.base_url or f"{self.endpoint}/chat/completions"
            try:
                body, _ = http_post_json(
                    url=url,
                    payload=payload,
                    headers=headers,
                    timeout=self.timeout,
                    provider_name=self.name,
                    sleep_fn=self.sleep_fn,
                )
            except ProviderError as e:
                # Fall back to native /api/chat if 404 and endpoint was /v1
                if "404" in str(e) and "/v1" in self.endpoint and not self.base_url:
                    native_url = self.endpoint.replace("/v1", "/api/chat")
                    n_headers, n_payload = build_local_native_request(
                        model=model,
                        messages=messages,
                        opts=opts,
                        key=key,
                        params=self.params,
                    )
                    body, _ = http_post_json(
                        url=native_url,
                        payload=n_payload,
                        headers=n_headers,
                        timeout=self.timeout,
                        provider_name=self.name,
                        sleep_fn=self.sleep_fn,
                    )
                else:
                    raise

        try:
            if "choices" in body:
                choice = body["choices"][0]
                message = choice["message"]
                refusal = message.get("refusal")
                if refusal:
                    raise ProviderContentError(f"local request was refused: {refusal}")
                text = message.get("content") or ""
            elif "message" in body:
                message = body["message"]
                refusal = message.get("refusal")
                if refusal:
                    raise ProviderContentError(f"local request was refused: {refusal}")
                text = message.get("content") or ""
            else:
                text = body.get("response") or ""
        except (KeyError, IndexError) as e:
            raise ProviderError(f"local malformed response: {body}") from e

        usage = body.get("usage", {})
        returned_model = body.get("model") or model
        return {
            "text": text,
            "usage": {"input_tokens": usage.get("prompt_tokens", usage.get("prompt_eval_count", 0)),
                      "output_tokens": usage.get("completion_tokens", usage.get("eval_count", 0))},
            "provider": self.name,
            "model": returned_model,
        }
