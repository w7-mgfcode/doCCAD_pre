# 7. Azure AI Foundry (Microsoft Foundry)

> **Volatility warning.** Model lineups and pricing change frequently. Verified against official
> documentation on **2026-08-14**. Re-verify before production decisions.

## 7.1 Platform overview & positioning

**Naming (verify-first, per directive):** At Ignite (November 2025) Microsoft renamed **Azure AI
Foundry → Microsoft Foundry**. As of 2026-08 official docs use both names interchangeably; the doc
tree moved to `learn.microsoft.com/azure/foundry` with the older portal documented under
`learn.microsoft.com/azure/foundry-classic` ("Microsoft Foundry (classic) portal"). The portal is
`ai.azure.com`. Product-Terms entries were updated January 2026
(learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure;
schneider.im/microsoft-foundry-the-new-name-for-azure-ai-foundry/; samexpert.com
/microsoft-product-terms-january-2026/, accessed 2026-08-14). "Azure OpenAI Service" survives as
the name of the OpenAI-model subset ("Azure OpenAI in Microsoft Foundry Models") and of the
pricing page.

Foundry is Microsoft's managed multi-vendor model platform. Its catalog splits into two legally
distinct groups (models-sold-directly-by-azure + models-from-partners docs, accessed 2026-08-14):

```
Microsoft Foundry
├── Foundry Models SOLD DIRECTLY BY AZURE   ← Microsoft's own product terms, Azure billing,
│    Azure OpenAI (GPT-5.x era, audio,        Azure data-privacy commitments apply.
│    image, video), Microsoft Phi/MAI,        "Models do NOT interact with services operated
│    DeepSeek, Meta Llama, xAI Grok,          by the model's provider."
│    Mistral (subset), FLUX (BFL), Cohere
├── Models from PARTNERS & COMMUNITY        ← "Non-Microsoft Products"; Azure Marketplace
│    Anthropic Claude 5/4.x, Mistral,         billing; provider sets license + price.
│    Cohere, NTT tsuzumi, Stability, ...      Serverless (Global Standard / Data Zone) or
│                                             managed compute.
└── Foundry Local / managed compute / Foundry Labs (edge + BYO-GPU + research)
```

Differentiation vs OpenAI direct (the sibling chapter): same OpenAI model weights and (since the
v1 API) near-identical wire format, but **Azure-side deployment model** (you create named
*deployments* of a model version inside a Foundry/Azure OpenAI resource), Azure quotas per
subscription, Entra ID auth/RBAC, data-zone/regional data-processing options, Azure Marketplace
procurement, an uptime **and** PTU latency SLA, and Azure compliance scope. Azure-specific prices
can lag OpenAI's (see 7.5).

## 7.2 Current model catalog

Authoritative list: **"Foundry Models sold directly by Azure"**
(learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure,
last updated 2026-07-23, accessed 2026-08-14) plus **"Models from partners and community"**. The
table is the notable, practically usable subset (catalog is 100+ IDs). Prices: USD per 1M tokens,
**Global Standard** deployment; sources in 7.5. FT = fine-tuning on Azure.

