---
id: foundation-ssg-anatomy
title: Anatomy of a Static Site Generator — The Ten-Layer Model
type: knowledge
category: foundations
tags: [ssg, architecture, layer-model, build-pipeline, plugins, themes]
sources:
  - outputs/00_research/analysis_brief.md            # layer-map mandate for all analysts
  - outputs/01_products/docusaurus/SAD_docusaurus.md # C4 L2/L3, Extensibility
  - outputs/01_products/mkdocs/SAD_mkdocs.md         # C4 L3 core components
  - outputs/01_products/zensical/SAD_zensical.md     # Rust/Python hybrid layer split
  - outputs/01_products/hyperbook/SAD_hyperbook.md   # C4 L3 markdown engine
  - outputs/01_products/mintlify/SAD_mintlify.md     # SaaS layer opacity
  - outputs/01_products/gitbook/SAD_gitbook.md       # SaaS layer opacity
confidence: HIGH
related: [foundation-docs-as-code, foundation-markdown-mdx-frontmatter, foundation-search-models, foundation-i18n-models, platform-comparison-logic]
---

# Anatomy of a Static Site Generator — The Ten-Layer Model

**Summary** — All six platform analyses in this corpus decomposed their subject into the same ten layers: authoring, configuration, parsing, build, rendering, plugin, theme, search, localization, delivery. The model makes wildly different systems (a Meta React monorepo, a 15-module Python package, a Rust/Python hybrid, two proprietary SaaS planes) directly comparable, and it localizes risk: most platform weaknesses live in exactly one layer.

## Core Logic

The layers, and what each one decides:

