# ÖSSZEHASONLÍTÁS — Six Documentation Platforms, One Target System

Date: 2026-08-12 · Method: six parallel repository-grounded SAD analyses (see `01_products/`), scored 1–5
against 11 weighted criteria (see `scorecard.csv`, weights in `decision_matrix.md`). Evidence tags per the
project evidence rules; per-criterion rationale, evidence and confidence live in each platform's `scores.json`.

## Master Comparison Table

| Dimension | Mintlify | GitBook | Docusaurus | MkDocs (+Material) | Zensical | Hyperbook |
|---|---|---|---|---|---|---|
| Primary audience | Startups/API-first product teams | Product & support teams wanting a hosted editor | Engineering teams, OSS projects | Python-adjacent eng teams | Material-for-MkDocs users migrating forward | Educators / interactive OER authors |
| Best use case | Polished hosted API docs with zero ops | Mixed technical/non-technical authoring with hosted editor | Docs-as-code portal with custom React components | Minimal-footprint static docs, Python shops | Fast static Material-style docs, early adopters | Interactive teaching books |
| GitHub / docs-as-code fit | 5 — true Git-canonical MDX [VERIFIED-OFFICIAL] | 3 — bidirectional sync, but internal block model is operational source of truth [VERIFIED-OFFICIAL] | 5 — everything is repo files [VERIFIED-REPO] | 5 — pure Git-tracked text [VERIFIED-REPO] | 5 — Git-in, static-out, reads mkdocs.yml [VERIFIED-REPO] | 4 — Markdown+frontmatter in Git, static CLI [VERIFIED-REPO] |
| AI extensibility | 5 — llms.txt, per-page .md, /mcp, agent visibility controls; but generation plane is vendor-run | 4 — llms.txt/.md/?ask=/MCP; platform AI is OpenAI-locked | 4 — no native AI (by design); generated MDX is first-class input; full remark/rehype + plugin hooks | 4 — 19-event plugin API + hooks; ideal substrate for external AI at CI time | 3 — no plugin/build API yet; AI must stay repo-side | 3 — no plugin API, but .md.yml data + Handlebars templates are a natural derived-page mechanism |
| Mermaid | 5 native + ELK | 4 native, round-trips as fences | 5 first-party theme (mermaid ≥11) | 4 via superfences + Material runtime | 5 zero-config | 5 native dual syntax |
| Localization (EN/HU) | 4 — `hu` officially supported | 4 — language variants | 4 — filesystem i18n; HU theme strings ~50%, closable locally | 3 — assembled from static-i18n + Material language packs | 2 — no multi-language content support yet | 3 — structural bilingual OK; no HU UI locale |
| Security & governance | 3 — sound model; SSO/RBAC/audit Enterprise-gated; hidden pages public-by-URL | 4 — SOC 2 + ISO 27001; role ladder | 4 — static plane, strong upstream governance | 3 — static + SafeLoader; composite risk of dormant core | 3 — static, attestations; alpha latest-only patch policy | 3 — static; protect element presentation-only |
| Scalability (corpus/build) | Vendor-managed [UNKNOWN internals] | Vendor-managed; 5,000 pages/section limit | Full rebuilds; Rspack + persistent cache + SSG worker threads [VERIFIED-REPO] | Full rebuilds; fine at small-medium scale | Differential builds (serve-verified); CI incrementality unproven | Dependency-aware incremental dev rebuilds; fine at scale target |
| Operational complexity | Near zero (hosted) | Zero (SaaS) | Low: one config, one CLI, static output; Node ≥24.14 | Lowest: one Python process, one YAML | Low, but alpha upgrade churn | Low; pin-and-vendor discipline needed |
| Extensibility | 2 — no build plugins, no remark/rehype hooks | 2 — no custom components; ContentKit only | 5 — plugin lifecycle + themes + swizzle + MDX components | 4 — mature plugin/event API | 1 — plugin system not yet public | 2 — 40 built-in directives, no plugin API |
| Self-hosting | 2 — Enterprise-only scoped engagement; static export also Enterprise-gated | 1 — none; OSS renderer still calls api.gitbook.com | 5 — plain static dir | 5 — plain static dir | 5 — plain static dir | 5 — plain static dir |
| Cost | 2 — Pro plan needed for the target workflow (~$450/mo annual, third-party-reported) | 3 — Free tier OK until custom domain (Premium $65/site/mo) | 5 — MIT, free hosting tiers | 5 — BSD-2/MIT, free | 5 — MIT, free | 5 — MIT, free |
| Lock-in | Medium-high: content portable (MDX), build/serve/search not | High: block model, normalized export | Low: MDX + static output; React coupling only | Low: plain Markdown | Low: Markdown; near-free fallback to Material (window closing) | Low-medium: directive syntax is Hyperbook-specific |
| **Weighted score** | **85.0** | **72.2** | **88.6** | **83.8** | **76.4** | **76.0** |
| Evidence confidence | HIGH (official docs repo cloned; internals UNKNOWN) | HIGH (docs + current OSS renderer) | HIGH (full repo deep dive) | HIGH (both repos cloned) | HIGH (repo @ v0.0.53) | HIGH (full clone) |
| Recommendation | Reject for this system: provider-dependence violates core principle | Reject: Git is a mirror, not the engine | **ADOPT — winner** | Conditional fallback; maintenance cliff 2026-11-05 | Watch; revisit at 1.0 + plugin API | Niche; not for developer/recruiter portal |

