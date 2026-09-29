import React, {useState} from 'react';
import Link from '@docusaurus/Link';

interface DependencyNode {
  canonicalId: string;
  canonicalPath: string;
  currentHash: string;
  isDrifted?: boolean;
  dependents: Array<{
    derivedId: string;
    derivedPath: string;
    contract: string;
    recordedHash: string;
  }>;
}

const INITIAL_NODES: DependencyNode[] = [
  {
    canonicalId: 'architecture-content-planes',
    canonicalPath: 'docs/source/architecture/content-planes.md',
    currentHash: 'sha256:8db3f04553bab7dc6084680768d215c4ce19922dc5f7d7d3e05c4eea4058989a',
    dependents: [
      {
        derivedId: 'recruiter-project-overview',
        derivedPath: 'docs/generated/recruiter/project-overview.mdx',
        contract: 'GenerateRecruiterPage',
        recordedHash: 'sha256:8db3f04553bab7dc6084680768d215c4ce19922dc5f7d7d3e05c4eea4058989a',
      },
      {
        derivedId: 'q-001-canonical-separation',
        derivedPath: 'docs/generated/questions/q-001-canonical-separation.mdx',
        contract: 'GenerateQuestionPage',
        recordedHash: 'sha256:8db3f04553bab7dc6084680768d215c4ce19922dc5f7d7d3e05c4eea4058989a',
      },
      {
        derivedId: 'interview-architecture-content-planes',
        derivedPath: 'docs/generated/interview/architecture-content-planes.interview.json',
        contract: 'GenerateInterviewPrep',
        recordedHash: 'sha256:8db3f04553bab7dc6084680768d215c4ce19922dc5f7d7d3e05c4eea4058989a',
      },
    ],
  },
  {
    canonicalId: 'security-trust-boundaries',
    canonicalPath: 'docs/source/security/trust-boundaries.md',
    currentHash: 'sha256:c0cca6dafec52ba6df0f8f477c5d8331eff745562f491a87563006499eff1677',
    dependents: [
      {
        derivedId: 'q-003-security-trust-zones',
        derivedPath: 'docs/generated/questions/q-003-security-trust-zones.mdx',
        contract: 'GenerateQuestionPage',
        recordedHash: 'sha256:c0cca6dafec52ba6df0f8f477c5d8331eff745562f491a87563006499eff1677',
      },
      {
        derivedId: 'interview-security-trust-boundaries',
        derivedPath: 'docs/generated/interview/security-trust-boundaries.interview.json',
        contract: 'GenerateInterviewPrep',
        recordedHash: 'sha256:c0cca6dafec52ba6df0f8f477c5d8331eff745562f491a87563006499eff1677',
      },
    ],
  },
  {
    canonicalId: 'validation-drift-detection',
    canonicalPath: 'docs/source/validation/drift-detection.md',
    currentHash: 'sha256:66743e3d517e91ecbc08636c41b4549e1f47811a3e591802f5d1b1c53a0a23db',
    dependents: [
      {
        derivedId: 'q-002-drift-detection',
        derivedPath: 'docs/generated/questions/q-002-drift-detection.mdx',
        contract: 'GenerateQuestionPage',
        recordedHash: 'sha256:66743e3d517e91ecbc08636c41b4549e1f47811a3e591802f5d1b1c53a0a23db',
      },
      {
        derivedId: 'interview-validation-drift-detection',
        derivedPath: 'docs/generated/interview/validation-drift-detection.interview.json',
        contract: 'GenerateInterviewPrep',
        recordedHash: 'sha256:66743e3d517e91ecbc08636c41b4549e1f47811a3e591802f5d1b1c53a0a23db',
      },
    ],
  },
];

