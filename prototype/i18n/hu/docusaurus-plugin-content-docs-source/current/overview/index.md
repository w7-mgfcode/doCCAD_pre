---
id: overview-index
slug: /overview
title: DOCCAD Rendszeráttekintés
type: canonical
audience: [developer, architect, operator, user, recruiter, interviewer]
owners: [architecture]
sources: [package.json, docusaurus.config.ts]
related: [overview-vision-and-goals, architecture-system-overview]
ai_generation:
  allowed: true
  derived_pages: [recruiter, interview, questions]
last_validated: 2026-09-21
---

# DOCCAD — GitHub-Natív MI Dokumentációs Rendszer

<div className="alert alert--success margin-bottom--lg">
  <strong>Magyar lokalizáció</strong>: Ez a dokumentum teljes mértékben elérhető magyar nyelven. A mély műszaki architektúra dokumentumok szándékosan az eredeti angol nyelven olvashatók.
</div>

Üdvözli a **DOCCAD**, egy nyílt architektúrájú, GitHub-natív dokumentációs ökoszisztéma, amelyet magas megbízhatóságot igénylő mérnökcsapatok számára terveztünk. A DOCCAD a verziókövetett kanonikus projektismeretet ellenőrzött, bizonyítékokkal alátámasztott származtatott nézetekké alakítja.

## Alapvető Filozófia

A hagyományos műszaki dokumentáció két alapvető hibalehetőséggel küzd:
1. **Manuális elavulás (Drift)**: Az architektúra-leírások, üzemeltetési útmutatók és API-leírások lassan elszakadnak a tényleges kódtól.
2. **MI Hallucináció és szennyezés**: A nem szabályozott mesterséges intelligencia eszközök ellenőrizetlen állításokat, kitalált mérőszámokat és elavult gyakorlatokat juttatnak a forráskódba.

A DOCCAD mindkét problémát felszámolja a **Két Strukturálisan Elválasztott Tartalmi Sík** bevezetésével:
- **Kanonikus Sík (`/docs`)**: Ember által írt, lektorált és automatikus generálással nem módosítható forrás. Ez a kizárólagos hiteles forrás.
- **Származtatott Sík (`/views`)**: Mesterséges intelligencia által generált nézetek (pl. toborzói összefoglalók, interjú-felkészítők és kérdés-válasz oldalak), amelyeket kizárólag kanonikus bizonyítékokból, PR-ellenőrzéssel állítunk elő.

## Fő Alapelvek

- **Docs-as-Code**: Minden tudás verziókövetett fájl a Gitben. Nincs futásidejű adatbázis vagy zárt tartalomkezelő.
- **MI-mentes Statikus Kiszolgálás**: A publikált weboldal egy tiszta statikus felület (Docusaurus 3.x). Az olvasók futásidejű MI-függőség, késleltetés és felhőköltség nélkül érik el a tartalmat.
- **Determinisztikus 1-es Szintű Visszakeresés**: A kontextus összeállítása pontos fájlelérési utakon és kulcsszó-keresésen alapul, így a lekérések determinisztikusak és pull requestekben auditálhatók.
- **Hash-alapú Mechanikus Eltérés-érzékelés**: Minden származtatott oldal rögzíti a felhasznált forrásfájlok `sha256` hash-értékét. Forrásváltozás esetén a CI csak az érintett oldalakat jelöli elavultnak.

## Gyors Hivatkozások

- [Rendszerarchitektúra Gerinc](/docs/architecture/system-overview) (Angol nyelven)
- [Két Tartalmi Sík Architektúra](/docs/architecture/content-planes) (Angol nyelven)
- [Döntések és ADR-ek](/docs/decisions/adr-001-github-source-of-truth) (Angol nyelven)
- [Minőségbiztosítási Kapuk](/docs/validation/quality-gates) (Angol nyelven)