| Model (deployment name) | Family | Context | Max out | Modalities in/out | Tools | Struct. out | FT | $ in / $ out per 1M |
|---|---|---|---|---|---|---|---|---|
| `gpt-5.6-sol` | GPT-5.6 | 1,050,000 (922K in) | 128K | text+image / text | Y | Y | N | 5.50 / 33.00¹ |
| `gpt-5.6-terra` | GPT-5.6 | 1,050,000 | 128K | text+image / text | Y | Y | N | 2.75 / 16.50¹ |
| `gpt-5.6-luna` | GPT-5.6 | 1,050,000 | 128K | text+image / text | Y | Y | N | 1.10 / 6.60¹ |
| `gpt-chat-latest` (preview) | GPT-chat | 128K | 16,384 | text / text | Y | Y | N | [UNVERIFIED] |
| `gpt-5.5` | GPT-5.5 | 1,050,000 | 128K | text+image / text | Y | Y | N | [UNVERIFIED] |
| `gpt-5.4` | GPT-5.4 | 1,050,000 | 128K | text+image / text | Y | Y | N | 2.50 / 15.00 (ext-ctx 5.00 / 22.50) |
| `gpt-5.4-pro` | GPT-5.4 | 1,050,000 | 128K | text+image / text | Y | Y | N | 30.00 / 180.00 |
| `gpt-5.4-mini` | GPT-5.4 | 400K (272K in) | 128K | text+image / text | Y | Y | N | [UNVERIFIED] |
| `gpt-5.4-nano` | GPT-5.4 | 400K | 128K | text / text | Y | Y | N | [UNVERIFIED] |
| `gpt-5.3-codex` / `gpt-5.2-codex` | Codex | 400K | — | text+image / text | Y | Y | N | [UNVERIFIED] |
| `gpt-5` (2025-08-07) | GPT-5 | 400K | 128K | text+image / text | Y | Y | Y (RFT, gated) | [UNVERIFIED] |
| `gpt-oss-120b` / `-20b` (preview) | gpt-oss | 131,072 | — | text / text | Y | Y | Y (20b SFT) | [UNVERIFIED] |
| `model-router` | Router | routes | routes | text(+image) / text | Y | Y | N | billed at routed model's rate |
| `o4-mini` / `o3` / `o3-pro` | o-series | 200K in/100K out | 100K | text(+image) / text | Y | Y | o4-mini RFT | [UNVERIFIED] |
| `gpt-4.1` / `-mini` / `-nano` | GPT-4.1 | 1,047,576 | 32,768 | text+image / text | Y | Y | Y (SFT/DPO) | [UNVERIFIED] |
| `computer-use-preview` | CUA | 8,192 | 1,024 | screen+text / actions | Y | N | N | [UNVERIFIED]; gated |
| `text-embedding-3-large` | Embeddings | 8,192 in | 3,072-d | text / vector | — | — | N | [UNVERIFIED] |
| `text-embedding-3-small` | Embeddings | 8,192 in | 1,536-d | text / vector | — | — | N | [UNVERIFIED] |
| `gpt-realtime-2.1` / `-mini` (2026-07-07) | Audio | 32K in/4K out | 4K | speech+text / speech+text | Y | N | N | token-billed, [UNVERIFIED] |
| `gpt-live-transcribe` (2026-07-29) | Audio | 32K in | — | speech / text | — | — | N | duration-billed, [UNVERIFIED] |
| `gpt-image-2`, `gpt-image-1.5` | Image | 4,000 chars | image | text+image / image | — | — | N | [UNVERIFIED]; 1.5 gated |
| `sora-2`, `sora` | Video | 4,000 chars | video | text/image/video / video | — | — | N | [UNVERIFIED] |
| `Phi-4` family (see 7.3) | Phi | 16K–128K | — | text(+image+audio) / text | varies | varies | N | MIT open weights; MaaS PAYG [UNVERIFIED] |
| `Phi-4-Reasoning-Vision` (15B) | Phi | [UNVERIFIED] | — | text+image / text | [UNVERIFIED] | — | N | [UNVERIFIED] |
| `DeepSeek-V4-Pro` | DeepSeek | 1,000,000 | 384K | text / text (reasoning) | Y | JSON | N | 2.00 / 8.00³ |
| `DeepSeek-V4-Flash` | DeepSeek | 1,000,000 | 384K | text / text (reasoning) | Y | JSON | N | 0.20 / 0.80³ |
| `DeepSeek-V3.2` / `-Speciale` | DeepSeek | 128K | 128K | text / text | Y | JSON | N | [UNVERIFIED] |
| `Llama-4-Maverick-17B-128E-Instruct-FP8` | Llama 4 | 1,000,000 | 1,000,000² | text+image / text | Y | Y | N | [UNVERIFIED] |
| `Llama-3.3-70B-Instruct` | Llama 3.3 | 128K | 8,192 | text / text | Y | Y | Y (SFT) | [UNVERIFIED] |
| Grok 4.2 (GA 2026-03-30) | xAI Grok | [UNVERIFIED] | — | text / text | Y | [UNVERIFIED] | N | [UNVERIFIED]³ |
| `Mistral-medium-2505`, `Codestral-2501`, `Ministral-3B` | Mistral | 128K / 262K / — | — | text / text | Y | Y | Ministral-3B SFT | [UNVERIFIED] |
| `claude-opus-5`, `claude-sonnet-5`, `claude-haiku-4-5` (partner) | Claude | up to 1M | up to 128K | text+image / text | Y | varies | N | [UNVERIFIED on Azure] |
| `Cohere-embed-v-4-0` | Embeddings | 512 tok + 2MP img | 256–1536-d | text+image / vector | — | — | N | [UNVERIFIED] |
| `FLUX.2-pro`, `FLUX.2-flex` (BFL) | Image | 32K prompt | image | text+image / image | — | — | N | [UNVERIFIED] |

¹ Rates actually billed on Azure as of 2026-08 per a Microsoft Q&A thread; OpenAI announced cuts
2026-07-30 (Luna −80%, Terra −20%) and Microsoft stated parity "effective August 1st", but
customers reported still being billed at the rates above mid-August
(learn.microsoft.com/en-us/answers/questions/5962521/, accessed 2026-08-14). A third-party tracker
already lists the reduced rates (Sol 5.00/30.00, Terra 2.00/12.00, Luna 0.20/1.20;
nops.io/blog/azure-ai-foundry-pricing/, accessed 2026-08-14). Re-verify at billing time.
² 1M max output as printed in the official model table — anomalous; re-verify.
³ Third-party (nops.io) figures; nops lists "Grok 4.5" and "DeepSeek-V4" prices — Grok 4.5 not yet
confirmed in Microsoft docs (Grok 4.2 GA per devblogs.microsoft.com/foundry/whats-new-in-microsoft-foundry-mar-2026/).

