---
id: development-setup
slug: /development/setup
title: Development Setup
type: canonical
audience: [developer]
sources: [package.json, .env.example, ai.config.yaml]
owners: [maintainer]
related: [overview, architecture-system-overview]
ai_generation:
  allowed: true
  derived_pages: []
last_validated: 2026-08-12
---

## Prerequisites

- Node.js 20 or newer (the PoC is validated with Node 22; Docusaurus 3.10 declares
  `node >=20.0`).
- Python 3.11+ with `PyYAML` (and optionally `jsonschema`) for the pipeline scripts.
- No API keys are required for the site build or for dry-run generation.

## Install and build the site

```bash
npm install --no-audit --no-fund
npm run build        # builds en + hu locales; hu falls back to English
npm run serve        # serve the static build locally
```

## Run the pipeline scripts

```bash
# Validate all frontmatter, schemas and provenance hashes (CI gate):
python3 scripts/validate_docs.py

# Rebuild the manifest and compute change impact without git history:
python3 scripts/detect_changes.py --all

# Dry-run a generation contract — assembles evidence and prompt, calls nothing:
python3 scripts/generate_page.py --contract GenerateRecruiterPage \
  --target architecture-system-overview --dry-run
```

## Configure providers (live generation only)

Copy `.env.example` to `.env` and export the variables, or set them as GitHub
Actions secrets. Keys are read only from the environment; model identifiers are
environment values referenced by `ai.config.yaml`. Never commit a key, and never put
a model name in code.
