# ADR-009: Static Deployment on GitHub Pages with Mode Variants

Status: Accepted · 2026-08-12

## Context
The artifact is a static directory. Hosting options: GitHub Pages, Netlify/Cloudflare/Vercel, own server,
Kubernetes (rejected out of hand at this scale).

## Decision
Mode B default: GitHub Actions builds and deploys to GitHub Pages via OIDC (no long-lived deploy secret).
The identical artifact serves Mode A (any static server / minimal self-host) and Mode C (privacy-oriented:
local model for generation, self-hosted static serving, nothing leaves the machine). Modes differ only in
ai.config.yaml routing and hosting target — one architecture, three postures.

## Consequences
+ Zero-cost, zero-server default colocated with the repo; per-mode drift is impossible by construction.
- Pages limits (soft 1GB site, public by default) — acceptable; private serving moves to Mode A/C.

## Alternatives
Netlify/Cloudflare: fine, adopted only if PR-preview deploys are later wanted (automation_architecture §4).
Own server in MVP rejected (a server to patch with no requirement driving it). Kubernetes rejected
(anti-overengineering rule — nothing here needs orchestration).
