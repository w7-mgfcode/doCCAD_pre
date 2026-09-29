# ADR-003: Bilingual EN/HU via language variants synced from monorepo directories

## Status
Proposed

## Context
The ecosystem requires bilingual EN/HU documentation. GitBook models translations as **variants** of
a site section, with a language picker shown when variants carry language metadata
[VERIFIED-OFFICIAL]. Git Sync supports monorepos: each synced section has its own Project directory
containing its `.gitbook.yaml`; assets are NOT shared across project directories ("A file referenced
from `packages/docs-en/.gitbook/assets/logo.png` isn't automatically available to the section synced
from `packages/docs-fr`") [VERIFIED-OFFICIAL]. GitBook's AI auto-translation is a paid add-on
(included in Ultimate; $25/50k words + $0.20/1k words on Premium) [VERIFIED-OFFICIAL]; Hungarian
availability in that add-on is unverified [UNKNOWN], and using it would route translation through
GitBook's OpenAI-backed service, outside the ecosystem's provider abstraction.

## Decision
Single docs repo with `docs/en/` and `docs/hu/` project directories, each with its own
`.gitbook.yaml`, `README.md`, `SUMMARY.md`, and duplicated `.gitbook/assets/`. Each directory syncs
to one variant (EN default, HU secondary) of the same site. Translation is produced by the
ecosystem's own AI pipeline (provider-abstracted) as ordinary PRs into `docs/hu/`; GitBook's
translation add-on is not used. Localized site/section titles are configured app-side for HU.

## Consequences
- EN and HU trees version together in one repo and one PR when desired; incremental regeneration
  can translate only changed pages.
- Asset duplication between directories is accepted; a CI step copies shared assets to both trees.
- Structural parity between the two `SUMMARY.md` files must be maintained by the pipeline.
- No dependency on GitBook AI pricing or language coverage.

## Alternatives
- **GitBook auto-translation add-on**: less pipeline work, rejected — provider lock-in, unverified
  HU support, per-word cost, translations would originate platform-side rather than in Git.
- **Two separate sites (EN site, HU site)**: doubles per-site cost and splits search; rejected.
- **Single mixed-language tree**: poor reader UX, no language picker; rejected.
