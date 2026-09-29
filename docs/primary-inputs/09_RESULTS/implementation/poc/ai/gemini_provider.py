"""Google Gemini generateContent REST adapter — plain HTTPS, no SDK (AD-5)."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any, Dict, List

from .provider import ProviderError, require_env, require_model

API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"


class GeminiProvider:
    name = "gemini"

    def __init__(self, model: str | None, env_key: str = "GEMINI_API_KEY",
                 timeout: int = 120):
        self.model = model
        self.env_key = env_key
        self.timeout = timeout

    def complete(self, task_meta: Dict[str, Any], messages: List[Dict[str, str]],
                 opts: Dict[str, Any] | None = None) -> Dict[str, Any]:
        opts = opts or {}
        api_key = require_env(self.env_key, self.name)
        model = require_model(self.model, self.name)

        system = "\n\n".join(m["content"] for m in messages if m["role"] == "system")
        contents = [
            {"role": "model" if m["role"] == "assistant" else "user",
             "parts": [{"text": m["content"]}]}
            for m in messages if m["role"] != "system"
        ]
        payload: Dict[str, Any] = {
            "contents": contents,
            "generationConfig": {
                "maxOutputTokens": int(opts.get("max_tokens", 4096)),
            },
        }
        if system:
            payload["systemInstruction"] = {"parts": [{"text": system}]}
        if "temperature" in opts:
            payload["generationConfig"]["temperature"] = float(opts["temperature"])

        url = f"{API_BASE}/{model}:generateContent"
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"content-type": "application/json",
                     "x-goog-api-key": api_key},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            raise ProviderError(
                f"gemini HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:500]}"
            ) from e
        except urllib.error.URLError as e:
            raise ProviderError(f"gemini unreachable: {e.reason}") from e

        try:
            parts = body["candidates"][0]["content"]["parts"]
        except (KeyError, IndexError) as e:
            raise ProviderError(f"gemini malformed response: {body}") from e
        text = "".join(p.get("text", "") for p in parts)
        usage = body.get("usageMetadata", {})
        return {
            "text": text,
            "usage": {"input_tokens": usage.get("promptTokenCount", 0),
                      "output_tokens": usage.get("candidatesTokenCount", 0)},
            "provider": self.name,
            "model": model,
        }
