# 6. AWS Bedrock

> **Volatility warning.** Model lineups and pricing change frequently. Verified against official
> documentation on **2026-08-14**. Re-verify before production decisions.

## 6.1 Platform overview & positioning

Amazon Bedrock is AWS's managed multi-vendor foundation-model service: a single control plane and
inference plane over models from **Anthropic, OpenAI, Amazon (Nova), Meta, Mistral AI, Cohere,
DeepSeek, Qwen, Google (Gemma), Z.AI, Moonshot AI, MiniMax, NVIDIA, xAI, AI21 Labs, Writer,
Stability AI, TwelveLabs, Luma AI** (docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html,
accessed 2026-08-14). It is not a model vendor competing on a single frontier model; it competes on
procurement (one AWS bill, one IAM boundary), data governance (prompts/outputs not used for training,
VPC endpoints, CloudTrail), and breadth.

Architecturally, Bedrock in 2026 has **two inference planes**:

```
                +--------------------------------------------+
  AWS SDK       |  bedrock-runtime.{region}.amazonaws.com    |  Converse / ConverseStream /
  (SigV4) ----->|  "classic" runtime, SigV4                  |  InvokeModel (+ stream)
                +--------------------------------------------+
                +--------------------------------------------+
  OpenAI /      |  bedrock-mantle.{region}.api.aws           |  OpenAI Responses & Chat Completions,
  Anthropic --->|  API-key or SigV4                          |  Anthropic Messages API
  SDKs          +--------------------------------------------+
```

The `bedrock-mantle` endpoint (GA 2026; console redesigned around it June 2026) exposes
**OpenAI-compatible and Anthropic-native APIs** so first-party SDKs (`openai`, `anthropic`) work
against Bedrock with a base-URL swap
(docs.aws.amazon.com/bedrock/latest/userguide/endpoints.html;
aws.amazon.com/about-aws/whats-new/2026/06/amazon-bedrock-redesigned-console-optimized-openai-anthropic-compatible-apis/,
accessed 2026-08-14). Some models are mantle-only: OpenAI's proprietary GPT-5.x line is served
**only** via the Responses API on `bedrock-mantle`, not via Converse/InvokeModel
(docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-56-sol.html, accessed 2026-08-14).

## 6.2 Current model catalog

The authoritative, continuously updated catalog is **"Models at a glance"**
(docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html) with one model-card page per model
(pattern: `.../model-card-<provider>-<model>.html`). The table below is the **notable, practically
usable subset** as of 2026-08-14 — not exhaustive (the full catalog is 110+ models across 19
providers). Prices are US-region on-demand per 1M tokens from aws.amazon.com/bedrock/pricing/ and
model cards (accessed 2026-08-14); rows marked ³ are third-party-sourced pending official
confirmation.

