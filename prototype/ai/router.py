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

from .provider import (
    Provider,
    ProviderError,
    ProviderTransportError,
    ProviderContentError,
    MissingKeyError,
    MissingModelError,
)
from .anthropic_provider import AnthropicProvider
from .gemini_provider import GeminiProvider
from .openai_provider import OpenAIProvider
from .local_provider import LocalProvider
from .fixture_provider import FixtureProvider
from .schema_adapt import get_provider_schema

_ENV_REF = re.compile(r"^\$\{([A-Z0-9_]+)\}$")

_ADAPTERS = {
    "anthropic": AnthropicProvider,
    "gemini": GeminiProvider,
    "openai": OpenAIProvider,
    "local": LocalProvider,
    "fixture": FixtureProvider,
}


class RoutingError(RuntimeError):
    pass


class PrivacyRoutingError(RoutingError):
    """A privacy-pinned task could not be routed to the local provider."""


class PrivacyRoutingConfigError(RoutingError):
    """A routing rule for privacy: private violates T12 by including non-local providers."""


class BudgetExceededError(RuntimeError):
    """Per-run call or token budget exceeded."""


BudgetError = BudgetExceededError


class SecretScanViolation(RuntimeError):
    """A secret or credential pattern was detected in the prompt context (T6)."""


SECRET_PATTERNS = [
    re.compile(r"\bsk-[a-zA-Z0-9_\-]{20,}\b"),
    re.compile(r"\bAIza[0-9A-Za-z\-_]{30,}\b"),
    re.compile(r"\bghp_[a-zA-Z0-9]{36}\b"),
    re.compile(r"-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----"),
    re.compile(r"\b(?:bearer|token)\s+[a-zA-Z0-9_\-\.]{20,}\b", re.IGNORECASE),
]


def scan_for_secrets(payload: str) -> None:
    """Scan prompt payload for credentials and secret patterns (T6). Abort on match."""
    for pattern in SECRET_PATTERNS:
        if pattern.search(payload):
            raise SecretScanViolation(
                f"Security Gate T6: Secret detected in context payload matching pattern: {pattern.pattern}"
            )


def validate_routing_config(cfg: Dict[str, Any]) -> None:
    """Check that every routing chain matching privacy: private contains only ['local'] (T12-config)."""
    routing_rules = cfg.get("routing", [])
    for idx, rule in enumerate(routing_rules):
        match = rule.get("match", {})
        if match.get("privacy") == "private":
            chain = rule.get("chain", [])
            if chain != ["local"]:
                raise PrivacyRoutingConfigError(
                    f"Routing rule {idx} matches 'privacy: private' but defines chain {chain}. "
                    f"Per T12, private chains must strictly contain only ['local']."
                )


def _resolve_env_ref(value: Any) -> Any:
    """Turn '${AI_MODEL_X}' into the env value (or None if unset)."""
    if isinstance(value, str):
        m = _ENV_REF.match(value.strip())
        if m:
            return os.environ.get(m.group(1)) or None
    return value