export default function DriftInspector(): React.JSX.Element {
  const [nodes, setNodes] = useState<DependencyNode[]>(INITIAL_NODES);
  const [simulatedSource, setSimulatedSource] = useState<string | null>(null);

  const handleSimulateEdit = (canonicalId: string) => {
    setSimulatedSource(canonicalId);
    setNodes((prev) =>
      prev.map((n) => {
        if (n.canonicalId === canonicalId) {
          return {
            ...n,
            isDrifted: true,
            currentHash: 'sha256:MODIFIED_CONTENT_7f9c2d...NEW_BYTES',
          };
        }
        return n;
      }),
    );
  };

  const handleTargetedRegen = () => {
    setSimulatedSource(null);
    setNodes(INITIAL_NODES);
  };

  return (
    <div style={{maxWidth: '1200px', margin: '0 auto', padding: '1.5rem 1rem'}}>
      <div style={{marginBottom: '1.5rem'}}>
        <h1 style={{fontSize: '2rem', marginBottom: '0.5rem'}}>Provenance & Drift Inspector</h1>
        <p style={{color: '#555', fontSize: '1rem', lineHeight: '1.5'}}>
          DOCCAD replaces manual auditing with cryptographic hash tracking. Observe how a byte change in a canonical
          source triggers mechanical staleness detection strictly for its dependent derived views while leaving unrelated views intact.
        </p>
      </div>

      <div style={{display: 'flex', gap: '1rem', alignItems: 'center', marginBottom: '1.5rem', backgroundColor: '#f9f9f9', padding: '1rem', borderRadius: '8px', border: '1px solid #e1e4e8'}}>
        <span style={{fontWeight: 600, fontSize: '0.9rem'}}>Interactive Drift Simulator:</span>
        <button
          onClick={() => handleSimulateEdit('architecture-content-planes')}
          disabled={simulatedSource === 'architecture-content-planes'}
          style={{
            backgroundColor: simulatedSource === 'architecture-content-planes' ? '#ccc' : '#e65100',
            color: '#fff',
            border: 'none',
            borderRadius: '6px',
            padding: '8px 14px',
            cursor: simulatedSource === 'architecture-content-planes' ? 'default' : 'pointer',
            fontSize: '0.85rem',
            fontWeight: 600,
          }}
        >
          ✏️ Simulate Edit on content-planes.md
        </button>
        <button
          onClick={handleTargetedRegen}
          disabled={!simulatedSource}
          style={{
            backgroundColor: simulatedSource ? '#28a745' : '#ccc',
            color: '#fff',
            border: 'none',
            borderRadius: '6px',
            padding: '8px 14px',
            cursor: simulatedSource ? 'pointer' : 'default',
            fontSize: '0.85rem',
            fontWeight: 600,
          }}
        >
          🔄 Run Targeted Regeneration (Reset Drift)
        </button>
      </div>

      <div style={{display: 'flex', flexDirection: 'column', gap: '1.5rem'}}>
        {nodes.map((node) => (
          <div
            key={node.canonicalId}
            style={{
              border: '1px solid #e1e4e8',
              borderRadius: '8px',
              padding: '1.25rem',
              backgroundColor: '#fff',
              borderLeft: node.isDrifted ? '6px solid #e65100' : '6px solid #28a745',
            }}
          >
            {/* Canonical Source Header */}
            <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.75rem'}}>
              <div>
                <span
                  style={{
                    fontSize: '0.75rem',
                    padding: '2px 8px',
                    borderRadius: '4px',
                    backgroundColor: '#e1f0ff',
                    color: '#0052cc',
                    fontWeight: 700,
                    marginRight: '0.5rem',
                  }}
                >
                  CANONICAL SOURCE
                </span>
                <span style={{fontWeight: 700, fontSize: '1.1rem'}}>{node.canonicalId}</span>
                <div style={{fontSize: '0.85rem', color: '#555', marginTop: '4px'}}>
                  File: <code>{node.canonicalPath}</code>
                </div>
              </div>
              <div style={{textAlign: 'right'}}>
                <span
                  style={{
                    padding: '4px 10px',
                    borderRadius: '12px',
                    backgroundColor: node.isDrifted ? '#ffebe6' : '#e6ffed',
                    color: node.isDrifted ? '#de350b' : '#00875a',
                    fontWeight: 700,
                    fontSize: '0.85rem',
                  }}
                >
                  {node.isDrifted ? '⚠️ SOURCE MODIFIED (DRIFT TRIGGERED)' : '✓ DISK HASH CURRENT'}
                </span>
                <div style={{fontSize: '0.75rem', color: '#666', marginTop: '4px'}}>
                  Disk: <code>{node.currentHash.slice(0, 24)}...</code>
                </div>
              </div>
            </div>

            {/* Dependents Table */}
            <h4 style={{fontSize: '0.9rem', marginBottom: '0.5rem', color: '#333'}}>Dependent Derived Views ({node.dependents.length}):</h4>
            <table style={{width: '100%', fontSize: '0.85rem', borderCollapse: 'collapse'}}>
              <thead>
                <tr style={{backgroundColor: '#f3f4f6', borderBottom: '1px solid #ddd', textAlign: 'left'}}>
                  <th style={{padding: '6px 10px'}}>Derived Artifact</th>
                  <th style={{padding: '6px 10px'}}>Contract</th>
                  <th style={{padding: '6px 10px'}}>Recorded Hash</th>
                  <th style={{padding: '6px 10px'}}>Status</th>
                </tr>
              </thead>
              <tbody>
                {node.dependents.map((dep) => {
                  const isStale = node.isDrifted;
                  return (
                    <tr key={dep.derivedId} style={{borderBottom: '1px solid #eee', backgroundColor: isStale ? '#fff8f6' : '#ffffff'}}>
                      <td style={{padding: '8px 10px'}}>
                        <Link to={`/views/${dep.derivedPath.replace('docs/generated/', '').replace('.mdx', '').replace('.interview.json', '')}`}>
                          <code>{dep.derivedPath}</code>
                        </Link>
                      </td>
                      <td style={{padding: '8px 10px'}}>{dep.contract}</td>
                      <td style={{padding: '8px 10px'}}>
                        <code>{dep.recordedHash.slice(0, 18)}...</code>
                      </td>
                      <td style={{padding: '8px 10px'}}>
                        <span
                          style={{
                            padding: '3px 8px',
                            borderRadius: '4px',
                            backgroundColor: isStale ? '#dc3545' : '#28a745',
                            color: '#fff',
                            fontWeight: 600,
                            fontSize: '0.75rem',
                          }}
                        >
                          {isStale ? 'STALE (REQUIRES REGEN)' : 'FRESH'}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        ))}
      </div>
    </div>
  );
}