| Model (Bedrock ID) | Family | Context | Max out | Modalities in/out | Tool use | Structured out | FT | $ in / $ out per 1M |
|---|---|---|---|---|---|---|---|---|
| `anthropic.claude-opus-5` | Claude 5 | 1M | 128K | text+image / text | Y | Y (runtime) | N | 5.00 / 25.00 |
| `anthropic.claude-sonnet-5` | Claude 5 | 1M | 128K | text+image / text | Y | N¹ | N | 2.00 / 10.00 |
| `anthropic.claude-fable-5` | Claude 5 | [UNVERIFIED] | [UNVERIFIED] | text+image / text | Y | [UNVERIFIED] | N | 10.00 / 50.00 |
| `anthropic.claude-opus-4-8` | Claude 4 | [UNVERIFIED] | [UNVERIFIED] | text+image / text | Y | Y | N | 5.00 / 25.00 |
| `anthropic.claude-sonnet-4-6-v1` | Claude 4 | 200K | 64K³ | text+image / text | Y | Y | N | 3.00 / 15.00 |
| `anthropic.claude-haiku-4-5` | Claude 4 | 200K | 64K³ | text+image / text | Y | Y | N | 1.00 / 5.00 |
| `amazon.nova-2-lite-v1:0` | Nova 2 | 1M | 64K | text+image+video / text | Y | N | N | 0.33 / 2.75³ |
| `amazon.nova-2-sonic-v1:0` | Nova 2 | — | — | speech / speech (bidir) | Y | N | N | [UNVERIFIED] |
| `amazon.nova-pro-v1:0` | Nova 1 | 300K | 5K | text+image+video / text | Y | Y | Y | 0.80 / 3.20 |
| `amazon.nova-micro-v1:0` | Nova 1 | 128K | 5K | text / text | Y | Y | Y | 0.035 / 0.14 |
| `openai.gpt-5.6-sol` | GPT-5.6 | 1M | [UNVERIFIED] | text+image / text | Y (server-side) | N² | N | 5.50 / 33.00 (short-ctx tier) |
| `openai.gpt-5.5` | GPT-5.5 | [UNVERIFIED] | [UNVERIFIED] | text+image / text | Y | [UNVERIFIED] | N | [UNVERIFIED] |
| `openai.gpt-oss-120b-1:0` | gpt-oss | 128K³ | [UNVERIFIED] | text / text | Y | Y | Y (RFT) | [UNVERIFIED] |
| `meta.llama4-maverick-17b-instruct-v1:0` | Llama 4 | 1M | [UNVERIFIED] | text+image / text | Y | Y | N | 0.50 / 0.80³ |
| `meta.llama4-scout-17b-instruct-v1:0` | Llama 4 | 1M³ | [UNVERIFIED] | text+image / text | Y | Y | N | 0.17 / 0.36³ |
| `meta.llama3-3-70b-instruct-v1:0` | Llama 3.3 | 128K | [UNVERIFIED] | text / text | Y | Y | Y | 0.99 / 3.96⁴ |
| `mistral.mistral-large-3-v1:0` | Mistral Large 3 | 128K³ | [UNVERIFIED] | text / text | Y | Y | N | 0.50 / 1.50 |
| `mistral.pixtral-large-2502-v1:0` | Pixtral | 128K³ | [UNVERIFIED] | text+image / text | Y | Y | N | [UNVERIFIED] |
| `deepseek.v3.2` | DeepSeek | 128K³ | [UNVERIFIED] | text / text | Y | [UNVERIFIED] | N | 0.62 / 1.85 |
| `deepseek.r1-v1:0` | DeepSeek R1 | 128K | 32K³ | text / text | N³ | N³ | N | [UNVERIFIED] |
| `qwen.qwen3-32b-v1:0` | Qwen3 | [UNVERIFIED] | [UNVERIFIED] | text / text | Y | Y | N | 0.20 / 0.78 |
| `cohere.embed-v4` | Embed v4 | — | — | text+image / embedding | — | — | N | [UNVERIFIED] |
| `cohere.rerank-v3-5:0` | Rerank | — | — | text / scores | — | — | N | $2.00 per 1K queries |
| `amazon.titan-embed-text-v2:0` | Titan Embed | 8K in | — | text / embedding (256/512/1024d) | — | — | N | 0.02 / — |
| `amazon.nova-multimodal-embeddings` | Nova Embed | — | — | text+image+video / embedding | — | — | N | [UNVERIFIED] |
| `ai21.jamba-1-5-large-v1:0` | Jamba 1.5 | 256K | [UNVERIFIED] | text / text | Y | Y | N | [UNVERIFIED] |

¹ Sonnet 5 model card lists "Structured outputs: not supported" on bedrock-runtime (accessed 2026-08-14).
² GPT-5.6 Sol card: structured outputs not supported via Bedrock Responses API.
³ Third-party source (cloudprice.net / cloudzero.com / hidekazu-konishi.com catalog, accessed 2026-08-14) — verify on the official pricing page.
⁴ Fetched from aws.amazon.com/bedrock/pricing/ 2026-08-14; anomalous vs earlier published Llama 3.3 pricing — re-verify.

Also currently listed but not cataloged here: Google Gemma 4/3, NVIDIA Nemotron 3, Z.AI GLM 5/4.7,
Moonshot Kimi K2.5, MiniMax M2.x, xAI Grok 4.3, Writer Palmyra X5, TwelveLabs Marengo/Pegasus
(video understanding), Stability AI image suite, Luma AI Ray v2 (video gen), Amazon Nova
Canvas/Reel (image/video gen, gen-1 Legacy). Source: model-cards.html, accessed 2026-08-14.

## 6.3 Model details & limitations

**Anthropic Claude (flagship line on Bedrock).** Claude 5 generation (Opus 5, Sonnet 5, plus
specialty Mythos 5 / Fable 5 at $10/$50) is Active alongside a long Claude 4.x tail (Opus
4.5–4.8, Sonnet 4/4.5/4.6, Haiku 4.5). Opus 5: 1M context / 128K output, launched 2026-07-24;
Sonnet 5: 1M/128K, launched 2026-06-30. Both support prompt caching (5-min and 1-h TTL, 4
checkpoints), batch, computer use, Guardrails, Knowledge Bases, Agents; neither supports
fine-tuning on Bedrock. Claude pricing on Bedrock is **identical to Anthropic first-party list
prices**, with a **10% premium on regional/cross-region endpoints** per Anthropic's pricing page
(platform.claude.com/docs/en/about-claude/pricing, accessed 2026-08-14). Sources:
model-card-anthropic-claude-opus-5.html, model-card-anthropic-claude-sonnet-5.html (2026-08-14).

