---
id: getting-started-quickstart
slug: /getting-started/quickstart
title: Gyorsindítási Útmutató
type: canonical
audience: [developer, operator, reviewer]
owners: [core]
sources: [package.json, scripts/validate_docs.py, scripts/detect_changes.py]
related: [getting-started-installation, validation-quality-gates]
ai_generation:
  allowed: true
  derived_pages: [recruiter, interview]
last_validated: 2026-09-21
---

# Gyorsindítási Útmutató

<div className="alert alert--success margin-bottom--lg">
  <strong>Magyar lokalizáció</strong>: Ez a dokumentum teljes mértékben elérhető magyar nyelven.
</div>

Ez az útmutató bemutatja az ellenőrzést, a helyi generálást és a statikus dokumentáció kiszolgálását.

## 1. Lépés: Ellenőrzés Futtatása

```bash
python3 scripts/validate_docs.py
```

## 2. Lépés: Eltérés- és Változásvizsgálat

```bash
python3 scripts/detect_changes.py --all
```

## 3. Lépés: Determinisztikus Kérdés-generálás

```bash
python3 scripts/generate_question.py \
  --question "How does DOCCAD detect drift when canonical architecture changes?" \
  --audience developer \
  --persist
```

## 4. Lépés: Statikus Oldal Fordítása

```bash
npm run build:demo
```

## 5. Lépés: Helyi Kiszolgálás

```bash
npm run serve
```
