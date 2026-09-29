# Part III — Cross-Provider Integration Blueprints (sections 11–20)

> **Volatility warning.** Everything provider-specific below is grounded in the Part II chapters,
> which were verified against official documentation on **2026-08-14**. Model lineups, prices, API
> shapes and limits change frequently — re-verify against the cited chapter (and its sources) before
> production decisions. Where a pattern is generic engineering knowledge rather than a chapter
> finding, it is labeled as such.

---

## 11. Provider-agnostic client patterns

### 11.1 Environment configuration — all 8 providers

| Provider | Key env var(s) | Auth mechanism | Base URL | Primary endpoint |
|---|---|---|---|---|
| OpenAI | `OPENAI_API_KEY` | `Authorization: Bearer` | `https://api.openai.com/v1` | `POST /responses` (recommended); `/chat/completions` supported (ch. 3 §3.6–3.7) |
| Google Gemini | `GEMINI_API_KEY` (`GOOGLE_API_KEY` also honored by SDKs) | `x-goog-api-key` header | `https://generativelanguage.googleapis.com` (`/v1beta`) | `POST /v1beta/interactions` (GA, recommended); `models/{m}:generateContent` classic (ch. 4 §4.6–4.7) |
| Anthropic | `ANTHROPIC_API_KEY` | `x-api-key` + required `anthropic-version: 2023-06-01` | `https://api.anthropic.com` | `POST /v1/messages` (ch. 5 §5.6–5.7) |
| AWS Bedrock | `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY`/`AWS_SESSION_TOKEN` (or IAM roles — preferred); `AWS_BEARER_TOKEN_BEDROCK` for Bedrock API keys | SigV4 signing; API key on mantle | `bedrock-runtime.{region}.amazonaws.com`; `bedrock-mantle.{region}.api.aws` | `Converse`/`ConverseStream`; mantle: `/openai/v1`, `/anthropic/v1/messages` (ch. 6 §6.6–6.7) |
| Azure / Microsoft Foundry | `AZURE_OPENAI_API_KEY` (or Entra ID via `azure-identity`, recommended) | `api-key` header / Bearer token | `https://<resource>.openai.azure.com/openai/v1/` | `POST /responses`, `/chat/completions` — `model` = **deployment name** (ch. 7 §7.6–7.7) |
| OpenRouter | `OPENROUTER_API_KEY` | `Authorization: Bearer` | `https://openrouter.ai/api/v1` | `POST /chat/completions`; `GET /models` for live catalog (ch. 8 §8.6–8.7) |
| Ollama (local) | none — **no auth on local API**; `OLLAMA_API_KEY` for Ollama Cloud | none locally; Bearer for cloud | `http://localhost:11434` (`/api` native, `/v1` OpenAI-compat, `api_key="ollama"` placeholder) | `POST /api/chat`; `/v1/chat/completions` (ch. 9 §9.6–9.7) |
| Hugging Face | `HF_TOKEN` | `Authorization: Bearer` | `https://router.huggingface.co/v1` | `POST /chat/completions` (chat only; other tasks via HF clients) (ch. 10 §10.6–10.7) |

Suggested twelve-factor layout — one variable set per provider, plus one selector:

```bash
LLM_PROVIDER=openai            # openai|gemini|anthropic|bedrock|azure|openrouter|ollama|hf
LLM_MODEL=gpt-5.6-terra        # provider-native model id (Azure: deployment name)
OPENAI_API_KEY=...             # only the providers you actually use
ANTHROPIC_API_KEY=...
GEMINI_API_KEY=...
AWS_REGION=us-east-1           # Bedrock: credentials from the standard AWS chain, no static key
AZURE_OPENAI_BASE_URL=https://myres.openai.azure.com/openai/v1/
OPENROUTER_API_KEY=...
HF_TOKEN=...
OLLAMA_BASE_URL=http://localhost:11434/v1
```

### 11.2 The thin-adapter pattern

Many surfaces speak the **OpenAI wire format**, so one `OpenAI()` client with a swapped
`base_url`/`api_key` covers a surprising share of the matrix:

```
                    ┌───────────────────────────────────────────────┐
                    │        openai SDK (base_url override)         │
                    └───┬──────────┬──────────┬──────────┬──────┬───┘
                        │          │          │          │      │
   api.openai.com/v1   openrouter  localhost  generative  bedrock-mantle…/openai/v1
   (Responses + Chat)  .ai/api/v1  :11434/v1  language…   (Responses+Chat; ch. 6 §6.8)
                       (Chat only) (Chat +    /v1beta/    <resource>.openai.azure.com
                       (ch. 8)     partial    openai/     /openai/v1 (ch. 7 §7.7)
                                   Responses; (beta,      router.huggingface.co/v1
                                   ch. 9 §9.7) ch. 4 §4.7) (Chat only; ch. 10 §10.7)
```

OpenAI-compatible surfaces (per chapters): **OpenRouter** (Chat Completions + extensions),
**Ollama** `/v1` (Chat Completions, embeddings, partial `/v1/responses` since v0.13.3; no
`logprobs`/`tool_choice`/`n` — ch. 9 §9.7), **Gemini compat endpoint** (beta: chat, embeddings,
images, audio, partial batch — ch. 4 §4.7), **Azure v1 API** (wire-identical Responses/Chat plus
Azure extensions — ch. 7 §7.7), **Bedrock mantle** (`/openai/v1`, and the *only* path to GPT-5.x
on Bedrock — ch. 6 §6.1), **HF router** (chat-completion task only — ch. 10 §10.7).

**Where the thin adapter breaks:**

- **Anthropic Messages** (first-party): different envelope entirely — `x-api-key` +
  `anthropic-version` headers, required `max_tokens`, content-block arrays, `tool_use`/`tool_result`
  blocks, `output_config` for structured output, its own SSE event grammar (ch. 5 §5.7–5.9). Use the
  `anthropic` SDK (which itself re-targets Bedrock mantle `/anthropic/v1/messages` and Ollama's
  Anthropic-compat endpoint via base-URL swap — ch. 6 §6.8, ch. 9 §9.7).
- **Bedrock Converse** (classic runtime): AWS-native JSON (`messages[].content[]` blocks,
  `inferenceConfig`, `toolConfig`) over SigV4 — model-agnostic *within Bedrock* but not
  OpenAI-shaped; streaming is an AWS event stream, not SSE (ch. 6 §6.7, §6.9).
- **Responses vs Chat Completions divergence**: OpenAI's recommended surface (Responses) has
  different tool and structured-output shapes (`text.format`, top-level tool `name`) than the Chat
  Completions shape the compat providers implement (ch. 3 §3.7, §3.9). A "thin adapter" that
  assumes Chat Completions everywhere quietly forfeits Responses-only features (built-in tools,
  `previous_response_id`, conversations).
- **Feature depth varies per compat surface**: e.g. Gemini compat is beta and skips
  Interactions-only features; Ollama compat ignores the API key and lacks `tool_choice`; HF router
  exposes no non-chat tasks; the same OpenRouter model id may hit endpoints with different
  parameter support (`supported_parameters` is the truth source — ch. 8 §8.3).

Practical adapter design (generic guidance): keep an internal request type of
`{model, system, messages, tools, json_schema, max_tokens, stream}`; write one adapter per *wire
format* (OpenAI-chat, OpenAI-responses, Anthropic-messages, Bedrock-converse, Gemini-interactions),
not one per vendor — that is 5 adapters for 8 providers, and the OpenAI-chat adapter serves
OpenRouter, Ollama, HF, Gemini-compat, Azure and mantle with only base-URL/auth differences.

### 11.3 Fallback-chain pseudocode

