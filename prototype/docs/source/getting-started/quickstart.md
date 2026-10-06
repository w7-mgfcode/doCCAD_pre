---
id: getting-started-quickstart
slug: /getting-started/quickstart
title: Quickstart Guide — Seed to Serve
type: canonical
visibility: public
audience: [developer, operator, reviewer]
owners: [core]
sources: [package.json, scripts/validate_docs.py, scripts/detect_changes.py]
related: [getting-started-installation, validation-quality-gates]
ai_generation:
  allowed: true
  derived_pages: [recruiter, interview]
last_validated: 2026-09-21
---

# Quickstart Guide — Seed to Serve

<!-- Archive mapping: Adapted from 09_RESULTS/implementation/poc/README.md -->

This guide walks you through validating the repository, running local deterministic generation, building the static documentation site, and serving it locally.

## Step 1: Validate Canonical & Derived Documentation

Run the deterministic validation script to check frontmatter schemas, structural plane boundaries, and `sha256` provenance hashes:

```bash
python3 scripts/validate_docs.py
```

Expected output:
```
Validated 25+ pages, 4 interview datasets, 15+ provenance hashes.
OK — frontmatter schemas valid, planes intact, provenance hashes current, security checks passed.
```

## Step 2: Run Change & Drift Detection

Inspect repository freshness and generate the dependency manifest:

```bash
python3 scripts/detect_changes.py --all
```

This command re-evaluates `.docs-manifest.json` and writes `impact.json`, verifying that all derived views match on-disk source hashes.

## Step 3: Run Deterministic Generation (Zero API Keys)

Generate a derived question answer or recruiter page using the offline `fixture` provider:

```bash
# Generate a question answer draft grounded in canonical evidence
python3 scripts/generate_question.py \
  --question "How does DOCCAD detect drift when canonical architecture changes?" \
  --audience developer \
  --persist
```

The output lands under `docs/generated/questions/` stamped with real `sha256` source digests and `provider: fixture`.

## Step 4: Build the Static Site

Build the static site for both English (`en`) and Hungarian (`hu`) locales:

```bash
# Build demo preview bundle (including demo-approved views and search index)
npm run build:demo
```

## Step 5: Serve Locally

Serve the static build on local port 3000:

```bash
npm run serve
```

Open your browser to:
- `http://localhost:3000/doCCAD_pre/` (Home page)
- `http://localhost:3000/doCCAD_pre/docs/overview` (Canonical documentation)
- `http://localhost:3000/doCCAD_pre/views/recruiter/project-overview` (Governed recruiter view)
- `http://localhost:3000/doCCAD_pre/hu/docs/overview` (Hungarian localized view)