class Router:
    def __init__(self, config_path: str | Path = "ai.config.yaml", budget: Dict[str, Any] | None = None,
                 adapter_kwargs: Dict[str, Dict[str, Any]] | None = None):
        raw = yaml.safe_load(Path(config_path).read_text(encoding="utf-8"))
        self.cfg: Dict[str, Any] = raw["ai"]
        validate_routing_config(self.cfg)
        self.providers_cfg: Dict[str, Dict[str, Any]] = self.cfg["providers"]
        self.rules: List[Dict[str, Any]] = self.cfg.get("routing", [])
        self.root: Path = Path(config_path).resolve().parent
        self.budget_cfg: Dict[str, Any] = budget if budget is not None else self.cfg.get("budget", {})
        self.max_tokens_per_run: int | None = self.budget_cfg.get("max_tokens_per_run")
        self.max_calls_per_run: int | None = self.budget_cfg.get("max_calls_per_run")
        self.calls_count: int = 0
        self.tokens_used: int = 0
        self.input_tokens: int = 0
        self.output_tokens: int = 0
        self.request_ids: List[str] = []
        self.last_provider: str = ""
        self.last_model: str = ""
        self.adapter_kwargs: Dict[str, Dict[str, Any]] = adapter_kwargs or {}

    def check_budget_before_call(self, estimated_tokens: int = 0) -> None:
        """Check call and token limits before making a provider call."""
        if self.max_calls_per_run is not None and self.calls_count + 1 > self.max_calls_per_run:
            raise BudgetExceededError(
                f"Per-run call budget exceeded: calls {self.calls_count} + 1 > max_calls_per_run {self.max_calls_per_run}"
            )
        if self.max_tokens_per_run is not None and self.tokens_used + estimated_tokens > self.max_tokens_per_run:
            raise BudgetExceededError(
                f"Per-run token budget exceeded: tokens {self.tokens_used} + {estimated_tokens} > max_tokens_per_run {self.max_tokens_per_run}"
            )

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
    # -- chain selection ---------------------------------------------------
    def select_chain_names(self, task_meta: Dict[str, Any], provider: str | None = None) -> List[str]:
        """Return the ordered provider names for a task (no instantiation)."""
        privacy_pinned = task_meta.get("privacy") == "private"

        if provider is not None:
            if privacy_pinned and provider != "local":
                raise PrivacyRoutingError(
                    f"Task is privacy: private but provider '{provider}' was requested. "
                    f"Refusing to route to any provider other than 'local'."
                )
            pcfg = self.providers_cfg.get(provider)
            if not pcfg or not pcfg.get("enabled", False):
                raise RoutingError(
                    f"Requested provider '{provider}' is disabled in ai.config.yaml or unknown."
                )
            return [provider]

        if privacy_pinned:
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
        if pcfg.get("params"):
            kwargs["params"] = pcfg["params"]
        if pcfg.get("token_param"):
            kwargs["token_param"] = pcfg["token_param"]
        if self.adapter_kwargs and name in self.adapter_kwargs:
            kwargs.update(self.adapter_kwargs[name])
        return _ADAPTERS[name](**kwargs)  # type: ignore[return-value]

    def chain_for(self, task_meta: Dict[str, Any], provider: str | None = None) -> List[Provider]:
        names = self.select_chain_names(task_meta, provider=provider)
        return [self.instantiate(n) for n in names]

    def format_usage_line(self) -> str:
        provider = self.last_provider or self.cfg.get("default_provider", "fixture")
        model = self.last_model or "unavailable"
        req_ids_str = ",".join(self.request_ids) if self.request_ids else "unavailable"
        return (
            f"Run usage: provider={provider} model={model} calls={self.calls_count} "
            f"input_tokens={self.input_tokens} output_tokens={self.output_tokens} "
            f"request_ids={req_ids_str}"
        )

    def format_run_report(
        self,
        contract: str,
        target: str,
        privacy: str,
        generation_mode: str,
        evidence_ids: List[str],
        gate_results: str,
        output_path: str,
        approval_status: str,
    ) -> str:
        provider = self.last_provider or self.cfg.get("default_provider", "fixture")
        model = self.last_model or "unavailable"
        req_ids_str = ",".join(self.request_ids) if self.request_ids else "unavailable"
        evidence_str = ", ".join(evidence_ids) if evidence_ids else "none"

        lines = [
            "### DOCCAD Generation Run Report",
            "",
            f"- **Contract:** {contract}",
            f"- **Target:** {target}",
            f"- **Privacy:** {privacy}",
            f"- **Provider:** {provider}",
            f"- **Returned Model:** {model}",
            f"- **Generation Mode:** {generation_mode}",
            f"- **Calls:** {self.calls_count}",
            f"- **Input Tokens:** {self.input_tokens}",
            f"- **Output Tokens:** {self.output_tokens}",
            f"- **Request IDs:** {req_ids_str}",
            f"- **Evidence IDs:** {evidence_str}",
            f"- **Gate Results:** {gate_results}",
            f"- **Output Path:** {output_path}",
            f"- **Approval Status:** {approval_status}",
            "",
        ]
        return "\n".join(lines)

    def write_step_summary(
        self,
        contract: str,
        target: str,
        privacy: str,
        generation_mode: str,
        evidence_ids: List[str],
        gate_results: str,
        output_path: str,
        approval_status: str,
    ) -> None:
        summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
        if summary_path:
            report_md = self.format_run_report(
                contract=contract,
                target=target,
                privacy=privacy,
                generation_mode=generation_mode,
                evidence_ids=evidence_ids,
                gate_results=gate_results,
                output_path=output_path,
                approval_status=approval_status,
            )
            with open(summary_path, "a", encoding="utf-8") as f:
                f.write(report_md)

    # -- execution with fallback ------------------------------------------
    def run_with_fallback(self, task_meta: Dict[str, Any],
                          messages: List[Dict[str, str]],
                          opts: Dict[str, Any] | None = None,
                          provider: str | None = None) -> Dict[str, Any]:
        for msg in messages:
            if isinstance(msg, dict) and "content" in msg:
                scan_for_secrets(str(msg["content"]))
        errors: List[str] = []
        chain_names = self.select_chain_names(task_meta, provider=provider)
        privacy_pinned = task_meta.get("privacy") == "private"

        est_tokens = int(task_meta.get("context_tokens", 0))
        if est_tokens <= 0 and messages:
            est_tokens = sum(len(str(m.get("content", ""))) // 4 for m in messages if isinstance(m, dict))
        if est_tokens <= 0 and opts and "max_tokens" in opts:
            est_tokens = int(opts["max_tokens"])

        for name in chain_names:
            self.check_budget_before_call(est_tokens)
            try:
                p = self.instantiate(name)
                call_opts = dict(opts) if opts else {}
                if "schema" not in call_opts and "contract" in call_opts:
                    contract = call_opts["contract"]
                    schema = get_provider_schema(contract, name, root_dir=self.root)
                    if schema:
                        call_opts["schema"] = schema
                self.calls_count += 1
                result = p.complete(task_meta, messages, call_opts)
                usage = result.get("usage") or {}
                in_tok = int(usage.get("input_tokens") or 0)
                out_tok = int(usage.get("output_tokens") or 0)
                call_tokens = (in_tok + out_tok) or est_tokens
                self.tokens_used += int(call_tokens)
                self.input_tokens += in_tok
                self.output_tokens += out_tok
                req_id = result.get("request_id")
                if req_id:
                    self.request_ids.append(str(req_id))
                self.last_provider = str(result.get("provider") or name)
                self.last_model = str(result.get("model") or "")
                return result
            except Exception as e:
                if isinstance(e, BudgetExceededError):
                    raise
                self.tokens_used += int(est_tokens)
                errors.append(f"{name}: {e}")
                if privacy_pinned:
                    raise PrivacyRoutingError(
                        f"Privacy-pinned task failed on local provider and MUST NOT "
                        f"fall back to cloud. Cause: {e}"
                    ) from e
                if isinstance(e, ProviderTransportError):
                    continue
                # Fail immediately on content errors or other non-transport errors
                raise
        raise ProviderTransportError(
            "All providers in chain failed:\n  " + "\n  ".join(errors)
        )


def providers_from_config(config_path: str | Path = "ai.config.yaml",
                          task_meta: Dict[str, Any] | None = None
                          ) -> Iterable[Provider]:
    """Convenience: yield provider instances for a task in fallback order."""
    return Router(config_path).chain_for(task_meta or {})