```
chain = [
  (openrouter, "anthropic/claude-sonnet-5"),   # OpenRouter has its own provider fallback (ch. 8 §8.7)
  (openai,     "gpt-5.6-terra"),
  (ollama,     "qwen3.6:27b"),                 # local last resort: degraded quality, never down
]

function generate(request):
  for (provider, model) in chain:
    try:
      return provider.call(model, request, timeout=per_provider_timeout)
    except NonRetryable(e):          # 400 schema, 401/403 auth, content policy
      log(e); continue_or_raise      # config bug → raise; policy block → try next provider
    except Retryable(e):             # 429/5xx/529 after in-provider backoff (see §12)
      log(e); continue               # fail over
  raise AllProvidersExhausted
```

Notes grounded in the chapters: OpenRouter natively supports `models: [primary, fallback…]` arrays
and multi-provider routing, so one OpenRouter entry already is a fallback chain (ch. 8 §8.7);
prompt caches do not transfer across providers — a failover request pays full input price; strict
structured-output guarantees differ per provider (ch. 8 §8.9), so validate JSON after every hop
regardless of which provider answered.

---

## 12. Retry, timeout, and streaming patterns

### 12.1 What the providers actually signal (from chapters)

| Provider | Rate limit / overload signals | Retry guidance from chapter |
|---|---|---|
| OpenAI | 429 `rate_limit_exceeded` (retry) vs `insufficient_quota` (billing — **never retry**); 500/503; `Retry-After` + `x-ratelimit-*` headers | exponential backoff + jitter; SDK auto-retries 2× (ch. 3 §3.10) |
| Gemini | 429 `rate_limit_exceeded` (per-minute) vs `quota_exceeded` (daily — wait/upgrade); 500/503/504 | retry 429/408/5xx only, 1→2→4→8 s + jitter; Python SDK auto-retries 4× (ch. 4 §4.10) |
| Anthropic | 429 `rate_limit_error` (`retry-after` header); **529 `overloaded_error`** — also arrives as an SSE `error` event mid-stream | SDKs auto-retry 429/5xx/connection with 2× backoff (ch. 5 §5.10) |
| Bedrock | `ThrottlingException` (429), `ModelNotReadyException` (429 — model loading), `ServiceUnavailableException` (503), `ModelTimeoutException` (408) | boto3 `Config(retries={"max_attempts":10,"mode":"adaptive"}, read_timeout=3600)` (ch. 6 §6.10) |
| Azure | 429 = TPM/RPM **or** monthly usage tier **or** regional capacity; honor `Retry-After`; 400 `content_filter` is not transient | backoff + jitter; consider PTU/spillover (ch. 7 §7.10) |
| OpenRouter | 429 rate limit; **402 = credits exhausted (stop, don't retry)**; **503 = no provider matches your routing constraints (loosen constraints, don't blind-retry)**; 502 upstream down | its own multi-provider fallback absorbs most transient upstream failures first (ch. 8 §8.10) |
| Ollama | no 429 — requests **queue** locally; 500 = engine OOM/crash; conn-refused/cold-load latency | retries only help load contention; pre-warm with `keep_alive: -1`; allow long first-token timeouts (ch. 9 §9.10) |
| Hugging Face | 429 with `RateLimit`/`RateLimit-Policy` headers (5-min windows); 402 credits; 5xx provider-side | `provider="auto"` fails over across partners; `huggingface_hub` ≥1.2.0 auto-retries 429 (ch. 10 §10.10) |

Cross-provider rules that fall out of the table:
1. Retry **only** 408, 429 (when it means rate, not billing), 5xx, and Anthropic's 529.
2. Never retry 400/401/403, OpenAI `insufficient_quota`, OpenRouter 402, Azure `content_filter`.
3. Always honor `Retry-After`/`retry-after` when present (OpenAI, Anthropic, Azure document it).
4. Errors can arrive **inside an open stream** (Anthropic SSE `error` events, Azure
   `finish_reason:"content_filter"`, OpenRouter post-200 SSE errors) — a 200 status is not success.

### 12.2 Canonical retry-with-backoff

Python (stdlib only; wrap any provider call that raises an error carrying `status`,
optional `code`, and response `headers`):

```python
import random
import time

RETRYABLE_STATUS = {408, 429, 500, 502, 503, 504, 529}
NON_RETRYABLE_CODES = {"insufficient_quota", "quota_exceeded", "content_filter"}

def call_with_backoff(fn, max_attempts=5, base=1.0, cap=60.0):
    for attempt in range(max_attempts):
        try:
            return fn()
        except ProviderError as e:                      # your adapter's error type
            retryable = (e.status in RETRYABLE_STATUS
                         and e.code not in NON_RETRYABLE_CODES)
            if not retryable or attempt == max_attempts - 1:
                raise
            delay = min(cap, base * 2 ** attempt)
            ra = e.headers.get("retry-after")
            if ra is not None:
                delay = max(delay, float(ra))           # server knows best
            time.sleep(delay + random.uniform(0, delay))  # full jitter
```

JavaScript:

```js
const RETRYABLE = new Set([408, 429, 500, 502, 503, 504, 529]);
const NON_RETRYABLE_CODES = new Set(["insufficient_quota", "quota_exceeded", "content_filter"]);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function callWithBackoff(fn, { maxAttempts = 5, base = 1000, cap = 60000 } = {}) {
  for (let attempt = 0; ; attempt++) {
    try {
      return await fn();
    } catch (e) {
      const retryable = RETRYABLE.has(e.status) && !NON_RETRYABLE_CODES.has(e.code);
      if (!retryable || attempt >= maxAttempts - 1) throw e;
      let delay = Math.min(cap, base * 2 ** attempt);
      const ra = e.headers?.get?.("retry-after");
      if (ra) delay = Math.max(delay, Number(ra) * 1000);
      await sleep(delay + Math.random() * delay);
    }
  }
}
```

Prefer the official SDKs' built-in retries where you use them (OpenAI `max_retries`, Anthropic
SDK defaults, boto3 adaptive mode, `huggingface_hub` — all documented in the respective §N.10);
the code above is for raw-HTTP adapters and for the outer *cross-provider* failover layer, which
SDK retries do not cover.

**Timeouts** (chapter-grounded): set connect timeouts short (~10 s) and read timeouts long —
Bedrock's boto3 default of 60 s is too short for long generations (ch. 6 §6.10); Anthropic advises
streaming or Batch for turns over 10 minutes (ch. 5 §5.10); Ollama cold model loads can take tens
of seconds before the first token (ch. 9 §9.10). Streaming largely dissolves the read-timeout
problem: apply an idle (inter-chunk) timeout instead of a total one.

### 12.3 SSE consumption — the three main API shapes

**Shape A — OpenAI Chat Completions chunks** (used verbatim by OpenRouter, HF router, Ollama `/v1`,
Gemini compat, Azure, Bedrock mantle): `data:` lines of `chat.completion.chunk` JSON, terminated by
`data: [DONE]`. OpenRouter interleaves SSE **comment lines** (`: OPENROUTER PROCESSING`) that crash
naive `JSON.parse` loops — skip lines not starting with `data:` (ch. 8 §8.9).

```python
import httpx, json

with httpx.stream("POST", url, headers=headers, json={**body, "stream": True}) as r:
    for line in r.iter_lines():
        if not line.startswith("data: "):
            continue                       # skips comments/keep-alives
        payload = line[6:]
        if payload == "[DONE]":
            break
        chunk = json.loads(payload)
        delta = chunk["choices"][0]["delta"].get("content")
        if delta:
            print(delta, end="")
        # last chunk may carry usage (OpenRouter does; ch. 8 §8.9)
```

**Shape B — OpenAI Responses semantic events** (OpenAI direct, Azure v1, mantle Responses): typed
events, not bare deltas — filter on `response.output_text.delta`, finish on `response.completed`
(ch. 3 §3.9, ch. 7 §7.9):

```python
with client.responses.stream(model="gpt-5.6-terra", input="Count to 5.") as stream:
    for event in stream:
        if event.type == "response.output_text.delta":
            print(event.delta, end="")
```

**Shape C — Anthropic Messages events**: fixed grammar `message_start` → per block
(`content_block_start` → `content_block_delta`* → `content_block_stop`) → `message_delta`
(cumulative usage) → `message_stop`, with `ping` and possible `error` events interleaved
(`overloaded_error` can arrive mid-stream). Delta subtypes: `text_delta`, `input_json_delta`
(partial tool-input JSON), `thinking_delta`, `signature_delta` (ch. 5 §5.9):

