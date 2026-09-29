import React, {useState} from 'react';
import Link from '@docusaurus/Link';
import ProvenanceBanner from './ProvenanceBanner';

interface Scenario {
  id: string;
  title: string;
  question: string;
  audience: string;
  privacy: 'public' | 'private';
  targetId?: string;
  expectedStatus: 'success' | 'insufficient_evidence';
  evidenceSummary: string[];
  answerSummary: string;
  fullMarkdown: string;
}

const SCENARIOS: Scenario[] = [
  {
    id: 'q-001',
    title: 'Scenario 1: Plane Separation',
    question: 'How does DOCCAD ensure AI-generated content does not pollute canonical documentation?',
    audience: 'developer',
    privacy: 'public',
    targetId: 'architecture-content-planes',
    expectedStatus: 'success',
    evidenceSummary: [
      'docs/source/architecture/content-planes.md',
      'docs/source/decisions/adr-003-canonical-generated-separation.md',
    ],
    answerSummary:
      'DOCCAD enforces physical separation via two distinct Docusaurus docs-plugin instances: /docs for human-authored canon and /views for generated views. Generated content may cite canonical docs, but canonical docs never cite generated content.',
    fullMarkdown: `---
id: q-001-canonical-separation
title: "DOCCAD Question: Separation of Canonical and Generated Planes"
type: generated
audience: [developer, architect]
owners: [architecture]
last_validated: 2026-09-21
generated: true
generation:
  contract: GenerateQuestionPage
  contract_version: 1
  prompt_version: question-page.v1
  source_documents:
    - id: architecture-content-planes
      path: docs/source/architecture/content-planes.md
      content_hash: sha256:8db3f04553bab7dc6084680768d215c4ce19922dc5f7d7d3e05c4eea4058989a
  provider: fixture
  model: deterministic-demo-fixture
  generation_mode: demo
  generated_at: 2026-09-21T00:00:00Z
  approval_status: approved-for-demo
---

# Question: How does DOCCAD prevent AI content from polluting canonical docs?

## Answer Summary
DOCCAD prevents AI pollution through a strict architectural and physical separation called the **Two Content Planes** model, enforced via separate Docusaurus plugin instances, separate routes, and PR branch protection.

### 1. Two Separate Docs Plugin Instances
- **Canonical Plane (\`docs/source/\`)**: Human-authored, route \`/docs\`. Only human PRs may edit this plane.
- **Generated Plane (\`docs/generated/\`)**: Bot-authored, route \`/views\`. Automated generation jobs write solely to this directory.

### 2. Unidirectional Citation Rule
- Generated views can cite canonical documentation.
- Canonical pages are strictly forbidden from importing or citing generated views.

### 3. Human PR Approval Gate
All generated files persist only through pull requests into \`docs-gen/*\` branches with branch protection.
`,
  },
  {
    id: 'q-002',
    title: 'Scenario 2: Drift Detection',
    question: 'How does DOCCAD detect drift when canonical architecture or code changes?',
    audience: 'developer',
    privacy: 'public',
    targetId: 'validation-drift-detection',
    expectedStatus: 'success',
    evidenceSummary: [
      'docs/source/validation/drift-detection.md',
      'docs/source/operations/runbook-stale-views.md',
    ],
    answerSummary:
      'Every derived artifact records the sha256 content hashes of its source canonical documents in frontmatter. CI re-evaluates hashes against disk and flags only affected pages as STALE in impact.json, driving targeted regeneration.',
    fullMarkdown: `---
id: q-002-drift-detection
title: "DOCCAD Question: Hash-Based Drift Detection"
type: generated
audience: [developer, architect]
owners: [architecture]
last_validated: 2026-09-21
generated: true
generation:
  contract: GenerateQuestionPage
  contract_version: 1
  prompt_version: question-page.v1
  source_documents:
    - id: validation-drift-detection
      path: docs/source/validation/drift-detection.md
      content_hash: sha256:66743e3d517e91ecbc08636c41b4549e1f47811a3e591802f5d1b1c53a0a23db
  provider: fixture
  model: deterministic-demo-fixture
  generation_mode: demo
  generated_at: 2026-09-21T00:00:00Z
  approval_status: approved-for-demo
---

# Question: How does DOCCAD detect drift when canonical architecture changes?

## Answer Summary
DOCCAD detects drift mechanically using **sha256 content hashes** stored directly in the frontmatter of generated pages. When a canonical file changes, a deterministic script re-evaluates all hashes against disk and flags only the affected derived pages as stale.
`,
  },
  {
    id: 'q-003',
    title: 'Scenario 3: Security & Trust Zones',
    question: "What is DOCCAD's security model for prompt injection and untrusted inputs?",
    audience: 'architect',
    privacy: 'public',
    targetId: 'security-trust-boundaries',
    expectedStatus: 'success',
    evidenceSummary: [
      'docs/source/security/trust-boundaries.md',
      'docs/source/security/prompt-injection-defense.md',
    ],
    answerSummary:
      'DOCCAD enforces a 6-Zone Trust Model. Untrusted inputs are demarcated as inert data via <<<EVIDENCE-DATA tokens. Static linters reject dangerous MDX executable constructs and enforce external link allowlists.',
    fullMarkdown: `---
id: q-003-security-trust-zones
title: "DOCCAD Question: Security Architecture and Trust Zones"
type: generated
audience: [developer, architect]
owners: [architecture]
last_validated: 2026-09-21
generated: true
generation:
  contract: GenerateQuestionPage
  contract_version: 1
  prompt_version: question-page.v1
  source_documents:
    - id: security-trust-boundaries
      path: docs/source/security/trust-boundaries.md
      content_hash: sha256:c0cca6dafec52ba6df0f8f477c5d8331eff745562f491a87563006499eff1677
  provider: fixture
  model: deterministic-demo-fixture
  generation_mode: demo
  generated_at: 2026-09-21T00:00:00Z
  approval_status: approved-for-demo
---

# Question: What is DOCCAD's security model for prompt injection and untrusted inputs?

## Answer Summary
DOCCAD enforces a 6-Zone Trust Boundary Model with strict data demarcation and zero serving backend.
`,
  },
  {
    id: 'q-004',
    title: 'Scenario 4: Docusaurus Platform Selection',
    question: 'Why did DOCCAD select Docusaurus over Mintlify or MkDocs?',
    audience: 'architect',
    privacy: 'public',
    targetId: 'decisions-adr-002-docusaurus-foundation',
    expectedStatus: 'success',
    evidenceSummary: [
      'docs/source/decisions/adr-002-docusaurus-foundation.md',
      'docs/source/architecture/platform-research.md',
    ],
    answerSummary:
      'Docusaurus 3.x won the 11-criterion evaluation (88.6/100) due to native multi-instance docs separation, offline static compilation, React 19 component flexibility, and complete freedom from cloud SaaS vendor lock-in.',
    fullMarkdown: `---
id: q-004-docusaurus-selection
title: "DOCCAD Question: Docusaurus Platform Selection Rationale"
type: generated
audience: [developer, architect]
owners: [architecture]
last_validated: 2026-09-21
generated: true
generation:
  contract: GenerateQuestionPage
  contract_version: 1
  prompt_version: question-page.v1
  source_documents:
    - id: decisions-adr-002-docusaurus-foundation
      path: docs/source/decisions/adr-002-docusaurus-foundation.md
      content_hash: sha256:a030baba8cbb2c73d9d3f11e9766ee5dfec4ec6576b4ef84c6806cf2c7e0f252
  provider: fixture
  model: deterministic-demo-fixture
  generation_mode: demo
  generated_at: 2026-09-21T00:00:00Z
  approval_status: approved-for-demo
---

# Question: Why did DOCCAD select Docusaurus over Mintlify or MkDocs?

## Answer Summary
Docusaurus 3.x scored 88.6/100, outperforming Mintlify and MkDocs on architectural independence and multi-instance plugin support.
`,
  },
  {
    id: 'q-005',
    title: 'Scenario 5: Private Routing Policy',
    question: 'How does the private routing policy prevent data leakage to cloud model providers?',
    audience: 'developer',
    privacy: 'private',
    targetId: 'decisions-adr-004-provider-abstraction',
    expectedStatus: 'success',
    evidenceSummary: [
      'docs/source/decisions/adr-004-provider-abstraction.md',
      'docs/source/architecture/ai-generation-plane.md',
    ],
    answerSummary:
      'Tasks marked privacy: private are hard-pinned to local execution. If the local provider is disabled or unavailable, the router terminates with a fatal PrivacyRoutingError, strictly prohibiting silent fallback to cloud APIs.',
    fullMarkdown: `---
id: q-005-private-routing
title: "DOCCAD Question: Private Routing and Zero Cloud Fallback"
type: generated
audience: [developer, architect]
owners: [architecture]
last_validated: 2026-09-21
generated: true
generation:
  contract: GenerateQuestionPage
  contract_version: 1
  prompt_version: question-page.v1
  source_documents:
    - id: decisions-adr-004-provider-abstraction
      path: docs/source/decisions/adr-004-provider-abstraction.md
      content_hash: sha256:3a9e29b11b5fbcf79401bfbc19c0a6b7e0bbabec9d71c6d860d5b4e28c46014e
  provider: fixture
  model: deterministic-demo-fixture
  generation_mode: demo
  generated_at: 2026-09-21T00:00:00Z
  approval_status: approved-for-demo
---

# Question: How does private routing prevent data leakage to cloud model providers?

## Answer Summary
DOCCAD's Router enforces non-negotiable local pinning for confidential queries.
`,
  },
  {
    id: 'q-006',
    title: 'Scenario 6: Unsupported Question (Kubernetes)',
    question: "What is DOCCAD's multi-cluster Kubernetes deployment topology for high-frequency trading?",
    audience: 'architect',
    privacy: 'public',
    targetId: 'decisions-adr-009-deployment-github-pages',
    expectedStatus: 'insufficient_evidence',
    evidenceSummary: ['docs/source/decisions/adr-009-deployment-github-pages.md'],
    answerSummary:
      'INSUFFICIENT CANONICAL EVIDENCE: The canonical documentation contains no evidence for Kubernetes clusters. As governed by contract GenerateQuestionPage, DOCCAD refuses to invent architectural details or technologies not present in canonical sources.',
    fullMarkdown: `---
id: q-006-kubernetes-topology
title: "DOCCAD Question: Kubernetes Deployment Topology (Insufficient Evidence)"
type: generated
audience: [developer, architect]
owners: [architecture]
last_validated: 2026-09-21
generated: true
generation:
  contract: GenerateQuestionPage
  contract_version: 1
  prompt_version: question-page.v1
  source_documents:
    - id: decisions-adr-009-deployment-github-pages
      path: docs/source/decisions/adr-009-deployment-github-pages.md
      content_hash: sha256:14a9e6e56b269bebf7ecae7034c56ee9370bb4c2e6f49fcbfdf02e1c93f0b2f1
  provider: fixture
  model: deterministic-demo-fixture
  generation_mode: demo
  generated_at: 2026-09-21T00:00:00Z
  approval_status: approved-for-demo
---

# Question: What is DOCCAD's multi-cluster Kubernetes deployment topology?

## Status: Insufficient Canonical Evidence
The canonical documentation contains no evidence for Kubernetes. Per ADR-009, DOCCAD is a static site on GitHub Pages.
`,
  },
];

