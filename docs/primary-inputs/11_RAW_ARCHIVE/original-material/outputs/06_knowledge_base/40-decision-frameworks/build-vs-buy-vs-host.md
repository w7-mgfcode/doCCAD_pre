---
id: framework-build-vs-buy-vs-host
title: Build vs Buy vs Host — SaaS and OSS-Static Decision Logic
type: knowledge
category: decision-frameworks
tags: [saas, self-hosting, lock-in, vendor-risk, platform-selection]
sources:
  - outputs/02_comparison/comparison.md (family split, lock-in row)
  - outputs/02_comparison/decision_matrix.md (Mintlify/GitBook rejections)
  - outputs/01_products/mintlify/ADRs/adr-005-exit-strategy-lock-in-bounds.md, outputs/01_products/gitbook/ADRs/adr-004-exit-strategy-fallback-ssg.md (existence as pattern)
  - outputs/03_solution/ADRs/adr-001-github-source-of-truth.md, adr-002-docusaurus-framework.md
confidence: HIGH
related: [framework-weighted-decision-model, framework-maintenance-risk-assessment, pattern-ai-in-ci-not-serving, practice-evidence-discipline]
---

# Build vs Buy vs Host — SaaS and OSS-Static Decision Logic

**Summary** — The six-platform field split cleanly into hosted SaaS (Mintlify, GitBook) and OSS static generators (Docusaurus, MkDocs, Zensical, Hyperbook), and the decision logic that resolved the split generalizes: decompose lock-in into four planes — content, build, search, and AI — and require that every plane your mission declares non-negotiable be exitable. SaaS lost here not on quality but because its best members lock exactly the planes this mission pinned.

## Core Logic

**The family split.** Hosted platforms shipped the best AI-*consumption* surfaces in the field (llms.txt, per-page `.md` endpoints, `/mcp` servers, agent visibility controls) but place build/serve/search/AI inside the vendor. The OSS SSGs ship zero AI features and plain static output — "which is exactly what the target architecture wants, because AI belongs in the generation plane (CI), not the serving plane."

**Lock-in as four separable planes** (from the comparison's lock-in row and the Mintlify rejection):

1. **Content plane** — can you get your source out byte-faithfully? Mintlify: yes (true Git-canonical MDX). GitBook: no — Git Sync mirrors an internal block model; exports are *normalized*, not byte-faithful [VERIFIED-OFFICIAL], which breaks any system whose provenance and drift detection depend on deterministic file identity. Content lock-in is the most disqualifying kind because it poisons everything downstream.
2. **Build plane** — can you produce the artifact without the vendor? Mintlify's static export and self-hosting are Enterprise-gated; the OSS four build a plain static directory anywhere.
3. **Search plane** — is search a build artifact (local index plugin, portable) or a vendor service (optional Algolia; GitBook/Mintlify built-in only)?
4. **AI plane** — do AI features run in *your* pipeline against your files, or inside the vendor (Mintlify's generation plane is vendor-run; GitBook's platform AI is OpenAI-locked)?

**The decision rule.** Buy (SaaS) is legitimate when the locked planes are ones your mission can afford to rent. Here, mission principle §9 — approved documentation must remain available when providers are unavailable — "extends naturally to the publishing vendor: a system whose stated purpose is provider independence cannot place its only rendering path inside one provider." That sentence is the whole framework: enumerate the planes, check each against your non-negotiables, and treat a violated non-negotiable as a veto regardless of weighted score (Mintlify was #2 at 85.0 and still rejected).

**Cost realism.** Weight the true workflow tier, not the free tier: the target workflow landed on Mintlify Pro (~$450/mo, third-party-reported, labeled as such) and GitBook Premium at custom-domain time — versus $0 MIT + free static hosting for the OSS family.

**Exit strategies are mandatory either way.** Every platform analysis produced exit/lock-in ADRs — for SaaS (lock-in bounds, fallback SSG) *and* for OSS (MkDocs pin-with-exit-date, Zensical revisit trigger, Hyperbook pin-and-vendor). "Host" is not lock-in-free; it trades vendor risk for maintenance risk (see framework-maintenance-risk-assessment).

## Best Practices

1. **Decompose lock-in per plane before comparing platforms**, because "portable content" marketing routinely coexists with a captive build or search plane.
2. **Test content portability at byte fidelity**, because normalized round-trips (GitBook) silently break hash-based provenance and deterministic diffing.
3. **Extend availability principles to every vendor in the serving path**, because a docs platform is a provider too — provider-independence missions must not exempt the publisher.
4. **Price the tier your actual workflow needs**, and label unverified prices, because free-tier comparisons flatter SaaS.
5. **Write the exit ADR at adoption time for OSS as well**, because dormant-maintainer risk is the self-hosted twin of vendor risk.

## Pitfalls

- Scoring SaaS "self-hosting" on marketing claims — the analysis brief explicitly banned crediting it; Mintlify scored 2, GitBook 1 on actual options.
- Averaging away a veto: a weighted model happily ranks a platform #2 while a single plane (build) makes it unusable — keep constraints outside the arithmetic.
- Conflating the two SaaS platforms: Mintlify is Git-canonical with a captive build; GitBook is captive at the *content* plane. Different planes, different severity — GitBook's is worse for this mission.
- Ignoring the hybrid future: the design keeps optional SaaS attachments (Algolia in Mode B only) at planes where lock-in is trivially reversible — buy at the edges, host the core.

## Expert Notes

The generalizable insight: **"buy" is a per-plane decision, not a per-product one.** The chosen architecture effectively buys commodity hosting (GitHub Pages, exitable — the same artifact serves any static server), rents model inference behind a thin adapter (exitable per pattern-thin-provider-abstraction), and owns content, build, and search outright. The planes owned are exactly the ones the mission declares existential; the planes rented are the ones with proven substitutes. That asymmetry — not OSS ideology — is why the SaaS candidates lost.

## Evidence & Further Reading

- `outputs/02_comparison/comparison.md` — family split, lock-in row, GitBook disqualification reasoning.
- `outputs/02_comparison/decision_matrix.md` — the Mintlify rejection paragraph (the framework in one sentence) and cost evidence.
- `outputs/01_products/mintlify/ADRs/adr-005-exit-strategy-lock-in-bounds.md`, `outputs/01_products/gitbook/ADRs/adr-004-exit-strategy-fallback-ssg.md` — exit ADRs as a practice.
- `outputs/03_solution/ADRs/adr-001-github-source-of-truth.md` — the files-only stance that makes content-plane lock-in a veto.