**OpenAI (new since 2025-08, proprietary line since 2026-06).** Open-weight `gpt-oss-120b/20b`
arrived 2025-08; proprietary **GPT-5.5, GPT-5.4 and Codex went GA on Bedrock 2026-06**, and the
**GPT-5.6 family (Sol/Terra/Luna)** launched 2026-07 (Sol: 2026-07-13, 1M context, us-east-1/2
in-region only, no cross-region profiles, no batch/streaming-via-Responses caveats apply). GPT-5.x
is **bedrock-mantle only** (OpenAI Responses API; Converse/InvokeModel rejected). AWS cut Luna
prices 80% and Terra 20% effective 2026-07-30 to track OpenAI first-party pricing. Sources:
aws.amazon.com/about-aws/whats-new/2026/06/amazon-bedrock-openai-models-codex-generally-available/;
.../2026/07/openai-gpt-terra-luna-pricing-bedrock/; model-card-openai-gpt-56-sol.html (2026-08-14).

**Amazon own-brand: Nova 2 is current; Titan text generation is gone.** The Titan-era text models
(Titan Text Express/Lite) no longer appear in the catalog; only **Titan embeddings and Titan Image
Generator v2** remain Active. Nova gen-1 (Micro/Lite/Pro/Premier/Canvas/Reel/Sonic) is being
sunset: Nova Premier EOL 2026-09-14, Canvas/Reel/Sonic-gen1 EOL 2026-09-30 (third-party catalog,
hidekazu-konishi.com, 2026-05 — verify per model card). Current line: **Nova 2 Lite** (1M ctx, 64K
out, text+image+video in, launched 2025-12-02, geo/global profiles only — no single-region
deployment), **Nova 2 Sonic** (bidirectional speech-to-speech), **Nova Multimodal Embeddings**.
Nova 2 Lite supports the new **Priority/Flex service tiers** (see 6.5). Source:
model-card-amazon-nova-2-lite.html (2026-08-14).

**Meta Llama.** Llama 4 Maverick/Scout (17B-active MoE, 1M context, multimodal) are current;
Llama 3.3 70B remains the dense workhorse; Llama 3.2 and 3.1 405B are Legacy-tier. Llama models
support fine-tuning on Bedrock (3.1/3.3 families).

**Mistral AI.** Mistral Large 3 (aggressively priced at $0.50/$1.50 in US regions), Pixtral Large
(vision), Ministral 3B/8B/14B edge line, Devstral 2 (code), Magistral (reasoning), Voxtral
(speech-in). One of the broadest non-US lineups on Bedrock (14 models).

**Cohere.** Pivoted on Bedrock to retrieval infrastructure: **Embed v4** (multimodal) and **Rerank
3.5** are the current models; Command R/R+ still listed but Legacy per third-party catalog.

**DeepSeek / Qwen / GLM / Kimi / MiniMax.** Bedrock added six open-weights models on 2026-02-10
(DeepSeek V3.2, MiniMax M2.1, GLM 4.7, GLM 4.7 Flash, Kimi K2.5, Qwen3 Coder Next), served through
OpenAI-compatible endpoints on mantle
(aws.amazon.com/about-aws/whats-new/2026/02/amazon-bedrock-adds-support-six-open-weights-models,
accessed 2026-08-14). DeepSeek-R1 (reasoning) has been serverless on Bedrock since 2025-03.

**AI21.** Jamba 1.5 Large/Mini (256K context hybrid SSM-transformer) — unchanged since 2024;
treat as maintenance-mode.

Known platform constraints: per-model feature matrices differ sharply (e.g., Sonnet 5 lacks
structured outputs on runtime; Nova 2 Lite lacks batch; GPT-5.6 lacks cross-region profiles) —
always read the model card before committing to a feature.

## 6.4 Embedding / audio / vision / video models

| Type | Models | Notes |
|---|---|---|
| Text embedding | `amazon.titan-embed-text-v2:0` (1024/512/256d, 8K in, $0.02/1M), Cohere Embed English/Multilingual v3 | Titan V2 is the KB default |
| Multimodal embedding | Amazon Nova Multimodal Embeddings (text/image/video), Cohere Embed v4, Titan Multimodal Embeddings G1, TwelveLabs Marengo 3.0 (video) | prices largely [UNVERIFIED] |
| Rerank | Cohere Rerank 3.5 ($2.00/1K queries), Amazon Rerank | used by KB reranking API |
| Speech | Nova 2 Sonic (speech↔speech), Voxtral Small/Mini (speech→text reasoning) | |
| Image gen/edit | Stability: SD 3.5 Large, Stable Image Core/Ultra + 13 editing primitives; Titan Image Generator v2; Nova Canvas (Legacy) | |
| Video gen | Luma AI Ray v2 (us-west-2), Nova Reel (Legacy) | |
| Video understanding | TwelveLabs Pegasus 1.2 | |