Also in catalog, not tabled: GPT-5.1/5.2/5.3 series tail, GPT-4o line, `codex-mini`, whisper/tts,
`gpt-4o-transcribe-diarize`, `gpt-realtime-translate`/`-whisper` (duration-billed), MAI-Image /
MAI-Thinking / MAI-Voice (via Speech), healthcare models, NVIDIA Nemotron (GA 2026-03), Fireworks
AI collection (DeepSeek V3.2, Kimi K2.5, MiniMax M2.5, preview), NTT `tsuzumi-7b`, Cohere
Command A / rerank v4.0. Sources: models-sold-directly-by-azure, models-from-partners, Foundry
March-2026 blog (accessed 2026-08-14).

## 7.3 Model details & limitations

**GPT-5.6 (sol / terra / luna)** — current flagship trio (training data June 2026): 1,050,000
context (922K input cap), 128K output, reasoning, Responses + Chat Completions, structured
outputs, computer use, and "multi-agent" orchestration capability. Token budget is shared: input +
reasoning + output all draw on the same window; e.g. on the 5.5/5.6-class Responses API a
921,549-token prompt leaves only ~451 tokens of generation (formula: available_generation =
922,000 − prompt_tokens). Default quota only for tenants in quota Tiers 5–6; others must request
(models-sold-directly-by-azure, accessed 2026-08-14).

**gpt-chat-latest (preview)** — continuously updated consumer-style chat alias (snapshots
2026-06-24 etc.), 128K/16,384. Preview: auto-upgrades, not for production pinning.

**GPT-5.5 / GPT-5.4 line** — GPT-5.5 (2026-04-24): 1.05M/128K. GPT-5.4 GA 2026-03-05 with
integrated computer use; `-pro` for maximum analysis depth; `-mini`/`-nano` at 400K (272K input)
for classification/extraction (Foundry Mar-2026 blog, accessed 2026-08-14).

**Codex line** (`gpt-5.3-codex`, `gpt-5.2-codex`, `gpt-5.1-codex[-mini|-max]`, `gpt-5-codex`) —
Responses-API-only coding models for Codex CLI / VS Code; `gpt-5.1-codex-max` supports
`reasoning_effort: xhigh`. **Reasoning gotcha:** `gpt-5.1`+ default `reasoning_effort` is `none`
— set it explicitly; reasoning models reject `temperature`/`top_p`.

**GPT-4.1 known issue** — documented failure with tool definitions >300K tokens even inside the
1M window (`context_length_exceeded` / `string_above_max_length` on Chat Completions; HTTP 500 on
Responses). Provisioned GPT-4.1 deployments cap context at 128K (spillover available).

**gpt-oss-120b/20b** — OpenAI open-weight (Apache-2.0), preview on Foundry; 20b runs on managed
compute and **Foundry Local** (on-device); 20b is SFT-fine-tunable (preview).

**model-router** — GA 2025-08; a deployable meta-model that auto-selects the underlying chat
model (supports GPT-5 series); you pay the routed model's price.

**Microsoft Phi (current state)** — Phi-4 generation is current: `Phi-4` (14B-class reasoning/math
SLM), `Phi-4-mini-instruct`, `Phi-4-multimodal-instruct` (text+image+audio in), `Phi-4-reasoning`,
`Phi-4-mini-reasoning`, and **Phi-4-Reasoning-Vision 15B** (announced 2026-03-04, multimodal
chain-of-thought). MIT-licensed open weights; run serverless (MaaS PAYG), on managed compute, via
Hugging Face/Ollama, or on-device via Foundry Local. No Phi-5 announced as of 2026-08-14
[UNVERIFIED beyond absence in docs]. Microsoft first-party **MAI** models (MAI-Image,
MAI-Thinking; MAI-Voice-1/MAI-Transcribe via Speech) now sit alongside Phi
(azure.microsoft.com/en-us/products/phi; techcommunity.microsoft.com Phi-4-Reasoning-Vision post;
models-sold-directly-by-azure, accessed 2026-08-14).

**Third-party highlights** — DeepSeek-V4-Pro/Flash: 1M context, 384K output reasoning models sold
directly by Azure (Azure privacy terms apply; weights never talk to DeepSeek). Llama-4-Maverick
17B-128E FP8: 1M-context multimodal. Grok 4.2 GA 2026-03-30. Mistral: Medium 2505 / Codestral
2501 / Ministral-3B (partner, Marketplace-billed). **Anthropic Claude** (opus-5, sonnet-5,
fable-5/mythos-5, 4.x tail) is listed as a partner model, hosted "on Azure or Anthropic
infrastructure" — different privacy posture than Azure-direct models; check terms
(models-from-partners, accessed 2026-08-14).

## 7.4 Embedding / audio / vision / video models

