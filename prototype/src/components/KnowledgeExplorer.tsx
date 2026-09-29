import React, {useState, useMemo} from 'react';
import Link from '@docusaurus/Link';

interface DocItem {
  id: string;
  title: string;
  plane: 'canonical' | 'generated';
  route: string;
  audience: string[];
  owners: string[];
}

const ALL_DOCS: DocItem[] = [
  // Canonical
  {id: 'overview-index', title: 'System Overview', plane: 'canonical', route: '/docs/overview', audience: ['developer', 'architect', 'operator', 'recruiter'], owners: ['architecture']},
  {id: 'overview-vision-and-goals', title: 'Vision, Tenets & Bilingual Strategy', plane: 'canonical', route: '/docs/overview/vision-and-goals', audience: ['developer', 'architect', 'recruiter'], owners: ['architecture']},
  {id: 'overview-glossary', title: 'Architectural Glossary', plane: 'canonical', route: '/docs/overview/glossary', audience: ['developer', 'architect', 'recruiter'], owners: ['architecture']},
  {id: 'getting-started-installation', title: 'Installation & Prerequisites', plane: 'canonical', route: '/docs/getting-started/installation', audience: ['developer', 'operator'], owners: ['core']},
  {id: 'getting-started-quickstart', title: 'Quickstart Guide — Seed to Serve', plane: 'canonical', route: '/docs/getting-started/quickstart', audience: ['developer', 'operator'], owners: ['core']},
  {id: 'architecture-system-overview', title: 'System Architecture Spine', plane: 'canonical', route: '/docs/architecture/system-overview', audience: ['developer', 'architect', 'operator'], owners: ['architecture']},
  {id: 'architecture-content-planes', title: 'Two Content Planes — Canonical vs Generated', plane: 'canonical', route: '/docs/architecture/content-planes', audience: ['developer', 'architect'], owners: ['architecture']},
  {id: 'architecture-ai-generation-plane', title: 'AI Generation Plane & Provider Abstraction', plane: 'canonical', route: '/docs/architecture/ai-generation-plane', audience: ['developer', 'architect'], owners: ['architecture']},
  {id: 'architecture-platform-research', title: 'Six-Platform Research & Evaluation', plane: 'canonical', route: '/docs/architecture/platform-research', audience: ['developer', 'architect'], owners: ['architecture']},
  {id: 'decisions-adr-001-github-source-of-truth', title: 'ADR-001: Git/GitHub as Source of Truth', plane: 'canonical', route: '/docs/decisions/adr-001-github-source-of-truth', audience: ['architect', 'developer'], owners: ['architecture']},
  {id: 'decisions-adr-002-docusaurus-foundation', title: 'ADR-002: Docusaurus 3.x Foundation', plane: 'canonical', route: '/docs/decisions/adr-002-docusaurus-foundation', audience: ['architect', 'developer'], owners: ['architecture']},
  {id: 'decisions-adr-003-canonical-generated-separation', title: 'ADR-003: Content Plane Separation', plane: 'canonical', route: '/docs/decisions/adr-003-canonical-generated-separation', audience: ['architect', 'developer'], owners: ['architecture']},
  {id: 'decisions-adr-004-provider-abstraction', title: 'ADR-004: Thin Provider Abstraction', plane: 'canonical', route: '/docs/decisions/adr-004-provider-abstraction', audience: ['architect', 'developer'], owners: ['architecture']},
  {id: 'decisions-adr-005-pr-gated-generation', title: 'ADR-005: PR-Gated Persistence', plane: 'canonical', route: '/docs/decisions/adr-005-pr-gated-generation', audience: ['architect', 'developer'], owners: ['architecture']},
  {id: 'decisions-adr-006-retrieval-level1', title: 'ADR-006: Level-1 Deterministic Retrieval', plane: 'canonical', route: '/docs/decisions/adr-006-retrieval-level1', audience: ['architect', 'developer'], owners: ['architecture']},
  {id: 'decisions-adr-007-mermaid-as-code', title: 'ADR-007: Mermaid-as-Code with CI Gate', plane: 'canonical', route: '/docs/decisions/adr-007-mermaid-as-code', audience: ['architect', 'developer'], owners: ['architecture']},
  {id: 'decisions-adr-008-build-time-ai', title: 'ADR-008: Build-Time AI over Runtime AI', plane: 'canonical', route: '/docs/decisions/adr-008-build-time-ai', audience: ['architect', 'developer'], owners: ['architecture']},
  {id: 'decisions-adr-009-deployment-github-pages', title: 'ADR-009: Static Deployment via GitHub Pages', plane: 'canonical', route: '/docs/decisions/adr-009-deployment-github-pages', audience: ['architect', 'operator'], owners: ['architecture']},
  {id: 'development-setup', title: 'Development Setup & Contribution', plane: 'canonical', route: '/docs/development/setup', audience: ['developer'], owners: ['core']},
  {id: 'development-contracts-and-schemas', title: 'Contract & Schema Authoring', plane: 'canonical', route: '/docs/development/contracts-and-schemas', audience: ['developer', 'architect'], owners: ['architecture']},
  {id: 'generation-pipeline-lifecycle', title: 'Generation Pipeline Lifecycle', plane: 'canonical', route: '/docs/generation/pipeline-lifecycle', audience: ['developer', 'architect'], owners: ['architecture']},
  {id: 'generation-contracts', title: 'Task Contracts Catalog', plane: 'canonical', route: '/docs/generation/contracts', audience: ['developer', 'architect'], owners: ['architecture']},
  {id: 'validation-quality-gates', title: 'Deterministic CI Quality Gates', plane: 'canonical', route: '/docs/validation/quality-gates', audience: ['developer', 'operator'], owners: ['core']},
  {id: 'validation-drift-detection', title: 'Hash-Based Drift Detection', plane: 'canonical', route: '/docs/validation/drift-detection', audience: ['developer', 'architect'], owners: ['architecture']},
  {id: 'security-trust-boundaries', title: 'Security Architecture & Trust Boundaries', plane: 'canonical', route: '/docs/security/trust-boundaries', audience: ['architect', 'developer'], owners: ['security']},
  {id: 'security-prompt-injection-defense', title: 'Prompt Injection Defenses', plane: 'canonical', route: '/docs/security/prompt-injection-defense', audience: ['architect', 'developer'], owners: ['security']},
  {id: 'operations-runbook-stale-views', title: 'Runbook: Resolving Stale Views', plane: 'canonical', route: '/docs/operations/runbook-stale-views', audience: ['operator', 'developer'], owners: ['operations']},
  {id: 'operations-monitoring-and-metrics', title: 'Operational Freshness & Drift Metrics', plane: 'canonical', route: '/docs/operations/monitoring-and-metrics', audience: ['operator', 'architect'], owners: ['operations']},
  {id: 'troubleshooting-generation-failures', title: 'Troubleshooting Generation Failures', plane: 'canonical', route: '/docs/troubleshooting/generation-failures', audience: ['operator', 'developer'], owners: ['operations']},

  // Generated Views
  {id: 'recruiter-project-overview', title: 'Executive Overview (Recruiter Briefing)', plane: 'generated', route: '/views/recruiter/project-overview', audience: ['recruiter', 'architect'], owners: ['architecture']},
  {id: 'interview-architecture-system-overview', title: 'Interview Prep: System Architecture', plane: 'generated', route: '/views/interview/architecture-system-overview', audience: ['interviewer', 'recruiter'], owners: ['architecture']},
  {id: 'interview-architecture-content-planes', title: 'Interview Prep: Content Planes', plane: 'generated', route: '/views/interview/architecture-content-planes', audience: ['interviewer', 'recruiter'], owners: ['architecture']},
  {id: 'interview-security-trust-boundaries', title: 'Interview Prep: Security Trust Boundaries', plane: 'generated', route: '/views/interview/security-trust-boundaries', audience: ['interviewer', 'recruiter'], owners: ['architecture']},
  {id: 'interview-validation-drift-detection', title: 'Interview Prep: Drift Detection', plane: 'generated', route: '/views/interview/validation-drift-detection', audience: ['interviewer', 'recruiter'], owners: ['architecture']},
  {id: 'q-001-canonical-separation', title: 'Question: Separation of Canonical & Generated', plane: 'generated', route: '/views/questions/q-001-canonical-separation', audience: ['developer', 'architect'], owners: ['architecture']},
  {id: 'q-002-drift-detection', title: 'Question: Hash-Based Drift Detection', plane: 'generated', route: '/views/questions/q-002-drift-detection', audience: ['developer', 'architect'], owners: ['architecture']},
  {id: 'q-003-security-trust-zones', title: 'Question: Security Architecture & Trust Zones', plane: 'generated', route: '/views/questions/q-003-security-trust-zones', audience: ['developer', 'architect'], owners: ['architecture']},
  {id: 'q-004-docusaurus-selection', title: 'Question: Docusaurus Platform Selection', plane: 'generated', route: '/views/questions/q-004-docusaurus-selection', audience: ['developer', 'architect'], owners: ['architecture']},
  {id: 'q-005-private-routing', title: 'Question: Private Routing Policy', plane: 'generated', route: '/views/questions/q-005-private-routing', audience: ['developer', 'architect'], owners: ['architecture']},
  {id: 'q-006-kubernetes-topology', title: 'Question: Kubernetes Topology (Unsupported)', plane: 'generated', route: '/views/questions/q-006-kubernetes-topology', audience: ['developer', 'architect'], owners: ['architecture']},
];