Source: model-cards.html + pricing page, accessed 2026-08-14.

## 6.5 Pricing model & cost notes

Five purchase modes (aws.amazon.com/bedrock/pricing/, accessed 2026-08-14):

1. **On-demand (Standard tier)** — per-token, per-region price lists; per-image/video for media
   models; per-query for rerank.
2. **Batch** — async JSONL jobs via S3; **50% of on-demand** across most supported text models.
3. **Provisioned Throughput** — hourly "model units" with 1-/6-month commitments; required for
   some customized models (e.g., Cohere Embed 3 listed at $7.12/h/unit). Not usable with
   cross-region inference profiles.
4. **Service tiers (new, 2026)** — per-request `serviceTier`: **Priority** (~1.75x, latency-SLO
   traffic), **Standard**, **Flex** (~50%, latency-tolerant), **Reserved** — supported model-by-model
   (e.g., Nova 2 Lite: Priority/Flex; Claude Opus 5: Standard+Batch only). Tier prices per model
   card / pricing page; third-party example for Nova 2 Lite global: 0.33/2.75 std, 0.165/1.38
   flex-batch, 0.578/4.81 priority (cloudprice.net, 2026-08-14).
5. **Prompt caching** — cache reads ≈10% of input price (Claude: writes 1.25x/2x for 5m/1h TTL,
   reads 0.1x; Nova: cache-read 0.25x [UNVERIFIED on current page]).

Cross-region pricing: geographic profiles bill at the **source-region price** (no routing
surcharge); **global profiles run ~10% cheaper** than geographic per AWS cross-region docs, while
Anthropic's page frames Bedrock regional/cross-region endpoints as a **10% premium over global**
— same delta, two framings. Guardrails billed separately: content filters $0.15/1K text units,
sensitive-info filters $0.10/1K text units, image filters $0.00075/image. Knowledge Bases: you pay
for embeddings + your vector store + retrieval-time model tokens; the KB orchestration itself has
no separate meter [structured-retrieval and reranking have their own line items — see pricing page].

## 6.6 Authentication & environment

Bedrock's default auth is **AWS IAM + SigV4 request signing** — the fundamental contrast with
API-key providers (OpenAI/Anthropic first-party):

- No static bearer key in the request; every call is signed with rotating credentials resolved
  from the standard AWS chain (env vars `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY`/
  `AWS_SESSION_TOKEN`, `~/.aws/credentials` profiles, or — preferred in production — **IAM roles**
  (EC2 instance profile, ECS/EKS task role via IRSA/Pod Identity, Lambda execution role) with zero
  stored secrets.
- Authorization is IAM policy on actions (`bedrock:InvokeModel`, `bedrock:InvokeModelWithResponseStream`,
  `bedrock:Converse*`) and resources (model ARNs, inference-profile ARNs — a cross-region profile
  requires permission on the profile **and** the underlying regional model ARNs; SCPs must allow
  destination regions, or `"aws:RequestedRegion": "unspecified"` for global profiles).
- Model access must be **enabled per model per account** in the console/API before first use
  (`AccessDeniedException` otherwise).

Since 2025-07 Bedrock also issues **Bedrock API keys** (short-term ~12h, and long-term IAM-user
backed) for the mantle endpoint and SDK compatibility: `x-api-key: $AWS_BEARER_TOKEN_BEDROCK` /
`OPENAI_API_KEY=<bedrock-api-key>` — lowering the onboarding gap with API-key providers
(docs.aws.amazon.com/bedrock/latest/userguide/inference-messages-api.html, accessed 2026-08-14).
Minimal IAM policy:

```json
{"Version":"2012-10-17","Statement":[{"Effect":"Allow",
  "Action":["bedrock:InvokeModel","bedrock:InvokeModelWithResponseStream"],
  "Resource":["arn:aws:bedrock:*::foundation-model/anthropic.claude-sonnet-5",
              "arn:aws:bedrock:*:123456789012:inference-profile/global.anthropic.claude-sonnet-5"]}]}
```

## 6.7 API endpoints & schemas

| Endpoint | Purpose |
|---|---|
| `bedrock.{region}.amazonaws.com` | control plane: model access, customization jobs, provisioned throughput, Guardrails config |
| `bedrock-runtime.{region}.amazonaws.com` | inference: `Converse`, `ConverseStream`, `InvokeModel`, `InvokeModelWithResponseStream`, `StartAsyncInvoke` (video) |
| `bedrock-mantle.{region}.api.aws` | OpenAI Responses + Chat Completions (`/openai/v1`), Anthropic Messages (`/anthropic/v1/messages`); API-key or SigV4 |
| `bedrock-agent` / `bedrock-agent-runtime` | Knowledge Bases + classic Agents build/runtime (incl. `Retrieve`, `RetrieveAndGenerate`) |
| AgentCore endpoints | AgentCore Runtime/Gateway/Memory (separate service surface) |

**Converse vs InvokeModel (bedrock-runtime):**

- **`Converse`/`ConverseStream`** — uniform, model-agnostic JSON schema (`messages[].content[]`
  blocks, `system`, `inferenceConfig{maxTokens,temperature,topP,stopSequences}`, `toolConfig`,
  `guardrailConfig`, `additionalModelRequestFields` for vendor extras). Swap `modelId`, keep code.
  Recommended default for text/chat.
- **`InvokeModel`** — passes an opaque `body` in each **vendor's native schema** (e.g., Anthropic
  body requires `"anthropic_version": "bedrock-2023-05-31"`). Required for models/features Converse
  doesn't cover (embeddings, image/video gen, some vendor-specific params).

