# 5. Anthropic Claude

> **Model lineups and pricing change frequently. Verified against official documentation on 2026-08-14. Re-verify before production decisions.**
>
> Official docs have consolidated at **platform.claude.com/docs** (docs.claude.com and docs.anthropic.com now 302-redirect there). Agent SDK docs live at **code.claude.com/docs**; MCP spec at **modelcontextprotocol.io**.

## 5.1 Platform overview & positioning

Anthropic exposes Claude models through a single first-party REST API (`https://api.anthropic.com`, primary endpoint `POST /v1/messages`), the Claude Console (`platform.claude.com`), and partner platforms (Amazon Bedrock, Google Cloud Vertex AI, Claude Platform on AWS, Microsoft Foundry). Positioning is agentic/coding/enterprise-first: no embedding, audio, image-generation, or video models; instead deep investment in tool use, structured outputs, prompt caching, the Files API, server-side tools (web search, code execution), computer use, hosted Managed Agents, the Claude Agent SDK, and the Model Context Protocol (MCP), which Anthropic originated.

The 2026-08 lineup is a 5-era lineup (Fable 5 / Opus 5 / Sonnet 5 at 1M context) plus Haiku 4.5 as the small tier. The 3.x families are retired; Claude 4.0/4.1 are retired; 4.5–4.8 models remain served but superseded (§5.18).

Source: https://platform.claude.com/docs/en/about-claude/models/overview (accessed 2026-08-14).

## 5.2 Current model catalog