- **Embeddings**: `text-embedding-3-large` (3,072-d), `-small` (1,536-d), both 8,192-token input,
  `dimensions` parameter supported; `text-embedding-ada-002` legacy. Limits: 2,048 array items and
  300K tokens per request. Cohere `embed-v-4-0` (Matryoshka 256–1536-d, text+image) as
  alternative. (models-sold-directly-by-azure; quotas-limits, accessed 2026-08-14.)
- **Audio**: current recommended stack is `gpt-realtime-2.1`/`-2.1-mini` (2026-07-07,
  speech-to-speech, improved silence/noise handling), `gpt-audio-1.5` (2026-02-23, audio gen),
  `gpt-live-transcribe` (2026-07-29, recommended streaming STT), `gpt-realtime-translate` and
  `gpt-realtime-whisper` (2026-05-06). Billing split: translate/whisper/live-transcribe are
  **duration-billed**, the rest token-billed. File STT: `whisper`, `gpt-transcribe`,
  `gpt-4o-transcribe(-diarize)` (25 MB cap). TTS: `tts(-hd)`, `gpt-4o-mini-tts`. Realtime API has
  WebRTC (2025-04) and SIP telephony (2025-10) transports.
- **Image**: `gpt-image-2`, `gpt-image-1.5` (limited access, high input-fidelity editing, ≤
  1024×1536), `gpt-image-1(-mini)`; BFL `FLUX.2-pro`/`FLUX.2-flex`/`FLUX.1-Kontext-pro` via
  `/images/generations` + `/images/edits`; MAI-Image.
- **Video**: `sora-2` (new) and `sora` (preview): text-, image- (2025-08) and video-to-video
  (2025-09) generation.

## 7.5 Pricing model & cost notes

Official price source: azure.microsoft.com/en-us/pricing/details/azure-openai/ — the page is
calculator-driven and rendered "$-" without region selection at access time (2026-08-14), so most
per-model numbers above come from Microsoft blog/Q&A posts or are [UNVERIFIED]. Structure
(verified from the pricing page + deployment-types doc):

- **Three price tiers by deployment type**: Global (cheapest) < Data Zone < Regional Standard.
  Provisioned (PTU) is capacity-priced; Batch is token-priced at **50% of Standard** with 24-h
  target turnaround. A **Priority Processing** lane (preview, 2026-03) adds a premium
  latency-sensitive tier.
- **Prompt caching**: cached input discounted (per-model %). **Note:** "Cache write charges are
  not active yet"; billing for cache writes starts **on or after 2026-08-21** — a live pricing
  change (pricing page, accessed 2026-08-14).
- **PTU (Provisioned Throughput Units)**: you buy model-agnostic PTU capacity per deployment
  (Global/Data Zone/Regional Provisioned SKUs), billed hourly, with **monthly and annual Azure
  Reservations** at substantial discounts (rates [UNVERIFIED — calculator only]). Each model has
  a minimum PTU size and tokens-per-PTU throughput table; capacity calculator in the Foundry
  portal. **Spillover** (GA 2025-08) routes overflow from a provisioned deployment to a standard
  deployment automatically.
- **GPT-5.6 parity lag**: OpenAI's 2026-07-30 cuts (Luna −80%, Terra −20%, Sol "Fast Mode")
  announced for Azure "effective August 1st" but billing still at old rates mid-August per
  customer reports — budget at old rates until invoices confirm (MS Q&A 5962521, accessed
  2026-08-14).
- **Partner models** (Claude, Mistral, Cohere, …): billed via **Azure Marketplace** at
  provider-set prices; unavailable on free/student/CSP subscriptions.
- **Fine-tuned model hosting** is charged per-hour while deployed (≈$120/day per third-party
  estimate, [UNVERIFIED official rate]); Developer-tier deployments avoid hosting cost but
  expire after 24 h.
- Agent Service: prompt agents = inference + tool usage; hosted agents add container compute
  (agents/overview, accessed 2026-08-14).

## 7.6 Authentication & environment

Two mechanisms on every Foundry/Azure OpenAI resource:

1. **API keys** — two rotatable keys per resource; sent as `api-key: $AZURE_OPENAI_API_KEY`
   header (legacy dated API) or as bearer/`api_key` in the v1 API.
2. **Microsoft Entra ID (recommended)** — RBAC roles (`Cognitive Services OpenAI User`/
   `Contributor`, `Azure AI User`) on the resource; tokens via `azure-identity`
   `DefaultAzureCredential` (supports managed identity, workload identity, CLI login). Token
   scope for the v1 API: `https://ai.azure.com/.default` (older docs:
   `https://cognitiveservices.azure.com/.default`). Keys can be disabled resource-wide for
   Entra-only posture (api-version-lifecycle doc, accessed 2026-08-14).

```bash
export AZURE_OPENAI_API_KEY="$API_KEY"            # if using keys
export OPENAI_BASE_URL="https://YOUR-RESOURCE.openai.azure.com/openai/v1/"
export OPENAI_API_KEY="$AZURE_OPENAI_API_KEY"     # lets plain OpenAI() client work unchanged
```

