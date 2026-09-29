# Mermaid Diagram Validation Report

- Date: 2026-08-12
- Validator: `@mermaid-js/mermaid-cli` (mmdc) **11.16.0**, installed locally via npm with `PUPPETEER_SKIP_DOWNLOAD=true` (the bare `npx -y @mermaid-js/mermaid-cli@latest -V` invocation failed silently in this sandbox because puppeteer could not download Chromium; a local install plus an explicit browser path fixed it).
- Browser: system Chromium at `/opt/pw-browsers/chromium` (symlink to `chromium-1194/chrome-linux/chrome`) via puppeteer config.

## Puppeteer config (`/tmp/puppeteer-config.json`)

```json
{
  "executablePath": "/opt/pw-browsers/chromium",
  "args": ["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
}
```

## Exact command (run per file)

```bash
./node_modules/.bin/mmdc -p /tmp/puppeteer-config.json \
  -i /home/claude/outputs/03_solution/diagrams/<name>.mmd \
  -o /tmp/mmd_out/<name>.svg
```

## Results

| File | Type | Result |
|---|---|---|
| c4_l1_context.mmd | flowchart TB | PASS |
| c4_l2_containers.mmd | flowchart TB | PASS |
| c4_l3_components.mmd | flowchart TB | PASS |
| deployment.mmd | flowchart TB | PASS |
| flow_git_change_to_docs.mmd | sequenceDiagram | PASS |
| flow_publishing.mmd | sequenceDiagram | PASS |
| flow_recruiter_generation.mmd | sequenceDiagram | PASS |
| flow_special_question.mmd | sequenceDiagram | PASS |
| model_routing.mmd | flowchart TB | PASS |
| trust_boundaries.mmd | (authored by security agent) | PASS |

10 / 10 files compiled to SVG in `/tmp/mmd_out/` with exit code 0 on the first validation run after authoring; no syntax fixes were required. Each output SVG was additionally checked to confirm it contains a rendered diagram (one `aria-roledescription` element) and no embedded "Syntax error" text.
