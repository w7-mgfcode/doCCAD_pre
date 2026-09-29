---
id: practice-ci-quality-gates
title: CI Quality Gates — The Deterministic Gate Ladder
type: knowledge
category: best-practices
tags: [ci, validation, quality-gates, negative-testing, deterministic-checks]
sources:
  - outputs/03_solution/ARCHITECTURE-SPINE.md (AD-10)
  - outputs/03_solution/automation_architecture.md (§3)
  - outputs/05_poc/.github/workflows/docs-validate.yml, outputs/05_poc/scripts/validate_docs.py
  - outputs/05_poc/VALIDATION_NOTES.md (§b–c, §f)
  - outputs/03_solution/security_architecture.md (validation criteria)
confidence: HIGH
related: [pattern-hash-drift-detection, pattern-pr-gated-generation, practice-github-actions-security, pattern-task-contracts]
---

# CI Quality Gates — The Deterministic Gate Ladder

**Summary** — Every PR (human or bot) passes an ordered ladder of deterministic, merge-blocking checks: lint → frontmatter schema → internal links → Mermaid compile → full build. AI-assisted checks are advisory labels only, never gates. The ladder's authority comes from two disciplines: cheap-and-specific checks run before expensive-and-general ones, and every gate is negative-tested — proven to actually fail on bad input.

## Core Logic

**The ladder** (docs-validate.yml, runs on every PR with `contents: read` only, no secrets):

1. **Lint** — markdownlint plus YAML well-formedness of contracts, config and workflows. Catches syntax garbage in seconds.
2. **Frontmatter schema validation** (`validate_docs.py`) — every page's metadata contract, plane integrity (no generated files in canonical paths), and provenance hash currency.
3. **Internal link check** — via `docusaurus build` with `onBrokenLinks: throw`; a broken internal link is a build failure and therefore a merge block.
4. **Mermaid compile** — mermaid-cli renders every `.mmd` and in-page diagram in sandboxed headless Chromium; a diagram that doesn't compile blocks merge.
5. **Manifest rebuild + impact/drift annotations** — advisory output for reviewers (stale sets, drift suspects).
6. **Security checks** — secrets scan (gitleaks-style), pinned-action audit.
7. **Full `docusaurus build`** — both plugin instances, both locales — the general integration gate; MDX v3 strictness means malformed AI output cannot merge.

**Order rationale.** Each rung is cheaper and more diagnostic than the next: a schema error should be reported as "field X invalid," not as a cryptic build stack trace three minutes later. The build comes last because it subsumes everything but explains nothing. The whole ladder is deterministic: same input, same verdict — which is what qualifies it to be merge-blocking. AI-assisted checks (fact-consistency, change classification) are labels helping the reviewer, "never merge-blocking on their own" (AD-10), because a non-reproducible check cannot fairly gate a merge.

**Negative testing.** A gate is only proven when it has failed on purpose. The security architecture's validation criteria demand that the MDX restriction, link allowlist, Mermaid compile and config-schema gates "each have at least one deliberately failing fixture in the test suite proving the gate actually blocks." VERIFIED BY EXECUTION in 05_poc: a `content_hash` deliberately corrupted via sed made `validate_docs.py` exit 1 naming the exact stale page and source, then pass again after restore; separately, `onBrokenLinks: throw` genuinely failed the build on two wrong slugs during PoC bring-up — the gate caught a real defect before it ever guarded a PR.

## Best Practices

1. **Order gates cheap→expensive, specific→general**, because feedback latency and diagnosability determine whether authors trust and use CI.
2. **Make merge-blocking checks deterministic only**, because flaky or judgment-based gates get overridden, and overriding becomes habit.
3. **Negative-test every gate with a failing fixture**, because a gate that has never failed is unverified — the PoC's corrupted-hash test is the model.
4. **Reuse the build as the final integration gate** (broken links, MDX strictness), because the framework's own validation is stronger than any recreation of it.
5. **Run validation with zero secrets**, because the gate job executes untrusted PR content; validation needs read access, nothing more.
6. **Keep advisory signals visibly advisory** (labels, comments, checklists), because mixing advice into the pass/fail channel erodes both.

## Pitfalls

- External link checking does not belong in the merge gate: "the web rots independently of PRs" — it runs as a scheduled weekly job instead.
- Blocking merges on code-vs-docs drift suspicion was rejected as review theater; the checklist comment respects author judgment.
- A gate ladder without the human gate behind it is incomplete: every deterministic check can pass on fluently wrong content (see pattern-pr-gated-generation).
- Tool gaps must be recorded, not papered over: actionlint was unavailable in the PoC environment, so workflows were YAML-parse-validated and the gap explicitly logged — the honest fallback also runs as the "lint-light" step.

## Expert Notes

The ladder doubles as the AI repair loop's oracle: on gate failure, the generation pipeline performs exactly one repair retry *with the validator error appended* — deterministic gates thus provide machine-readable feedback to the model without ever ceding gate authority to it. Also note the gates' second job: they run identically on human and bot PRs, so quality policy is uniform and the bot earns no special path. Dependency bumps get the same treatment — a Dependabot PR that breaks Mermaid compile cannot merge.

## Evidence & Further Reading

- `outputs/03_solution/automation_architecture.md` §3 — full pipeline specs for validate/generate/publish/scheduled workflows.
- `outputs/05_poc/.github/workflows/docs-validate.yml` — the ladder as an executable workflow.
- `outputs/05_poc/VALIDATION_NOTES.md` §b (build-gate catch of real slug defects), §c (negative hash test), §f (Mermaid compilation).
- `outputs/03_solution/security_architecture.md` — validation criteria requiring deliberately-failing fixtures per gate.