Per models overview (https://platform.claude.com/docs/en/about-claude/models/overview, accessed 2026-08-14) and pricing (https://platform.claude.com/docs/en/about-claude/pricing, accessed 2026-08-14):

| Model | API id (pinned) | Family/tier | Context | Output limit | Modalities in/out | Tool use | Structured output | Fine-tuning | $ in / $ out per 1M |
|---|---|---|---|---|---|---|---|---|---|
| Claude Fable 5 | `claude-fable-5` | Fable / frontier | 1M | 128k | text+image / text | Yes | Yes | No | 10.00 / 50.00 |
| Claude Opus 5 | `claude-opus-5` | Opus / frontier | 1M | 128k | text+image / text | Yes | Yes | No | 5.00 / 25.00 |
| Claude Sonnet 5 | `claude-sonnet-5` | Sonnet / mid | 1M | 128k | text+image / text | Yes | Yes | No | 2.00 / 10.00 |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` (alias `claude-haiku-4-5`) | Haiku / small | 200k | 64k | text+image / text | Yes | Yes | No | 1.00 / 5.00 |

Notes:
- **Claude Mythos 5** (`claude-mythos-5`): invitation-only, defensive-cybersecurity workflows ("Project Glasswing"); same specs/pricing as Fable 5. Not generally available.
- Still served but superseded (migration targets in §5.18): Opus 4.8 / 4.7 / 4.6 ($5/$25), Sonnet 4.6 ($3/$15), Opus 4.5 and Sonnet 4.5 (pricing no longer on the current pricing page — [UNVERIFIED]).
- Model ids are **pinned snapshots**, not evergreen. Training/knowledge cutoffs: Fable 5 Jan 2026; Opus 5 May 2026; Sonnet 5 Jan 2026; Haiku 4.5 trained Jul 2025 / knowledge Feb 2025.
- Sonnet 5 $2/$10 is introductory pricing extended through 2026-08-31 per the pricing page; re-verify after that date.

## 5.3 Model details & limitations

### Fable 5 (`claude-fable-5`)
Top-priced frontier model. **Adaptive thinking is always on** (models overview lists extended thinking "No — adaptive thinking always on"): reasoning depth is model-controlled; there is no manual `budget_tokens` mode. Pricing page groups it under "Newer Models (Limited Availability)" while the overview lists it on all platforms — treat regional/tier availability as account-dependent. 1M context, 128k output.

### Opus 5 (`claude-opus-5`)
Frontier workhorse. Adaptive thinking (`thinking: {"type": "adaptive"}`) with `output_config.effort` control. Supports **Fast Mode** (Opus 5 and 4.8 only) at $10/$50 per 1M — faster output, not combinable with Batch API, stacks with caching and data-residency multipliers.

### Sonnet 5 (`claude-sonnet-5`)
Mid-tier default. Adaptive thinking. 1M context at flat pricing (no long-context tier surcharge per pricing page).

### Haiku 4.5 (`claude-haiku-4-5-20251001`)
Small/fast tier, last 4.5-era model in the main catalog. 200k context, 64k output. Uses **manual extended thinking** (`thinking: {"type": "enabled", "budget_tokens": N}`), not adaptive.

### Cross-cutting constraints (all per official docs, accessed 2026-08-14)
- **Sampling parameters deprecated on 4.7+ era models**: `temperature`, `top_p`, `top_k` set to non-default values return **400** on Claude 4.7+ (and Mythos Preview). Source: https://platform.claude.com/docs/en/about-claude/model-deprecations.
- Extended thinking (`type: "enabled"`) is **rejected with 400 on Opus 4.6+ / Sonnet 4.7+**; deprecated on Sonnet 4.6. Source: extended-thinking doc (§5.9).
- `stop_reason` values now include `pause_turn` (long-running turn paused), `refusal`, and `model_context_window_exceeded`; refusals carry `stop_details` with `category` (`cyber`, `bio`, `frontier_llm`, `reasoning_extraction`, `general_harms`).
- Tokenizer change: "Claude 4.7+ tokenizer: ~30% more tokens than earlier versions" (pricing page) — token-count assumptions from 4.5-era do not transfer.
- Tool-use system-prompt overhead (tool-use overview): Opus 5 286 tokens (`auto`/`none`) / 406 (`any`/`tool`); Sonnet 5 354/474; Haiku 4.5 496/588.

## 5.4 Embedding / audio / vision / video models

- **Embeddings: none.** Anthropic explicitly does not offer an embedding model and recommends third-party providers, primarily **Voyage AI** (`voyage-4-large`, `voyage-4`, `voyage-4-lite`, open-weight `voyage-4-nano`, plus code/finance/law/multimodal/context variants; up to 32k-token inputs; 256–2048 dims). Source: https://platform.claude.com/docs/en/docs/build-with-claude/embeddings (accessed 2026-08-14).
- **Vision:** image *input* only (JPEG/PNG/GIF/WebP via base64, URL, or `file_id`); no image generation.
- **Audio/video:** no audio or video modalities in or out. [Not offered per current docs.]

## 5.5 Pricing model & cost notes

All prices USD per 1M tokens; source: https://platform.claude.com/docs/en/about-claude/pricing (accessed 2026-08-14).

| Model | Input | Output | Batch in/out (−50%) | 5m cache write (1.25×) | 1h cache write (2×) | Cache read (0.1×) |
|---|---|---|---|---|---|---|
| Fable 5 | 10.00 | 50.00 | 5.00 / 25.00 | 12.50 | 20.00 | 1.00 |
| Opus 5 | 5.00 | 25.00 | 2.50 / 12.50 | 6.25 | 10.00 | 0.50 |
| Opus 4.8 / 4.7 / 4.6 | 5.00 | 25.00 | 2.50 / 12.50 | 6.25 | 10.00 | 0.50 |
| Sonnet 5 | 2.00 | 10.00 | 1.00 / 5.00 | 2.50 | 4.00 | 0.20 |
| Sonnet 4.6 | 3.00 | 15.00 | 1.50 / 7.50 | 3.75 | 6.00 | 0.30 |
| Haiku 4.5 | 1.00 | 5.00 | 0.50 / 2.50 | 1.25 | 2.00 | 0.10 |

- **Batch API:** 50% off input and output; not combinable with Fast Mode.
- **Fast Mode** (Opus 5/4.8 only): $10/$50.
- **Data residency:** `inference_geo: "us"` applies a **1.1× multiplier** to all token categories; default global routing at standard price.
- **Long context:** full 1M window at standard pricing (no tiered surcharge).
- **Thinking tokens billed as output tokens** (both adaptive and manual modes); tracked in `usage.output_tokens_details.thinking_tokens`.
- **Server tools:** web search $10 per 1,000 searches (+tokens); web fetch free beyond tokens; code execution free with web search/fetch, otherwise $0.05/hour (5-min minimum) after 1,550 free hours/month/org.
- **Managed Agents:** tokens at standard rates + **$0.08 per session-hour** while status is `running`.
- **Claude Platform on AWS / Microsoft Foundry** bill in Claude Consumption Units (100 CCU = $1). Bedrock/Google Cloud regional or multi-region endpoints carry a 10% premium over global endpoints.

## 5.6 Authentication & environment

- Header auth: `x-api-key: $ANTHROPIC_API_KEY` plus required `anthropic-version: 2023-06-01` and `content-type: application/json`.
- SDK convention: environment variable `ANTHROPIC_API_KEY`; base URL override at client construction.
- Keys are created in the Claude Console and scoped to workspaces (Files are workspace-scoped to the uploading key's workspace).
- Beta features are opted into via `anthropic-beta: <flag>` headers (e.g. `files-api-2025-04-14`, `mcp-client-2025-11-20`, `computer-use-2025-11-24`).
- OAuth/IAM: not used on the first-party API; Bedrock uses AWS credentials/IAM, Vertex uses Google Cloud IAM.

Source: https://platform.claude.com/docs/en/api/messages.md and /docs/en/api/client-sdks (accessed 2026-08-14).

## 5.7 API endpoints & schemas

Base URL `https://api.anthropic.com`; versioning via the `anthropic-version` header (current documented value still `2023-06-01`; new behavior ships behind beta headers).

| Endpoint | Purpose |
|---|---|
| `POST /v1/messages` | Create a message (streaming or not) |
| `POST /v1/messages/count_tokens` | Count input tokens (no `stream`/`inference_geo`) |
| `POST /v1/messages/batches` (+ `GET`, `/{id}`, `/{id}/results`, `/{id}/cancel`, `DELETE /{id}`) | Message Batches API |
| `POST /v1/files` (+ `GET`, `/{id}`, `/{id}/content`, `DELETE /{id}`) | Files API (beta) |

Request body (Messages, key fields): required `model`, `max_tokens`, `messages`; optional `system` (string or text-block array), `tools` (custom + server tools: `code_execution`, `bash`, `web_search`, `web_fetch`, `text_editor`, `memory`, `tool_search`), `tool_choice` (`auto` | `any` | `tool` | `none`), `thinking` (`enabled` | `disabled` | `adaptive`), `output_config` (structured-output format + `effort`), `metadata.user_id`, `stop_sequences`, `stream`, top-level `cache_control`, `container`, `inference_geo`, `service_tier` (`auto` | `standard_only`), and legacy sampling params (`temperature`/`top_p`/`top_k` — 400 on 4.7+ models when non-default).

Response shape:

```json
{
  "id": "msg_...", "type": "message", "role": "assistant", "model": "claude-opus-5",
  "content": [ {"type": "thinking", "thinking": "...", "signature": "..."},
               {"type": "text", "text": "...", "citations": []} ],
  "stop_reason": "end_turn | max_tokens | stop_sequence | tool_use | pause_turn | refusal | model_context_window_exceeded",
  "stop_sequence": null,
  "stop_details": {"type": "refusal", "category": "cyber|bio|frontier_llm|reasoning_extraction|general_harms", "explanation": null},
  "usage": {
    "input_tokens": 0, "output_tokens": 0,
    "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0,
    "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 0},
    "output_tokens_details": {"thinking_tokens": 0},
    "server_tool_use": {"web_search_requests": 0, "web_fetch_requests": 0},
    "service_tier": "standard", "inference_geo": null
  },
  "container": null
}
```

Content block types: `text`, `thinking`, `redacted_thinking`, `tool_use` (with `caller` field), `server_tool_use`, `web_search_tool_result`, `web_fetch_tool_result`, `code_execution_tool_result`, `bash_code_execution_tool_result`, `text_editor_code_execution_tool_result`, `tool_search_tool_result`, `container_upload`. Input blocks additionally: `image` (base64/url/file), `document` (base64/text/url/file + optional `citations`), `tool_result`.

Request size limits: Messages and count_tokens 32 MB; Batches 256 MB; Files 500 MB.

Source: https://platform.claude.com/docs/en/api/messages.md, /docs/en/api/errors (accessed 2026-08-14).

## 5.8 SDK integration

Official SDKs: Python (`pip install anthropic`), TypeScript (`npm install @anthropic-ai/sdk`), Java, Go, Ruby, C#, PHP. Source: https://platform.claude.com/docs/en/api/client-sdks (accessed 2026-08-14).

Python:

```python
import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY

msg = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=1024,
    system="You are a terse technical assistant.",
    thinking={"type": "adaptive"},
    output_config={"effort": "medium"},
    messages=[{"role": "user", "content": "Explain token bucket rate limiting."}],
)
print(msg.content[-1].text, msg.usage.output_tokens)
```

TypeScript:

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic(); // reads ANTHROPIC_API_KEY
const msg = await client.messages.create({
  model: "claude-sonnet-5",
  max_tokens: 1024,
  thinking: { type: "adaptive" },
  messages: [{ role: "user", content: "Explain token bucket rate limiting." }],
});
console.log(msg.content.at(-1));
```

curl:

```bash
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "anthropic-version: 2023-06-01" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -d '{
    "model": "claude-haiku-4-5",
    "max_tokens": 512,
    "messages": [{"role": "user", "content": "Hello, Claude"}]
  }'
