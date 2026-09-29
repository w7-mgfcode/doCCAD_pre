# ADR-001: GitHub Repository as the Single Source of Truth

Status: Accepted · 2026-08-12

## Context
The system needs one authoritative store for canonical docs, generated views, prompts, contracts, schemas,
pipeline code and CI config, with history, review workflow, and provenance. Candidates: Git repo only; Git +
CMS/database; SaaS docs platform with Git sync (GitBook-style mirror).

## Decision
A single GitHub repository holds everything the system knows. No runtime datastore exists. All change flows
through commits/PRs; all automation is derived from repo state.

## Consequences
+ History, blame, review, rollback and provenance come free; the system degrades gracefully to "a repo with
  a static site" if all automation is ignored; one backup story (git clones/mirrors).
+ Drift detection can be purely hash/diff based.
- Binary/media-heavy content is a poor fit (acceptable: docs are text + Mermaid).
- Repo growth from generated content must be managed (wholesale file replacement, no AI-edit chains).

## Alternatives
Git+DB hybrid rejected: two sources of truth is the failure mode this system exists to prevent. SaaS mirror
rejected: research showed normalized exports break deterministic file identity (GitBook analysis).
