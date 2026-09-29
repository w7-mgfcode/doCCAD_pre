"""OpenAI chat-completions REST adapter — plain HTTPS, no SDK (AD-5)."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any, Dict, List

from .provider import ProviderError, require_env, require_model

API_URL = "https://api.openai.com/v1/chat/completions"


class OpenAIProvider:
    name = "openai"

    def __init__(self, model: str | None, env_key: str = "OPENAI_API_KEY",
                 timeout: int = 120):
        self.model = model
        self.env_key = env_key
        self.timeout = timeout

    def complete(self, task_meta: Dict[str, Any], messages: List[Dict[str, str]],
                 opts: Dict[str, Any] | None = None) -> Dict[str, Any]:
        opts = opts or {}
        api_key = require_env(self.env_key, self.name)
        model = require_model(self.model, self.name)

        payload: Dict[str, Any] = {
            "model": model,
            "messages": messages,  # OpenAI accepts system/user/assistant natively
            "max_tokens": int(opts.get("max_tokens", 4096)),
        }
        if "temperature" in opts:
            payload["temperature"] = float(opts["temperature"])

        req = urllib.request.Request(
            API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"content-type": "application/json",
                     "authorization": f"Bearer {api_key}"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            raise ProviderError(
                f"openai HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:500]}"
            ) from e
        except urllib.error.URLError as e:
            raise ProviderError(f"openai unreachable: {e.reason}") from e

        try:
            text = body["choices"][0]["message"]["content"] or ""
        except (KeyError, IndexError) as e:
            raise ProviderError(f"openai malformed response: {body}") from e
        usage = body.get("usage", {})
        return {
            "text": text,
            "usage": {"input_tokens": usage.get("prompt_tokens", 0),
                      "output_tokens": usage.get("completion_tokens", 0)},
            "provider": self.name,
            "model": model,
        }
