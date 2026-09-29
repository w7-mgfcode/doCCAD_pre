---
id: foundation-docs-as-code
title: Docs-as-Code — Git as Source of Truth, PR as Editorial Gate, CI as Quality Gate
type: knowledge
category: foundations
tags: [docs-as-code, git, github, pr-review, ci, canonicality, governance]
sources:
  - outputs/00_research/analysis_brief.md            # target-ecosystem definition
  - outputs/01_products/gitbook/SAD_gitbook.md       # GitHub Integration, Threat Model (block-model counter-example)
  - outputs/01_products/docusaurus/SAD_docusaurus.md # Business & Functional Fit, GitHub Integration
  - outputs/01_products/mkdocs/SAD_mkdocs.md         # Extensibility, AI Integration Suitability
  - outputs/01_products/mintlify/SAD_mintlify.md     # GitHub Integration (SaaS that still passes)
  - outputs/02_comparison/comparison.md              # "Git-canonicality is not uniform" finding
confidence: HIGH
related: [foundation-ssg-anatomy, foundation-markdown-mdx-frontmatter, platform-gitbook, platform-docusaurus, platform-comparison-logic]
---

# Docs-as-Code — Git as Source of Truth, PR as Editorial Gate, CI as Quality Gate

**Summary** — Docs-as-code treats documentation exactly like software: content is plain text files in a Git repository, every change flows through a pull request that a human reviews, and CI runs deterministic checks that can fail the merge. This corpus's six-platform analysis shows the paradigm is not a feature checkbox but a structural property — some platforms have it by construction, some emulate it, and one (GitBook) demonstrates precisely how a platform can *look* docs-as-code while its real source of truth lives elsewhere.

## Core Logic

The paradigm has three load-bearing mechanisms, and each maps to a different guarantee:

1. **Git as the canonical store.** All system state — content, navigation, configuration, translations, even theme overrides — is version-controlled text. This yields deterministic file identity (a page is exactly the bytes in the repo), free history/backup/rollback, and provider independence: the corpus outlives any renderer. In the field study, Docusaurus, MkDocs, Zensical and Hyperbook satisfy this by construction ("no content store other than the repo" [VERIFIED-REPO] for Docusaurus; MkDocs is "Git-tracked text" end to end [VERIFIED-REPO]). Mintlify satisfies it despite being SaaS: MDX + `docs.json` live in your repo, and even its web editor and AI agent write back via commits/PRs [VERIFIED-OFFICIAL].

2. **PR review as the editorial gate.** Because content is files, GitHub's review machinery (branch protection, required checks, CODEOWNERS) becomes the documentation's editorial workflow for free. This matters doubly when an AI layer generates derived content: generated Markdown lands as a PR like any human change, so provenance, diff review and rejection cost nothing extra. This is why the target ecosystem's brief made "derived AI content goes through validation + PR review" a hard rule — the gate already exists; you only have to route through it.

3. **CI as the quality gate.** A deterministic build doubles as an automated reviewer: MkDocs `--strict` and single-file Python hooks, Docusaurus `onBrokenLinks: 'throw'` + MDX compilation + Joi frontmatter validation, Zensical `--strict` link/anchor validation — all fail the PR, not production [VERIFIED-REPO for all three]. Failure modes are build-time and loud; the published site never sees malformed content.

**The counter-model: CMS/SaaS content stores.** The canonical counter-example is GitBook. Its Git Sync bidirectionally mirrors a repo, but the **operational source of truth is GitBook's internal block document model — Markdown is a serialization that gets parsed on import and regenerated on export** [VERIFIED-OFFICIAL]. Consequences documented by GitBook itself: exports are normalized (not byte-faithful), sync "may create new markdown files instead of using the existing ones", README files duplicate, GitHub PRs do not become GitBook change requests, and app-side merges land as direct `GITBOOK-n` commits that bypass GitHub PR review [VERIFIED-OFFICIAL]. Git becomes a *faithful mirror*, not the engine. A system whose drift detection and provenance depend on deterministic file identity cannot be built on a mirror — this single finding drove GitBook's disqualification despite competent scores elsewhere (see [comparison-logic](../10-platforms/comparison-logic.md)).

