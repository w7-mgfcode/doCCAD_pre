# AI Model Documentation Suite — Table of Contents

Multi-vendor, developer-ready reference. Verified against official documentation 2026-08-14; model
lineups and pricing change frequently — re-verify before production decisions. Scope: currently
available, practically usable models only; legacy families appear only in per-chapter migration notes.

## Part I — Foundations
0. Conventions, evidence rules, terminology (00_CONVENTIONS.md)
1. This table of contents
2. How to read the catalogs: pricing units, context vs output limits, modality notation

## Part II — Provider Chapters (each follows the 20-section template in 00_CONVENTIONS.md)
3. OpenAI — platform, current model catalog, embeddings/audio/vision, API + SDKs, limits, deployment
4. Google Gemini (AI Studio / Gemini API) — incl. Gemma open models
5. Anthropic Claude — Messages API, tool use, agent SDK/MCP
6. AWS Bedrock — multi-vendor managed models (Anthropic, Meta, Mistral, Cohere, Amazon own-brand …)
7. Azure AI Foundry — OpenAI models on Azure + model catalog (Phi, Llama, Mistral …)
8. OpenRouter — aggregation layer: routing, unified API, pricing model, dynamic model catalog
9. Ollama — local inference: hardware realities, quantization, current usable open-weight lineup
10. Hugging Face — Inference API/Endpoints, Transformers, TGI, Spaces

Each provider chapter contains: current model catalog table · capabilities & limitations · pricing ·
context/output limits · multimodal support · fine-tuning · embedding/audio/vision models · agent support ·
RAG notes · deployment options · authentication · endpoints & schemas · Python/JS/curl examples ·
streaming · tool use / structured output · error handling & retry · rate limits · region availability ·
security/compliance/SLA (documented only) · legacy & migration · task-suitability verdict · sources.

## Part III — Cross-Provider Integration Blueprints
11. Provider-agnostic client patterns: env config, thin adapters, fallback chains
12. Retry, timeout, and streaming patterns (Python + JS)
13. Tool use / function calling across providers — schema differences table
14. RAG pipeline blueprint (embeddings → store → retrieve → ground) with per-provider slots
15. Agent patterns and MCP: what each provider officially supports
16. Vision & audio pipelines
17. Local inference setup (Ollama, HF TGI) incl. Docker
18. Deployment: containers, serverless (Lambda / Cloud Run), managed endpoints
19. Monitoring, logging, cost optimization (caching, batching, routing by tier)
20. Security & compliance across providers: keys, data-usage policies, residency

## Part IV — Unified Model Selection Guide
21. Master comparison matrix (all providers, from structured model data)
22. Task-type suitability map: classification · summarization · reasoning · coding · agents ·
    multimodal · RAG · embeddings · speech · vision
23. Price/performance ranking by tier (budget / mid / premium reasoning)
24. Selection dimensions: latency · context window · accuracy · local vs cloud · compliance · region ·
    open-source vs frontier
25. Decision trees ("If your use case is X, choose Y") — ASCII
26. Avoid-lists ("Avoid these models for X") — evidence-based warnings
27. Scorecards & tradeoff analysis (incl. ASCII spider profiles)
28. Migration & versioning strategy across providers

## Part V — Appendices
A. Structured model data (providers/*.models.json — machine-readable)
B. Master source register with access dates
C. Glossary