Agent-side auth adds Entra **Agent Identity**, managed identity, and OAuth identity passthrough
for MCP tools (Foundry Mar-2026 blog).

## 7.7 API endpoints & schemas

**Current scheme — v1 API (GA since 2025-08):** no `api-version` parameter; continuous feature
delivery; plain `openai` clients work.

```
Base URLs (both valid):
  https://<resource>.openai.azure.com/openai/v1/
  https://<resource>.services.ai.azure.com/openai/v1/

Main endpoints under the base:
  POST /responses               ← primary (Responses API; agents build on it)
  POST /chat/completions
  POST /embeddings
  POST /images/generations | /images/edits
  POST /audio/transcriptions | /audio/speech ; WS/WebRTC /realtime
  POST /batches ; /files ; /fine_tuning/jobs ; /evals
```

Key Azure difference vs OpenAI direct: `model` refers to your **deployment name** (which you
chose at deployment time), not necessarily the upstream model id. Preview features are opted into
via headers (e.g. `"aoai-evals": "preview"` historically) or `/alpha/` path segments instead of
dated api-versions. **Legacy scheme** (still supported): `https://<resource>.openai.azure.com/
openai/deployments/<deployment>/chat/completions?api-version=2024-10-21` with `AzureOpenAI()`
clients — migrate off it. OpenAPI 3.0 spec: github.com/Azure/azure-rest-api-specs
`.../OpenAI.v1/azure-v1-v1-generated.json`. (api-version-lifecycle, accessed 2026-08-14.)
Request/response JSON bodies are wire-identical to OpenAI's Responses/Chat Completions schemas
plus Azure extensions (`content_filter_results`, On Your Data `data_sources`).

## 7.8 SDK integration

**Python (openai ≥1.x, v1 API):**

```python
import os
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://ai.azure.com/.default")

client = OpenAI(
    base_url="https://YOUR-RESOURCE.openai.azure.com/openai/v1/",
    api_key=token_provider)                    # or api_key=os.environ["AZURE_OPENAI_API_KEY"]

resp = client.responses.create(model="gpt-5.4",          # deployment name
                               input="Summarize RFC 9110 in 3 bullets.")
print(resp.output_text)
```

**JavaScript/TypeScript (openai pkg):**

```javascript
import OpenAI from "openai";
const client = new OpenAI({
  baseURL: "https://YOUR-RESOURCE.openai.azure.com/openai/v1/",
  apiKey: process.env.AZURE_OPENAI_API_KEY,   // or Entra bearer via @azure/identity
});
const r = await client.responses.create({ model: "gpt-5.4", input: "Hello" });
console.log(r.output_text);
```

**curl:**

```bash
curl "https://YOUR-RESOURCE.openai.azure.com/openai/v1/responses" \
  -H "Authorization: Bearer $AZURE_OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-5.4","input":"ping"}'
```

**Azure-native SDKs:** `azure-ai-projects` 2.0.x (Python, 2026-03; bundles `openai` +
`azure-identity`, constructor-level `allow_preview=True`, agents unified under
`AIProjectClient`), `@azure/ai-projects` 2.0.x (JS), `Azure.AI.Projects` 2.0 (.NET, GA
2026-04-01), `azure-ai-projects` 2.0 Java (first stable, 2026-03-27). Use these for
projects/agents/evals/connections; use the `openai` client for raw inference. (Foundry Mar-2026
blog, accessed 2026-08-14.)

## 7.9 Streaming, tool use, structured output

```python
# Streaming (Responses API)
with client.responses.stream(model="gpt-5.4", input="Write a haiku") as stream:
    for event in stream:
        if event.type == "response.output_text.delta":
            print(event.delta, end="")

# Tool use
tools = [{"type": "function", "name": "get_weather",
          "parameters": {"type": "object",
                         "properties": {"city": {"type": "string"}},
                         "required": ["city"]}}]
r = client.responses.create(model="gpt-5.4", input="Weather in Oslo?", tools=tools)
# → r.output contains a function_call item; execute, then send
#   {"type":"function_call_output","call_id":..., "output":...} in a follow-up call.

# Structured output (JSON schema)
r = client.responses.create(
    model="gpt-5.4", input="Extract: 'Ada, 36, Oslo'",
    text={"format": {"type": "json_schema", "name": "person", "strict": True,
          "schema": {"type": "object", "properties": {
              "name": {"type": "string"}, "age": {"type": "integer"},
              "city": {"type": "string"}},
              "required": ["name", "age", "city"], "additionalProperties": False}}})
```

Shapes match the OpenAI Responses API (wire-compatible per Foundry Agent Service docs); verified
against the v1 lifecycle doc's client pattern, not re-tested per-parameter — treat the
`text.format` block as OpenAI-current. Reasoning models: use `reasoning: {"effort": "high"}`
(Responses) / `reasoning_effort` (Chat Completions); remember `gpt-5.1`+ defaults to `none`.

## 7.10 Error handling & retry

