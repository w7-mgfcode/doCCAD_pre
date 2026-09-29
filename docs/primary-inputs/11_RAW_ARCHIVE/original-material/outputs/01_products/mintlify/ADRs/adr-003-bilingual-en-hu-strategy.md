# ADR-003: Bilingual EN/HU via language trees with an external translation pipeline

## Status
Proposed (2026-08-12)

## Context
The ecosystem requires bilingual English/Hungarian documentation. Mintlify supports localization through per-locale directory trees plus a `navigation.languages` array (full navigation per language, language switcher rendered automatically, first entry = default). Hungarian (`hu`) is in the officially supported language-code list, and search/MCP support language filtering. Mintlify offers a paid Translations automation (avg ≈913 credits/run) using its own agent; alternatively, translations can be produced by any external pipeline — Mintlify itself maintains its es/fr/zh trees via the open-source General Translation toolchain with bot-authored PRs, proving the external pattern at scale.

## Decision
- English is canonical and default; Hungarian lives in a mirrored `hu/` tree with identical filenames and structure.
- Translation is performed by the ecosystem's own provider-abstracted AI pipeline (not Mintlify credits): on merge of English changes, a GitHub Action translates changed files (tracked via per-file source hashes) and opens a `hu` PR for human review.
- `docs.json` navigation is duplicated per language using `$ref`-split navigation fragments; a generator script derives the `hu` fragment from the `en` fragment plus a translated-labels map, so navigation never drifts structurally.
- CI enforces tree parity: file-list diff between `en` and `hu` scopes plus staleness detection (source hash newer than translation) fails the check or labels the PR.
- Derived content (ADR-002) is translated the same way, after the English derivation is merged, keeping one generation axis at a time.

## Consequences
- Hungarian readers get a native switcher, localized search results, and language-filtered MCP retrieval at no extra platform cost.
- Roughly 2x content volume in the repo; parity CI and hash tracking are new pipeline components (bounded, one-engineer-sized).
- Avoiding Mintlify's Translations automation preserves provider independence and avoids per-run credit costs, at the price of building the (simple) translation Action ourselves.
- Same page path must never appear in two languages' navigation (documented undefined behavior) — the generator script guarantees this.

## Alternatives
- **Mintlify Translations automation:** least build effort, but Pro-plan credits per run, vendor-locked model choice, and less control over glossary/terminology.
- **Separate `hu` deployment/subdomain:** rejected — loses the integrated switcher and doubles configuration.
- **Machine translation at read time:** violates static-first and quality-review requirements.
