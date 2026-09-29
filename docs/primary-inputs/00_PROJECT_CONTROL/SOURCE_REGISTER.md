# Source Register

Sources of everything in this archive. Machine-readable dest-to-source mapping incl. classification notes:
`copy_map.json` (533 copies); per-file sha256: `PROJECT_MANIFEST.json`.

**S1 — Cowork session workspace** (`/home/claude/outputs/`, session docs-platform-architecture-2026-08-12,
2026-08-12..13): source of ALL research, architecture, PoC, validation and knowledge-base material. Raw
byte-preserved snapshot: `11_RAW_ARCHIVE/original-material/outputs/` (node_modules, build caches and
packaging zips excluded — rebuildable, recorded in COLLECTION_REPORT).

**S2 — Session conversation** (same session): source of PROMPT-001/002 transcriptions, VISION,
REQUIREMENTS, CONSTRAINTS, REJECTED_ALTERNATIVES, OPEN_QUESTIONS, task history. Labeled EXPLICIT/INFERRED
per statement; transcriptions labeled near-verbatim.

**S3 — Local synced skill documents** (`/root/.claude/skills/synced/`, collected 2026-08-13): the three
methodology SKILL.md files → `10_EXTERNAL_ARTIFACTS/reference-documents/skills/`.

**S4 — External web/repositories** (accessed 2026-08-12 during research): NOT retained as snapshots;
every URL with access date and what it evidenced is preserved in the per-platform `sources.md` files and
aggregated in `02_RESEARCH/references/EXTERNAL_SOURCES.md`.

No other sources were used. SECRETS: none discovered during collection; the only credential-shaped files
are `.env.example` templates (placeholders, verified).