```python
with client.messages.stream(model="claude-sonnet-5", max_tokens=512,
                            messages=[{"role": "user", "content": "Count to 5."}]) as stream:
    for text in stream.text_stream:
        print(text, end="")
    final = stream.get_final_message()     # usage lives here
```

Not SSE at all (do not pipe through an SSE parser): **Bedrock Converse** streams an AWS binary
event stream — iterate `converse_stream()["stream"]` for `contentBlockDelta`/`metadata` events
(ch. 6 §6.9); **Ollama native** `/api/chat` streams NDJSON, one JSON object per line, ending with a
`done: true` object carrying token counts (ch. 9 §9.9). **Gemini classic**
`:streamGenerateContent?alt=sse` is SSE with `candidates[].content` chunks; Interactions streaming
is documented but its event snippet was not captured in ch. 4 (§4.9) — verify before relying on
event names.

---

## 13. Tool use / function calling across providers

### 13.1 Schema-shape comparison

| Surface | Tool definition | Model's call appears as | You return the result as | Forcing a tool |
|---|---|---|---|---|
| OpenAI Responses (ch. 3 §3.9) | `{"type":"function","name","description","parameters":<JSON Schema>,"strict":true}` — **name at top level** | `output[]` item `type:"function_call"` with `call_id`, `name`, arguments | input item `{"type":"function_call_output","call_id","output"}` (+ `previous_response_id`) | `tool_choice` (per Responses reference); built-in tools (`web_search`, `mcp`, …) need no loop |
| OpenAI Chat Completions shape (as passed through by OpenRouter/HF/Ollama-compat; ch. 8 §8.9, ch. 10 §10.9) | `tools:[{"type":"function","function":{name,description,parameters}}]` | `finish_reason:"tool_calls"`, `message.tool_calls[]` | message with `role:"tool"`, `tool_call_id` | `tool_choice` (Ollama compat does **not** support it — ch. 9 §9.7) |
| Anthropic Messages (ch. 5 §5.9) | `{"name","description","input_schema":<JSON Schema>,"strict":true}` — note **`input_schema`**, no `type` wrapper | `stop_reason:"tool_use"` + content block `{"type":"tool_use","id","name","input"}` | user-turn block `{"type":"tool_result","tool_use_id","content"}` | `tool_choice: {"type":"auto"\|"any"\|"tool"\|"none"}`; parallel calls default |
| Gemini Interactions (ch. 4 §4.9) | `{"type":"function","name","description","parameters":<JSON Schema>}` in `tools[]` | function-call **step** in the `steps[]` history | send result back as next input (loop per docs) | `generation_config.tool_choice: auto\|any\|none\|validated`; **Gemini 3 stateless mode must round-trip thought signatures** or you get `missing_thought_signature` |
| Bedrock Converse (ch. 6 §6.9) | `toolConfig.tools[].toolSpec: {name, inputSchema: {"json": <JSON Schema>}}` | `stopReason:"tool_use"` + content block `{"toolUse":{toolUseId,name,input}}` | user message block `{"toolResult":{toolUseId, content:[{"json":…}]}}` | `toolChoice` (also the standard structured-output workaround: one required tool) |

Same JSON Schema everywhere; what moves is (a) the wrapper key (`parameters` vs `input_schema` vs
`inputSchema.json`), (b) where the call shows up (typed output item vs stop-reason + content block
vs step history), and (c) the result-return convention. Strictness guarantees also differ:
Anthropic strict tools are grammar-backed with documented limits (≤20 strict tools, no
`minLength`/`maximum`, ch. 5 §5.9); OpenRouter warns exact compliance "is not guaranteed on every
endpoint" (ch. 8 §8.9); on Bedrock, structured output is a per-model-card flag (ch. 6 §6.9).

### 13.2 One worked example, ported across three providers

Task: `get_weather(city) -> {"temp_c": …}`, two-step loop.

**OpenAI Responses:**

```python
from openai import OpenAI
client = OpenAI()

tools = [{"type": "function", "name": "get_weather",
          "description": "Get current weather for a city",
          "parameters": {"type": "object",
                         "properties": {"city": {"type": "string"}},
                         "required": ["city"], "additionalProperties": False},
          "strict": True}]

r1 = client.responses.create(model="gpt-5.6-terra", input="Weather in Oslo?", tools=tools)
call = next(i for i in r1.output if i.type == "function_call")
r2 = client.responses.create(
    model="gpt-5.6-terra", previous_response_id=r1.id, tools=tools,
    input=[{"type": "function_call_output", "call_id": call.call_id,
            "output": '{"temp_c": 14}'}])
print(r2.output_text)
```

**Anthropic Messages:**

```python
import anthropic
client = anthropic.Anthropic()

tools = [{"name": "get_weather",
          "description": "Get current weather for a city",
          "strict": True,
          "input_schema": {"type": "object",
                           "properties": {"city": {"type": "string"}},
                           "required": ["city"], "additionalProperties": False}}]

msgs = [{"role": "user", "content": "Weather in Oslo?"}]
m1 = client.messages.create(model="claude-sonnet-5", max_tokens=512,
                            tools=tools, messages=msgs)
tu = next(b for b in m1.content if b.type == "tool_use")
msgs += [{"role": "assistant", "content": m1.content},
         {"role": "user", "content": [{"type": "tool_result",
                                       "tool_use_id": tu.id,
                                       "content": '{"temp_c": 14}'}]}]
m2 = client.messages.create(model="claude-sonnet-5", max_tokens=512,
                            tools=tools, messages=msgs)
print(m2.content[-1].text)
```

**Bedrock Converse (same Claude model, AWS schema):**

```python
import boto3
client = boto3.client("bedrock-runtime", region_name="us-east-1")

tool_cfg = {"tools": [{"toolSpec": {
    "name": "get_weather",
    "description": "Get current weather for a city",
    "inputSchema": {"json": {"type": "object",
                             "properties": {"city": {"type": "string"}},
                             "required": ["city"]}}}}]}

msgs = [{"role": "user", "content": [{"text": "Weather in Oslo?"}]}]
r1 = client.converse(modelId="global.anthropic.claude-sonnet-5",
                     messages=msgs, toolConfig=tool_cfg)
tu = next(b["toolUse"] for b in r1["output"]["message"]["content"] if "toolUse" in b)
msgs += [r1["output"]["message"],
         {"role": "user", "content": [{"toolResult": {
             "toolUseId": tu["toolUseId"], "content": [{"json": {"temp_c": 14}}]}}]}]
r2 = client.converse(modelId="global.anthropic.claude-sonnet-5",
                     messages=msgs, toolConfig=tool_cfg)
print(r2["output"]["message"]["content"][0]["text"])
```

The loop skeleton is identical (define → detect call → execute → append result → re-call); a
portable agent core only needs the three translation functions visible above. Tool-definition
token overhead is real and provider-specific (e.g. Anthropic documents 286–588 system-prompt
tokens per model/choice mode — ch. 5 §5.3); prune unused tools.

---

## 14. RAG pipeline blueprint

```
docs ──chunk──▶ embed (pluggable) ──▶ store (numpy / vector DB) ──▶ retrieve top-k
                                                                        │
query ──embed(query-mode)──────────────────────────────────────────────┘
                                                                        ▼
                                                grounded prompt ──▶ generator (any §11 provider)
```

### 14.1 Embeddings choice (from the chapters)