## Key Findings Across the Field

**The field splits into two families.** Mintlify and GitBook are hosted platforms with excellent AI-consumption
surfaces (llms.txt, per-page .md endpoints, MCP servers) but place the build/serve/AI plane inside a vendor.
The four OSS tools are static-first and provider-independent but ship zero AI features — which is exactly what
the target architecture wants, because AI belongs in the generation plane (CI), not the serving plane.

**Git-canonicality is not uniform.** Only Docusaurus, MkDocs, Zensical and Hyperbook treat repo files as the
single operational source of truth. Mintlify is Git-canonical but vendor-built. GitBook's Git Sync is a
bidirectional mirror of an internal block model; exports are normalized, not byte-faithful [VERIFIED-OFFICIAL].
That disqualifies GitBook for a system whose provenance and drift detection depend on deterministic file
identity.

**The MkDocs ecosystem is in transition.** Material for MkDocs ends public security support 2026-11-05
[VERIFIED-REPO: SECURITY.md]; MkDocs core is dormant (last release 2024-08-30). Its successor Zensical is
technically promising (Rust+Python, differential builds, zero-config Mermaid) but pre-1.0 with no plugin API
and no multi-language content support [VERIFIED-REPO @ v0.0.53]. Adopting either today means either a dated
exit plan (MkDocs) or alpha churn (Zensical).

**Extensibility is the decisive criterion in practice.** The target system needs a custom InterviewPrep
component, provenance-aware frontmatter, multi-instance content separation (canonical vs generated), and CI
hooks for validation. Only Docusaurus (plugin lifecycle + MDX components + multi-instance docs, all
dogfooded upstream [VERIFIED-REPO]) and MkDocs (19-event plugin API) offer this natively; Docusaurus does it
with an active core team and first-party Mermaid.

## HU: ÖSSZEHASONLÍTÁS

Hat dokumentációs platformot vizsgáltunk meg azonos mélységben, valós repository-elemzésre alapozva, 11
súlyozott kritérium mentén. **A győztes a Docusaurus (88,6/100)**: minden tartalma Git-ben tárolt fájl, első
osztályú Mermaid-támogatással, több-példányos docs-pluginnal (amely természetes határvonalat ad a kanonikus és
az AI-generált tartalom között), MDX-komponensekkel (InterviewPrep blokk), beépített fájlrendszer-alapú
i18n-nel (magyar fordítások ~50%-ban készek, helyben pótolhatók), és tisztán statikus, bárhol önüzemeltethető
kimenettel. A Mintlify (85,0) nyers pontszámban második, de a build/kiszolgáló/AI sík a szolgáltatónál fut, az
önüzemeltetés és a statikus export Enterprise-hoz kötött — ez sérti a rendszer alapelvét, miszerint az AI és a
szolgáltató nem lehet kötelező függőség. A MkDocs (83,8) architekturálisan kiváló és a legegyszerűbb, de a
Material for MkDocs biztonsági támogatása 2026. november 5-én megszűnik, a MkDocs mag pedig gyakorlatilag
alvó állapotú. A Zensical (76,4) ígéretes utód, de 1.0 előtti, plugin-API és többnyelvű tartalomkezelés
nélkül. A Hyperbook (76,0) oktatási célra kiváló, fejlesztői/toborzói portálnak nem az. A GitBook (72,2)
esetében a Git csak tükör, nem a motor — a determinisztikus provenance emiatt nem garantálható.
