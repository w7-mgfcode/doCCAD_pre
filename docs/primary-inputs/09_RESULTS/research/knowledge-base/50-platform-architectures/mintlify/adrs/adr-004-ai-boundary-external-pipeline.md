# ADR-004: AI boundary — external provider-abstracted generation; Mintlify AI as optional consumer surface only

## Status
Proposed (2026-08-12)

## Context
The ecosystem mandates a provider abstraction (Claude/Gemini/OpenAI/local models) for generating derived content, and forbids AI in the serving path. Mintlify ships substantial built-in AI: an assistant (reader Q&A), an agent + automations (PR-writing maintenance bot), an admin MCP for AI tools to edit content/settings, and agent-job REST APIs. These are Pro-plan features, credit-metered, and run on Mintlify-chosen models (own-model endpoints only on Enterprise self-host). Separately, Mintlify auto-publishes AI-consumption surfaces that cost nothing and require no vendor AI: llms.txt/llms-full.txt, per-page `.md` endpoints, the site search MCP server, skill.md, and the contextual menu.

## Decision
- All content *generation* (derived views, translations) runs in the ecosystem's own GitHub Actions pipeline behind its own provider abstraction. Mintlify's agent, automations, and agent-job API are not architectural dependencies.
- The zero-cost AI-consumption surfaces (llms.txt, `.md` export, search MCP, skill.md, contextual menu) are enabled and treated as product features of the published site.
- `markdown.instructions` in `docs.json` and `<Visibility for="agents">` blocks are used to shape what external AI consumers see — maintained as canonical content.
- The Mintlify assistant (reader-facing Q&A) is a deferred, optional add-on: it may be enabled if/when on Pro, but nothing depends on it; disabling it must not degrade the documented experience.
- The admin MCP is not connected by default; if ever used for convenience editing, it is scoped to the single deployment and constrained to PR mode by branch protection.

## Consequences
- Provider independence and cost control are preserved; model choice/upgrades happen in code we own.
- We forgo the convenience of Mintlify automations (changelog, broken-links fixes, translations) or reimplement the few we need as Actions.
- The published site remains fully AI-optional to serve, matching the static-first rule.
- If the assistant is later enabled, its answer quality depends on the same content hygiene (frontmatter, structure) the pipeline already enforces — no extra authoring cost.

## Alternatives
- **Mintlify agent/automations as the generation engine:** fastest start, tight platform integration (PR grouping, Slack), but provider-locked, credit-metered, and couples the ecosystem's core differentiator to a vendor black box.
- **Hybrid (Mintlify automations for maintenance, external pipeline for derivation):** viable later; rejected initially to keep one generation path and one review discipline.