`modelId` accepts a base model ID, an **inference-profile ID** (`us.`/`eu.`/`apac.`/`jp.`/`au.`/
`global.` prefix), a provisioned-throughput ARN, or a custom-model deployment ARN. Versioning is
in the model ID itself (`-v1:0` suffixes; newest Anthropic IDs drop it, e.g.
`anthropic.claude-opus-5`), not an API version header.

## 6.8 SDK integration

Python (boto3 ≥ 1.34; Converse):

```python
import boto3
client = boto3.client("bedrock-runtime", region_name="us-east-1")
resp = client.converse(
    modelId="global.anthropic.claude-sonnet-5",
    system=[{"text": "You are a terse assistant."}],
    messages=[{"role": "user", "content": [{"text": "Three uses of SQS?"}]}],
    inferenceConfig={"maxTokens": 512, "temperature": 0.3},
)
print(resp["output"]["message"]["content"][0]["text"])
print(resp["usage"])   # {'inputTokens':..,'outputTokens':..,'totalTokens':..}
```

JavaScript (`@aws-sdk/client-bedrock-runtime` v3):

```javascript
import { BedrockRuntimeClient, ConverseCommand } from "@aws-sdk/client-bedrock-runtime";
const client = new BedrockRuntimeClient({ region: "us-east-1" });
const resp = await client.send(new ConverseCommand({
  modelId: "global.anthropic.claude-sonnet-5",
  messages: [{ role: "user", content: [{ text: "Three uses of SQS?" }] }],
  inferenceConfig: { maxTokens: 512 },
}));
console.log(resp.output.message.content[0].text);
```

curl against mantle (Anthropic Messages, API key):

```bash
curl -X POST https://bedrock-mantle.us-east-1.api.aws/anthropic/v1/messages \
  -H "x-api-key: $BEDROCK_API_KEY" -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{"model":"anthropic.claude-sonnet-5","max_tokens":512,
       "messages":[{"role":"user","content":"Three uses of SQS?"}]}'
```

OpenAI SDK against mantle (only way to reach GPT-5.x on Bedrock):

```python
from openai import OpenAI  # OPENAI_API_KEY=<bedrock key>, OPENAI_BASE_URL=https://bedrock-mantle.us-east-1.api.aws/openai/v1
client = OpenAI()
r = client.responses.create(model="openai.gpt-5.6-sol", input="Summarize SigV4 in two sentences.")
```

All verified against model-card sample code / inference-messages-api docs, accessed 2026-08-14.

## 6.9 Streaming, tool use, structured output

Streaming (boto3):

```python
stream = client.converse_stream(modelId="global.anthropic.claude-sonnet-5",
    messages=[{"role":"user","content":[{"text":"Stream a haiku."}]}])
for ev in stream["stream"]:
    if "contentBlockDelta" in ev:
        print(ev["contentBlockDelta"]["delta"].get("text",""), end="")
    elif "metadata" in ev:
        usage = ev["metadata"]["usage"]
```

Tool use (Converse `toolConfig`; loop: request → `stopReason=="tool_use"` → run tool → append
`toolResult` block → re-call):

