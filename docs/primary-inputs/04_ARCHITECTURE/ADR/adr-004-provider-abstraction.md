# ADR-004: Thin AI Provider Abstraction, Config-Routed, No Framework

Status: Accepted · 2026-08-12

## Context
Generation must work against Anthropic, Google, OpenAI and OpenAI-compatible local endpoints, with routing
by privacy, context size, structured-output need, cost and availability. Frameworks (LangChain, LiteLLM
proxy) exist but import large dependency trees to wrap four HTTP POST shapes.

## Decision
One Protocol (`complete(task_meta, messages, opts) -> {text, usage, provider, model}`), four ~40-line
adapters, a router reading ai.config.yaml ordered chains. Privacy routing is enforced (private -> local,
hard fail). Model names live only in config/env, never code. One repair retry max; no agent loops.

## Consequences
+ Fully auditable AI surface; provider churn is a config edit; local mode enables Modes A/C offline.
- We own four adapters' upkeep (small, contract-tested); no framework niceties like streaming (not needed
  for batch generation).

## Alternatives
LangChain/LiteLLM rejected (dependency surface, supply-chain exposure, debugging opacity for one engineer).
Single-provider hard-coding rejected (mission constraint). Autonomous multi-agent orchestration rejected
(anti-overengineering rule; no requirement needs it).
