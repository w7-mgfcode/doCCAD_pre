---
id: foundation-mermaid-diagrams-as-code
title: Mermaid and Diagrams-as-Code — Rendering Models, Validation, Syntax Discipline
type: knowledge
category: foundations
tags: [mermaid, diagrams-as-code, mermaid-cli, client-side-rendering, validation, ci]
sources:
  - outputs/00_research/analysis_brief.md              # label-syntax rules for analysts
  - outputs/01_products/docusaurus/SAD_docusaurus.md   # first-party theme-mermaid, client-side caveat
  - outputs/01_products/mkdocs/SAD_mkdocs.md           # superfences + Material runtime, CDN caveat
  - outputs/01_products/zensical/SAD_zensical.md       # zero-config fence, unpkg dependency
  - outputs/01_products/hyperbook/SAD_hyperbook.md     # dual syntax
  - outputs/01_products/mintlify/SAD_mintlify.md       # ELK + zoom/pan
  - outputs/01_products/gitbook/SAD_gitbook.md         # fence round-trip
  - outputs/03_solution/ADRs/adr-007-mermaid-as-code.md
  - outputs/03_solution/diagrams/VALIDATION.md         # mermaid-cli validation procedure
confidence: HIGH
related: [foundation-docs-as-code, foundation-ssg-anatomy, platform-docusaurus, platform-mkdocs, platform-zensical]
---

# Mermaid and Diagrams-as-Code — Rendering Models, Validation, Syntax Discipline

**Summary** — Diagrams-as-code stores diagrams as text (Mermaid) in the same Git repository as prose, making them diffable, PR-reviewable, AI-editable, and CI-validatable. All six evaluated platforms support Mermaid fences natively or near-natively; the real design decisions are client-side vs. build-time rendering, how to validate diagrams in CI (mermaid-cli), and a short list of syntax rules — above all keeping parentheses and brackets out of node labels — that determine whether generated diagrams compile at all.

## Core Logic

