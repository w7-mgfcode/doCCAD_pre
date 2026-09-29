---
id: getting-started-installation
slug: /getting-started/installation
title: Telepítés és Előfeltételek
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

# Telepítés és Előfeltételek

<div className="alert alert--success margin-bottom--lg">
  <strong>Magyar lokalizáció</strong>: Ez a dokumentum teljes mértékben elérhető magyar nyelven.
</div>

A DOCCAD szabványos, könnyen elérhető eszközökre épül, bármilyen zárt felhős infrastruktúra nélkül.

## Rendszerkövetelmények

1. **Node.js**: Node 20+, 22+ vagy 24+ verzió.
2. **npm**: npm 10+ vagy 11+ verzió.
3. **Python**: Python 3.11+ verzió (`pyyaml` és `jsonschema` csomagokkal).
4. **Git**: Standard verziókövető kliens.

## Telepítés Lépései

```bash
# Lépjen be a prototype könyvtárba
cd prototype

# Telepítse a csomagokat
npm install --no-audit --no-fund

# Ellenőrizze a Python környezetet
python3 -c "import yaml; import jsonschema; print('Környezet kész')"
```