| Embedder | Where | Dims / input limit | Cost | Notes |
|---|---|---|---|---|
| `text-embedding-3-large` / `-small` | OpenAI, Azure | 3072 / 1536 native; `dimensions` param (Matryoshka-style); 8,192-token input | $0.13 / $0.02 per 1M in (OpenAI list) | shortened-large beats full ada-002; Batch API −50% (ch. 3 §3.2, §3.13; ch. 7 §7.4) |
| `gemini-embedding-2` (preview-ID discrepancy noted) / `gemini-embedding-001` | Gemini API | 128–3072 flexible (MRL); 8,192 / 2,048-token input | 2: [UNVERIFIED]; 001: $0.15 (2025 blog, may be stale) | embedding-2 is multimodal (text/image/video/audio/PDF); task steering: `task_type` on 001, inline `task:` prefixes on 2 (ch. 4 §4.4, §4.13) |
| Cohere `embed-v4` / `amazon.titan-embed-text-v2:0` | Bedrock | Embed v4 multimodal, 256–1536d Matryoshka; Titan v2 256/512/1024d, 8K in | Embed v4 [UNVERIFIED]; Titan $0.02 per 1M | Titan v2 is the Knowledge Bases default (ch. 6 §6.2, §6.13); Cohere embed-v4 also on Azure (ch. 7 §7.4) |
| Voyage AI (`voyage-4-*`) | third party | up to 32K-token inputs, 256–2048d | see Voyage | Anthropic ships **no embedder** and recommends Voyage (ch. 5 §5.4) |
| `Qwen3-Embedding-0.6B/4B/8B`, `embeddinggemma-300m`, `BAAI/bge-m3`, `gte-multilingual-base` | local via **Ollama `/api/embed`** or **HF TEI** | bge-m3: 8,192 in, dense+sparse; MRL truncation on Qwen3/EmbeddingGemma | hardware only | current local picks per ch. 9 §9.4 and ch. 10 §10.13; serve with TEI for production batching/rerankers |

Rules that hold across chapters: (a) index and query with the **same model and dimension** —
vectors are not portable between embedders (explicitly noted for the OpenRouter hybrid pattern,
ch. 8 §8.13); (b) use asymmetric task steering where offered (Gemini task types, Qwen3
instruction-awareness); (c) Matryoshka truncation (768–1024d) is the documented cost dial on
OpenAI/Gemini/Cohere/Qwen — it shrinks vector-store cost with little recall loss.

### 14.2 Chunking guidance (generic engineering knowledge, not chapter-specific)

- Start with ~500–1,500 tokens per chunk, 10–20% overlap; align boundaries to structure
  (headings/paragraphs/functions) rather than fixed bytes.
- Keep chunks well under the embedder's input limit — silent truncation is a real failure mode
  (Ollama defaults `truncate: true`; set `truncate: false` to fail loudly — ch. 9 §9.13).
- Store the source text and metadata (doc id, position) beside each vector; retrieval quality
  problems are debugged by reading what was actually indexed.
- Managed alternatives exist at every hosted provider if you'd rather not own this: OpenAI
  `file_search` (vector stores; ZDR-ineligible — ch. 3 §3.13), Gemini file search / URL context
  (ch. 4 §4.13), Anthropic Files API + citations (ch. 5 §5.13), Bedrock Knowledge Bases with
  managed chunking modes (ch. 6 §6.13), Azure AI Search / On Your Data (ch. 7 §7.13).

### 14.3 Minimal end-to-end example with a pluggable embedder

```python
"""Minimal RAG: numpy store, pluggable embedder, any §11 chat adapter as generator."""
from typing import Protocol
import numpy as np

class Embedder(Protocol):
    def embed(self, texts: list[str]) -> np.ndarray: ...   # (n, d), L2-normalized

class OpenAIEmbedder:
    def __init__(self, model="text-embedding-3-small", dimensions=512):
        from openai import OpenAI
        self.client, self.model, self.dim = OpenAI(), model, dimensions
    def embed(self, texts):
        r = self.client.embeddings.create(model=self.model, input=texts,
                                          dimensions=self.dim)
        v = np.array([d.embedding for d in r.data])
        return v / np.linalg.norm(v, axis=1, keepdims=True)

class OllamaEmbedder:
    def __init__(self, model="qwen3-embedding:0.6b"):
        import ollama
        self.ollama, self.model = ollama, model
    def embed(self, texts):
        r = self.ollama.embed(model=self.model, input=texts)
        v = np.array(r.embeddings)
        return v / np.linalg.norm(v, axis=1, keepdims=True)

def chunk(text: str, size=1000, overlap=150) -> list[str]:
    return [text[i:i + size] for i in range(0, max(len(text) - overlap, 1), size - overlap)]

class Index:
    def __init__(self, embedder: Embedder):
        self.embedder, self.chunks, self.vecs = embedder, [], None
    def add(self, docs: list[str]):
        self.chunks = [c for d in docs for c in chunk(d)]
        self.vecs = self.embedder.embed(self.chunks)
    def search(self, query: str, k=5) -> list[str]:
        q = self.embedder.embed([query])[0]
        scores = self.vecs @ q                       # cosine (all normalized)
        return [self.chunks[i] for i in np.argsort(-scores)[:k]]

def answer(index: Index, chat_fn, question: str) -> str:
    ctx = "\n---\n".join(index.search(question))
    return chat_fn(system="Answer ONLY from the provided context. Say 'not found' otherwise.",
                   user=f"Context:\n{ctx}\n\nQuestion: {question}")
```

### 14.4 When you do / don't need a vector DB (honest note)

Brute-force numpy over normalized vectors is exact, dependency-free, and fast enough for
surprisingly large corpora — a matrix–vector product over hundreds of thousands of 512-d float32
vectors is milliseconds on a laptop (generic knowledge). Reach for a vector DB only when you need:
persistent multi-process access, incremental updates with deletes, metadata filtering at scale,
approximate search over many millions of vectors, or a managed service boundary. Two
chapter-documented alternatives also displace the DB entirely at small scale: (a) long context +
prompt caching — 1M-token windows with ~0.1× cached-input pricing make "stuff the corpus in the
prompt, cache the prefix" viable for mid-size corpora (ch. 4 §4.13, ch. 5 §5.13); (b) provider-
managed retrieval (§14.2 list) where its data-retention terms are acceptable (note OpenAI vector
stores are ZDR-ineligible — ch. 3 §3.16).

---

## 15. Agent patterns and MCP

### 15.1 What each provider officially ships (chapter-verified)

| Provider | Official agent offering | MCP status |
|---|---|---|
| OpenAI | **Agents SDK** (Python `openai-agents`, TS) — handoffs, guardrails, sessions, tracing; hosted tools (web search, computer use, shell, apply_patch); ChatKit UI (ch. 3 §3.14) | first-class: remote MCP servers as Responses/Agents-SDK tools |
| Anthropic | **Claude Agent SDK** (Py/TS; Claude Code loop as a library — subagents, hooks, sessions, skills); **Managed Agents** (hosted, $0.08/session-hr); server tools incl. computer use, `tool_search` (ch. 5 §5.14) | **originated MCP** (spec rev 2026-07-28); Messages-API MCP connector (remote HTTP, tools-only, beta header); Agent SDK supports full MCP incl. stdio |
| Gemini | **Interactions API** is itself agent-oriented (server-side state, step history, multi-tool); managed agent models (`deep-research-*`, `antigravity-preview`); computer-use model; `-customtools` variant (ch. 4 §4.14) | not documented on pages fetched for ch. 4 — [UNVERIFIED]; OpenAI-compat endpoint lets OpenAI-ecosystem agent frameworks target Gemini |
| Bedrock | **AgentCore** (GA 2025-10): Runtime (8-h serverless sessions), **Gateway (turns APIs/Lambda into MCP tools)**, Memory, Identity, Browser, Code Interpreter, OTel observability; classic Bedrock Agents de-emphasized; Strands Agents OSS (ch. 6 §6.14) | first-class protocol in Gateway and Runtime |
| Azure | **Foundry Agent Service** (GA; ex "Azure AI Agent Service") — prompt agents + hosted agents (your framework in managed containers), per-agent Entra identity, tracing/evals, M365 distribution (ch. 7 §7.14) | MCP servers as tools (managed "Toolbox", OAuth/Entra auth); **A2A protocol in preview** |
| OpenRouter | no agent runtime; uniform OpenAI tool loop + fallback arrays + `reasoning_effort` normalization work with any framework (ch. 8 §8.14) | `@openrouter/mcp` package converts MCP servers' tools for use through the API |
| Ollama | CLI agent mode (v0.32.0+); tool-calling API as the primitive; drop-in OpenAI/Anthropic-compat backend for agent frameworks (ch. 9 §9.14) | consumed by client frameworks, not by Ollama itself; no first-party MCP server documented |
| Hugging Face | **smolagents** (minimal code-executing agents); tiny-agents MCP-client loop [MEDIUM per ch. 10] (ch. 10 §10.14) | official **HF MCP Server** (`huggingface.co/mcp`): hub search, Spaces tools, Providers access |