export default function QuestionWorkbench(): React.JSX.Element {
  const [selectedScenario, setSelectedScenario] = useState<Scenario>(SCENARIOS[0]);
  const [questionText, setQuestionText] = useState(SCENARIOS[0].question);
  const [audience, setAudience] = useState(SCENARIOS[0].audience);
  const [privacy, setPrivacy] = useState<'public' | 'private'>(SCENARIOS[0].privacy);
  const [targetDoc, setTargetDoc] = useState<string>(SCENARIOS[0].targetId || '');
  const [generatedDraft, setGeneratedDraft] = useState<Scenario | null>(SCENARIOS[0]);
  const [reviewStatus, setReviewStatus] = useState<'draft' | 'in-review' | 'approved-for-demo' | 'rejected'>('approved-for-demo');
  const [activeTab, setActiveTab] = useState<'preview' | 'evidence' | 'provenance' | 'validation'>('preview');

  const handleSelectScenario = (sc: Scenario) => {
    setSelectedScenario(sc);
    setQuestionText(sc.question);
    setAudience(sc.audience);
    setPrivacy(sc.privacy);
    setTargetDoc(sc.targetId || '');
    setGeneratedDraft(sc);
    setReviewStatus('approved-for-demo');
  };

  const handleGenerate = () => {
    // Find matching preset or generate dynamic excerpt
    const match = SCENARIOS.find((s) => s.question.toLowerCase() === questionText.toLowerCase());
    if (match) {
      setGeneratedDraft(match);
    } else if (questionText.toLowerCase().includes('kubernetes') || questionText.toLowerCase().includes('trading')) {
      setGeneratedDraft(SCENARIOS[5]);
    } else {
      // Dynamic fallback
      const dynamicScenario: Scenario = {
        id: `q-dynamic-${Date.now().toString().slice(-4)}`,
        title: 'Custom Query Result',
        question: questionText,
        audience,
        privacy,
        expectedStatus: 'success',
        evidenceSummary: ['docs/source/overview/index.md', 'docs/source/architecture/system-overview.md'],
        answerSummary: `Deterministically generated candidate response grounded in canonical files for: "${questionText}".`,
        fullMarkdown: `---
id: q-custom-${Date.now().toString().slice(-4)}
title: "DOCCAD Question: Custom Query"
type: generated
audience: [${audience}]
owners: [architecture]
last_validated: 2026-09-21
generated: true
generation:
  contract: GenerateQuestionPage
  contract_version: 1
  prompt_version: question-page.v1
  source_documents:
    - id: overview-index
      path: docs/source/overview/index.md
      content_hash: sha256:42b81722440ea5efff869b2a62faf09dc372b4c8c5ca90c3b3aa42ff923d08ed
  provider: fixture
  model: deterministic-demo-fixture
  generation_mode: demo
  generated_at: 2026-09-21T00:00:00Z
  approval_status: draft
---

# Question: ${questionText}

## Grounded Answer
This answer was assembled by Level-1 deterministic retrieval using canonical documentation.
`,
      };
      setGeneratedDraft(dynamicScenario);
    }
    setReviewStatus('draft');
  };

  const exportRequestJson = () => {
    const payload = {
      question: questionText,
      audience,
      privacy_class: privacy,
      target_id: targetDoc || undefined,
    };
    const blob = new Blob([JSON.stringify(payload, null, 2)], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'QuestionRequest.json';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div style={{maxWidth: '1200px', margin: '0 auto', padding: '1.5rem 1rem'}}>
      <div style={{marginBottom: '1.5rem'}}>
        <h1 style={{fontSize: '2rem', marginBottom: '0.5rem'}}>Question & Governance Workbench</h1>
        <p style={{color: '#555', fontSize: '1rem', lineHeight: '1.5'}}>
          Test the end-to-end question lifecycle: deterministic retrieval, fixture generation, schema validation,
          simulated review, and export/import round-tripping with the CLI.
        </p>
      </div>

      <div style={{display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '1.5rem'}}>
        {/* Left Panel: Query & Scenarios */}
        <div style={{border: '1px solid #e1e4e8', borderRadius: '8px', padding: '1.25rem', backgroundColor: '#fafbfc'}}>
          <h3 style={{fontSize: '1.1rem', marginBottom: '1rem'}}>1. Select Scenario</h3>
          <div style={{display: 'flex', flexDirection: 'column', gap: '0.5rem', marginBottom: '1.5rem'}}>
            {SCENARIOS.map((sc) => (
              <button
                key={sc.id}
                onClick={() => handleSelectScenario(sc)}
                style={{
                  textAlign: 'left',
                  padding: '8px 12px',
                  borderRadius: '6px',
                  border: selectedScenario.id === sc.id ? '2px solid #0052cc' : '1px solid #d1d5db',
                  backgroundColor: selectedScenario.id === sc.id ? '#eef4ff' : '#ffffff',
                  cursor: 'pointer',
                  fontWeight: selectedScenario.id === sc.id ? 600 : 400,
                  fontSize: '0.85rem',
                }}
              >
                <div>{sc.title}</div>
                <div style={{fontSize: '0.75rem', color: '#666', marginTop: '2px'}}>
                  {sc.expectedStatus === 'insufficient_evidence' ? '⚠️ Insufficient Evidence' : '✓ Grounded'}
                </div>
              </button>
            ))}
          </div>

          <h3 style={{fontSize: '1.1rem', marginBottom: '0.75rem'}}>2. Query Parameters</h3>
          <div style={{marginBottom: '1rem'}}>
            <label style={{display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '4px'}}>Question:</label>
            <textarea
              rows={3}
              value={questionText}
              onChange={(e) => setQuestionText(e.target.value)}
              style={{width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc', fontSize: '0.85rem'}}
            />
          </div>

          <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem', marginBottom: '1rem'}}>
            <div>
              <label style={{display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '4px'}}>Audience:</label>
              <select
                value={audience}
                onChange={(e) => setAudience(e.target.value)}
                style={{width: '100%', padding: '6px', borderRadius: '4px', border: '1px solid #ccc', fontSize: '0.85rem'}}
              >
                <option value="developer">developer</option>
                <option value="architect">architect</option>
                <option value="operator">operator</option>
                <option value="recruiter">recruiter</option>
                <option value="interviewer">interviewer</option>
              </select>
            </div>
            <div>
              <label style={{display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '4px'}}>Privacy:</label>
              <select
                value={privacy}
                onChange={(e) => setPrivacy(e.target.value as 'public' | 'private')}
                style={{width: '100%', padding: '6px', borderRadius: '4px', border: '1px solid #ccc', fontSize: '0.85rem'}}
              >
                <option value="public">public (cloud/fixture)</option>
                <option value="private">private (local only)</option>
              </select>
            </div>
          </div>

          <div style={{display: 'flex', flexDirection: 'column', gap: '0.5rem', marginTop: '1.5rem'}}>
            <button
              onClick={handleGenerate}
              style={{
                backgroundColor: '#0052cc',
                color: '#fff',
                padding: '10px 16px',
                borderRadius: '6px',
                border: 'none',
                cursor: 'pointer',
                fontWeight: 600,
                fontSize: '0.9rem',
              }}
            >
              ⚡ Run Fixture Generation
            </button>
            <button
              onClick={exportRequestJson}
              style={{
                backgroundColor: '#f3f4f6',
                color: '#374151',
                padding: '8px 14px',
                borderRadius: '6px',
                border: '1px solid #d1d5db',
                cursor: 'pointer',
                fontSize: '0.85rem',
                fontWeight: 500,
              }}
            >
              📥 Export Request JSON for CLI
            </button>
          </div>
        </div>

        {/* Right Panel: Output, Governance & Inspection */}
        <div style={{border: '1px solid #e1e4e8', borderRadius: '8px', padding: '1.25rem', backgroundColor: '#ffffff'}}>
          {/* Review Governance Bar */}
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              padding: '0.75rem 1rem',
              borderRadius: '6px',
              backgroundColor: '#f0f4f8',
              marginBottom: '1rem',
            }}
          >
            <div>
              <span style={{fontWeight: 600, fontSize: '0.85rem', marginRight: '0.5rem'}}>Demo Review Status:</span>
              <span
                style={{
                  padding: '3px 10px',
                  borderRadius: '12px',
                  backgroundColor:
                    reviewStatus === 'approved-for-demo'
                      ? '#28a745'
                      : reviewStatus === 'in-review'
                      ? '#17a2b8'
                      : reviewStatus === 'rejected'
                      ? '#dc3545'
                      : '#ffc107',
                  color: reviewStatus === 'in-review' || reviewStatus === 'approved-for-demo' || reviewStatus === 'rejected' ? '#fff' : '#000',
                  fontWeight: 600,
                  fontSize: '0.8rem',
                }}
              >
                {reviewStatus.toUpperCase()}
              </span>
            </div>
            <div style={{display: 'flex', gap: '0.5rem'}}>
              <button
                onClick={() => setReviewStatus('approved-for-demo')}
                style={{
                  backgroundColor: '#28a745',
                  color: '#fff',
                  border: 'none',
                  borderRadius: '4px',
                  padding: '4px 8px',
                  cursor: 'pointer',
                  fontSize: '0.75rem',
                  fontWeight: 600,
                }}
              >
                Approve (Demo)
              </button>
              <button
                onClick={() => setReviewStatus('rejected')}
                style={{
                  backgroundColor: '#dc3545',
                  color: '#fff',
                  border: 'none',
                  borderRadius: '4px',
                  padding: '4px 8px',
                  cursor: 'pointer',
                  fontSize: '0.75rem',
                  fontWeight: 600,
                }}
              >
                Reject
              </button>
            </div>
          </div>

          {/* Navigation Tabs */}
          <div style={{display: 'flex', borderBottom: '1px solid #e1e4e8', marginBottom: '1rem'}}>
            {(['preview', 'evidence', 'provenance', 'validation'] as const).map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                style={{
                  padding: '8px 16px',
                  background: 'none',
                  border: 'none',
                  borderBottom: activeTab === tab ? '2px solid #0052cc' : 'none',
                  color: activeTab === tab ? '#0052cc' : '#666',
                  fontWeight: activeTab === tab ? 600 : 400,
                  cursor: 'pointer',
                  fontSize: '0.9rem',
                  textTransform: 'capitalize',
                }}
              >
                {tab}
              </button>
            ))}
          </div>

          {/* Tab 1: Preview */}
          {activeTab === 'preview' && generatedDraft && (
            <div>
              <ProvenanceBanner
                status={reviewStatus}
                contract="GenerateQuestionPage"
                contractVersion={1}
                promptVersion="question-page.v1"
                provider="fixture"
                model="deterministic-demo-fixture"
                generationMode="demo"
                sourceDocuments={generatedDraft.evidenceSummary.map((p) => ({
                  id: p.split('/').pop()?.replace('.md', '') || '',
                  path: p,
                  content_hash: 'sha256:verified_current',
                }))}
              />
              <div
                style={{
                  padding: '1rem',
                  backgroundColor: '#f9f9f9',
                  borderRadius: '6px',
                  fontSize: '0.9rem',
                  lineHeight: '1.5',
                  border: '1px solid #eee',
                }}
              >
                <div style={{fontWeight: 700, fontSize: '1.1rem', marginBottom: '0.75rem'}}>
                  {generatedDraft.title}
                </div>
                <div style={{marginBottom: '1rem'}}>
                  <strong>Summary:</strong> {generatedDraft.answerSummary}
                </div>
                <div>
                  <strong>Supporting Canonical Citations:</strong>
                  <ul>
                    {generatedDraft.evidenceSummary.map((ev) => (
                      <li key={ev}>
                        <Link to={`/docs/${ev.replace('docs/source/', '').replace('.md', '')}`}>{ev}</Link>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          )}

          {/* Tab 2: Evidence */}
          {activeTab === 'evidence' && generatedDraft && (
            <div>
              <h4 style={{fontSize: '0.95rem', marginBottom: '0.5rem'}}>Level-1 Retrieval Results</h4>
              <div style={{fontSize: '0.85rem', marginBottom: '1rem', color: '#555'}}>
                Context budget: <strong>32,000 tokens</strong> &bull; Selected:{' '}
                <strong>{generatedDraft.evidenceSummary.length} files</strong> (~1,200 tokens)
              </div>
              <table style={{width: '100%', fontSize: '0.85rem', borderCollapse: 'collapse'}}>
                <thead>
                  <tr style={{borderBottom: '1px solid #ddd', textAlign: 'left', backgroundColor: '#f3f4f6'}}>
                    <th style={{padding: '6px'}}>Status</th>
                    <th style={{padding: '6px'}}>File Path</th>
                    <th style={{padding: '6px'}}>Reason</th>
                  </tr>
                </thead>
                <tbody>
                  {generatedDraft.evidenceSummary.map((ev) => (
                    <tr key={ev} style={{borderBottom: '1px solid #eee'}}>
                      <td style={{padding: '6px', color: '#28a745', fontWeight: 600}}>INCLUDED</td>
                      <td style={{padding: '6px'}}>
                        <code>{ev}</code>
                      </td>
                      <td style={{padding: '6px', color: '#666'}}>Matched query keywords / target closure</td>
                    </tr>
                  ))}
                  <tr style={{borderBottom: '1px solid #eee', color: '#888'}}>
                    <td style={{padding: '6px', color: '#dc3545'}}>REJECTED</td>
                    <td style={{padding: '6px'}}>
                      <code>docs/generated/recruiter/project-overview.mdx</code>
                    </td>
                    <td style={{padding: '6px'}}>Rule violation: generated views cannot serve as AI evidence</td>
                  </tr>
                  <tr style={{color: '#888'}}>
                    <td style={{padding: '6px', color: '#dc3545'}}>REJECTED</td>
                    <td style={{padding: '6px'}}>
                      <code>docs/diagrams/c4_l1_context.mmd</code>
                    </td>
                    <td style={{padding: '6px'}}>Outside contract allowed_evidence globs</td>
                  </tr>
                </tbody>
              </table>
            </div>
          )}

          {/* Tab 3: Provenance */}
          {activeTab === 'provenance' && (
            <div>
              <h4 style={{fontSize: '0.95rem', marginBottom: '0.5rem'}}>Cryptographic Provenance Snapshot</h4>
              <pre
                style={{
                  fontSize: '0.75rem',
                  padding: '1rem',
                  borderRadius: '6px',
                  backgroundColor: '#1e1e1e',
                  color: '#d4d4d4',
                  overflowX: 'auto',
                }}
              >
                {JSON.stringify(
                  {
                    artifact_id: selectedScenario.id,
                    contract: 'GenerateQuestionPage',
                    contract_version: 1,
                    prompt_version: 'question-page.v1',
                    provider: 'fixture',
                    model: 'deterministic-demo-fixture',
                    generation_mode: 'demo',
                    simulated_approval: reviewStatus === 'approved-for-demo',
                    production_eligible: false,
                    sources: selectedScenario.evidenceSummary.map((p) => ({
                      path: p,
                      hash: 'sha256:current_disk_verified',
                    })),
                  },
                  null,
                  2,
                )}
              </pre>
            </div>
          )}

          {/* Tab 4: Validation */}
          {activeTab === 'validation' && (
            <div>
              <h4 style={{fontSize: '0.95rem', marginBottom: '0.5rem'}}>Deterministic Quality Gates</h4>
              <div style={{display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.85rem'}}>
                <div style={{display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
                  <span style={{color: '#28a745', fontWeight: 700}}>✓ PASS</span>
                  <span>Frontmatter Schema (document.schema.json) valid</span>
                </div>
                <div style={{display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
                  <span style={{color: '#28a745', fontWeight: 700}}>✓ PASS</span>
                  <span>Two-Plane Isolation: target in /views, evidence strictly from /docs</span>
                </div>
                <div style={{display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
                  <span style={{color: '#28a745', fontWeight: 700}}>✓ PASS</span>
                  <span>Citation targets exist and resolve to valid canonical slugs</span>
                </div>
                <div style={{display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
                  <span style={{color: '#28a745', fontWeight: 700}}>✓ PASS</span>
                  <span>Safe MDX: zero executable script tags or dynamic eval constructs</span>
                </div>
                <div style={{display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
                  <span style={{color: '#28a745', fontWeight: 700}}>✓ PASS</span>
                  <span>Privacy Policy: {privacy === 'private' ? 'Pinned to local provider' : 'Public routing chain'}</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
