"""Anthropic Messages API adapter — plain HTTPS, no SDK (AD-5)."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any, Dict, List

from .provider import ProviderError, require_env, require_model

API_URL = "https://api.anthropic.com/v1/messages"
API_VERSION = "2023-06-01"


class AnthropicProvider:
    name = "anthropic"

    def __init__(self, model: str | None, env_key: str = "ANTHROPIC_API_KEY",
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
        chat = [m for m in messages if m["role"] != "system"]
        payload: Dict[str, Any] = {
            "model": model,
            "max_tokens": int(opts.get("max_tokens", 4096)),
            "messages": chat,
        }
        if system:
            payload["system"] = system
        if "temperature" in opts:
            payload["temperature"] = float(opts["temperature"])

        req = urllib.request.Request(
            API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "content-type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": API_VERSION,
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            raise ProviderError(
                f"anthropic HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:500]}"
            ) from e
        except urllib.error.URLError as e:
            raise ProviderError(f"anthropic unreachable: {e.reason}") from e

        text = "".join(b.get("text", "") for b in body.get("content", [])
                       if b.get("type") == "text")
        usage = body.get("usage", {})
        return {
            "text": text,
            "usage": {"input_tokens": usage.get("input_tokens", 0),
                      "output_tokens": usage.get("output_tokens", 0)},
            "provider": self.name,
            "model": model,
        }
