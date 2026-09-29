"""Local OpenAI-compatible endpoint adapter (Ollama, llama.cpp server, vLLM).

Used for privacy-pinned tasks (AD-5 / router privacy rule): no data leaves the
machine. No API key is required by default; if LOCAL_API_KEY is set it is sent as a
bearer token (vLLM deployments sometimes require one).
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any, Dict, List

from .provider import ProviderError, require_model


class LocalProvider:
    name = "local"

    def __init__(self, model: str | None,
                 endpoint: str = "http://localhost:11434/v1",
                 env_key: str = "LOCAL_API_KEY", timeout: int = 300):
        self.model = model
        self.endpoint = endpoint.rstrip("/")
        self.env_key = env_key
        self.timeout = timeout

    def complete(self, task_meta: Dict[str, Any], messages: List[Dict[str, str]],
                 opts: Dict[str, Any] | None = None) -> Dict[str, Any]:
        opts = opts or {}
        model = require_model(self.model, self.name)

        payload: Dict[str, Any] = {
            "model": model,
            "messages": messages,
            "max_tokens": int(opts.get("max_tokens", 4096)),
        }
        if "temperature" in opts:
            payload["temperature"] = float(opts["temperature"])

        headers = {"content-type": "application/json"}
        key = os.environ.get(self.env_key, "").strip()
        if key:
            headers["authorization"] = f"Bearer {key}"

        req = urllib.request.Request(
            f"{self.endpoint}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            raise ProviderError(
                f"local HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:500]}"
            ) from e
        except urllib.error.URLError as e:
            raise ProviderError(
                f"local endpoint {self.endpoint} unreachable: {e.reason}. "
                f"Privacy-pinned tasks hard-fail here — they never fall back to cloud."
            ) from e

        try:
            text = body["choices"][0]["message"]["content"] or ""
        except (KeyError, IndexError) as e:
            raise ProviderError(f"local malformed response: {body}") from e
        usage = body.get("usage", {})
        return {
            "text": text,
            "usage": {"input_tokens": usage.get("prompt_tokens", 0),
                      "output_tokens": usage.get("completion_tokens", 0)},
            "provider": self.name,
            "model": model,
        }
