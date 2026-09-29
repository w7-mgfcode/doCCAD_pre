# ADR-007: Mermaid-as-Code with CI Compilation Gate

Status: Accepted · 2026-08-12

## Context
Diagrams must be versionable, diffable, AI-editable under contract, and validated. Options: Mermaid, PlantUML
(JVM), Graphviz, hand-drawn/SVG, draw.io binaries.

## Decision
All diagrams are Mermaid: fenced blocks in-page or .mmd files under docs/diagrams/ (shared/referenced ones).
First-party theme renders client-side. CI compiles every diagram with mermaid-cli in sandboxed headless
Chromium; compile failure blocks merge. AI diagram changes only via UpdateMermaidDiagram contract PRs.
Label conventions forbid ()[]{} to avoid parser breakage.

## Consequences
+ Diagrams diff like code; GitHub also renders mermaid fences natively in review; single grammar for humans
  and AI. - Client-side rendering means no-JS readers see source text (accepted; source is readable);
  complex layouts are limited vs dedicated tools (accepted at this scale).

## Alternatives
PlantUML rejected (JVM dependency, no native Docusaurus/GitHub rendering). Binary diagram formats rejected
(undiffable, unreviewable, un-generatable).