The dividing question is therefore not "does it sync with Git?" but: **if the repo and the platform disagree, which one wins?** In true docs-as-code, the repo wins by definition because there is nothing else.

## Best Practices

1. **Make the build the validation gate.** Run the full production build on every PR with strictness maxed (broken links, frontmatter schema, compile errors) — because a failing PR is infinitely cheaper than a broken deploy, and it is the only reviewer that never gets tired.
2. **Route all writers — human, AI, WYSIWYG editors — through commits.** If a platform offers an app-side editing path that commits directly (GitBook change requests), disable or role-restrict it; otherwise your editorial gate has a hole in it.
3. **Treat configuration as content.** `mkdocs.yml`, `docusaurus.config.ts`, `docs.json` belong in the same repo under the same review — config drift is content drift.
4. **Keep governance in CI, not in the platform.** Validation hooks, EN/HU parity checks, directive whitelists implemented as CI scripts survive a platform migration; platform-plugin implementations do not (explicit MkDocs recommendation [INFERRED, corpus-consistent]).
5. **Design the exit on day one.** Docs-as-code's promise is portability; it only holds if canonical content stays close to plain Markdown + frontmatter and platform-specific syntax is contained (see each platform ADR-00x exit strategies).

## Pitfalls

- **"Git integration" marketing vs. Git canonicality.** GitBook scores 3/5 on docs-as-code fit despite real Git Sync, because the block model owns truth [VERIFIED-OFFICIAL]. Always test the round-trip: commit a file with custom frontmatter, let the platform touch it, diff the result.
- **Bidirectional sync without a merge model.** GitBook resolves collisions by *creating new files*, not merging [VERIFIED-OFFICIAL] — silent structural corruption in a system that assumes file stability.
- **Vendor-operated build plane.** Mintlify is Git-canonical but the build/serve plane is a black box; content survives vendor failure, publishing does not. Docs-as-code degrades gracefully only if you can rebuild elsewhere.
- **Governance theater.** Branch protection means little if a platform bot or app-side merge can bypass it; audit which identities can write to the synced branch.

## Expert Notes

- The analysts' sharpest cross-cutting insight: the six platforms split into two families — hosted platforms with excellent AI-consumption surfaces but vendor-owned build planes (Mintlify, GitBook) vs. OSS static generators with zero AI features — and the *absence* of platform AI is an advantage, because AI belongs in the generation plane (CI), not the serving plane (comparison.md, Key Findings).
- Docs-as-code inverts the CMS trust model: instead of trusting a database + permissions system, you trust Git history + review. That makes the npm/PyPI build toolchain the *real* attack surface — every SAD's threat model puts supply chain at or near the top.
- One-engineer operability falls out of the paradigm almost automatically: steady state is "merge PRs, CI rebuilds, static host serves" — no servers, no backups beyond Git.

## Evidence & Further Reading

- Target ecosystem rules: `outputs/00_research/analysis_brief.md`
- The block-model counter-example, in full: `outputs/01_products/gitbook/SAD_gitbook.md` (§GitHub Integration, §Threat Model) and `outputs/01_products/gitbook/ADRs/adr-001-git-sync-one-way-discipline.md`
- By-construction fits: `outputs/01_products/docusaurus/SAD_docusaurus.md`, `outputs/01_products/mkdocs/SAD_mkdocs.md`
- Field-wide canonicality finding: `outputs/02_comparison/comparison.md`
- Platform profiles: [docusaurus](../10-platforms/docusaurus.md), [gitbook](../10-platforms/gitbook.md), [mintlify](../10-platforms/mintlify.md), [mkdocs](../10-platforms/mkdocs.md)
