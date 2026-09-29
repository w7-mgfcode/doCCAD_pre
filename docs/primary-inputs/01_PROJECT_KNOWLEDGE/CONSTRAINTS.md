# Constraints  [EXPLICIT — user-imposed]

From PROMPT-001 §22 (verbatim substance): GitHub remains the system of record; prefer static/build-time
generation; AI must not sit in the critical path for ordinary documentation reads; prefer files over
databases; prefer metadata manifests over graph databases; prefer built-in search before a search cluster;
prefer built-in/plugin functionality over custom services; no Kubernetes unless justified; no microservice
without an independent lifecycle/scaling/security reason; no vector database until retrieval quality/corpus
size requires one; no multi-agent swarm for ordinary generation; every component must identify the simpler
alternative it beat; the MVP must be comprehensible and operable by one capable engineer.

Additional: never commit real API keys (.env.example only); recruiter/derived content must be
evidence-grounded with fabrication prohibited; proprietary platform internals must never be invented;
GitBook archived OSS repos are [HISTORICAL] only; EN/HU bilingual requirement on key deliverables.