| HTTP | Azure meaning | Action |
|---|---|---|
| 400 `content_filter` | Prompt blocked by content filter (see 7.17); details in `content_filter_results` | Don't retry unchanged; surface policy error |
| 401 | Bad key / missing token | Fix auth; check key not disabled |
| 403 | Entra RBAC denied / network (VNet, private endpoint) rules | Assign `Azure AI User` role; check firewall |
| 404 `DeploymentNotFound` | Deployment name wrong or not yet propagated | Verify deployment name (not model id) |
| 408/5xx | Transient | Retry with backoff |
| 429 | TPM/RPM exceeded, **or monthly usage-tier exceeded, or regional capacity strain** | Honor `Retry-After`; exponential backoff; consider PTU/spillover |

Streaming responses can terminate with `finish_reason: "content_filter"` mid-stream — always
check `finish_reason`. Filtered completions return `finish_reason:"content_filter"` instead of
`stop`. Retry pattern: exponential backoff w/ jitter (docs show `tenacity`), gradual ramp-up, and
quota-increase request at aka.ms/oai/stuquotarequest (quotas-limits; content-filter docs,
accessed 2026-08-14).

## 7.11 Rate limits & quotas

Model changed materially on **2026-05-07** (quotas-limits doc, accessed 2026-08-14):

- **Subscription-scoped pools**: Global Standard quota for a model/version is one pool across all
  regions per subscription; Data Zone Standard pools per data zone. Deployments share the pool
  (no per-deployment carve-out).
- **7 quota tiers** (Free, 1–6) assigned per subscription from usage, EA/MCA-E relationship, and
  payment history; **auto-upgrade** as you approach limits (opt-out via
  `quotaTiers` PATCH `tierUpgradePolicy: NoAutoUpgrade`,
  api-version `2025-10-01-preview`). GPT-5.6/5.5 default quota only at Tiers 5–6.
- Sample Tier-1 defaults: `gpt-5` Global Standard 10K RPM / 1M TPM; `gpt-4o-mini` 20K RPM / 2M
  TPM; `o3-mini` 5M TPM.
- **Usage tiers** (2026): per-tenant *monthly* token ceilings per model (e.g. gpt-5 32B,
  gpt-5.1 86B, gpt-5.4 50B, gpt-4o-mini 85B tokens/month); exceeding them brings latency
  variability and 429s even under TPM. Standard-family only (not Batch/PTU).
- **Batch quota** in enqueued tokens (e.g. gpt-5: 5B Enterprise / 200M default / 50M credit-card);
  file limits 200 MB (1 GB BYOS), 100K requests/file.
- Resource limits: 30 Azure OpenAI resources/subscription, 32 standard deployments/resource,
  embeddings ≤2,048 inputs & ≤300K tokens/request.

## 7.12 Fine-tuning & customization

Methods: **SFT**, **DPO**, **RFT** (fine-tuning table in models-sold-directly-by-azure, accessed
2026-08-14). Current matrix (GA unless noted): `gpt-4.1`/`-mini`/`-nano` (SFT+DPO), `gpt-4o`,
`gpt-4o-mini` (SFT[/DPO]), `o4-mini` (RFT), **`gpt-5` (RFT, invitation-gated)**; preview:
`Ministral-3B`, `Qwen-32B`, `Llama-3.3-70B-Instruct`, `gpt-oss-20b` (SFT, Global-only).
Training location options: **regional** (North Central US, Sweden Central, East US2 typical),
**Global Training** (cheaper, no residency guarantee), **Developer tier** (evaluation-only
deployments, 24-hour lifetime, no SLA). Limits: ≤720 h/job, ≤2B training tokens. Hosted
fine-tuned deployments: ≤10/resource, billed hourly while deployed. A Fine-Tuning CLI with cost
estimation shipped 2026-03. Stored Completions API captures production traffic for distillation/
eval sets. Prices per-model on the pricing calculator [UNVERIFIED here].

## 7.13 RAG & embedding pipeline notes

Canonical Azure pattern: `text-embedding-3-*` (or Cohere embed v4) → **Azure AI Search**
(vector + hybrid + semantic ranker) → grounded generation, either client-side, via the **On Your
Data** `data_sources` extension, or via Agent Service **File search** tool (managed chunking/
embedding/vector store). Groundedness detection content filter (streaming, select regions:
Central US, East US, France Central, Canada East) can flag ungrounded claims at generation time.
Batch API at 50% is well suited to corpus embedding; mind the 300K-token/request embeddings cap
and 2,048-item array cap. Third-party cost anchor for a typical production RAG stack: AI Search
$150–300/mo (nops.io, third-party, accessed 2026-08-14).

## 7.14 Agent support

**Microsoft Foundry Agent Service** (GA; formerly "Azure AI Agent Service") — built **on the
Responses API, wire-compatible with OpenAI agents** (agents/overview, updated 2026-06-02; Foundry
Mar-2026 blog, accessed 2026-08-14):