**Why diagrams-as-code.** The solution ADR-007 states the rationale compactly: diagrams must be *versionable, diffable, AI-editable under contract, and validated*. Binary formats (draw.io, hand-drawn SVG) are undiffable, unreviewable and un-generatable; PlantUML needs a JVM and renders natively on neither GitHub nor the chosen platforms. Mermaid fenced blocks give one grammar for humans and AI, and — decisive dual-rendering property — **GitHub renders the same ```mermaid fences natively in the repo/PR view**, so the canonical file previews during review with zero duplication [VERIFIED-OFFICIAL, noted in the MkDocs SAD].

**Platform support is uniformly good, mechanically similar.** Docusaurus: first-party `@docusaurus/theme-mermaid` (mermaid ≥11.14, dark/light aware, optional ELK) [VERIFIED-REPO]. MkDocs: `pymdownx.superfences` custom fence + Material's lazy-loading runtime [VERIFIED-REPO]. Zensical: zero-config fence in every scaffolded project, themed via `--md-mermaid-*` CSS variables [VERIFIED-REPO]. Hyperbook: dual syntax (fences *and* `:::mermaid`), bundled mermaid.min.js shipped only when used [VERIFIED-REPO]. Mintlify: native fences plus ELK layout and zoom/pan/reset controls [VERIFIED-OFFICIAL]. GitBook: native blocks that round-trip through Git Sync as fenced code [VERIFIED-OFFICIAL].

**The central trade-off: client-side vs. build-time rendering.** Every OSS platform in the field renders Mermaid *client-side*: the page ships diagram source (or a base64 payload) plus mermaid.js, and the browser draws SVG at view time. Consequences, verified per platform:

- No-JS readers and crawlers see code, not diagrams [VERIFIED-REPO: Docusaurus `loadMermaid.ts` dynamic import; same model in Material/Zensical/Hyperbook].
- Diagram text is absent from build-time search indexes (Zensical SAD).
- Pages using diagrams pay mermaid's bundle weight; Material and Zensical load mermaid@11 from unpkg CDN by default — an availability/tampering/GDPR concern, self-hostable via privacy plugin or `extra_javascript` [VERIFIED-REPO].

Build-time SVG pre-rendering (mermaid-cli in the pipeline, commit SVGs) buys SEO/no-JS fidelity and print quality at the cost of an extra toolchain and worse review ergonomics (SVG diffs instead of text diffs). The corpus's consistent recommendation: accept client-side rendering as the default, pre-render only business-critical diagrams (recruiter PDFs, print) — Zensical ADR-005 and Docusaurus recommendation #10 both land here.

**Validation via mermaid-cli.** Because client-side rendering fails *silently at view time*, CI must compile diagrams. The validated procedure (`outputs/03_solution/diagrams/VALIDATION.md`, 10/10 diagrams passed with mmdc 11.16.0):

- `npx @mermaid-js/mermaid-cli -i diagram.mmd -o out.svg` per file; nonzero exit blocks merge.
- In sandboxed CI, puppeteer needs an explicit Chromium path and `--no-sandbox` args via a puppeteer config file; the naive `npx mmdc` invocation *failed silently* when Chromium could not download — pin the browser and check the exit path [OBSERVED].
- Belt-and-braces: verify the output SVG contains a rendered diagram (`aria-roledescription` element) and no embedded "Syntax error" text — mmdc has historically emitted error-SVGs with exit 0 in some modes.

**Syntax pitfalls (the label-parentheses issue).** The analysis brief hard-coded rules for its own analysts because they are the empirical failure modes of generated Mermaid: use `flowchart`/`graph TB` and `sequenceDiagram`, avoid experimental syntax and C4-plugin syntax (model C4 levels with flowchart subgraphs), keep labels short, and **never put round parentheses `(` `)` or square brackets `[` `]` inside node label text** — they collide with Mermaid's node-shape grammar (`id[label]`, `id(label)`) and break parsing. ADR-007 turns this into a standing convention: labels forbid `()[]{}`. Safe alternatives: hyphens, "slash", or quoted labels (`id["label"]`) — the corpus's diagrams simply avoid the characters.

## Best Practices

1. **Compile every diagram in CI with a pinned mermaid-cli major matching the runtime mermaid major** — version skew between validator and renderer reintroduces silent failures.
2. **Enforce the label character convention (`()[]{}` forbidden) in a lint step and in AI generation prompts/contracts** — it converts the most common generation failure into a pre-commit fix.
3. **Self-host mermaid.js** (privacy plugin / `extra_javascript` / local bundle) to pin the renderer version and remove the unpkg dependency [VERIFIED-REPO: MkDocs, Zensical mitigations].
4. **Keep shared diagrams in `.mmd` files, page-local ones as fences** — `.mmd` files are individually validatable and reusable; fences keep review context local (solution ADR-007 pattern).
5. **Route AI diagram edits through a dedicated contract** (the solution's `UpdateMermaidDiagram` PR contract) so diagram changes are always compile-gated and human-reviewed.

## Pitfalls

- **Silent view-time failure**: a syntactically broken diagram renders as an error box (or raw text) in production while the build stayed green — only CI compilation catches it.
- **Parentheses in labels** — e.g. `A[Static Hosting (Pages, Netlify)]` — the single most common authoring/generation error; the brief's diagrams use `Static Hosting - Pages, Netlify` instead.
- **mmdc environment fragility**: puppeteer/Chromium download failures can no-op the validation step; treat "validator ran" as something to assert, not assume [OBSERVED].
- **Assuming diagrams are searchable/SEO-visible** — with client-side rendering they are not; if a diagram carries load-bearing content, duplicate the key facts in prose.

## Expert Notes

- Mermaid support turned out to be a *solved* differentiator: five platforms scored 4–5 on the 8%-weight criterion, so it rarely decided anything — but its **absence** would have been a veto given the ecosystem's Mermaid-as-code rule. Some criteria matter as gates, not gradients.
- The dual-rendering property (same fence renders on GitHub and on the published site) quietly enforces dialect discipline: any Mermaid feature GitHub's renderer chokes on will be caught by reviewers before deploy.
- Client-side rendering is philosophically consistent with static-first: the *source* is canonical and readable; the rendering is progressive enhancement. The corpus accepts "no-JS readers see source text" explicitly for this reason (ADR-007 consequences).

## Evidence & Further Reading

- Validation procedure and results: `outputs/03_solution/diagrams/VALIDATION.md`; `outputs/05_poc/.github/workflows/docs-validate.yml` (CI implementation)
- Decision record: `outputs/03_solution/ADRs/adr-007-mermaid-as-code.md`
- Per-platform Mermaid sections: `outputs/01_products/*/SAD_*.md` (§Mermaid Support)
- Syntax rules origin: `outputs/00_research/analysis_brief.md` (§Deliverables, diagram rules)
- Related: [ssg anatomy](static-site-generator-anatomy.md), [docs-as-code](docs-as-code.md)
