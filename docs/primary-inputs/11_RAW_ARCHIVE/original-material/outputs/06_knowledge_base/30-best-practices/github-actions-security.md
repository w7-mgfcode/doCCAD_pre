---
id: practice-github-actions-security
title: GitHub Actions Security for AI Pipelines
type: knowledge
category: best-practices
tags: [github-actions, ci-security, secrets, oidc, pwn-request, supply-chain]
sources:
  - outputs/03_solution/security_architecture.md (§3, §5, T7, T8, T9, T13)
  - outputs/03_solution/automation_architecture.md (§3, §5)
  - outputs/05_poc/.github/workflows/docs-validate.yml, docs-generate.yml
confidence: HIGH
related: [practice-ci-quality-gates, pattern-pr-gated-generation, pattern-ai-in-ci-not-serving, practice-prompt-injection-defenses]
---

# GitHub Actions Security for AI Pipelines

**Summary** — When CI holds AI provider keys and write access, the workflows themselves become the primary attack surface. The distilled posture: least-privilege permissions per workflow, provider secrets confined to a protected environment reachable only from `main`, an outright ban on the pwn-request patterns, SHA-pinned actions, unprivileged fork-PR validation, and OIDC where it genuinely applies (Pages deploys) — with an honest note on where it doesn't (model provider APIs).

## Core Logic

**Least-privilege permissions.** Repo default is read-only; each workflow declares exactly what it needs:

```yaml
# validate (every PR):      permissions: { contents: read }
# generate (dispatch only): permissions: { contents: write, pull-requests: write }
#                           environment: generation   # provider keys live ONLY here
# deploy:                   permissions: { contents: read, pages: write, id-token: write }
#                           environment: github-pages
```

A leaked validate-job token can read the public repo — nothing else. Grep-checkability is part of the design: "every workflow file contains an explicit `permissions:` block" is a stated validation criterion.

**Environment-protected secrets.** The three provider keys exist only in a `generation` environment whose deployment-branch policy is `main` — fork PRs and feature branches can never resolve them. An optional required-reviewer on the environment acts as a cheap tripwire for scheduled runs. Rotation is quarterly and runbook-scripted (revoke first on suspicion); **hard spend limits in every provider console** are named as "the actual blast-radius control for a solo operator" — a stolen key's damage is capped in currency.

**Pwn-request patterns, banned (T8).** Two classic vectors: (a) `pull_request_target` workflows checking out PR head code with secrets available; (b) expression injection — `run: echo "${{ github.event.pull_request.title }}"` interpolates attacker text into the shell (branch names, labels, issue bodies likewise). Policy: `pull_request_target` is banned repo-wide and CI asserts its absence; no `${{ github.event.* }}` interpolation inside `run:` blocks — untrusted fields pass through `env:` (env vars are data, not shell text). Generation jobs trigger only on `workflow_dispatch`/`schedule`/push to `main` — never on PR events. Result per the threat model: the pwn-request class is "effectively eliminated… by never mixing PR-triggered execution with privilege."

**Fork-PR policy.** Fork PRs get full deterministic validation with a read-only token and no environment secrets (GitHub's default, kept); the repo additionally requires approval for all outside-collaborator workflow runs.

**SHA pinning + supply chain (T9).** Every `uses:` references a full 40-char commit SHA with the version as a trailing comment — tags are mutable, SHAs are not. Lockfiles committed, `npm ci` only; pip pinned with `--require-hashes`; Dependabot maintains the pins (native beats self-hosted Renovate for one engineer). The generation scripts are deliberately SDK-free, keeping vendor dependency trees out of the secrets zone. mermaid-cli (headless Chromium parsing partially bot-authored input) runs only in the secretless validation job.

**OIDC — honest scoping.** Pages deploys use the OIDC `id-token: write` flow — no stored deploy credential exists to steal, and it's *less* setup than a PAT. But model providers authenticate with static API keys; "claiming otherwise would be inventing capability." The honest ceiling is static keys + environment protection + spend limits, revisited if providers ship workload-identity federation for inference.

## Best Practices

1. **Declare a `permissions:` block in every workflow and lint for it**, because the default token is broader than any docs job needs.
2. **Bind provider secrets to a branch-restricted environment, not repo secrets**, because repo secrets are exposed to any privileged workflow on any branch — same setup effort, strictly better isolation.
3. **Ban `pull_request_target` and event-field interpolation in `run:`**, and assert the ban in CI, because these two patterns account for the realistic secret-exfiltration paths.
4. **Pin actions to commit SHAs and let Dependabot move the pins**, because a hijacked tag is a supply-chain compromise that costs nothing to prevent.
5. **Set provider spend limits**, because for a solo operator a hard cap beats any monitoring stack.
6. **Separate trigger classes**: PR events → validation only; privileged generation → dispatch/schedule/main-push only.

## Pitfalls

- Mixing validation and generation in one workflow inevitably leaks privilege into PR-triggered paths — keep them as separate files with separate triggers and permissions.
- Don't trade Chromium's sandbox for container convenience: if the image forces `--no-sandbox`, run mermaid-cli on the plain runner instead.
- The PoC pinned actions to major version tags with an explicit note to SHA-pin in production — acceptable only because it was labeled; unlabeled it would be drift.
- If a privileged workflow ever ran against untrusted PR code, assume secret exposure and rotate all keys immediately (runbook R2/R1).

## Expert Notes

The pattern behind the rules: **privilege follows trigger, not repository**. What a job may do is determined by what event started it and which environment it can enter — never by whose code it processes. That single principle generates the whole posture, and it is what lets a public repo safely accept anonymous PRs into a pipeline that elsewhere holds three paid API keys and a publish path.

## Evidence & Further Reading

- `outputs/03_solution/security_architecture.md` §3 (identity/secrets, permissions blocks, environments, rotation), §5 (supply chain), T7/T8/T9/T13, §6 runbooks R1/R2.
- `outputs/03_solution/automation_architecture.md` §3, §5 — workflow triggers and security posture summary.
- `outputs/05_poc/.github/workflows/docs-validate.yml`, `docs-generate.yml` — permissions blocks and environment usage in executable form.
