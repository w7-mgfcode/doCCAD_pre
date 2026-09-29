# Requirements Register  [EXPLICIT unless marked]

All derived from PROMPT-001 (user mission, 2026-08-12). IDs referenced by TRACEABILITY_MATRIX.md.

| ID | Requirement | Source |
|---|---|---|
| REQ-001 | Research six documentation platforms with equal, repository-grounded depth | PROMPT-001 §A,§14,§16,§40-B |
| REQ-002 | Select the publishing foundation via a weighted 11-criterion decision model | PROMPT-001 §18 |
| REQ-003 | Git/GitHub is the single source of truth; files over databases | PROMPT-001 §1,§22 |
| REQ-004 | Structural separation of canonical vs AI-generated knowledge; no silent promotion | PROMPT-001 §2 |
| REQ-005 | AI provider abstraction: Claude, Gemini, OpenAI, local/Ollama; no deep coupling | PROMPT-001 §8 |
| REQ-006 | Published docs must remain readable with every AI provider unavailable | PROMPT-001 §9 |
| REQ-007 | Minimum sufficient retrieval; vector DB only past an explicit decision boundary | PROMPT-001 §10 |
| REQ-008 | Automated GitHub ingestion with incremental (not full-corpus) regeneration | PROMPT-001 §6 |
| REQ-009 | Provenance metadata contract on all documents; drift detection, deterministic-first | PROMPT-001 §7,§27 |
| REQ-010 | Evidence-grounded recruiter views (30s/2min/deep) — no fabricated claims | PROMPT-001 §24 |
| REQ-011 | Interview-prep as reusable per-page component, build-time preferred | PROMPT-001 §4,§25 |
| REQ-012 | Special-question → governed dedicated-page workflow with safest/simplest lifecycle | PROMPT-001 §5 |
| REQ-013 | Bilingual EN/HU capability; Hungarian executive summaries in key documents | PROMPT-001 §16,§19,§39 |
| REQ-014 | Anti-overengineering: one-engineer operability; every component beats a simpler alternative | PROMPT-001 §22,§40-E |
| REQ-015 | Runnable PoC demonstrating 5 scenarios with truthful executed-vs-not validation | PROMPT-001 §34-§37 |
| REQ-016 | Security architecture covering AI-specific threats and trust boundaries | PROMPT-001 §29 |
