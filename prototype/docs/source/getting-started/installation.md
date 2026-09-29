---
id: getting-started-installation
slug: /getting-started/installation
title: Installation & Toolchain Prerequisites
type: canonical
audience: [developer, operator]
owners: [core]
sources: [package.json, tsconfig.json]
related: [getting-started-quickstart, development-setup]
ai_generation:
  allowed: true
  derived_pages: [interview]
last_validated: 2026-09-21
---

# Installation & Toolchain Setup

<!-- Archive mapping: Adapted from 09_RESULTS/implementation/poc/README.md and 04_ARCHITECTURE/SAD/ARCHITECTURE-SPINE.md -->

DOCCAD is built to run entirely on standard, accessible development toolchains with zero proprietary infrastructure.

## System Prerequisites

1. **Node.js**: Node 20.x, 22.x, or 24.x (verified on Node v24.19.0).
2. **npm**: npm 10.x or 11.x (verified on npm 11.17.0).
3. **Python**: Python 3.11+ (verified on Python 3.14.4).
   - Core packages: `pyyaml>=6.0`, `jsonschema>=4.19` (standard library fallback is available).
4. **Git**: Standard Git client for revision control.

## Workspace Setup

Clone the repository and install Node dependencies:

```bash
# Navigate to the prototype workspace
cd prototype

# Install npm dependencies (zero-audit, deterministic lockfile)
npm install --no-audit --no-fund

# Verify Python environment
python3 -c "import yaml; import jsonschema; print('Python environment ready')"
```

## Key Dependencies Overview

- **`@docusaurus/core@3.10.2`**: Publishing engine and static site compiler.
- **`@docusaurus/theme-mermaid` & `@mermaid-js/layout-elk`**: In-page diagram compilation.
- **`@easyops-cn/docusaurus-search-local`**: Offline static search indexing across canonical `/docs` and generated `/views`.
- **`react@^19.0.0` & `react-dom@^19.0.0`**: Modern interactive components (`EvidenceLink`, `InterviewPrep`, and Workbenches).