### 15.2 MCP as the cross-provider tool protocol

MCP (Anthropic-originated, open spec at modelcontextprotocol.io, current revision 2026-07-28 per
ch. 5 §5.14) is the one tool-integration format that appears on **both sides of every major stack
surveyed**: consumable by OpenAI Responses/Agents SDK, Anthropic Messages/Agent SDK, Azure Agent
Service; producible by Bedrock AgentCore Gateway and the HF MCP Server; bridgeable into plain
OpenAI-format tools for OpenRouter/Ollama. Practical consequence: **write each tool once as an MCP
server**, and you get portability across providers that native `tools[]` arrays cannot give you —
the per-provider difference collapses to "how do I attach this server" (a config block) instead of
"how do I re-encode this schema".

Caveats from the chapters: the Anthropic Messages MCP connector is remote-HTTP + tools-only (no
resources/prompts, no stdio) — full MCP requires the Agent SDK/Claude Code side (ch. 5 §5.14);
Gemini's MCP position was unverified at access date (ch. 4 §4.14); MCP servers are third-party
code with tool-description injection risk — apply the same trust review as any dependency (generic
security guidance).

### 15.3 Keep-it-simple guidance

- **A loop with tools is usually enough.** Every provider's agent story reduces to §13's
  define→call→execute→append→re-call loop plus persistence. Adopt an agent framework when you
  need its specific machinery (handoffs, tracing, managed sandboxes), not by default.
- Prefer **workflow-shaped code** (fixed sequence of model calls with checked outputs) over
  open-ended autonomous loops for anything with correctness requirements; cap iterations and
  spend per task (generic guidance; token/session meters in §19).
- Managed runtimes (AgentCore Runtime, Foundry hosted agents, Anthropic Managed Agents) buy you
  sandboxing, identity and observability at the price of platform lock-in and per-session cost
  (e.g. $0.08/session-hour on Anthropic — ch. 5 §5.5). Self-host the loop first; graduate when
  isolation or scale demands it.
- Long-running agents amplify every cost lever in §19 — prompt caching and small-model routing for
  subagent tasks (explicitly what Gemini positions Flash-Lite for — ch. 4 §4.3) matter more here
  than anywhere else.

---

## 16. Vision & audio pipelines

### 16.1 Capability matrix (from chapters/sidecars, 2026-08-14)

| Provider | Image in | Image out | Audio in | Audio out (TTS/speech) | Video | PDF/file input |
|---|---|---|---|---|---|---|
| OpenAI | yes (GPT-5.6 trio, codex) | `gpt-image-2` | STT models (`gpt-transcribe`, realtime line) | `gpt-realtime-2.1`, `gpt-4o-mini-tts`, `gpt-audio-1.5` | Sora **shutting down 2026-09-24** | files via Files/file_search; flagship text models: no audio I/O (ch. 3 §3.2–3.4) |
| Gemini | yes (all reasoning models) | Nano Banana line (`gemini-3.1-flash-image`, `3-pro-image`) | yes (native input) | TTS models + Live API (WSS realtime) | in: yes; out: Veo 3.1, omni-flash | **native PDF input** on reasoning models (ch. 4 §4.2–4.4) |
| Anthropic | yes (input only) | **no** | **no** | **no** | **no** | `document` blocks (PDF/text, base64/URL/`file_id`) + citations (ch. 5 §5.4, §5.7) |
| Bedrock | per model (Claude, Nova, Llama 4, Pixtral) | Stability, Titan Image v2 | Voxtral, Nova 2 Sonic | Nova 2 Sonic (speech↔speech) | in: Nova, TwelveLabs; out: Luma Ray v2 | per model card — always check (ch. 6 §6.4) |
| Azure | yes (GPT lines, Phi-4-multimodal) | `gpt-image-2/-1.5`, FLUX.2, MAI-Image | whisper/gpt-transcribe/realtime; 25 MB file cap for file STT | `tts(-hd)`, `gpt-4o-mini-tts`, MAI-Voice | Sora-2 (preview lineage) | On Your Data / file search (ch. 7 §7.4) |
| OpenRouter | broad (per-model `input_modalities`) | catalog image models | some models list `audio` in | partner TTS (MiniMax, per-character pricing) | partner video models (per-second) | `file` modality on some models; workflows [UNVERIFIED] (ch. 8 §8.4) |
| Ollama | yes (qwen3.5/3.6, gemma4, qwen3-vl, …) — **base64 only, no remote URL fetch** | removed in v0.32.6 | gemma4 E2B/E4B audio-in only | **no** | no | no (feed extracted text) (ch. 9 §9.4) |
| Hugging Face | open VLMs (Qwen3-VL, Gemma 4, Muse Glimmer) | FLUX.2, LTX video via Providers | Whisper large-v3(-turbo) | open TTS models exist; not chapter-cataloged | LTX-2.5 etc. via Providers | n/a (self-managed) (ch. 10 §10.4) |

Structural takeaway: Anthropic is text+image-in/text-out only (pair with other providers for
media); Gemini is the widest single-key multimodal surface; on Bedrock and OpenRouter modality is
a **per-model** property you must check, not a platform property.

### 16.2 One vision example (portable OpenAI-chat shape)

The Chat Completions image form works across OpenAI-compat surfaces (OpenRouter, Ollama `/v1`,
Gemini compat, Azure, HF router) — base64 data URLs are the lowest common denominator, since
Ollama does not fetch remote URLs (ch. 9 §9.4):

```python
import base64
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")  # or any §11 base_url
b64 = base64.b64encode(open("chart.png", "rb").read()).decode()

r = client.chat.completions.create(
    model="qwen3-vl:8b",   # swap model per provider
    messages=[{"role": "user", "content": [
        {"type": "text", "text": "Summarize this chart in two sentences."},
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
    ]}])
print(r.choices[0].message.content)
```

Anthropic-native equivalent uses an `image` content block (`{"type":"image","source":{"type":
"base64","media_type":"image/png","data":…}}`) inside the same user turn (ch. 5 §5.7).

### 16.3 One STT + TTS example (OpenAI audio endpoints; Azure exposes the same routes — ch. 7 §7.7)

```python
from openai import OpenAI
client = OpenAI()

# Speech-to-text (batch file STT)
with open("meeting.mp3", "rb") as f:
    text = client.audio.transcriptions.create(model="gpt-transcribe", file=f).text

# Text-to-speech
speech = client.audio.speech.create(model="gpt-4o-mini-tts", voice="alloy",
                                    input=text[:500])
open("summary.mp3", "wb").write(speech.read())
```

Alternatives per chapters: Gemini TTS returns base64 PCM 24 kHz/16-bit mono with 30 named voices
and up to 2 speakers (ch. 4 §4.4); realtime/conversational audio needs socket transports, not
HTTP — OpenAI Realtime (WebRTC/WS/SIP, ephemeral client secrets), Gemini Live (WSS, 16 kHz PCM in
/ 24 kHz out), Bedrock Nova 2 Sonic (ch. 3 §3.15, ch. 4 §4.4, ch. 6 §6.4). Open/self-hosted STT:
Whisper large-v3(-turbo) via HF Providers or Endpoints (ch. 10 §10.4).

### 16.4 File/PDF handling differences (recurring integration trap)

