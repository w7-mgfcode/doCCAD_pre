# ADR-005: Generated Content Persists Only Through Pull Requests

Status: Accepted · 2026-08-12

## Context
Options for persisting AI output: direct commit to main; auto-merge bot PRs; human-approved PRs; ephemeral
runtime pages never persisted.

## Decision
All generated artifacts land on docs-gen/* branches as PRs carrying a machine-produced run report (evidence
list, gates passed, tokens, provider). Branch protection requires human approval; auto-merge is disabled for
generation PRs; the bot cannot approve its own PRs. Unmerged drafts expire after 30 days. Special-question
pages follow the same path (preview PR -> approval -> versioned page).

## Consequences
+ Human gate on every published derived word; provenance recorded at merge; misinformation and injection
  outcomes are bounded by review; full audit trail free from GitHub.
- Reviewer latency and fatigue (mitigated: small diffs, batching, run reports); not suitable for real-time
  Q&A (explicit non-goal).

## Alternatives
Auto-persist rejected (bypasses the only trustworthy gate). Ephemeral-only rejected (loses versioning,
review and reuse). Direct commit rejected outright.