```

## 5.9 Streaming, tool use, structured output examples

**Streaming** (`"stream": true`, SSE): event order `message_start` → per block (`content_block_start` → `content_block_delta`* → `content_block_stop`) → `message_delta` (cumulative usage) → `message_stop`; interleaved `ping` and possible `error` events (e.g. `overloaded_error`). Delta types: `text_delta`, `input_json_delta` (partial JSON strings for tool input), `thinking_delta`, `signature_delta`. With `thinking.display: "omitted"`, only `signature_delta` is sent for thinking blocks. Per-tool `eager_input_streaming` enables fine-grained tool-parameter streaming. Source: https://platform.claude.com/docs/en/docs/build-with-claude/streaming (accessed 2026-08-14).

**Tool use** (custom tool + result round trip):

```json
{
  "model": "claude-opus-5",
  "max_tokens": 1024,
  "tools": [{
    "name": "get_weather",
    "description": "Get current weather for a location.",
    "strict": true,
    "input_schema": {
      "type": "object",
      "properties": {"location": {"type": "string"}},
      "required": ["location"],
      "additionalProperties": false
    }
  }],
  "tool_choice": {"type": "auto"},
  "messages": [{"role": "user", "content": "Weather in Osaka?"}]
}
```

The model returns `stop_reason: "tool_use"` with a `tool_use` block (`id`, `name`, `input`); you append the assistant content plus a user turn containing `{"type": "tool_result", "tool_use_id": "...", "content": "..."}` and call again. Parallel tool calls are default; disable via `tool_choice: {"type": "any", "disable_parallel_tool_use": true}`. Source: https://platform.claude.com/docs/en/docs/agents-and-tools/tool-use/overview (accessed 2026-08-14).

**Structured outputs** — two mechanisms, combinable (source: https://platform.claude.com/docs/en/docs/build-with-claude/structured-outputs, accessed 2026-08-14):

1. JSON output via `output_config.format` (the older top-level `output_format` still works but is deprecated):

```json
{
  "model": "claude-sonnet-5",
  "max_tokens": 1024,
  "messages": [{"role": "user", "content": "Extract: John Smith wants an Enterprise demo Tuesday 2pm"}],
  "output_config": {
    "format": {
      "type": "json_schema",
      "schema": {
        "type": "object",
        "properties": {"name": {"type": "string"}, "plan": {"type": "string"}, "demo": {"type": "boolean"}},
        "required": ["name", "plan", "demo"],
        "additionalProperties": false
      }
    }
  }
}
```

2. Strict tool use: `"strict": true` in a tool definition guarantees schema-conformant `input`.

Limits: ≤20 strict tools/request; ≤24 optional parameters across strict schemas; ≤16 union-typed parameters; `minimum`/`maximum`/`minLength`/`maxLength` unsupported; incompatible with citations and message prefill; first request pays grammar-compilation latency (cached 24h). Thinking is not constrained by the grammar — only final output.

## 5.10 Error handling & retry

| HTTP | `error.type` | Meaning |
|---|---|---|
| 400 | `invalid_request_error` | Malformed request (incl. deprecated params on 4.7+) |
| 401 | `authentication_error` | Bad/revoked key |
| 402 | `billing_error` | Billing problem |
| 403 | `permission_error` | Key lacks access |
| 404 | `not_found_error` | Resource missing |
| 409 | `conflict_error` | State conflict |
| 413 | `request_too_large` | Over byte limit |
| 429 | `rate_limit_error` | Rate limited (`retry-after` header) |
| 500 | `api_error` | Internal error |
| 504 | `timeout_error` | Request timed out |
| 529 | `overloaded_error` | Capacity; also arrives as SSE `error` event |

Error body: `{"type":"error","error":{"type":"...","message":"..."},"request_id":"req_..."}`; every response carries a `request-id` header. SDKs raise typed exceptions and auto-retry transient failures (connection errors, 429, 5xx) with exponential backoff (2× default). For turns >10 minutes use streaming or the Batch API; keep TCP keep-alive on. Source: https://platform.claude.com/docs/en/api/errors (accessed 2026-08-14).

## 5.11 Rate limits & quotas

Source: https://platform.claude.com/docs/en/api/rate-limits (accessed 2026-08-14). The old numbered tiers (1–4) are replaced by named tiers:

| Tier | Monthly spend cap |
|---|---|
| Start | $500 |
| Build | $1,000 |
| Scale | $200,000 |
| Custom | none (account team) |

Advancement is based on usage history/account standing (exact thresholds not published — [UNVERIFIED]); new orgs may begin in a lower-limit Evaluation tier. Documented per-model limits (Start tier; Build/Scale same per docs): Opus 5 / Sonnet 5 / Haiku 4.5 each **1,000 RPM, 2,000,000 input TPM, 400,000 output TPM**.

- **Cache-aware ITPM:** only *uncached* input tokens count toward ITPM (billed at 0.1× when read) — with 80% cache hits, ~10M effective input tokens/min on a 2M ITPM limit.
- **Token bucket** algorithm: continuous replenishment, no fixed reset windows.
- **Batches:** separate 1,000 RPM (all models combined); ≤100,000 requests/batch; ≤200,000 requests in the processing queue.
- Headers: `anthropic-ratelimit-requests-remaining`, `anthropic-ratelimit-input-tokens-remaining`, `anthropic-ratelimit-output-tokens-remaining`, `retry-after`.

## 5.12 Fine-tuning & customization

No self-serve fine-tuning on the first-party Claude API; no fine-tuning docs exist for current models (accessed 2026-08-14). Customization levers instead: system prompts, prompt caching, structured outputs, tools/skills, and MCP servers. Historical Bedrock fine-tuning applied only to retired Claude 3 Haiku. Any current partner-platform fine-tuning: [UNVERIFIED — not published].

## 5.13 RAG & embedding pipeline notes

Anthropic ships no embedder; the documented pattern is external embeddings (Voyage AI recommended; see §5.4) + your vector store, with Claude as the generator. Platform features relevant to RAG:

- **Citations**: enable per `document` block (`"citations": {"enabled": true}`) — responses return `text` blocks with citation locations (`char_location`, `page_location`, `content_block_location`, `search_result_location`).
- **Files API** for reusable corpora (upload once, reference by `file_id`; PDFs and text as `document` blocks).
- **Server-side web search / web fetch** tools for retrieval without your own pipeline.
- **Prompt caching** (up to 4 breakpoints, 5m/1h TTL) to amortize large static context; 1M context windows reduce chunking pressure but input cost still scales linearly.

## 5.14 Agent support

- **Claude Agent SDK** (Python + TypeScript; repos `anthropics/claude-agent-sdk-python` and `anthropics/claude-agent-sdk-typescript`): the Claude Code agent loop as a library — built-in file/command/web tools, hooks, subagents, permissions, sessions (resume/fork), skills/commands/memory loaded from `.claude/`, plugins, MCP. Docs: https://code.claude.com/docs/en/agent-sdk/overview (accessed 2026-08-14). Note: third-party products may not offer claude.ai login/rate limits; API keys required.
- **Managed Agents**: hosted REST product — Anthropic runs the agent and sandbox; billed tokens + $0.08/session-hour (§5.5).
- **Server tools in Messages**: `web_search_20250305`, `web_fetch`, `code_execution` (sandboxed containers, `container` reuse, `container_upload` blocks), `text_editor`, `bash`, `memory`, and `tool_search` (regex/BM25 on-demand tool discovery for large tool sets).
- **Computer use** (beta): tool `computer_20251124` (predecessor `computer_20250124`), header `anthropic-beta: computer-use-2025-11-24`; models: Opus 5, Sonnet 5, Opus 4.5–4.8, Sonnet 4.6. Actions include screenshot/click/type/scroll/drag plus new `zoom` (`enable_zoom: true`). Prompt-injection classifiers enabled by default. Source: https://platform.claude.com/docs/en/docs/agents-and-tools/tool-use/computer-use-tool (accessed 2026-08-14).

### MCP (Model Context Protocol)

Anthropic originated and open-sourced MCP (Nov 2024) as a standard for connecting AI applications to external tools/data; it is now cross-vendor (Claude, ChatGPT, VS Code, Cursor, etc.). Current spec revision: **2026-07-28** at https://modelcontextprotocol.io (accessed 2026-08-14). Primitives: tools, resources, prompts; transports: stdio and HTTP (Streamable HTTP/SSE). In the Messages API, the **MCP connector** (beta header `mcp-client-2025-11-20`; `mcp-client-2025-04-04` deprecated) takes an `mcp_servers` array (`{"type":"url","url":"https://…","name":"…","authorization_token":"…"}`); remote HTTP servers only (no stdio), tool-calls-only (no MCP resources/prompts server-side), OAuth tokens obtained by the caller. The Agent SDK and Claude Code support full MCP including local stdio servers. Sources: https://platform.claude.com/docs/en/docs/agents-and-tools/mcp-connector; https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro.md (accessed 2026-08-14).

## 5.15 Deployment patterns

- First-party API: fully managed/serverless; `service_tier` (`auto`/`standard_only`); Batch API for offline bulk (≤100k requests, most <1h, 24h expiry, results 29 days, JSONL).
- **Amazon Bedrock**: all four current models available via AWS IAM/SDKs — see https://platform.claude.com/docs/en/api/claude-on-amazon-bedrock (one-line cross-ref; regional endpoints +10%).
- **Google Cloud Vertex AI**: all four current models via GCP — see https://platform.claude.com/docs/en/api/claude-on-vertex-ai (one-line cross-ref; regional endpoints +10%).
- **Claude Platform on AWS** and **Microsoft Foundry**: CCU-billed (100 CCU = $1).
- Managed Agents for hosted long-running agents; Agent SDK for self-hosted agent loops in your own infra.

## 5.16 Region availability & data residency

- Default: global routing at standard pricing. **US-only inference**: `inference_geo: "us"` at 1.1× on all token categories (Claude API and Claude Platform on AWS); `usage.inference_geo` echoes routing. Source: pricing page (accessed 2026-08-14).
- Per-region availability matrices for Bedrock/Vertex are maintained by those platforms; not enumerated here — [UNVERIFIED in this pass].

## 5.17 Security, compliance & SLA

Documented data handling (https://privacy.claude.com/en/articles/7996866, /7996868, accessed 2026-08-14):

- **No training on commercial/API data by default** ("By default, we will not use your inputs or outputs from our commercial products … to train our models"); explicit feedback or opt-in may be used.
- **Retention:** API inputs/outputs auto-deleted from backend within **30 days**, except usage-policy violations (up to 2 years; trust-and-safety scores 7 years), feedback (5 years), legal holds.
- **Zero Data Retention (ZDR)** available by agreement; Files API content is *not* ZDR-eligible; computer use is ZDR-eligible (client-side screenshots). Structured-output schemas are cached 24h (docs advise no PHI in schemas for HIPAA).
- Certifications (SOC 2, ISO, HIPAA BAA availability) and uptime SLAs: not verified in this pass — [UNVERIFIED — see Anthropic Trust Center].

## 5.18 Legacy models & migration notes

Policy: ≥60 days' notice before retiring publicly released models; email to active deployments; Anthropic has published model-weight preservation commitments. Bedrock/Vertex set their own retirement schedules. Source: https://platform.claude.com/docs/en/about-claude/model-deprecations (accessed 2026-08-14).

Retired (requests fail):

| Model | Retired | Replacement |
|---|---|---|
| `claude-opus-4-1-20250805` | 2026-08-05 | `claude-opus-4-8` (now → Opus 5) |
| `claude-opus-4-20250514` | 2026-06-15 | `claude-opus-4-8` |
| `claude-sonnet-4-20250514` | 2026-06-15 | `claude-sonnet-4-6` |
| `claude-3-7-sonnet-20250219` | 2026-02-19 | `claude-sonnet-4-6` |
| `claude-3-5-haiku-20241022` | 2026-02-19 | `claude-haiku-4-5-20251001` |
| `claude-3-haiku-20240307` | 2026-04-20 | `claude-haiku-4-5-20251001` |

Active-but-superseded, with earliest retirement dates: `claude-opus-4-8` (≥2027-05-28), `claude-opus-4-7` (≥2027-04-16), `claude-opus-4-6` (≥2027-02-05), `claude-opus-4-5-20251101` (≥2026-11-24), `claude-sonnet-4-6` (≥2027-02-17), `claude-sonnet-4-5-20250929` (≥2026-09-29 — imminent), `claude-haiku-4-5-20251001` (≥2026-10-15). Current 5-era floors: Fable 5 ≥2027-06-09, Opus 5 ≥2027-07-24, Sonnet 5 ≥2027-06-30.

API-surface migrations:
- `thinking: {"type":"enabled","budget_tokens":N}` → `thinking: {"type":"adaptive"}` + `output_config.effort` (`low|medium|high`); manual mode 400s on Opus 4.6+/Sonnet 4.7+; adaptive may skip thinking on easy inputs. Interleaved-thinking beta header (`interleaved-thinking-2025-05-14`) only needed for manual mode on 4.5-era.
- `output_format` → `output_config.format` (old form deprecated).
- Drop non-default `temperature`/`top_p`/`top_k` before moving to 4.7+/5-era models (400).
- Budget/effort changes invalidate prompt-cache breakpoints; hold them stable in cached conversations.
- Re-baseline token budgets: 4.7+ tokenizer yields ~30% more tokens.

## 5.19 Task-suitability verdict

**Best at (evidence-based):** agentic tool-use workloads (richest server-tool set, parallel + strict tools, tool search, computer use, Agent SDK/MCP origin); long-context work (1M standard-priced); cost-engineered high-volume serving (cache-aware rate limits + 0.1× cache reads + 50% batch); schema-guaranteed extraction (grammar-backed structured outputs). Sonnet 5 at $2/$10 is the price-performance anchor; Haiku 4.5 for latency/cost-sensitive routing; Opus 5/Fable 5 for frontier reasoning.

**Worst at / avoid:** anything needing embeddings, audio, image/video generation, or speech (none offered — pair with Voyage AI etc.); self-serve fine-tuning (none); strict determinism knobs (sampling params removed on 4.7+; adaptive thinking is nondeterministic in depth); Fable 5 for budget workloads ($10/$50, limited availability). Structured outputs exclude citations and prefill — pick one per request.

## 5.20 Sources

All accessed 2026-08-14:

1. Models overview — https://platform.claude.com/docs/en/about-claude/models/overview
2. Pricing — https://platform.claude.com/docs/en/about-claude/pricing
3. Messages API reference — https://platform.claude.com/docs/en/api/messages.md
4. Rate limits — https://platform.claude.com/docs/en/api/rate-limits
5. Errors — https://platform.claude.com/docs/en/api/errors
6. Client SDKs — https://platform.claude.com/docs/en/api/client-sdks
7. Extended/adaptive thinking — https://platform.claude.com/docs/en/docs/build-with-claude/extended-thinking
8. Structured outputs — https://platform.claude.com/docs/en/docs/build-with-claude/structured-outputs
9. Streaming — https://platform.claude.com/docs/en/docs/build-with-claude/streaming
10. Prompt caching — https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching
11. Batch processing — https://platform.claude.com/docs/en/docs/build-with-claude/batch-processing
12. Files API — https://platform.claude.com/docs/en/docs/build-with-claude/files
13. Tool use overview — https://platform.claude.com/docs/en/docs/agents-and-tools/tool-use/overview
14. Computer use — https://platform.claude.com/docs/en/docs/agents-and-tools/tool-use/computer-use-tool
15. MCP connector — https://platform.claude.com/docs/en/docs/agents-and-tools/mcp-connector
16. MCP spec/intro — https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro.md
17. Embeddings guidance — https://platform.claude.com/docs/en/docs/build-with-claude/embeddings
18. Model deprecations — https://platform.claude.com/docs/en/about-claude/model-deprecations
19. Agent SDK overview — https://code.claude.com/docs/en/agent-sdk/overview
20. Data retention — https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data
21. Training-data policy — https://privacy.claude.com/en/articles/7996868-is-my-data-used-for-model-training
