"""Provider abstraction (AD-5): one interface, thin adapters, no framework.

Every adapter implements ``complete(task_meta, messages, opts) -> dict`` returning::

    {"text": str, "usage": {"input_tokens": int, "output_tokens": int},
     "provider": str, "model": str}

``messages`` is a list of ``{"role": "system"|"user"|"assistant", "content": str}``.
``task_meta`` carries contract/task identifiers for logging only — adapters must not
branch on it. ``opts`` may carry ``max_tokens`` and ``temperature``.

Model identifiers come from configuration (ai.config.yaml -> env vars), never from
code. API keys come only from environment variables.
"""

from __future__ import annotations

from typing import Any, Dict, List, Protocol, runtime_checkable


class ProviderError(RuntimeError):
    """Base error for provider failures (transport, HTTP, malformed response)."""


class MissingKeyError(ProviderError):
    """Raised when the provider's API key env var is absent or empty."""


class MissingModelError(ProviderError):
    """Raised when no model identifier is configured for the provider."""


@runtime_checkable
class Provider(Protocol):
    """Structural interface every adapter satisfies."""

    name: str

    def complete(
        self,
        task_meta: Dict[str, Any],
        messages: List[Dict[str, str]],
        opts: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        """Run one completion and return {text, usage, provider, model}."""
        ...


def require_env(env_var: str, provider_name: str) -> str:
    """Fetch a required API key from the environment with a clear error."""
    import os

    value = os.environ.get(env_var, "").strip()
    if not value:
        raise MissingKeyError(
            f"Provider '{provider_name}' requires the environment variable "
            f"{env_var} to be set. No key found — refusing to call. "
            f"(Keys are never stored in files; see .env.example.)"
        )
    return value


def require_model(model: str | None, provider_name: str) -> str:
    """Ensure a model id was resolved from config/env, never hard-coded."""
    if not model:
        raise MissingModelError(
            f"Provider '{provider_name}' has no model configured. Set the model "
            f"env var referenced in ai.config.yaml (see .env.example)."
        )
    return model