- **Gemini**: PDFs are a first-class input modality on reasoning models; File API for large
  uploads (ch. 4 §4.2, §4.7).
- **Anthropic**: PDFs go in `document` blocks (base64/URL/`file_id` via the beta Files API) and
  can drive citations; request-size cap 32 MB, files up to 500 MB (ch. 5 §5.7, §5.13).
- **OpenAI**: no PDF modality on the model itself — route documents through `file_search`
  vector stores or pre-extract text/images (ch. 3 §3.13).
- **Ollama / local**: no document type; extract text (or rasterize pages to images for a VLM)
  before the prompt (ch. 9 §9.4).
- **Azure/Bedrock**: per-model; Bedrock model cards and Azure model pages are the truth source
  (ch. 6 §6.3 "read the model card", ch. 7 §7.2).

---

## 17. Local inference setup (Ollama, HF stack) incl. Docker

### 17.1 Ollama recipes

Bare metal (ch. 9 §9.8, §9.15): `curl -fsSL https://ollama.com/install.sh | sh` (Linux/systemd),
desktop apps for macOS/Windows; configure via `systemctl edit ollama` environment overrides.

Docker Compose (GPU, from the chapter's docker/env documentation — ch. 9 §9.6, §9.15):

```yaml
services:
  ollama:
    image: ollama/ollama            # ollama/ollama:rocm for AMD
    ports:
      - "127.0.0.1:11434:11434"     # bind to localhost — the API has NO auth (ch. 9 §9.17)
    volumes:
      - ollama:/root/.ollama
    environment:
      OLLAMA_CONTEXT_LENGTH: "32768"   # default is 4096 regardless of model! (ch. 9 §9.3)
      OLLAMA_KEEP_ALIVE: "30m"
      OLLAMA_NUM_PARALLEL: "2"         # each slot reserves its own KV cache
      OLLAMA_KV_CACHE_TYPE: "q8_0"     # halves KV memory
    deploy:
      resources:
        reservations:
          devices: [{driver: nvidia, count: all, capabilities: [gpu]}]
volumes:
  ollama:
```

Then `docker exec -it <ctr> ollama pull qwen3.6:27b`. The two classic mistakes, both
chapter-documented: publishing 11434 on 0.0.0.0 without a fronting authenticated proxy (ch. 9
§9.17), and forgetting that the **default context is 4,096 tokens** with silent prompt truncation
(ch. 9 §9.3, §9.7).

### 17.2 HF stack: vLLM/SGLang for generation, TEI for embeddings (TGI is EOL)

**TGI was archived 2026-03-21**; HF's stated direction is vLLM/SGLang (+ llama.cpp/MLX locally)
(ch. 10 §10.1). Both expose OpenAI-compatible servers, so §11's thin adapter applies unchanged.

```yaml
services:
  vllm:                              # generation
    image: vllm/vllm-openai:latest   # pin a version in production
    command: ["--model", "meta-models/Muse-Glimmer-30B", "--max-model-len", "32768"]
    ports: ["127.0.0.1:8000:8000"]
    environment: {HF_TOKEN: "${HF_TOKEN}"}          # for gated repos (ch. 10 §10.6)
    volumes: ["hf-cache:/root/.cache/huggingface"]
    deploy:
      resources:
        reservations:
          devices: [{driver: nvidia, count: all, capabilities: [gpu]}]

  tei:                               # embeddings + rerankers (ch. 10 §10.13)
    image: ghcr.io/huggingface/text-embeddings-inference:1.9
    command: ["--model-id", "Qwen/Qwen3-Embedding-0.6B"]
    ports: ["127.0.0.1:8080:80"]
    volumes: ["tei-data:/data"]
volumes: {hf-cache: {}, tei-data: {}}
```

Clients: `base_url="http://localhost:8000/v1"` for vLLM chat; TEI serves `POST /embed` and
`POST /rerank` (ch. 10 §10.13). vLLM flags above are illustrative — the exact serving flags for
big MoE models come from each model card (DeepSeek/GLM cards document vLLM-first deployment,
ch. 10 §10.3). Managed middle ground: HF Inference Endpoints run vLLM/SGLang/TEI as managed
engines per instance-hour (ch. 10 §10.5).

### 17.3 Hardware sizing (consolidated from ch. 9 §9.5/§9.15 and ch. 10 §10.15 — **estimates**)

| Class (default ~4-bit quant unless noted) | Examples | Memory needed | Typical speed (community estimates, unverified) |
|---|---|---|---|
| Tiny (≤4B) | llama3.2 1B/3B, phi4-mini, gemma4 E-series | 2–6 GB | fast even on CPU |
| Small (7–9B) | qwen3.5:9b, gpt-oss-ish distills | ~8 GB VRAM | ~80–140 tok/s on RTX-4090-class; ~30–60 on M-series; 5–12 CPU-only |
| Mid (24–35B) | qwen3.6:27b (17 GB disk), qwen3-coder:30b (19 GB), muse-glimmer (18 GB), gemma4:31b (20 GB) | 24–32 GB VRAM or Apple unified memory | ~25–50 tok/s fully offloaded; "falls off a cliff" if layers spill to RAM |
| MoE low-active | gemma4:26b-a4b (3.8B act), nemotron-3.5-lightning (3B act) | total-param memory, **near-small-model speed** | MoE VRAM is set by total params, not active (ch. 10 §10.3) |
| Large (100–130B) | gpt-oss:120b (65 GB, MXFP4), qwen3.5:122b (81 GB) | one 80 GB GPU or ≥96 GB unified-memory Mac | ~30–50 tok/s (gpt-oss:120b/80 GB — estimate) |
| Frontier MoE (≥300B) | DeepSeek V4, GLM-5.2, Kimi K3 | multi-node H200-class clusters | not practical locally — use Providers/cloud tags (ch. 9 §9.2, ch. 10 §10.3) |

Add to weights: KV cache (linear in context length; halve/quarter with `q8_0`/`q4_0` KV) plus
~1–2 GB overhead; BF16 self-hosting needs ≈2 bytes/param + KV (ch. 10 §10.15). Official anchors
(the only non-estimates): gpt-oss:20b "runs on 16 GB RAM"; gpt-oss:120b "fits a single 80 GB GPU"
(ch. 9 §9.5).

### 17.4 When local wins (and when it doesn't)

**Wins:** privacy/residency — data never leaves the machine, fully offline after model download
(ch. 9 §9.16); zero marginal cost — sustained high-utilization workloads amortize hardware vs
per-token billing (break-even math is deployment-specific — generic guidance); latency — no
network hop and no rate-limit queueing for single-tenant loads; egress control is trivially
auditable (§20.3). **Loses:** frontier quality — "even the best ~35B local models trail current
hosted frontier models" (ch. 9 §9.19); high-QPS multi-user serving on Ollama (use vLLM/SGLang —
ch. 9 §9.15); compliance certifications (none published for the OSS runtime — ch. 9 §9.17);
anything needing >80 GB-class models without cluster hardware.

---

## 18. Deployment: containers, serverless, managed endpoints

### 18.1 Container pattern — proxy with key isolation

Never ship provider keys to browsers/mobile — the server-side-proxy pattern is the documented
baseline at every hosted provider (ch. 3 §3.15, ch. 4 §4.15, ch. 8 §8.15). Minimal FastAPI proxy
that injects the key, pins the model allowlist, and passes SSE through:

```python
# app.py — container-deployable proxy; the ONLY place the provider key exists
import os
import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse

UPSTREAM = "https://api.openai.com/v1/chat/completions"   # or any §11 base URL
ALLOWED_MODELS = {"gpt-5.6-terra", "gpt-5.6-luna"}
app = FastAPI()

@app.post("/v1/chat")
async def chat(req: Request):
    body = await req.json()
    if body.get("model") not in ALLOWED_MODELS:
        raise HTTPException(400, "model not allowed")
    headers = {"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"}
    client = httpx.AsyncClient(timeout=httpx.Timeout(10, read=600))

    async def relay():
        async with client.stream("POST", UPSTREAM, json=body, headers=headers) as r:
            async for chunk in r.aiter_bytes():
                yield chunk
        await client.aclose()

    return StreamingResponse(relay(), media_type="text/event-stream")
```

