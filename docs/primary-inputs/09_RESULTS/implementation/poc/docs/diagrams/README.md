# Canonical diagram sources

Every shared diagram is a Mermaid `.mmd` file in this directory, imported by
reference from canonical pages. One diagram per file; the file name states the view.
Labels avoid `()[]{}` characters; colors come from the theme, never hard-coded.
CI compiles every `.mmd` with mermaid-cli — a diagram that does not compile blocks
the merge. AI may modify these files only through `UpdateMermaidDiagram` contract PRs.

| File | View |
| --- | --- |
| `generation-pipeline.mmd` | End-to-end generation pipeline, contract to merged PR |
