"""Config-driven provider router (AD-5 / ai_architecture §2).

Loads ai.config.yaml, resolves ${ENV_VAR} model references, applies ordered routing
rules and returns an ordered chain of provider instances. Rules:

1. ``privacy: private`` is ENFORCED: the chain is pinned to the local provider and a
   PrivacyRoutingError is raised if it cannot be satisfied — never a cloud fallback.
2. First matching rule wins (task match, context-size match, then the {} default).
3. Fallback iteration (``run_with_fallback``) advances on transport/HTTP failures
   only — never on content grounds.
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List

import yaml

from .provider import Provider, ProviderError
from .anthropic_provider import AnthropicProvider
from .gemini_provider import GeminiProvider
from .openai_provider import OpenAIProvider
from .local_provider import LocalProvider

_ENV_REF = re.compile(r"^\$\{([A-Z0-9_]+)\}$")

_ADAPTERS = {
    "anthropic": AnthropicProvider,
    "gemini": GeminiProvider,
    "openai": OpenAIProvider,
    "local": LocalProvider,
}


class RoutingError(RuntimeError):
    pass


class PrivacyRoutingError(RoutingError):
    """A privacy-pinned task could not be routed to the local provider."""


def _resolve_env_ref(value: Any) -> Any:
    """Turn '${AI_MODEL_X}' into the env value (or None if unset)."""
    if isinstance(value, str):
        m = _ENV_REF.match(value.strip())
        if m:
            return os.environ.get(m.group(1)) or None
    return value


class Router:
    def __init__(self, config_path: str | Path = "ai.config.yaml"):
        raw = yaml.safe_load(Path(config_path).read_text(encoding="utf-8"))
        self.cfg: Dict[str, Any] = raw["ai"]
        self.providers_cfg: Dict[str, Dict[str, Any]] = self.cfg["providers"]
        self.rules: List[Dict[str, Any]] = self.cfg.get("routing", [])

    # -- rule matching -----------------------------------------------------
    @staticmethod
    def _ctx_matches(spec: str, context_tokens: int) -> bool:
        m = re.match(r"^([<>])\s*(\d+)k$", str(spec).strip())
        if not m:
            return False
        limit = int(m.group(2)) * 1000
        return context_tokens > limit if m.group(1) == ">" else context_tokens < limit

    def _rule_matches(self, match: Dict[str, Any], task_meta: Dict[str, Any]) -> bool:
        if not match:  # {} default rule
            return True
        if "privacy" in match and task_meta.get("privacy") != match["privacy"]:
            return False
        if "task" in match and task_meta.get("task") != match["task"]:
            return False
        if "context_tokens" in match and not self._ctx_matches(
                match["context_tokens"], int(task_meta.get("context_tokens", 0))):
            return False
        return True

    # -- chain selection ---------------------------------------------------
    def select_chain_names(self, task_meta: Dict[str, Any]) -> List[str]:
        """Return the ordered provider names for a task (no instantiation)."""
        if task_meta.get("privacy") == "private":
            # Hard pin (AD-5): never silently upgrade a private task to cloud.
            local_cfg = self.providers_cfg.get("local", {})
            if not local_cfg.get("enabled", False):
                raise PrivacyRoutingError(
                    "Task is privacy: private but the local provider is disabled "
                    "in ai.config.yaml. Refusing to route to any cloud provider."
                )
            return ["local"]
        for rule in self.rules:
            if self._rule_matches(rule.get("match", {}), task_meta):
                chain = [p for p in rule["chain"]
                         if self.providers_cfg.get(p, {}).get("enabled", False)]
                if chain:
                    return chain
        default = self.cfg.get("default_provider")
        if default and self.providers_cfg.get(default, {}).get("enabled", False):
            return [default]
        raise RoutingError(f"No enabled provider chain matches task {task_meta!r}")

    def instantiate(self, name: str) -> Provider:
        pcfg = self.providers_cfg[name]
        model = _resolve_env_ref(pcfg.get("model"))
        kwargs: Dict[str, Any] = {"model": model}
        if pcfg.get("env_key"):
            kwargs["env_key"] = pcfg["env_key"]
        if name == "local" and pcfg.get("endpoint"):
            kwargs["endpoint"] = pcfg["endpoint"]
        return _ADAPTERS[name](**kwargs)  # type: ignore[return-value]

    def chain_for(self, task_meta: Dict[str, Any]) -> List[Provider]:
        return [self.instantiate(n) for n in self.select_chain_names(task_meta)]

    # -- execution with fallback ------------------------------------------
    def run_with_fallback(self, task_meta: Dict[str, Any],
                          messages: List[Dict[str, str]],
                          opts: Dict[str, Any] | None = None) -> Dict[str, Any]:
        errors: List[str] = []
        chain = self.chain_for(task_meta)
        privacy_pinned = task_meta.get("privacy") == "private"
        for provider in chain:
            try:
                return provider.complete(task_meta, messages, opts)
            except ProviderError as e:
                errors.append(f"{provider.name}: {e}")
                if privacy_pinned:
                    raise PrivacyRoutingError(
                        f"Privacy-pinned task failed on local provider and MUST NOT "
                        f"fall back to cloud. Cause: {e}"
                    ) from e
        raise ProviderError(
            "All providers in chain failed:\n  " + "\n  ".join(errors)
        )


def providers_from_config(config_path: str | Path = "ai.config.yaml",
                          task_meta: Dict[str, Any] | None = None
                          ) -> Iterable[Provider]:
    """Convenience: yield provider instances for a task in fallback order."""
    return Router(config_path).chain_for(task_meta or {})