Express equivalent (sketch): read body → validate model → `fetch(UPSTREAM, {headers: {Authorization:
`Bearer ${process.env.OPENAI_API_KEY}`}, body})` → pipe `res.body` to the client with
`Content-Type: text/event-stream`. Add per-user authn, rate limiting and the §19 usage logging at
this choke point — it is the natural place for all three. For browser realtime audio specifically,
OpenAI's ephemeral client secrets (`POST /v1/realtime/client_secrets`) replace the proxy so
clients connect via WebRTC without the master key (ch. 3 §3.15).

### 18.2 Serverless notes — AWS Lambda and Cloud Run

Chapter-grounded: the Gemini chapter states SSE streaming pass-through works on both Cloud Run and
Lambda functions (ch. 4 §4.15); Bedrock from Lambda should use the **execution role** (no stored
secrets — ch. 6 §6.6). The rest is generic platform knowledge — kept qualitative, verify current
limits before contracting:

- **Cold start**: keep dependencies thin (raw `httpx`/`fetch` beats heavyweight SDK trees);
  provisioned concurrency (Lambda) / min-instances (Cloud Run) for latency-sensitive paths.
- **Streaming**: Lambda requires response streaming mode (Function URLs); classic
  API-Gateway-buffered Lambda breaks SSE. Cloud Run supports HTTP streaming natively. If you cannot
  stream, fall back to polling a job store.
- **Timeouts**: both platforms cap request duration well below the longest model generations
  (Lambda's ceiling is minutes, not hours). Long jobs belong in Batch APIs (50% cheaper anyway —
  §19.3) or async workers, with the function returning a job id.
- **Concurrency vs rate limits**: serverless scale-out can stampede a per-minute token quota;
  put a shared limiter (queue/semaphore) between wide fan-out and the provider.

### 18.3 Managed / reserved-capacity endpoints compared

| Offering | Unit | SLA / guarantee (as documented) | Chapter |
|---|---|---|---|
| OpenAI Scale Tier | reserved TPM units, 30-day min | 99.9% uptime + latency commitments (page listed pre-5.6 models at access) | ch. 3 §3.15, §3.17 |
| Azure Provisioned (PTU) | PTU-hour, monthly/annual reservations; spillover to Standard | 99.9% availability + per-model latency SLA on Provisioned | ch. 7 §7.15, §7.17 |
| Bedrock Provisioned Throughput | model units, 1-/6-month commitments (not combinable with inference profiles) | Bedrock SLA 99.9% [commitment tier partially verified] | ch. 6 §6.5, §6.17 |
| Gemini Priority tier | per-request `serviceTier`, ~1.8× standard | guaranteed capacity; no published SLA on this API path | ch. 4 §4.5, §4.17 |
| Anthropic | `service_tier` auto/standard_only; Fast Mode (Opus) | no published SLA verified in ch. 5 | ch. 5 §5.15, §5.17 |
| HF Inference Endpoints | instance-hour (L4 $0.80/h … H100 $10/h), autoscale 0..N | no published uptime SLA on accessed pages | ch. 10 §10.5, §10.17 |
| Ollama Cloud | subscription ($20/$100 per month) + weighted token metering | no published SLA/certs | ch. 9 §9.5, §9.17 |

Rule of thumb: pay-as-you-go until 429s or latency SLOs force the issue; then Priority-style
per-request tiers; reserved capacity (PTU/Scale Tier/Provisioned) only for sustained, predictable
load — every chapter's reserved option carries commitments measured in months.

---

## 19. Monitoring, logging, cost optimization

### 19.1 Token accounting — usage field names per provider

| Surface | Where | Input / output fields | Cache & extras |
|---|---|---|---|
| OpenAI-chat shape (OpenAI, OpenRouter, HF, Ollama `/v1`, Azure, Gemini-compat) | `usage` | `prompt_tokens` / `completion_tokens` | OpenRouter: `prompt_tokens_details.cached_tokens`, `cache_write_tokens`; exact billed cost via `GET /api/v1/generation?id=` (ch. 8 §8.5) |
| Anthropic Messages | `usage` | `input_tokens` / `output_tokens` | `cache_creation_input_tokens`, `cache_read_input_tokens`, `cache_creation.ephemeral_{5m,1h}_input_tokens`, `output_tokens_details.thinking_tokens`, `server_tool_use.*` (ch. 5 §5.7) |
| Gemini generateContent | `usageMetadata` | prompt/candidates token counts | Interactions responses carry `usage` incl. `total_cached_tokens` (ch. 4 §4.7) |
| Bedrock Converse | `usage` (in `metadata` event when streaming) | `inputTokens` / `outputTokens` / `totalTokens` | (ch. 6 §6.8–6.9) |
| Ollama native | final `done:true` object | `prompt_eval_count` / `eval_count` | durations in **nanoseconds** (`total_duration`, `load_duration`) (ch. 9 §9.7) |

Streaming caveat: usage arrives at the **end** (final chunk / `message_delta` / `metadata` event) —
a client that abandons a stream early may never see it; log at the proxy. Also note mid-stream
cancellation does not stop billing on all OpenRouter upstreams (Bedrock, Google, Groq, Mistral
complete and charge in full — ch. 8 §8.9).

### 19.2 Structured logging pattern (one JSON line per model call, at the §18 proxy)

```python
import json, time, uuid

def log_call(provider, model, usage, t0, status, request_id=None, cached_in=0):
    print(json.dumps({
        "evt": "llm_call", "id": str(uuid.uuid4()), "ts": time.time(),
        "provider": provider, "model": model, "status": status,
        "latency_ms": round((time.time() - t0) * 1000),
        "in_tokens": usage.get("in", 0), "out_tokens": usage.get("out", 0),
        "cached_in_tokens": cached_in,
        "provider_request_id": request_id,      # e.g. Anthropic request-id header (ch. 5 §5.10)
        "est_cost_usd": estimate_cost(provider, model, usage, cached_in),
    }))
```

Log prompts/completions separately (if at all) with retention and access controls matched to §20's
data policies; keep the metrics line free of content so it can flow to any log pipeline. Capture
the provider's request id — every chapter's support path starts from it. Platform-native options:
Bedrock model-invocation logging + CloudWatch/CloudTrail (ch. 6 §6.15), Azure Monitor + Agent
Service tracing (ch. 7 §7.14), AgentCore/TEI expose OTel (ch. 6 §6.14, ch. 10 §10.13).

### 19.3 Cost levers, ranked by typical impact (all multipliers chapter-verified)

1. **Prompt caching — up to ~90% off repeated input.** Cache reads ≈0.1× input across OpenAI,
   Anthropic, Gemini (0.25× on some via OpenRouter); writes cost extra on some (OpenAI 5.6 1.25×,
   Anthropic 1.25×/2× by TTL; Azure cache-write billing starts ~2026-08-21) (ch. 3 §3.5, ch. 5
   §5.5, ch. 4 §4.5, ch. 7 §7.5). Structure prompts as [stable prefix | variable tail]; hold
   breakpoints stable; on Anthropic, cache-aware rate limits also multiply effective throughput
   (ch. 5 §5.11). On OpenRouter, sticky `session_id` routing preserves hits (ch. 8 §8.5).
2. **Batching — flat 50% wherever offered.** OpenAI, Anthropic, Gemini, Bedrock, Azure Batch and
   OpenRouter `:batch` variants all document −50% for 24-h-window async work (ch. 3 §3.5, ch. 5
   §5.5, ch. 4 §4.5, ch. 6 §6.5, ch. 7 §7.5, ch. 8 §8.5). Anything not interactive belongs here.