- **Authoring** — the format writers (and generators) produce: which Markdown dialect, frontmatter schema, component/directive syntax. Determines portability and how reviewable AI output is.
- **Configuration** — the file(s) that define the site: `docusaurus.config.ts`, `mkdocs.yml`, `zensical.toml`, `docs.json`, `hyperbook.json`/`hyperlibrary.json`, `.gitbook.yaml`+`SUMMARY.md`. Single-file config is a one-engineer-operability signal; executable config (TypeScript, `!!python/name:` tags) is also an attack surface [VERIFIED-REPO: MkDocs].
- **Parsing** — Markdown/MDX → AST: MDX v3 remark/rehype (Docusaurus), Python-Markdown + pymdownx (MkDocs, Zensical), remark + 40 directive plugins (Hyperbook), proprietary import into a block model (GitBook).
- **Build** — orchestration: full rebuild (MkDocs, Docusaurus, Hyperbook CI) vs. differential dataflow (Zensical's `zrx` engine [VERIFIED-REPO]) vs. vendor-run workers (Mintlify, GitBook). Determines CI cost and feedback latency.
- **Rendering** — AST → HTML: React SSG with client hydration (Docusaurus), Jinja2 (MkDocs), MiniJinja in Rust (Zensical), Handlebars + rehype (Hyperbook), Next.js renderer over an API (GitBook).
- **Plugin** — the extension contract: Docusaurus typed lifecycle (`loadContent → contentLoaded → postBuild`), MkDocs 19-event `BasePlugin` + single-file hooks, Zensical **none yet** (module system unshipped), Hyperbook **none** (compiled-in directives), Mintlify/GitBook **none** (content-side components / hosted integrations only). This layer decided the comparison in practice (see [comparison-logic](../10-platforms/comparison-logic.md)).
- **Theme** — presentation customization: swizzling (Docusaurus), Jinja `extends`/`custom_dir` overrides (MkDocs/Zensical), CSS/scripts only (Hyperbook, Mintlify), closed (GitBook).
- **Search** — see [search-models](search-models.md): build-time local index vs. SaaS vs. undisclosed.
- **Localization** — see [i18n-models](i18n-models.md): filesystem copies vs. plugin-assembled vs. variants vs. absent.
- **Delivery** — the artifact and its runtime dependencies: plain static directory (four OSS tools) vs. vendor CDN you cannot rebuild yourself (Mintlify below Enterprise, GitBook always).

### The six platforms mapped

| Layer | Docusaurus | MkDocs(+Material) | Zensical | Hyperbook | Mintlify | GitBook |
|---|---|---|---|---|---|---|
| Authoring | MDX v3 | Python-Markdown+pymdownx | pymdownx dialect | MD + `:::` directives | MDX | Block editor / GitBook-MD |
| Config | one TS file | one YAML | TOML or mkdocs.yml | JSON (+library JSON) | docs.json | .gitbook.yaml + SUMMARY.md |
| Parsing | remark/rehype MDX | Python-Markdown | Python (Rust planned) | remark+40 directives | vendor black box | block-model import |
| Build | webpack/Rspack, SSG workers | single Python process | Rust `zrx` differential | Node CLI, incremental dev | vendor workers | vendor sync+publish |
| Rendering | React hydration | Jinja2 | MiniJinja | Handlebars+rehype | vendor renderer | Next.js over api.gitbook.com |
| Plugin | typed lifecycle, 38-pkg monorepo | 19 events + hooks | none (alpha) | none | none (snippets only) | none (ContentKit SaaS) |
| Theme | swizzle 69 components | custom_dir overrides | overrides (MiniJinja) | CSS/scripts | 8 themes + CSS | closed |
| Search | Algolia 1st-party / local plugin | lunr (incl. `lunr.hu`) | Disco (Rust index, client) | lunr | undisclosed engine | Quick Find + AI (SaaS) |
| Localization | filesystem i18n built-in | static-i18n plugin assembly | not yet (dual build) | multi-book hyperlibrary | `hu/` dir + languages nav | language variants |
| Delivery | static dir | static dir | static dir | static dir | vendor CDN (export = Enterprise) | vendor CDN only |

All rows [VERIFIED-REPO]/[VERIFIED-OFFICIAL] per the respective SADs; SaaS internal layers are [INFERRED]/[UNKNOWN] where noted in those documents.

## Best Practices

1. **Evaluate platforms layer-by-layer, not holistically** — averages hide vetoes. GitBook is strong in six layers and disqualified by two (parsing owns truth; delivery cannot be self-hosted).
2. **Locate each requirement in its layer before comparing.** "Custom InterviewPrep component" is a plugin/theme-layer question; "EN/HU" is localization-layer; conflating them produces vague scores.
3. **Ask who owns each layer.** Any layer you cannot inspect or rebuild (Mintlify build plane, GitBook everything, Zensical's minified Disco client) is vendor risk to price in explicitly.
4. **Prefer platforms whose delivery layer is a dumb static directory** if provider independence is a requirement — it makes every other layer replaceable.
5. **Ground the layer map in the actual repo** (package/module layout, not docs) — the analysis brief mandated this, and it caught claims marketing would have hidden (e.g., Zensical's Markdown rendering is still Python behind the Rust facade [VERIFIED-REPO]).

## Pitfalls

- **Mistaking theme capability for platform capability.** "MkDocs" as adopted is really MkDocs + Material + 4–6 plugins; Mermaid, i18n UI strings and modern search all live in the theme/plugin layers — and so does the 2026-11-05 support cliff [VERIFIED-REPO].
- **Assuming the plugin layer exists.** Zensical and Hyperbook look like normal SSGs until you need an extension point and find shims or compiled-in directives [VERIFIED-REPO].
- **Ignoring the build layer's execution semantics.** MkDocs hooks, Zensical macros/markdown-exec, and executable configs mean *the build runs code from the repo* — fork-PR CI must run without secrets (every OSS threat model in the corpus).
- **Confusing dev-server incrementality with CI incrementality.** Hyperbook and Zensical do incremental *dev* rebuilds; production/CI builds are full rebuilds for every platform except (partially, serve-mode) Zensical [VERIFIED-REPO].

## Expert Notes

- Client-side rendering leaks across layers: Mermaid and search both execute in the reader's browser on all four OSS platforms, so "static-first" really means "static + trusted client JS" — the delivery layer ships an execution environment.
- Layer opacity correlates with score confidence, not score value: Mintlify scored 85.0 with two layers [UNKNOWN]; the analysts handled this by scoring only verified interfaces and recording the unknowns as constraints — a method worth copying.
- The layer model doubles as a migration checklist: exit cost = Σ(per-layer translation cost), which is why every SAD's migration plan enumerates lock-in per layer (pymdownx syntax, directive syntax, docs.json, swizzled components).

## Evidence & Further Reading

- Layer-map mandate: `outputs/00_research/analysis_brief.md` (§Required repository deep dive)
- C4 L2/L3 sections of each SAD under `outputs/01_products/*/SAD_*.md` (all diagrams mermaid-cli-validated)
- Platform profiles: [docusaurus](../10-platforms/docusaurus.md), [mkdocs](../10-platforms/mkdocs.md), [zensical](../10-platforms/zensical.md), [hyperbook](../10-platforms/hyperbook.md), [mintlify](../10-platforms/mintlify.md), [gitbook](../10-platforms/gitbook.md)