```python
tool_cfg = {"tools":[{"toolSpec":{"name":"get_weather",
  "inputSchema":{"json":{"type":"object","properties":{"city":{"type":"string"}},
                  "required":["city"]}}}}]}
resp = client.converse(modelId="global.anthropic.claude-sonnet-5",
                       messages=msgs, toolConfig=tool_cfg)
if resp["stopReason"] == "tool_use":
    tu = next(b["toolUse"] for b in resp["output"]["message"]["content"] if "toolUse" in b)
    msgs += [resp["output"]["message"],
             {"role":"user","content":[{"toolResult":{"toolUseId":tu["toolUseId"],
               "content":[{"json":{"temp_c":21}}]}}]}]
    resp = client.converse(modelId="global.anthropic.claude-sonnet-5",
                           messages=msgs, toolConfig=tool_cfg)
```

Structured output: support is **per model** (model-card flag "Structured outputs"). Where absent
(e.g. Sonnet 5 on runtime, GPT-5.6 via Responses), use the standard workaround: a single required
tool whose `inputSchema` is your JSON schema, plus `toolChoice: {"tool": {"name": ...}}`.

## 6.10 Error handling & retry

| Exception (runtime) | HTTP | Meaning / action |
|---|---|---|
| `ThrottlingException` | 429 | RPM/TPM quota exceeded — exponential backoff + jitter; consider cross-region profile or Priority tier |
| `ValidationException` | 400 | bad schema, unsupported feature for model, context overflow |
| `AccessDeniedException` | 403 | IAM denied or **model access not enabled** in account/region |
| `ResourceNotFoundException` | 404 | wrong modelId/region combination |
| `ModelNotReadyException` | 429 | custom/marketplace model still loading — retry |
| `ModelTimeoutException` | 408 | model took too long — retry |
| `ModelErrorException` | 424 | model returned error |
| `ServiceQuotaExceededException` | 400 | hard quota — request increase |
| `ServiceUnavailableException` / `InternalServerException` | 503/500 | retry with backoff |

Source: Bedrock Runtime API reference (docs.aws.amazon.com/bedrock/latest/APIReference/), accessed
2026-08-14. boto3 pattern — raise both retry ceiling and read timeout (long generations exceed the
60 s default):

```python
from botocore.config import Config
cfg = Config(retries={"max_attempts": 10, "mode": "adaptive"},
             read_timeout=3600, connect_timeout=10)
client = boto3.client("bedrock-runtime", config=cfg)
```

## 6.11 Rate limits & quotas

Quotas are **per account, per region, per model** in requests/min and tokens/min, listed in
Service Quotas (`docs.aws.amazon.com/general/latest/gr/bedrock.html` + console); many are
adjustable by request. Exact numbers vary widely by model/region and change often —
[UNVERIFIED — see Service Quotas console for current values]. Levers when throttled: cross-region
inference profiles (spreads load across regions; AWS states higher effective throughput),
Priority service tier, provisioned throughput, batch for offline work. Mantle endpoint advertises
"higher initial throughput with fair-share distribution" (endpoints.html, accessed 2026-08-14).

## 6.12 Fine-tuning & customization

Customization jobs run from the control plane (console/`bedrock` API), output a custom model
invoked via provisioned throughput or on-demand custom-model deployment:

- **Fine-tuning (SFT, incl. LoRA/PEFT)** — Amazon Nova gen-1 (Micro/Lite/Pro), Meta Llama
  3.1/3.3, Titan-era models; per-model support flag on each model card. Current-generation
  frontier models (Claude 4.5+/5, GPT-5.x, Nova 2 Lite) do **not** support fine-tuning on Bedrock.
- **Reinforcement fine-tuning (RFT)** — GA since 2025-12 (AWS claims avg +66% accuracy over base);
  extended 2026-02 to **open-weight models via OpenAI-compatible APIs** (gpt-oss etc.); Nova RFT
  jobs documented at rft-nova-models.html.
- **Distillation** — teacher→student (e.g., Claude/Llama teacher into Nova/Llama student).
- **Continued pre-training** — Titan/Nova text models.
- Also: import of custom weights (Custom Model Import, Llama/Mistral architectures).

Sources: docs.aws.amazon.com/bedrock/latest/userguide/reinforcement-fine-tuning.html;
aws.amazon.com/about-aws/whats-new/2025/12/bedrock-reinforcement-fine-tuning-66-base-models;
.../2026/02/amazon-bedrock-reinforcement-fine-tuning-openai (accessed 2026-08-14).

## 6.13 RAG & embedding pipeline notes (Knowledge Bases)

