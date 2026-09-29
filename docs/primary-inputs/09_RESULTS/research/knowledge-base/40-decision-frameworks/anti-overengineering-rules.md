---
id: framework-anti-overengineering-rules
title: Anti-Overengineering Rules — Every Component Beats a Simpler Alternative
type: knowledge
category: decision-frameworks
tags: [simplicity, minimalism, solo-operator, design-discipline, gate-e]
sources:
  - outputs/00_research/analysis_brief.md (anti-overengineering as hard rule)
  - outputs/03_solution/ARCHITECTURE-SPINE.md (invariants, Deferred)
  - outputs/03_solution/security_architecture.md (§7 Simplicity Check)
  - outputs/03_solution/ai_architecture.md (§2 inline "beat" notes)
  - outputs/04_validation/validation_report.md (Gate E)
confidence: HIGH
related: [framework-weighted-decision-model, pattern-leveled-retrieval, pattern-thin-provider-abstraction, framework-build-vs-buy-vs-host]
---

# Anti-Overengineering Rules — Every Component Beats a Simpler Alternative

**Summary** — Anti-overengineering was a *hard rule* of the corpus, not a taste: the system must be operable by one capable engineer, and every component must demonstrably beat a simpler alternative — with the beaten alternative named in writing where the component is defined. Validation Gate E audited exactly this. The discipline produced an MVP of "a repo + one static site + four CI workflows" while a conventional design of the same requirements would have shipped a vector DB, a graph DB, an agent framework, and a server fleet.

## Core Logic

**The rule set** (distilled from the mission invariants, spine, and Gate E):

1. **One-engineer operability is a design constraint**, not an aspiration — every control and component is sized to be read, debugged, and evolved by a single person ("every control… is a file the engineer can read in one sitting").
2. **Every component names the simpler alternative it beat.** This is the enforcement mechanism: ADRs 001–009 all carry Alternatives sections; the AI architecture annotates components inline ("Beat: LangChain… Beat: per-task hard-coded clients"); the security architecture maintains a full Simplicity Check table — control vs simpler alternative vs why the control wins — with the standing instruction: "If a control ever stops beating its simpler alternative, downgrade it."
3. **Defer by naming, not by silence.** Unbuilt capabilities are recorded with their trigger conditions (Level-2 retrieval, runtime chat, SSO, graph store, auto-HU-translation) so restraint is a decision with a paper trail, and escalation requires evidence, "not enthusiasm."
4. **Deterministic and platform-native before custom** — a file beats a service; a GitHub feature beats a self-hosted tool; a hash beats a model call.
5. **Structures must earn existence**: a taxonomy directory requires ≥2 planned pages or content starts in the parent; adding a Docusaurus plugin requires an ADR ("process friction as a control").

**The Gate E questions.** Applied to each component:
- **Can this be removed?** (Removals actually applied: no vector DB, no graph DB, no search cluster, no Kubernetes/microservices/servers, no agent framework, no runtime AI.)
- **Can the framework do it?** (Broken-link checking = `docusaurus build`; separation = multi-instance plugin; i18n = filesystem locales.)
- **Can GitHub Actions do it?** ("GitHub Actions and repo files cover every automation requirement" — no orchestrator, no job runner, no queue.)
- **Can a file do it?** (Dependency graph = one manifest JSON that beat a graph DB "for a query set answerable by one dict lookup"; allowlist = one YAML; incident log = `SECURITY-LOG.md` one-liners.)

**Rejecting complexity is also a decision.** The Simplicity Check cuts both ways: some rows record rejecting the *more* complex option (no WAF/CDN layer, no guard-model gate, no OIDC proxy for providers — "a proxy adds a server to a serverless design — rejected as theater"). Symmetrically, "nothing" must also be beaten: the incident log wins over no log because "'nothing' loses the memory that makes the third incident cheaper than the first."

## Best Practices

1. **Write the beaten alternative into the component's home document**, because a simplicity claim without a named alternative is unauditable and unrevisitable.
2. **Ask the four questions in order (remove / framework / Actions / file)** before designing anything custom, because each yes eliminates a maintenance surface permanently.
3. **Attach evidence-based triggers to every deferral**, because "later" without a boundary means either never or whenever someone gets excited.
4. **Audit simplicity as a validation gate**, because a rule that isn't checked at the end was a wish.
5. **Re-run the comparison over time** — downgrade controls that stop beating their alternative — because simplicity debt accrues in both directions.

## Pitfalls

- Anti-overengineering is not minimalism theater: the system still has 13 modeled threats, 9 task contracts, and a full gate ladder. The rule trims *components*, not rigor.
- The most dangerous additions are prestigious ones (vector DB, multi-agent orchestration): each was rejected specifically because "no requirement justifies them" — requirements, not fashion, admit components.
- Under-engineering hides here too: skipping the human gate, the schema checks, or the incident log would be "simpler" and wrong; each survives because it beats its simpler alternative *on the record*.
- A named-alternative discipline degenerates into boilerplate if the "why it wins" column isn't concrete — the corpus's rows cite effort, blast radius, and failure modes, not platitudes.

## Expert Notes

The framework's quiet power is that it converts architecture review into a falsifiable exercise: any reviewer can pick a component, read its beaten alternative, and argue the comparison — no access to the architect's intent required. It also composes with the weighted decision model: simplicity carried 12% weight in platform selection, and MkDocs — "architecturally the simplest system in the field" — still lost on maintenance evidence, proving the rule is *beats the simpler alternative*, not *simplest wins*.

## Evidence & Further Reading

- `outputs/04_validation/validation_report.md` Gate E — the audit and the applied-removal list.
- `outputs/03_solution/security_architecture.md` §7 — the 15-row Simplicity Check table, including complexity-rejection rows.
- `outputs/03_solution/ai_architecture.md` §2 — inline "beat" annotations; `outputs/03_solution/ADRs/` — Alternatives sections throughout.
- `outputs/03_solution/ARCHITECTURE-SPINE.md` — Deferred section (named non-decisions with triggers).