- **Prompt agents** (fully managed, declarative) and **hosted agents** (your code — Microsoft
  Agent Framework, LangGraph, OpenAI Agents SDK, Anthropic SDK — run in managed containers).
- Tools: web search (preview), file search, code interpreter, memory (preview), custom functions,
  **MCP servers** (remote + Azure Functions; centrally managed versioned "Toolbox"); MCP auth via
  key, Entra Agent Identity, managed identity, OAuth passthrough. **A2A protocol** in preview.
- Non-OpenAI models supported (DeepSeek, Llama, xAI, etc.). Each agent can get its own **Entra
  Agent Identity**; BYO-VNet end-to-end private networking (2026-03); tracing GA, Evaluations GA
  with continuous monitoring to Azure Monitor; guardrails incl. Task Adherence and tool-call/
  tool-response intervention points plus third-party (Prisma AIRS, Zenity) integrations.
- Distribution to Teams / M365 Copilot / Entra Agent Registry. Pricing: inference + tool usage
  (+ container compute for hosted).
- The old **Assistants API** remains preview-only for legacy gpt-4o versions in select regions —
  treat as legacy (see 7.18).

## 7.15 Deployment patterns

Deployment-type matrix (deployment-types doc, accessed 2026-08-14):

| Type (SKU) | Processing | Billing | Notes |
|---|---|---|---|
| Global Standard (`GlobalStandard`) | any Azure region | per-token | Default; new models land here first; biggest quota |
| Data Zone Standard (`DataZoneStandard`) | within US / EU / APAC zone | per-token | Residency middle ground |
| Standard (`Standard`) | single region | per-token | Regional compliance; fewer models |
| Global Provisioned (`GlobalProvisionedManaged`) | any region | PTU-hour / reservation | Guaranteed throughput + latency SLA |
| Data Zone Provisioned (`DataZoneProvisionedManaged`) | zone | PTU | |
| Regional Provisioned (`ProvisionedManaged`) | region | PTU | Limited regions |
| Global / Data Zone Batch (`GlobalBatch`/`DataZoneBatch`) | any / zone | −50% tokens | 24-h target, no realtime SLA |
| Developer (`DeveloperTier`) | any | per-token | FT evaluation only; 24-h life; no SLA |

Beyond serverless: **managed compute** (dedicated VMs for open/community models incl. BYO
weights via Fireworks collection), **Foundry Local** (on-device/edge runtime — e.g.
`gpt-oss-20b`, Phi), **spillover** PTU→Standard, **Model Router** for cost-routing, and
**Priority Processing** (preview). Control plane: Foundry Control Plane ARM API (2026-03) unifies
agents/models/tools management.

## 7.16 Region availability & data residency

Approach: availability is **per model × per deployment type**, enumerated in "Region availability
for Foundry Models sold by Azure" — always check that page, not marketing region lists. ~27+
regions carry Standard SKUs (Australia East … West US3); fine-tuning restricted to a handful
(North Central US, Sweden Central, East US2 + Global). Data zones: **US**, **EU** (and APAC per
deployment-types doc). Documented residency commitments (data-privacy legal doc, updated
2026-05-18, accessed 2026-08-14): **data at rest always stays in the customer-designated
geography** for every deployment type; *processing* location varies — Global = any Azure region,
Data Zone = within zone, Standard/Regional Provisioned = in-region. Abuse-monitoring stores are
kept in the resource's geography; EEA resources get EEA-located human reviewers. Azure Government
has separate docs/filters.

## 7.17 Security, compliance & SLA

- **Data privacy (documented commitments):** prompts/completions are not available to OpenAI or
  other model providers, not used to train foundation models, models are stateless;
  fine-tuning data never trains base models. Flagged content may be stored for human abuse
  review (geography-local, SAW + JIT access); **Modified Abuse Monitoring** opt-out removes
  storage/human review (automated review remains) — verify via the `ContentLogging:false`
  resource attribute. AES-256 at rest, CMK optional
  (learn.microsoft.com/en-us/legal/cognitive-services/openai/data-privacy, accessed 2026-08-14).
- **Content filtering / Responsible AI layer** (Azure AI Content Safety, on by default for
  Azure-direct models; Whisper exempt): hate/sexual/violence/self-harm at 4 severity levels
  (default blocks low+), Prompt Shields (jailbreak + indirect injection, incl. spotlighting),
  Protected Material text/code, PII detection (2025-10), Groundedness (streaming, select
  regions), blocklists; **modified/disabled filters require Microsoft approval**
  (ncv.microsoft.com form); request-level filter configs supported. 2026 UI: "Guardrails +
  controls" in the portal; agent-specific Task Adherence and tool-call guardrails
  (content-filter doc, accessed 2026-08-14). This filtering layer is a real behavioral delta vs
  OpenAI direct: identical models can refuse/400 differently on Azure.
