import React, {type ReactNode} from 'react';

export interface ProvenanceProps {
  contract?: string;
  contractVersion?: number;
  promptVersion?: string;
  provider?: string;
  model?: string;
  generationMode?: string;
  status?: string;
  sourceDocuments?: Array<{id: string; path: string; content_hash: string}>;
}

export default function ProvenanceBanner({
  contract = 'GenerateQuestionPage',
  contractVersion = 1,
  promptVersion = 'question-page.v1',
  provider = 'fixture',
  model = 'deterministic-demo-fixture',
  generationMode = 'demo',
  status = 'approved-for-demo',
  sourceDocuments = [],
}: ProvenanceProps): ReactNode {
  return (
    <div
      style={{
        border: '1px solid #0052cc',
        borderRadius: '6px',
        padding: '0.85rem 1.15rem',
        marginBottom: '1.5rem',
        backgroundColor: 'rgba(0, 82, 204, 0.05)',
      }}
    >
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem'}}>
        <span style={{fontWeight: 700, color: '#0052cc', fontSize: '0.95rem'}}>
          GOVERNED AI ARTIFACT &mdash; PROVENANCE RECORD
        </span>
        <span
          style={{
            fontSize: '0.8rem',
            padding: '2px 8px',
            borderRadius: '12px',
            backgroundColor: status === 'approved-for-demo' ? '#28a745' : '#ffc107',
            color: status === 'approved-for-demo' ? '#fff' : '#000',
            fontWeight: 600,
          }}
        >
          {status.toUpperCase()}
        </span>
      </div>
      <div style={{fontSize: '0.85rem', lineHeight: '1.45'}}>
        <div>
          <strong>Task Contract:</strong> <code>{contract} v{contractVersion}</code> &bull;{' '}
          <strong>Prompt:</strong> <code>{promptVersion}</code> &bull;{' '}
          <strong>Provider:</strong> <code>{provider}</code> ({model}) &bull;{' '}
          <strong>Mode:</strong> <code>{generationMode}</code>
        </div>
        {sourceDocuments.length > 0 && (
          <div style={{marginTop: '0.35rem'}}>
            <strong>Grounded Evidence ({sourceDocuments.length} files):</strong>{' '}
            {sourceDocuments.map((s, idx) => (
              <span key={s.id} style={{marginRight: '0.5rem'}}>
                <code>{s.id}</code>
                <span style={{fontSize: '0.75rem', color: '#666'}}> ({s.content_hash.slice(0, 16)}...)</span>
                {idx < sourceDocuments.length - 1 ? ',' : ''}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
