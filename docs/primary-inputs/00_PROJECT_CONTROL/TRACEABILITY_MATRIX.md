# Traceability Matrix

Chains: REQUIREMENT → TASK → RESULT/ARTIFACT → DECISION → DOCUMENT. Confidence: EXPLICIT (stated in
prompts/artifacts) unless marked INFERRED. No invented relationships; gaps are marked.

| Requirement | Origin | Task(s) | Result / artifact | Decision | Describing document |
|---|---|---|---|---|---|
| REQ-001 six-platform research, equal depth | PROMPT-001 §A,§16 | TASK-002..007 | RES-001..006 | feeds DEC-001 | six SADs; Gate B in DOC-002 |
| REQ-002 weighted decision model | PROMPT-001 §18 | TASK-008 | RES-007 scorecard+matrix | DEC-001 Docusaurus | decision_matrix.md; comparison.md |
| REQ-003 GitHub source of truth | PROMPT-001 §1,§22 | TASK-009 | ARCH-001 spine AD-1 | DEC-002 | adr-001; solution_architecture §12-13 |
| REQ-004 canonical/generated separation | PROMPT-001 §2 | TASK-009, TASK-010 | ARCH-003 content model; PoC dual-instance config | DEC-004 | adr-003; content_architecture.md |
| REQ-005 provider abstraction | PROMPT-001 §8 | TASK-009, TASK-010 | ARCH-004 §2; PoC ai/ code | DEC-005 | adr-004; ai_architecture.md |
| REQ-006 AI-free static reads | PROMPT-001 §9 | TASK-009..011 | no-keys build VERIFIED BY EXECUTION | DEC-009 | adr-008; validation_report Gate D |
| REQ-007 minimal retrieval + boundary | PROMPT-001 §10 | TASK-009 | ARCH-004 §3 | DEC-007 | adr-006 |
| REQ-008 ingestion + incremental regen | PROMPT-001 §6 | TASK-009, TASK-010 | ARCH-005; PoC detect_changes.py | DEC-006 (PR path) | automation_architecture.md |
| REQ-009 provenance + drift | PROMPT-001 §7,§27 | TASK-009..011 | frontmatter contract; hash negative-test executed | DEC-004/006 | content_architecture §5; validation_report |
| REQ-010 recruiter views | PROMPT-001 §24 | TASK-009, TASK-010 | contract + demo page with real hashes | DEC-006 | ai_architecture §6; 06_AI_DOCUMENTATION/recruiter/ |
| REQ-011 interview prep component | PROMPT-001 §4,§25 | TASK-009, TASK-010 | schema + component + demo JSON/MDX | DEC-009 (build-time) | ai_architecture §7; 06_AI_DOCUMENTATION/interview/ |
| REQ-012 special-question workflow | PROMPT-001 §5 | TASK-009 | flow diagram + contract | DEC-006 lifecycle | solution_architecture §20; flow_special_question.mmd |
| REQ-013 EN/HU bilingual | PROMPT-001 §16,§39 | TASK-002..013 | HU sections in all SADs + solution; PoC hu locale built | — | Gate F (hu build executed); i18n strategy in content_architecture §8 |
| REQ-014 anti-overengineering | PROMPT-001 §22 | TASK-009, TASK-011 | simpler-alternative notes throughout | all DEC | Gate E in validation_report; CONSTRAINTS.md |
| REQ-015 runnable validated PoC | PROMPT-001 §34-37 | TASK-010, TASK-011 | PoC + execution log | validates DEC-003..010 | VALIDATION_NOTES; validation_report Gate F |
| REQ-016 security architecture | PROMPT-001 §29 | TASK-009 | ARCH-006 + trust_boundaries.mmd | — | security_architecture.md |

Post-research chain (knowledge distillation): user request (conversation, 2026-08-12/13, EXPLICIT) →
TASK-013 → DOC-001 knowledge base → no new decisions (distillation only).
Archival chain: PROMPT-002 → TASK-014 → this archive → no decisions (preservation only).

Known gap [UNKNOWN]: PROMPT-001 §11 mandated three methodology skills; bmad-architecture's companion
tooling was absent in the execution environment — methodology applied manually, recorded in
validation_report "Skill Usage Statement" and ARCHITECTURE-SPINE frontmatter.
