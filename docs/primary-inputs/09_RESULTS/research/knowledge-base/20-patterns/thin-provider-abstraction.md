---
id: pattern-thin-provider-abstraction
title: Thin Provider Abstraction — Protocol, Four Adapters, YAML Routing
type: knowledge
category: patterns
tags: [provider-independence, llm-routing, privacy, no-framework, adapters]
sources:
  - outputs/03_solution/ARCHITECTURE-SPINE.md (AD-5)
  - outputs/03_solution/ADRs/adr-004-provider-abstraction.md
  - outputs/03_solution/ai_architecture.md (§2)
  - outputs/05_poc/ai/ (provider.py, router.py, four adapters), outputs/05_poc/ai.config.yaml
  - outputs/04_validation/validation_report.md (Gate D)
confidence: HIGH
related: [pattern-ai-in-ci-not-serving, pattern-task-contracts, framework-anti-overengineering-rules, practice-prompt-injection-defenses]
---

# Thin Provider Abstraction — Protocol, Four Adapters, YAML Routing

**Summary** — Model access sits behind one Python Protocol (`complete(task_meta, messages, opts) → {text, usage, provider, model}`), four ~40-line HTTP adapters (Anthropic, Gemini, OpenAI, OpenAI-compatible local), and a router that reads ordered provider chains from `ai.config.yaml`. No LangChain, no LiteLLM, no agent framework. Provider churn becomes a config edit; privacy routing is a hard-enforced pin, not a preference.

## Core Logic

**Problem.** Generation must work against multiple cloud providers *and* a local endpoint, with routing by privacy class, task type, context size, structured-output need, cost tier, and availability — without provider lock-in and without importing a framework's dependency tree into the credentialed CI zone.

**Solution structure.**

```
ai/
├── provider.py   # Protocol: complete(task_meta, messages, opts) -> {text, usage, provider, model}
├── anthropic.py  # Messages API over raw HTTPS
├── gemini.py     # generateContent REST
├── openai.py     # chat completions REST
├── local.py      # OpenAI-compatible endpoint (Ollama, llama.cpp, vLLM)
└── router.py     # ai.config.yaml policy -> ordered provider chain
```

**Mechanics.**
- Routing rules match on task metadata and yield an ordered fallback chain, e.g. default `[anthropic, gemini, openai]`, large-context `[gemini, anthropic]`.
- **Privacy hard-pin**: `match: {privacy: private} → chain: [local]` — enforced, not advisory. If the local provider is unavailable, the job hard-fails rather than silently upgrading to a cloud provider; a CI schema gate on `ai.config.yaml` rejects any config whose private chain contains a cloud adapter (threat T12). VERIFIED BY EXECUTION in 05_poc: `generate_page.py --privacy private` raised `PrivacyRoutingError` and exited 1 with the local provider disabled.
- Fallback triggers only on availability errors (5xx/timeout) — never on content grounds, so routing can't be gamed by output.
- Model names live *only* in config/env (`${AI_MODEL_ANTHROPIC}` etc.), never in code: provider model churn never requires a code change.
- One repair retry maximum; no autonomous loops, no multi-agent orchestration, no latency-based load balancing — all deliberately absent under the anti-overengineering rule.

VERIFIED BY EXECUTION in 05_poc: dry-run assembled the chain `anthropic → gemini → openai` from `ai.config.yaml` with zero keys present and no network call; live calls are code-complete but unexercised (no keys, by design — honestly recorded).

## Best Practices

1. **Keep adapters small enough to audit in one sitting** (~40 lines each), because the adapter layer runs inside the secrets zone and auditability is the security control.
2. **Put every model name and key reference in config/env, never code**, because model IDs churn faster than architecture.
3. **Make privacy routing fail closed** — hard error, not cloud fallback — and validate it with a config schema gate, because a tired config edit must not be able to break the policy.
4. **Restrict fallback to availability errors**, because content-triggered fallback turns routing into an unauditable quality judgment.
5. **Log token counts, never payloads**, in adapters, because provider-call logs otherwise become a secret/PII sink.

## Pitfalls

- **LangChain/LiteLLM-style frameworks were rejected**: hundreds of transitive dependencies to wrap four HTTP POST shapes — supply-chain exposure in the credentialed zone, debugging opacity for one engineer, and no needed feature (streaming is pointless for batch generation).
- **Per-task hard-coded clients** were rejected because routing logic would fork per script.
- Owning four adapters means owning their upkeep; mitigated by contract tests and the deliberately SDK-free, near-stdlib footprint (stdlib + PyYAML + raw HTTPS).
- Don't add providers speculatively: Phase 1 of the roadmap runs one cloud adapter plus local; the full four-provider routing arrives in Phase 2.

## Expert Notes

The abstraction is thin *on purpose*: the interface is the smallest thing that supports routing and provenance stamping (the run report records which provider actually served each task, making the routing policy auditable per AD-8). The SDK-free choice is also a supply-chain decision — three fewer vendor dependency trees in the zone that holds API keys (security_architecture.md §5). The local adapter is not a toy: it is what makes Modes A/C (self-hosted, privacy-oriented, fully offline generation) the *same architecture* as cloud Mode B, differing only in `ai.config.yaml` routing and hosting target (ADR-009).

## Evidence & Further Reading

- `outputs/03_solution/ADRs/adr-004-provider-abstraction.md` — decision and rejected alternatives.
- `outputs/03_solution/ai_architecture.md` §2 — routing policy YAML and supported criteria.
- `outputs/05_poc/ai/` and `outputs/05_poc/ai.config.yaml` — working implementation; `outputs/05_poc/VALIDATION_NOTES.md` §e — dry-run and privacy hard-fail transcripts.
- `outputs/03_solution/security_architecture.md` T12 and §5 — cross-provider exposure and dependency budget.
