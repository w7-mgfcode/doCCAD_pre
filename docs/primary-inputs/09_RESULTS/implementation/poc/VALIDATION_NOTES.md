# Validation Notes — executed 2026-08-12

Environment: Linux container, Node v22.22.2, npm 10.9.7, Python 3.11.15
(PyYAML 6.0.3, jsonschema 4.26.0 present). Every command below was actually run
in `/home/claude/outputs/05_poc/`; results are verbatim outcomes, including the
failures encountered and how they were fixed.

## Version decision (no pin needed)

`npm view @docusaurus/core@latest version engines` → `3.10.2`, `node: '>=20.0'`.
Node 22 satisfies the *published* engine range of Docusaurus 3.10.2, so the PoC
uses 3.10.2 unpinned-down — no downgrade to 3.7/3.8 was necessary. (The design
seed's "Node >= 24.14" is stricter than what 3.10.2 actually requires.)

## a) npm install

```
npm install --no-audit --no-fund
```
**PASS** — `added 1329 packages in 2m` (one deprecation warning for transitive
`uuid@8.3.2`; harmless).

Fix applied during validation: the first `npm run build` failed with
`Module not found: Can't resolve '@mermaid-js/layout-elk'` —
`@docusaurus/theme-mermaid@3.10.2` declares it as a required peer dependency.
Resolved with `npm install @mermaid-js/layout-elk@^0.1.9` (now in package.json).

## b) npm run build (full, en + hu)

```
npm run build
```
**PASS** (second attempt, after two fixes):

1. Peer-dep failure above.
2. `onBrokenLinks: throw` correctly failed the build: custom frontmatter `id`
   values changed the default doc slugs, so `/docs/architecture/system-overview`
   and `/docs/development/setup` did not exist. Fixed by adding explicit `slug`
   frontmatter to those two canonical pages, then **recomputing the sha256
   provenance hashes** in all three generated artifacts (the canonical files'
   bytes changed — exactly the drift the hash mechanism is for).

Final result, full build of BOTH locales (not `--locale en`):
```
[INFO] Website will be built for all these locales: en, hu
[SUCCESS] Generated static files in "build".
[SUCCESS] Generated static files in "build/hu".
```
The `hu` locale builds entirely via English fallback (no translations shipped).

`npm run typecheck` (tsc over config + components): **PASS**, exit 0.

## c) validate_docs.py — positive and negative

```
python3 scripts/validate_docs.py
```
**PASS**: `Validated 5 pages, 1 interview datasets, 5 provenance hashes.` /
`OK — frontmatter schemas valid, planes intact, provenance hashes current.` exit 0.

Negative proof — corrupted the first 8 hex chars of one `content_hash` in
`docs/generated/recruiter/project-overview.mdx` via sed, reran:
**FAILS as required**, exit 1:
```
FAIL — 1 violation(s) (1 stale):
  - docs/generated/recruiter/project-overview.mdx: STALE — hash mismatch for
    docs/source/architecture/system-overview.md
```
Hash restored; rerun exits 0 again.

## d) detect_changes.py --all

```
python3 scripts/detect_changes.py --all
```
**PASS**, exit 0 (works with no git repo present):
```
Manifest: .docs-manifest.json (6 entries)
Impact:   impact.json (mode: full-scan)
  affected canonical: 3   stale generated: 0   nothing to regenerate
```
Drift demo: appended one byte to `docs/source/development/setup.md`, reran —
correctly reported `stale generated: 1` with a regeneration plan
(`GenerateRecruiterPage --target recruiter-project-overview`); byte removed,
clean state re-verified. `.docs-manifest.json` and `impact.json` are committed
as produced by the final clean run.

## e) generate_page.py dry run (zero keys)

```
env -u ANTHROPIC_API_KEY -u OPENAI_API_KEY -u GEMINI_API_KEY \
  python3 scripts/generate_page.py --contract GenerateRecruiterPage \
  --target architecture-system-overview --dry-run
```
**PASS**, exit 0, no network call, nothing written. Output shows: contract +
prompt version, evidence assembly with the allowlist refusing `scripts/*.py` and
`ai/*.py` (they are in the target's `sources` closure but outside
`allowed_evidence` — the refusal is printed), 3 evidence files accepted, provider
chain `anthropic -> gemini -> openai` selected from ai.config.yaml, full
assembled prompt with `<<<EVIDENCE-DATA ... EVIDENCE-DATA>>>` delimited blocks,
and the would-be branch `docs-gen/generaterecruiterpage-architecture-system-overview`.

Privacy hard-pin proof: same command with `--privacy private` raises
`PrivacyRoutingError: ... local provider is disabled ... Refusing to route to any
cloud provider.` exit 1 — **expected hard failure, PASS**.

## f) Mermaid compilation (mmdc)

Puppeteer config `{"executablePath": "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
"args": ["--no-sandbox", "--disable-setuid-sandbox"]}`:

```
npx -y @mermaid-js/mermaid-cli@11 -p puppeteer-config.json \
  -i docs/diagrams/generation-pipeline.mmd -o generation-pipeline.svg     # PASS (27 KB svg)
# in-page diagram extracted from docs/source/architecture/system-overview.md:
npx -y @mermaid-js/mermaid-cli@11 -p puppeteer-config.json \
  -i inpage-diagram.mmd -o inpage-diagram.svg                             # PASS (23 KB svg)
```
Both diagrams compile; SVGs written to /tmp (not kept — validation artifacts only).

## g) Workflow syntax check

`actionlint` is not installed in the container (**not executed**). Fallback per
plan: `yaml.safe_load` over both workflow files, `ai.config.yaml` and all three
contracts — **PASS**, all six parse to non-empty mappings.

## h) Serve smoke test (optional — executed)

`npm run serve -- --port 3050` + curl status codes:
```
200 /                                            200 /docs/overview/
200 /docs/architecture/system-overview/          200 /views/recruiter/project-overview/
200 /views/interview/architecture-system-overview/
200 /hu/docs/overview/        <- hu fallback serving English content
```
The interview page HTML contains the "AI-generated content" provenance banner
rendered by `<InterviewPrep>`. (Mermaid renders client-side, so the diagram is
not greppable in static HTML — verified instead via mmdc compilation above.)

## Not executed / known gaps

- `actionlint` (unavailable) — YAML well-formedness checked instead; the same
  fallback runs as the "lint-light" step in docs-validate.yml.
- Live (non-dry-run) generation — deliberately not run: no API keys exist in
  this environment and none may be placed anywhere.
- The GitHub workflows themselves were not executed (no GitHub runner here).

## Post-verification cleanup

After all checks above went green, `build/` and `.docusaurus/` were **deleted**
to save disk, as agreed. `node_modules/` is kept so every command above is
immediately re-runnable; re-create the build artifacts with `npm run build`.
