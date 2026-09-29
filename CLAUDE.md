@AGENTS.md

# Claude Code notes

- Path-scoped rules in `.claude/rules/` auto-load when you read a matching file; the index is
  `.claude/rules/README.md`.
- `.claude/settings.json` denies file edits (including new files) under
  `docs/primary-inputs/11_RAW_ARCHIVE/` and `docs/primary-inputs/03_PROMPTS/`.
- Subagents: `codebase-analyst` (depth on one subsystem), `research-agent` (parallel breadth),
  `code-reviewer` (finished changes — pass it the changed-file list; `git status` covers tracked
  paths, but `.claude/` and `.agents/` are git-ignored).
- AI-layer changes (this file, `AGENTS.md`, `.claude/`, `.agents/`): use the `ai-layer-review` skill.
- Orientation: `/base_cm:prime_nogit`. Planning loop: `/core_piv_loop:plan-feature` → `/core_piv_loop:execute`.
