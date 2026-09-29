---
id: architecture-ai-generation-plane
slug: /architecture/ai-generation-plane
title: AI Generation Plane & Provider Abstraction
type: canonical
audience: [developer, architect]
owners: [architecture]
sources: [ai/provider.py, ai/router.py, ai.config.yaml]
related: [architecture-system-overview, decisions-adr-004-provider-abstraction]
ai_generation:
  allowed: true
  derived_pages: [recruiter, interview]
last_validated: 2026-09-21
---

# AI Generation Plane & Provider Abstraction

<!-- Archive mapping: Adapted from 06_AI_DOCUMENTATION/model-strategy/ai_architecture.md and ADR-004 -->

DOCCAD treats AI as an **offline enrichment layer**, not a serving-time dependency.

## Provider Abstraction Design (AD-5)

Rather than importing massive multi-agent orchestration frameworks (such as LangChain, AutoGen, or CrewAI), DOCCAD defines a clean, ~40-line Python `Protocol`:

```python
class Provider(Protocol):
    name: str

    def complete(
        self,
        task_meta: Dict[str, Any],
        messages: List[Dict[str, str]],
        opts: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        """Returns: {text, usage, provider, model}"""
```

### Why Thin Adapters Beat Frameworks
1. **Auditable Security**: Each provider adapter (Anthropic, Gemini, OpenAI, Local, Fixture) is plain HTTP/JSON code without hidden background prompts or tracking.
2. **Deterministic Control**: Token usage, error codes, and headers are directly exposed to quality gates.
3. **Low Maintenance**: Upgrading or adding a provider requires zero core architectural refactoring.

## Routing Engine & Privacy Hard-Pinning

Routing logic is declared in `ai.config.yaml` and resolved dynamically by `ai/router.py`:

```yaml
ai:
  default_provider: fixture
  providers:
    fixture:   {enabled: true,  model: "deterministic-demo-fixture"}
    anthropic: {enabled: true,  env_key: ANTHROPIC_API_KEY, model: ${AI_MODEL_ANTHROPIC}}
    gemini:    {enabled: true,  env_key: GEMINI_API_KEY,    model: ${AI_MODEL_GEMINI}}
    openai:    {enabled: true,  env_key: OPENAI_API_KEY,    model: ${AI_MODEL_OPENAI}}
    local:     {enabled: false, endpoint: "http://localhost:11434/v1", model: ${AI_MODEL_LOCAL}}
  routing:
    - match: {privacy: private}
      chain: [local]
    - match: {}
      chain: [fixture, anthropic, gemini, openai]
```

### The Irrevocable Privacy Rule
If a task specifies `privacy: private`, the router pins the provider chain to `local`. If the local endpoint is unavailable, `Router` raises a `PrivacyRoutingError`. Falling back to cloud APIs for private tasks is prohibited by code design.