export default function KnowledgeExplorer(): React.JSX.Element {
  const [search, setSearch] = useState('');
  const [planeFilter, setPlaneFilter] = useState<'all' | 'canonical' | 'generated'>('all');
  const [audienceFilter, setAudienceFilter] = useState<string>('all');

  const filteredDocs = useMemo(() => {
    return ALL_DOCS.filter((doc) => {
      if (planeFilter !== 'all' && doc.plane !== planeFilter) return false;
      if (audienceFilter !== 'all' && !doc.audience.includes(audienceFilter)) return false;
      if (search) {
        const q = search.toLowerCase();
        return doc.title.toLowerCase().includes(q) || doc.id.toLowerCase().includes(q);
      }
      return true;
    });
  }, [search, planeFilter, audienceFilter]);

  const clearFilters = () => {
    setSearch('');
    setPlaneFilter('all');
    setAudienceFilter('all');
  };

  return (
    <div style={{maxWidth: '1200px', margin: '0 auto', padding: '1.5rem 1rem'}}>
      <div style={{marginBottom: '1.5rem'}}>
        <h1 style={{fontSize: '2rem', marginBottom: '0.5rem'}}>Knowledge Explorer</h1>
        <p style={{color: '#555', fontSize: '1rem', lineHeight: '1.5'}}>
          Explore the complete corpus of {ALL_DOCS.length} verified artifacts across the canonical and derived planes.
          Filter by audience persona, content plane, or keyword.
        </p>
      </div>

      {/* Filter Controls */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: '2fr 1fr 1fr auto',
          gap: '1rem',
          alignItems: 'center',
          backgroundColor: '#fafbfc',
          padding: '1rem',
          borderRadius: '8px',
          border: '1px solid #e1e4e8',
          marginBottom: '1.5rem',
        }}
      >
        <input
          type="text"
          placeholder="Search by title or ID..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{padding: '8px 12px', borderRadius: '4px', border: '1px solid #ccc', fontSize: '0.9rem'}}
        />

        <select
          value={planeFilter}
          onChange={(e) => setPlaneFilter(e.target.value as any)}
          style={{padding: '8px', borderRadius: '4px', border: '1px solid #ccc', fontSize: '0.85rem'}}
        >
          <option value="all">All Planes ({ALL_DOCS.length})</option>
          <option value="canonical">Canonical /docs ({ALL_DOCS.filter((d) => d.plane === 'canonical').length})</option>
          <option value="generated">Derived /views ({ALL_DOCS.filter((d) => d.plane === 'generated').length})</option>
        </select>

        <select
          value={audienceFilter}
          onChange={(e) => setAudienceFilter(e.target.value)}
          style={{padding: '8px', borderRadius: '4px', border: '1px solid #ccc', fontSize: '0.85rem'}}
        >
          <option value="all">All Audiences</option>
          <option value="developer">Developer</option>
          <option value="architect">Architect</option>
          <option value="operator">Operator</option>
          <option value="recruiter">Recruiter</option>
          <option value="interviewer">Interviewer</option>
        </select>

        <button
          onClick={clearFilters}
          style={{
            padding: '8px 14px',
            backgroundColor: '#f3f4f6',
            border: '1px solid #d1d5db',
            borderRadius: '4px',
            cursor: 'pointer',
            fontSize: '0.85rem',
          }}
        >
          Clear Filters
        </button>
      </div>

      {/* Results Count */}
      <div style={{marginBottom: '0.75rem', fontSize: '0.85rem', color: '#666'}}>
        Showing <strong>{filteredDocs.length}</strong> of {ALL_DOCS.length} documents
      </div>

      {/* Table */}
      {filteredDocs.length > 0 ? (
        <div style={{border: '1px solid #e1e4e8', borderRadius: '8px', overflow: 'hidden'}}>
          <table style={{width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem'}}>
            <thead>
              <tr style={{backgroundColor: '#f6f8fa', borderBottom: '1px solid #e1e4e8', textAlign: 'left'}}>
                <th style={{padding: '10px 14px'}}>Plane</th>
                <th style={{padding: '10px 14px'}}>Document Title</th>
                <th style={{padding: '10px 14px'}}>Audience</th>
                <th style={{padding: '10px 14px'}}>Owner</th>
                <th style={{padding: '10px 14px'}}>Action</th>
              </tr>
            </thead>
            <tbody>
              {filteredDocs.map((doc) => (
                <tr key={doc.id} style={{borderBottom: '1px solid #eee'}}>
                  <td style={{padding: '10px 14px'}}>
                    <span
                      style={{
                        padding: '2px 8px',
                        borderRadius: '4px',
                        backgroundColor: doc.plane === 'canonical' ? '#e1f0ff' : '#f0e6ff',
                        color: doc.plane === 'canonical' ? '#0052cc' : '#6f42c1',
                        fontWeight: 700,
                        fontSize: '0.75rem',
                      }}
                    >
                      {doc.plane === 'canonical' ? '/DOCS' : '/VIEWS'}
                    </span>
                  </td>
                  <td style={{padding: '10px 14px'}}>
                    <Link to={doc.route} style={{fontWeight: 600}}>
                      {doc.title}
                    </Link>
                    <div style={{fontSize: '0.75rem', color: '#666', marginTop: '2px'}}>
                      ID: <code>{doc.id}</code>
                    </div>
                  </td>
                  <td style={{padding: '10px 14px'}}>
                    <div style={{display: 'flex', gap: '4px', flexWrap: 'wrap'}}>
                      {doc.audience.map((a) => (
                        <span key={a} style={{backgroundColor: '#f3f4f6', padding: '1px 6px', borderRadius: '3px', fontSize: '0.7rem'}}>
                          {a}
                        </span>
                      ))}
                    </div>
                  </td>
                  <td style={{padding: '10px 14px'}}>{doc.owners.join(', ')}</td>
                  <td style={{padding: '10px 14px'}}>
                    <Link
                      to={doc.route}
                      style={{
                        padding: '4px 10px',
                        borderRadius: '4px',
                        backgroundColor: '#0052cc',
                        color: '#fff',
                        textDecoration: 'none',
                        fontSize: '0.75rem',
                        fontWeight: 600,
                      }}
                    >
                      Open &rarr;
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div style={{padding: '3rem', textAlign: 'center', backgroundColor: '#fafbfc', borderRadius: '8px', border: '1px dashed #ccc'}}>
          <div style={{fontSize: '1.2rem', fontWeight: 600, marginBottom: '0.5rem', color: '#555'}}>No matching documents found</div>
          <p style={{fontSize: '0.9rem', color: '#777', marginBottom: '1rem'}}>
            Try broadening your search query or clearing active filters.
          </p>
          <button
            onClick={clearFilters}
            style={{padding: '6px 14px', backgroundColor: '#0052cc', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer'}}
          >
            Reset Filters
          </button>
        </div>
      )}
    </div>
  );
}
