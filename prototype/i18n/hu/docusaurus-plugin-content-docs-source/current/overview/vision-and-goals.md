---
id: overview-vision-and-goals
slug: /overview/vision-and-goals
title: Jövőkép és Alapelvek
type: canonical
audience: [developer, architect, recruiter, user]
owners: [architecture]
sources: [package.json]
related: [overview-index, architecture-content-planes]
ai_generation:
  allowed: true
  derived_pages: [recruiter, interview]
last_validated: 2026-09-21
---

# Jövőkép, Alapelvek és Kétnyelvű Stratégia

<div className="alert alert--success margin-bottom--lg">
  <strong>Magyar lokalizáció</strong>: Ez a dokumentum teljes mértékben elérhető magyar nyelven.
</div>

## A DOCCAD Jövőképe

A DOCCAD egy olyan mérnöki szervezetet valósít meg, ahol a dokumentáció nem másodlagos feladat, hanem aktív, ellenőrizhető és folyamatosan naprakész rendszereszköz.

### Hat Alapvető Szabály

1. **Fájlok az adatbázisok felett**: A GitHub az elsődleges hiteles forrás. Minden leírás és döntés verziókövetett fájl.
2. **MI a CI-ben, soha a kiszolgálásban**: A látogatók statikus HTML felületet olvasnak futásidejű felhőfüggőségek nélkül.
3. **Kanonikus Függetlenség**: A hiteles dokumentáció akkor is fordítható és olvasható, ha a világ összes MI szolgáltatója elérhetetlen.
4. **Irányított Származtatás**: Az MI által generált nézetek kizárólag emberi ellenőrzésen (pull request) keresztül kerülhetnek a repóba.
5. **Mechanikus Eltérés-érzékelés**: A tartalmi eltéréseket `sha256` ellenőrzőösszegek követik, nem bizonytalan időbélyegek.
6. **Kétnyelvű EN/HU Stratégia**: A forrásnyelv az angol, a vezérlőfelület és a bevezető áttekintések magyarul is elérhetők.
