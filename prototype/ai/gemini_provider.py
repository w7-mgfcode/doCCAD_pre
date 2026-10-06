"""Google Gemini generateContent REST adapter — plain HTTPS, no SDK (AD-5)."""

from __future__ import annotations

import json
from typing import Any, Callable, Dict, List, Optional

from .http import http_post_json
from .provider import ProviderContentError, ProviderError, require_env, require_model

API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"


def build_gemini_request(
    model: str,
    messages: List[Dict[str, str]],
    opts: Dict[str, Any],
    api_key: str,
    params: Optional[Dict[str, Any]] = None,
) -> tuple[Dict[str, str], Dict[str, Any]]:
    """Build Gemini headers and request payload in one function (P2-02, P2-03)."""
    system = "\n\n".join(m["content"] for m in messages if m["role"] == "system")
    contents = [
        {"role": "model" if m["role"] == "assistant" else "user",
         "parts": [{"text": m["content"]}]}
        for m in messages if m["role"] != "system"
    ]
    gen_config: Dict[str, Any] = {
        "maxOutputTokens": int(opts.get("max_tokens", 4096)),
    }

    # Sampling parameters: opt-in only if configured in params (P2-03, KB C2.2)
    if params:
        for k in ("temperature", "topP", "topK"):
            if k in params:
                gen_config[k] = params[k]

    # Structured JSON output via responseMimeType + responseJsonSchema (P2-02, KB C1.1)
    if "schema" in opts:
        gen_config["responseMimeType"] = "application/json"
        gen_config["responseJsonSchema"] = opts["schema"]

    payload: Dict[str, Any] = {
        "contents": contents,
        "generationConfig": gen_config,
    }
    if system:
        payload["systemInstruction"] = {"parts": [{"text": system}]}

    headers = {
        "content-type": "application/json",
        "x-goog-api-key": api_key,
    }
    return headers, payload


class GeminiProvider:
    name = "gemini"

    def __init__(self, model: str | None, env_key: str = "GEMINI_API_KEY",
                 timeout: int = 120, base_url: str | None = None,
                 sleep_fn: Optional[Callable[[float], None]] = None,
                 params: Optional[Dict[str, Any]] = None):
        self.model = model
        self.env_key = env_key
        self.timeout = timeout
        self.base_url = base_url
        self.sleep_fn = sleep_fn
        self.params = params or {}

    def complete(self, task_meta: Dict[str, Any], messages: List[Dict[str, str]],
                 opts: Dict[str, Any] | None = None) -> Dict[str, Any]:
        opts = opts or {}
        api_key = require_env(self.env_key, self.name)
        model = require_model(self.model, self.name)

        headers, payload = build_gemini_request(
            model=model,
            messages=messages,
            opts=opts,
            api_key=api_key,
            params=self.params,
        )

        url = self.base_url or f"{API_BASE}/{model}:generateContent"

        body, _ = http_post_json(
            url=url,
            payload=payload,
            headers=headers,
            timeout=self.timeout,
            provider_name=self.name,
            sleep_fn=self.sleep_fn,
        )

        try:
            candidates = body.get("candidates") or []
            if not candidates:
                # Check for block/refusal
                prompt_feedback = body.get("promptFeedback", {})
                block_reason = prompt_feedback.get("blockReason")
                if block_reason:
                    raise ProviderContentError(f"gemini prompt was blocked by safety: {block_reason}")
                raise ProviderError(f"gemini returned no candidates: {body}")
            candidate = candidates[0]
            finish_reason = candidate.get("finishReason")
            if finish_reason in ("SAFETY", "RECITATION", "BLOCKLIST", "PROHIBITED_CONTENT"):
                raise ProviderContentError(f"gemini generation refused ({finish_reason})")
            parts = candidate["content"]["parts"]
        except (KeyError, IndexError) as e:
            raise ProviderError(f"gemini malformed response: {body}") from e

        text = "".join(p.get("text", "") for p in parts)
        usage = body.get("usageMetadata", {})
        returned_model = body.get("modelVersion") or body.get("model") or model
        return {
            "text": text,
            "usage": {"input_tokens": usage.get("promptTokenCount", 0),
                      "output_tokens": usage.get("candidatesTokenCount", 0)},
            "provider": self.name,
            "model": returned_model,
        }