**Bedrock Knowledge Bases** is the managed RAG layer: point it at data sources (S3, web crawler,
Confluence/Salesforce/SharePoint connectors), pick an embedding model (default Titan Text
Embeddings V2; Cohere Embed also supported) and a vector store (OpenSearch Serverless default;
Aurora PostgreSQL/pgvector, Pinecone, Redis Enterprise, MongoDB Atlas, **S3 Vectors** — the 2025
low-cost native option), and it handles chunking (fixed/semantic/hierarchical/custom-Lambda),
embedding, sync, retrieval, reranking (Cohere Rerank 3.5 / Amazon Rerank), and citation-bearing
generation. Runtime APIs: `Retrieve` (chunks only) and `RetrieveAndGenerate` (grounded answer)
on `bedrock-agent-runtime`; KBs also attach to Agents and to Converse via `guardrail`/agent
integration. Structured data retrieval (natural-language→SQL over Redshift) and GraphRAG
(Neptune) are additional KB modes. Source:
docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html, accessed 2026-08-14.

## 6.14 Agent support

Two distinct offerings — naming matters in 2026:

- **Amazon Bedrock Agents ("classic")** — the older fully-managed declarative agent (action
  groups from OpenAPI/Lambda, KB attachment, memory, `InvokeAgent` runtime). Still available and
  documented, but AWS's strategic push has moved to AgentCore.
- **Amazon Bedrock AgentCore** — GA since 2025-10 (aws.amazon.com/about-aws/whats-new/2025/10/
  amazon-bedrock-agentcore-available, accessed 2026-08-14). Framework- and model-agnostic
  production platform ("any framework, any model" — LangChain/LangGraph, CrewAI, OpenAI Agents
  SDK, Claude Agent SDK, Strands Agents, custom): modular services — **Runtime** (serverless agent
  hosting, session isolation, up to 8h executions), **Gateway** (turns APIs/Lambda into MCP tools),
  **Memory** (short/long-term), **Identity** (OAuth/agent identity), **Code Interpreter**,
  **Browser**, **Observability** (OTel-based). Consumption-priced (no per-agent fee);
  aws.amazon.com/bedrock/agentcore/pricing/ for meters. MCP is a first-class protocol in Gateway
  and Runtime.
- Related: Strands Agents (AWS's open-source agent framework) commonly deployed onto AgentCore.

New builds should target AgentCore (or a framework on AgentCore Runtime); classic Agents remain
supported for existing declarative deployments. Source: aws.amazon.com/bedrock/agentcore/,
accessed 2026-08-14.

## 6.15 Deployment patterns

- **Serverless on-demand** is the default: no capacity management; scale governed by quotas.
- **Cross-region inference profiles** for resilience/throughput: geographic (`us.`, `eu.`,
  `apac.`, `jp.`, `au.` — data stays in-geo) vs **global** (`global.` — any commercial region,
  ~10% cheaper, requires SCP allowance for unspecified region). Provisioned throughput is NOT
  compatible with inference profiles. Source: cross-region-inference.html, accessed 2026-08-14.
- **Provisioned throughput** for guaranteed capacity / customized models.
- **Batch** (S3-in/S3-out JSONL) for offline at 50%.
- **PrivateLink** VPC interface endpoints for private connectivity; CloudWatch metrics +
  CloudTrail + model-invocation logging (S3/CloudWatch) for ops; mantle gained CloudWatch metrics
  2026-06.
- **Guardrails** apply at Converse/InvokeModel via `guardrailConfig`, standalone via `ApplyGuardrail`
  (works even on non-Bedrock models), and include content/topic/word/PII filters, contextual
  grounding checks, and Automated Reasoning checks. Not available on mantle endpoint (endpoints.html).

## 6.16 Region availability & data residency

Bedrock is live in 30+ commercial regions plus GovCloud, but **model availability is strictly
model-by-region**. Do not assume any model exists in your region: consult the per-model
"Regional availability" section of each model card (docs.aws.amazon.com/bedrock/latest/userguide/
model-cards.html → model page), which distinguishes *in-region*, *geo cross-region*, and *global*
access. Patterns observed 2026-08-14: newest Anthropic models keep small in-region footprints
(us-east-1, eu-north-1, eu-west-1, ap-southeast-4, us-gov-west-1 for Sonnet 5) and rely on
profiles; Nova 2 Lite is **profile-only** (no in-region deployment); GPT-5.6 is US-only with no
profiles. Data residency: in-region invocation keeps inference in-region; geographic profiles keep
it in-geography; global profiles process anywhere on AWS's network (encrypted in transit;
processing region logged in CloudTrail `additionalEventData.inferenceRegion`). AWS states prompts
and outputs are not stored for or shared with model providers and not used to train.

## 6.17 Security, compliance & SLA

- **SLA** (aws.amazon.com/bedrock/sla/, last updated 2023-10-04, accessed 2026-08-14): monthly
  uptime commitment **99.9%** [UNVERIFIED — commitment tier inferred from credit table; page
  sections rendered partially]; service credits: 10% (<99.9%), 25% (<99.0%), 100% (<95.0%),
  claims within two billing cycles.
