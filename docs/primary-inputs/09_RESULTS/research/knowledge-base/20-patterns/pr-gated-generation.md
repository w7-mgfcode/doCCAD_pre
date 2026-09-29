---
id: pattern-pr-gated-generation
title: PR-Gated Generation — Bot Branch, Run Report, Human Approval
type: knowledge
category: patterns
tags: [pull-requests, human-in-the-loop, governance, bot-branches, review]
sources:
  - outputs/03_solution/ARCHITECTURE-SPINE.md (AD-9)
  - outputs/03_solution/ADRs/adr-005-generated-content-via-pr.md
  - outputs/03_solution/solution_architecture.md (§20)
  - outputs/03_solution/security_architecture.md (T2, T11, §7)
  - outputs/05_poc/.github/workflows/docs-generate.yml
confidence: HIGH
related: [pattern-canonical-generated-separation, pattern-ai-in-ci-not-serving, pattern-task-contracts, practice-github-actions-security, practice-ci-quality-gates]
---

# PR-Gated Generation — Bot Branch, Run Report, Human Approval

**Summary** — AI output persists exclusively through pull requests: the bot commits to `docs-gen/*` branches, the PR carries a machine-produced run report, branch protection requires human approval, and auto-merge is banned for generation PRs. This is the single control standing between model output and the published site that no prompt injection can defeat deterministically — which is precisely why it may never be automated away.

## Core Logic

**Problem.** Four ways existed to persist AI output: direct commit to main, auto-merged bot PRs, human-approved PRs, or ephemeral runtime pages never persisted. Direct commit and auto-merge bypass the only trustworthy gate; ephemeral output loses versioning, review and reuse.

**Solution structure.**

1. A generation job (triggered by `workflow_dispatch`, issue form, or the stale-set sweep — never by PR events) runs a task contract and writes artifacts under `docs/generated/**` only.
2. The bot commits to a branch named `docs-gen/<task>-<id>` and opens a PR.
3. The PR carries a **run report**: evidence file list (so grounding is reviewable), gates passed, token usage, and which provider/model actually served the task.
4. The full deterministic validation pipeline runs on the PR (practice-ci-quality-gates).
5. **Human approval is required** by branch protection; the bot cannot approve its own PRs; auto-merge is never enabled for generation PRs.
6. On merge, `approval_status: approved` is set by merge automation and provenance is fixed at merge time.
7. **Draft expiry**: unmerged drafts expire with branch deletion after 30 days — abandoned AI output does not accumulate as ambient repo state.

Special-question pages follow the identical path: structured request → preview PR → approval → versioned page under `generated/questions/`; drafts expire unmerged.

**Why auto-merge is banned.** The threat model is explicit: delimiting and schema gates reduce but do not eliminate prompt injection; "an injection that produces schema-valid, allowlist-clean, plausible-but-wrong prose survives to human review… this is why AD-9 forbids auto-merge" (T2). The security simplicity check states the trade directly: "Auto-merge deletes the only non-deterministic-proof gate against T2/T11; one click per PR is cheap." The same gate bounds misinformation (T11), the top *business* risk for a recruiter-facing site.

VERIFIED BY EXECUTION in 05_poc (partially): `docs-generate.yml` implements the bot-branch flow with least-privilege permissions and environment-protected secrets; the dry run printed the would-be branch name `docs-gen/generaterecruiterpage-architecture-system-overview`. Actual PR opening was placeholder-commented (no GitHub runner in the environment) — an honestly recorded gap.

## Best Practices

1. **Attach a run report to every generation PR**, because a reviewer who can see the evidence list, gates and provider can review grounding, not just prose.
2. **Keep generation diffs small and batched**, because reviewer fatigue is the pattern's real failure mode; wholesale file replacement (no AI-edits-AI diffs) keeps diffs comprehensible.
3. **Enforce the gate with platform features** (branch protection, required reviews, bot-cannot-self-approve), because policy documents don't block merges — settings do.
4. **Expire unmerged drafts (30 days)**, because stale bot branches otherwise become an unreviewed shadow corpus.
5. **Record approval status in frontmatter at merge**, because "approved" must be a machine-set fact, not an editable claim.

## Pitfalls

- Reviewer latency is the accepted cost; this pattern is explicitly *not suitable for real-time Q&A* — that's a non-goal, and pretending otherwise reintroduces runtime AI.
- Auto-merging "obviously clean" PRs is the seductive regression: every deterministic gate can pass on a page that is fluently wrong. The gates filter; the human decides.
- A human gate that rubber-stamps is worse than none (false assurance). Mitigations are structural: small diffs, run reports, provenance banners keeping reviewers oriented.
- Don't let the bot write outside `docs/generated/**` — CI fails such PRs (pattern-canonical-generated-separation); the write-scope gate and the approval gate back each other up.

## Expert Notes

This pattern converts GitHub's native machinery into an AI governance system for free: history, blame, rollback, audit trail, review UI — all inherited (ADR-001). The rejected alternatives are worth remembering verbatim: "Auto-persist rejected (bypasses the only trustworthy gate). Ephemeral-only rejected (loses versioning, review and reuse). Direct commit rejected outright." Takedown is also PR-shaped: revert the generation PR, redeploy, then diagnose which layer failed — canon, contract, prompt, or hash gate (security runbook R3).

## Evidence & Further Reading

- `outputs/03_solution/ADRs/adr-005-generated-content-via-pr.md` — decision, consequences, alternatives.
- `outputs/03_solution/security_architecture.md` T2, T11, §7 simplicity check, §6 R3 takedown runbook.
- `outputs/03_solution/solution_architecture.md` §20 — special-question lifecycle with expiry.
- `outputs/05_poc/.github/workflows/docs-generate.yml` — concrete workflow; `outputs/05_poc/VALIDATION_NOTES.md` §e.
