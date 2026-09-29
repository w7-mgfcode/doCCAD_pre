# Open Questions & Unresolved Items

From session evidence gaps (progress_final.json) and design deferrals (ARCHITECTURE-SPINE.md §Deferred).

**Evidence gaps [UNKNOWN]:** Mintlify Pro exact pricing (third-party-reported ~$450/mo only); Mintlify
search engine technology and backend internals; GitBook custom-frontmatter round-trip fidelity, API rate
limits, sync-failure webhooks; Zensical Spark pricing, Disco search OSS status, native i18n timing;
Hyperbook HU lunr stemmer presence in dist; several GitHub metrics read from rendered pages (REST API was
blocked in-session); Docusaurus absolute build times on the target corpus (unmeasured).

**Design deferrals [EXPLICIT]:** Level-2+ retrieval implementation choice (until boundary trips); runtime
Q&A chat (out of scope; isolated service if ever); enterprise SSO/private-site auth (Harden phase);
graph store for dependencies (manifest until insufficient); automatic HU translation of generated pages.

**Validation not-executed items [EXPLICIT]:** live model API calls (no keys by design); actionlint
(unavailable — workflows YAML-parsed only); real GitHub Pages deployment; future.faster flags and search
plugin excluded from PoC deliberately.

**Archival gaps [EXPLICIT]:** sub-agent working prompts (beyond the preserved analysis brief) were not
persisted as files during research and exist only as summaries; external web pages/clone contents consulted
during research were processed in ephemeral containers and not retained — URLs preserved in
02_RESEARCH/references/EXTERNAL_SOURCES.md. Verbatim byte-exact copies of the two mission prompts were not
preserved at receipt time; near-verbatim transcriptions are in 03_PROMPTS/master/ (labeled).