- Compliance: Bedrock is in scope for SOC 1/2/3, ISO 27001/27017/27018/9001, PCI DSS, HIPAA
  eligibility, FedRAMP High (GovCloud) per AWS Services in Scope
  (aws.amazon.com/compliance/services-in-scope/, accessed 2026-08-14 — verify per certification).
- Encryption at rest (KMS, incl. customer-managed keys for customizations/KBs), TLS in transit,
  IAM/SCP governance, PrivateLink, CloudTrail audit.

## 6.18 Legacy models & migration notes

| Legacy | Status | Migrate to |
|---|---|---|
| Titan Text Express/Lite | removed from catalog | Nova 2 Lite / Nova Micro |
| Nova gen-1 Premier | EOL 2026-09-14³ | Nova 2 Lite / Claude |
| Nova Canvas/Reel/Sonic gen-1 | EOL 2026-09-30³ / Legacy | Stability / Luma Ray v2 / Nova 2 Sonic |
| Claude 3.x (3.5 Haiku, 3 Haiku) | listed, Legacy-tier | Haiku 4.5 |
| Claude Sonnet 4 / Opus 4.1 / 4.5 | superseded, still Active | Sonnet 5 / Opus 5 |
| Llama 3.2 / 3.1 405B | Legacy³ | Llama 4 Scout/Maverick |
| Cohere Command R/R+ | Legacy³ | (Cohere on Bedrock is now Embed/Rerank) |
| AI21 Jamba 1.5 | stale (2024) | — |
| Bedrock Agents (classic) | supported, de-emphasized | AgentCore |

³ = third-party catalog (hidekazu-konishi.com, 2026-05) — confirm dates on model cards. Migration
mechanics: model IDs are immutable; upgrades are explicit ID swaps. Converse-based code migrates
across vendors with minimal change; InvokeModel bodies do not. Anthropic model IDs dropped the
date/version suffix in the 5.x generation.

## 6.19 Task-suitability verdict

**Best for:** organizations already on AWS wanting frontier models (Claude 5, GPT-5.6, Llama 4,
Nova 2) under existing IAM/VPC/CloudTrail governance; multi-vendor A/B via one Converse schema;
regulated workloads needing data-residency-aware routing (geo profiles) and HIPAA/FedRAMP scope;
cost-tiered serving (batch 50%, Flex, caching, global profiles); production agents (AgentCore is
among the most complete managed agent runtimes as of 2026-08).

**Worst for:** day-zero access to vendor features (structured outputs, newest API features often
lag or are absent per model card — e.g. no structured outputs on Sonnet 5 runtime or GPT-5.6);
fine-tuning frontier models (not offered — only Nova/Llama/open-weights customization); simple
projects where SigV4/IAM setup is overhead (mitigated by Bedrock API keys + mantle); GPT-5.x
outside US regions. The per-model feature matrix is the recurring operational hazard: every
capability must be checked per model card, per region.

## 6.20 Sources

All accessed 2026-08-14.

Official (AWS/Anthropic):
- https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html (catalog)
- https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-anthropic-claude-sonnet-5.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-anthropic-claude-opus-5.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-amazon-nova-2-lite.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-56-sol.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/endpoints.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/inference-messages-api.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/reinforcement-fine-tuning.html
- https://aws.amazon.com/bedrock/pricing/
- https://aws.amazon.com/bedrock/sla/
- https://aws.amazon.com/bedrock/agentcore/
- https://aws.amazon.com/about-aws/whats-new/2025/10/amazon-bedrock-agentcore-available
- https://aws.amazon.com/about-aws/whats-new/2026/02/amazon-bedrock-adds-support-six-open-weights-models
- https://aws.amazon.com/about-aws/whats-new/2026/06/amazon-bedrock-openai-models-codex-generally-available/
- https://aws.amazon.com/about-aws/whats-new/2026/07/openai-gpt-terra-luna-pricing-bedrock/
- https://aws.amazon.com/about-aws/whats-new/2026/06/amazon-bedrock-redesigned-console-optimized-openai-anthropic-compatible-apis/
- https://platform.claude.com/docs/en/about-claude/pricing (Claude price parity + Bedrock premium note)

Third-party (labeled where used):
- https://hidekazu-konishi.com/entry/amazon_bedrock_model_catalog_2026.html (catalog snapshot 2026-05)
- https://www.cloudzero.com/blog/amazon-bedrock-pricing/ (2026-07 price roundup)
- https://cloudprice.net/models/global.amazon.nova-2-lite-v1:0 (Nova 2 Lite tier prices)