3. **Tier routing — order-of-magnitude spread.** Route easy traffic to the small tier
   (Luna $0.10/$0.60 vs Sol $2.50/$15; Haiku $1/$5 vs Fable $10/$50; flash-lite $0.10/$0.40 —
   ch. 3/5/4 §N.2) with a cheap classifier or escalate-on-failure. Managed routers exist: Azure
   `model-router` (billed at routed model's rate — ch. 7 §7.3), `openrouter/auto` +
   `sort:"price"`/`:floor` (ch. 8 §8.7), Flex/Priority service tiers (Gemini, Bedrock).
4. **Context discipline.** Long context is where budgets die: OpenAI 5.6 bills 2×/1.5× above 272K
   input; Gemini Pro steps up above 200K; thinking tokens bill as output (Anthropic tracks them in
   `thinking_tokens`; effort knobs — `reasoning.effort`, `thinking_level`, `output_config.effort`
   — directly cut them); Anthropic's 4.7+ tokenizer yields ~30% more tokens than 4.5-era budgets
   assumed (ch. 3 §3.5, ch. 4 §4.5, ch. 5 §5.3–5.5). Trim history, cap `max_tokens`, retrieve
   instead of stuffing.

### 19.4 Simple cost-tracking snippet

```python
# $/1M tokens (input, output, cached-input) — seed from chapter §N.2/N.5 tables;
# re-verify before billing decisions (prices change; some were MEDIUM confidence).
PRICES = {
    ("openai", "gpt-5.6-terra"):     (1.00, 6.00, 0.10),
    ("openai", "gpt-5.6-luna"):      (0.10, 0.60, 0.01),
    ("anthropic", "claude-sonnet-5"): (2.00, 10.00, 0.20),
    ("anthropic", "claude-haiku-4-5"): (1.00, 5.00, 0.10),
    ("gemini", "gemini-3.7-flash"):  (0.75, 3.75, 0.075),   # promo to 2026-12-31
    ("ollama", "*"):                 (0.0, 0.0, 0.0),
}

def estimate_cost(provider, model, usage, cached_in=0):
    p_in, p_out, p_cache = PRICES.get((provider, model),
                                      PRICES.get((provider, "*"), (0, 0, 0)))
    fresh_in = max(usage.get("in", 0) - cached_in, 0)
    return (fresh_in * p_in + cached_in * p_cache + usage.get("out", 0) * p_out) / 1e6
```

For exact rather than estimated numbers: OpenRouter's `/generation` endpoint returns the actual
charge per request (ch. 8 §8.5); AWS/Azure billing exports are authoritative on those platforms
(and Azure showed a documented price-parity lag in 2026-08 — budget at billed rates, ch. 7 §7.5).

---

## 20. Security & compliance across providers

### 20.1 Key management

- **One key per app/environment, least scope**: OpenAI project-scoped keys, Anthropic
  workspace-scoped keys, HF fine-grained tokens ("create one access token per app"), Azure
  two rotatable keys per resource (ch. 3 §3.6, ch. 5 §5.6, ch. 10 §10.6, ch. 7 §7.6).
- **Prefer identity over static secrets where the platform offers it**: Bedrock IAM roles
  (instance/task/Lambda execution roles — "zero stored secrets", ch. 6 §6.6); Azure Entra ID with
  `DefaultAzureCredential`, and disable resource keys entirely for Entra-only posture (ch. 7 §7.6).
- Keys live only server-side (§18.1); browser/mobile realtime uses ephemeral client secrets
  (ch. 3 §3.15). OpenRouter BYOK concentrates all lab keys in one third party ("securely
  encrypted" per docs, 5% fee) — a convenience/blast-radius tradeoff to make consciously
  (ch. 8 §8.6).
- Rotate on schedule and on any suspected exposure; scope monitoring (§19.2) so anomalous spend
  surfaces fast — spend is usually the first leak indicator (generic guidance).

### 20.2 Data-usage policy summary (pointer table — the chapters' §17 are the record; do not rely on this summary alone)

| Provider | Documented default posture (as verified in chapter) | Detail |
|---|---|---|
| OpenAI | API data not used for training by default; abuse logs ≤30 days; Responses **stored by default** (`store:false` for stateless); ZDR by approval (vector stores/assistants ineligible) | ch. 3 §3.17, §3.7 |
| Gemini | **Free tier: inputs/outputs used for product improvement incl. human review — do not send sensitive data.** Paid tier: not used to improve products; limited abuse logging | ch. 4 §4.17 |
| Anthropic | No training on API data by default; 30-day backend deletion; ZDR by agreement (Files API not ZDR-eligible); schemas cached 24 h (no PHI in schemas) | ch. 5 §5.17 |
| Bedrock | Prompts/outputs not stored for or shared with model providers, not used to train; HIPAA-eligible/FedRAMP-High scope; global profiles process in any region (CloudTrail logs where) | ch. 6 §6.16–6.17 |
| Azure | Not available to OpenAI; not used to train; abuse-monitoring storage unless Modified Abuse Monitoring approved; content filters on by default (behavioral delta vs OpenAI direct); data at rest stays in designated geography | ch. 7 §7.16–7.17 |
| OpenRouter | No prompt logging by default (opt-in earns 1% discount); ZDR policy + per-request `zdr`/`data_collection:"deny"` routing; **`:free` endpoints often allow provider data use**; no published certifications | ch. 8 §8.17 |
| Ollama | Local: data never leaves the machine — but the local API is **unauthenticated by design**; Cloud claims no-logging/no-training, no published certs/SLA | ch. 9 §9.16–9.17 |
| Hugging Face | Providers route to partner infra — residency/retention are provider-dependent, not HF-pinned; pickle and `trust_remote_code` are code-execution risks; enterprise audit/RBAC/SSO tiers | ch. 10 §10.16–10.17 |

Certification claims (SOC 2/ISO/HIPAA) were verified only for AWS and Azure platform scopes in
the chapters; the rest were [UNVERIFIED] at access date — check each vendor's trust portal before
procurement (ch. 3/5/8/9/10 §N.17).

### 20.3 Egress control for local mode

Local inference's compliance story only holds if the box actually stays local:

- Bind Ollama to `127.0.0.1` (default) and never expose 11434 without an authenticating TLS proxy;
  firewall the port; in Docker publish `127.0.0.1:11434:11434` only (ch. 9 §9.17, §17.1 above).
- Legitimate egress is enumerable: registry pulls (`ollama.com`), hub downloads
  (`huggingface.co/...`/resolve). Route them through an egress proxy (`HTTPS_PROXY` is the
  supported knob for Ollama pulls — ch. 9 §9.6) and default-deny everything else; air-gapped
  operation works by pre-copying the models directory (ch. 9 §9.16, air-gap doc [UNVERIFIED]).
- Supply chain: pin model digests (Ollama blobs are SHA256 content-addressed but community
  namespaces are unvetted — ch. 9 §9.17); prefer safetensors, treat pickle checkpoints and
  `trust_remote_code=True` as arbitrary code execution and pin revisions (ch. 10 §10.17); keep
  the runtime patched (historical pull-path CVEs — ch. 9 §9.17).

### 20.4 Secrets-in-CI practices (generic engineering guidance)

- Use the CI system's secret store with environment/branch scoping; production keys reachable only
  from protected branches and required-review workflows. Never echo secrets; mask logs.
- Prefer **OIDC federation over static cloud keys** in CI: GitHub/GitLab OIDC → AWS IAM role
  (Bedrock) or Entra workload identity (Azure) issues short-lived credentials per job — this is
  the CI extension of the same no-static-secrets posture the chapters document for runtime
  (ch. 6 §6.6, ch. 7 §7.6).
- Tests should default to mocks or a local Ollama service container (free, no secret needed);
  gate real-API integration tests behind a manual/nightly job with a dedicated low-limit key,
  so a leaked CI key is a bounded blast radius.
- Scan for committed secrets (pre-commit hooks + repo scanning); provider key formats (`sk-proj-`,
  `hf_`, …) are pattern-matchable. Rotate immediately on any hit — assume published means
  compromised.

---

*End of Part III. Continue with Part IV (Unified Model Selection Guide, sections 21–28).*
