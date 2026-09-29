# Contributing to the PRE-DOCCAD Archive

This repository is a **provenance-aware knowledge archive**. The prime rule: **preserve first, structure
second, improve later.** Never delete or rewrite historical material; supersede it.

Adding material: place originals under 11_RAW_ARCHIVE/original-material/ (or leave in place if born here);
put an organized copy in the appropriate numbered section; assign the next free stable ID for its class
(REQ/TASK/DEC/DOC/ARCH/DIAG/RES/REF/PROMPT — see 00_PROJECT_CONTROL/ENTITY_REGISTER.md); add a
PROJECT_KNOWLEDGE.json entry and, if it participates in a requirement chain, a TRACEABILITY_MATRIX row;
update COLLECTION_REPORT statistics only via a new dated section. Superseding: mark the old artifact
SUPERSEDED in the entity register, never delete it. Improvements to imperfect documents: record a task in
08_TASKS (FUTURE) instead of editing the historical artifact — new versions become new artifacts.
Never commit secrets; if a secret is found, do not archive it and record "SECRET DETECTED — NOT ARCHIVED"
in 01_PROJECT_KNOWLEDGE/OPEN_QUESTIONS.md.
