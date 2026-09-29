# Archive Structure Conventions

| Folder | Purpose | Layer |
|---|---|---|
| 00_PROJECT_CONTROL/ | Index, registers, traceability, knowledge JSON, manifest, collection report | maintained |
| 01_PROJECT_KNOWLEDGE/ | Conversational/project-level knowledge: vision, requirements, decisions, constraints, rejected alternatives, open questions (EXPLICIT/INFERRED/UNKNOWN labeled) | maintained |
| 02_RESEARCH/ | Platform research (six platforms + _comparison) and aggregated external source logs | organized copy |
| 03_PROMPTS/ | First-class prompt artifacts: master missions, research brief, generation prompt templates | historical |
| 04_ARCHITECTURE/ | Target-system architecture: SAD set, 9 ADRs, C4/deployment/data-flow Mermaid sources, decision matrix | organized copy |
| 05_DOCUMENTATION_DESIGN/ | Information architecture / content model; documentation process (CI, ingestion, drift) | organized copy |
| 06_AI_DOCUMENTATION/ | AI-layer design + PoC copies: model strategy, provider abstraction code, contracts/schemas, demo recruiter/interview artifacts | organized copy |
| 07_MERMAID/ | All standalone .mmd by type + register + 32 diagrams extracted from Markdown (provenance header per file) | organized copy / index |
| 08_TASKS/ | TASK_REGISTER; completed checkpoint record; future roadmap | maintained |
| 09_RESULTS/ | RESULT_REGISTER; validation evidence; knowledge base; runnable PoC; session manifest | organized copy |
| 10_EXTERNAL_ARTIFACTS/ | Collected external reference documents (methodology skills) | organized copy |
| 11_RAW_ARCHIVE/ | Byte-preserved original session workspace (outputs/ snapshot, node_modules/build excluded) | historical — never edit |
| 12_FUTURE/ | Backlog and ideas recorded during archiving | maintained |

Conventions: organized artifacts are copies of raw sources (dest→source in SOURCE_REGISTER.md /
PROJECT_MANIFEST.json); nothing in `historical` layers is ever edited; IDs are stable and never recycled;
empty directories are not created. The baseline structure from PROMPT-002 §8 was followed with these
recorded adaptations: research subfolders ai-models/architecture/security/deployment were not created
(no artifacts of those classes exist separately — AI/security/deployment research lives inside the platform
SADs and the solution documents); 05_ subfolders limited to the two with real content; 08_TASKS uses
registers instead of empty status folders except completed/ and future/.
