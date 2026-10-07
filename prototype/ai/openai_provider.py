"""OpenAI chat-completions REST adapter — plain HTTPS, no SDK (AD-5)."""

from __future__ import annotations

import json
from typing import Any, Callable, Dict, List, Optional

from .http import http_post_json
from .provider import ProviderContentError, ProviderError, require_env, require_model

API_URL = "https://api.openai.com/v1/chat/completions"


def build_openai_request(
    model: str,
    messages: List[Dict[str, str]],
    opts: Dict[str, Any],
    api_key: str,
    params: Optional[Dict[str, Any]] = None,
    token_param: str = "max_tokens",
) -> tuple[Dict[str, str], Dict[str, Any]]:
    """Build OpenAI headers and request payload in one function (P2-02, P2-03)."""
    max_tokens = int(opts.get("max_tokens", 4096))
    payload: Dict[str, Any] = {
        "model": model,
        "messages": messages,
    }

    # Token parameter name: opt-in max_completion_tokens (P2-03, KB C1.10)
    if token_param == "max_completion_tokens":
        payload["max_completion_tokens"] = max_tokens
    else:
        payload["max_tokens"] = max_tokens

    # Sampling parameters: opt-in only if configured in params (P2-03, KB C2.2)
    if params:
        for k in ("temperature", "top_p", "frequency_penalty", "presence_penalty"):
            if k in params:
                payload[k] = params[k]

    # Structured JSON output via response_format strict json_schema (P2-02, KB C1.8, C1.9)
    if "schema" in opts:
        payload["response_format"] = {
            "type": "json_schema",
            "json_schema": {
                "name": opts.get("schema_name", "output_schema"),
                "strict": True,
                "schema": opts["schema"],
            },
        }

    headers = {
        "content-type": "application/json",
        "authorization": f"Bearer {api_key}",
    }
    return headers, payload


class OpenAIProvider:
    name = "openai"

    def __init__(self, model: str | None, env_key: str = "OPENAI_API_KEY",
                 timeout: int = 120, base_url: str | None = None,
                 sleep_fn: Optional[Callable[[float], None]] = None,
                 params: Optional[Dict[str, Any]] = None,
                 token_param: str = "max_tokens"):
        self.model = model
        self.env_key = env_key
        self.timeout = timeout
        self.base_url = base_url or API_URL
        self.sleep_fn = sleep_fn
        self.params = params or {}
        self.token_param = token_param

    def complete(self, task_meta: Dict[str, Any], messages: List[Dict[str, str]],
                 opts: Dict[str, Any] | None = None) -> Dict[str, Any]:
        opts = opts or {}
        api_key = require_env(self.env_key, self.name)
        model = require_model(self.model, self.name)

        headers, payload = build_openai_request(
            model=model,
            messages=messages,
            opts=opts,
            api_key=api_key,
            params=self.params,
            token_param=self.token_param,
        )

        body, resp_headers = http_post_json(
            url=self.base_url,
            payload=payload,
            headers=headers,
            timeout=self.timeout,
            provider_name=self.name,
            sleep_fn=self.sleep_fn,
        )

        try:
            choice = body["choices"][0]
            message = choice["message"]
            refusal = message.get("refusal")
            if refusal:
                raise ProviderContentError(f"openai request was refused by model: {refusal}")
            text = message.get("content") or ""
        except (KeyError, IndexError) as e:
            raise ProviderError(f"openai malformed response: {body}") from e

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
            "usage": {"input_tokens": usage.get("prompt_tokens", 0),
                      "output_tokens": usage.get("completion_tokens", 0)},
            "provider": self.name,
            "model": returned_model,
            "request_id": req_id,
        }