- **SLA:** Microsoft publishes SLAs for online services at
  microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services. For Azure
  OpenAI/Foundry Models: **99.9% monthly availability**, credits 10%/25% below 99.9%/99%; plus a
  **latency SLA for Provisioned deployments** (99% of 5-min windows meeting per-model
  tokens-per-second floors, e.g. 25 t/s on gpt-4o) — figures corroborated via third-party SLA
  analysis (redresscompliance.com/azure-openai-sla-and-support, accessed 2026-08-14); confirm
  exact current text in the licensing document before contracting. Batch and Developer tiers:
  no SLA.
- **Compliance:** Azure platform certification portfolio (ISO 27001/27017/27018, SOC 1/2/3,
  HIPAA BAA, FedRAMP High for Azure Government, EU Data Boundary) applies per the Microsoft
  Trust Center / Service Trust Portal; per-service scope statements there [specific per-cert
  scope for Foundry not re-verified here].

## 7.18 Legacy models & migration notes

- **API**: dated `api-version` scheme + `AzureOpenAI()` clients → migrate to **v1** base URL +
  plain `OpenAI()` clients (7.7). Assistants API (preview, legacy gpt-4o/gpt-4/3.5 only, 11
  regions) → **Responses API / Agent Service**.
- **Models**: GPT-4o/4.1/o1/o3 generations remain deployable but are pre-GPT-5-era; GPT-4.5
  Preview, o1-preview, gpt-3.5-turbo, DALL-E 3, ada-002 are legacy — consult "model retirements"
  page for dates (not re-verified). Preview-tagged models auto-upgrade and are unfit for
  production pinning.
- **Platform**: Azure AI Studio → Azure AI Foundry (2024) → Microsoft Foundry (2025-11); classic
  portal/docs live under `/azure/foundry-classic`. **PromptFlow deprecated** (migrate to
  Framework Workflows by 2027-04-20); Azure ML "Import Data" connections and low-priority VMs
  deprecated 2026-03; new managed VNets lose default internet egress after 2026-03-31 (Foundry
  Mar-2026 blog, accessed 2026-08-14).

## 7.19 Task-suitability verdict

**Best when:** you want OpenAI's current frontier line (GPT-5.6 sol/terra/luna, Codex, realtime
audio, Sora 2) under Azure governance — Entra ID/RBAC, VNet privacy, data-zone processing,
uptime + PTU-latency SLA, Marketplace procurement; enterprise agent platforms (Agent Service is
the most complete managed agent runtime of the clouds surveyed: Responses-wire-compatible, MCP +
A2A, per-agent Entra identity, M365 distribution); regulated workloads needing EU/US data-zone
processing; hybrid/edge SLM deployment (Phi + Foundry Local); using DeepSeek/Grok-class models
under Microsoft's no-provider-access privacy terms.

**Worst when:** you need day-zero OpenAI price parity (documented 2-week+ lag on the 2026-07
cuts) or day-zero features (Azure trails OpenAI direct on some launches); ungated permissive
content generation (default filters + approval gates for modification add refusals and latency);
simple low-ops prototyping (resource/deployment/quota-tier machinery is heavyweight vs a single
OpenAI key); breadth of non-OpenAI frontier models (Anthropic presence is partner-tier —
Bedrock/Anthropic-direct are more natural Claude homes); predictable throughput without capacity
planning (usage tiers + tier-gated GPT-5.6 quota surprise teams at scale).

## 7.20 Sources (all accessed 2026-08-14)

1. learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure (updated 2026-07-23)
2. learn.microsoft.com/en-us/azure/ai-foundry/foundry-models/concepts/models-from-partners
3. learn.microsoft.com/en-us/azure/foundry-classic/openai/whats-new
4. learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/deployment-types
5. learn.microsoft.com/en-us/azure/ai-foundry/openai/api-version-lifecycle (updated 2026-05-13)
6. learn.microsoft.com/en-us/azure/ai-foundry/openai/quotas-limits
7. learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/content-filter
8. learn.microsoft.com/en-us/azure/ai-foundry/agents/overview (updated 2026-06-02)
9. learn.microsoft.com/en-us/legal/cognitive-services/openai/data-privacy (updated 2026-05-18)
10. learn.microsoft.com/en-us/answers/questions/5962521/pricing-of-openai-gpt-5-6-models-luna-terra (GPT-5.6 Azure pricing thread)
11. devblogs.microsoft.com/foundry/whats-new-in-microsoft-foundry-mar-2026/
12. azure.microsoft.com/en-us/pricing/details/azure-openai/ (calculator-driven; cache-write billing note)
13. azure.microsoft.com/en-us/products/phi/
14. techcommunity.microsoft.com/blog/azure-ai-foundry-blog/introducing-phi-4-reasoning-vision-to-microsoft-foundry/4499154 (2026-03-04)
15. Third-party (labeled): nops.io/blog/azure-ai-foundry-pricing/; redresscompliance.com/azure-openai-sla-and-support; schneider.im/microsoft-foundry-the-new-name-for-azure-ai-foundry/; samexpert.com/microsoft-product-terms-january-2026/
16. microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services (SLA of record; exact current text not re-fetched)
