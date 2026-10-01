import React, {type ReactNode} from 'react';
import Link from '@docusaurus/Link';

// Mirrors schemas/interview.schema.json (ai_architecture §7). Keep in sync by hand:
// the JSON is validated by scripts/validate_docs.py; this type only aids rendering.
export interface InterviewConcept {
  name: string;
  explanation: string;
}

export interface InterviewDesignDecision {
  decision: string;
  rationale: string;
  evidence: string; // canonical doc id or ADR id
}

export interface InterviewTradeoff {
  choice: string;
  benefit: string;
  cost: string;
}

export interface InterviewExampleAnswer {
  question: string;
  answer: string;
}

export interface InterviewEvidenceLink {
  label: string;
  to: string;
}

export interface InterviewGenerationProvenance {
  contract: string;
  contract_version: number;
  prompt_version: string;
  provider: string;
  model: string;
  generated_at: string;
  approval_status: 'draft' | 'in-review' | 'approved';
  source_documents: Array<{id: string; path: string; content_hash: string}>;
}

export interface InterviewData {
  id: string;
  elevator_pitch: string;
  technical_explanation: string;
  concepts: InterviewConcept[];
  design_decisions: InterviewDesignDecision[];
  tradeoffs: InterviewTradeoff[];
  likely_questions: string[];
  example_answers: InterviewExampleAnswer[];
  follow_ups: string[];
  evidence_links: InterviewEvidenceLink[];
  generation?: InterviewGenerationProvenance;
}

function Section({title, children}: {title: string; children: ReactNode}) {
  return (
    <details className="poc-interview-section" open={false}>
      <summary>{title}</summary>
      <div>{children}</div>
    </details>
  );
}

declare const require: any;

let interviewMap: Record<string, InterviewData> = {};
try {
  const context = require.context('@site/docs/generated/interview', false, /\.interview\.json$/);
  context.keys().forEach((key: string) => {
    const d = context(key);
    const baseId = key.replace(/^\.\//, '').replace(/\.interview\.json$/, '');
    interviewMap[baseId] = d;
    if (d && d.id) {
      interviewMap[d.id] = d;
    }
  });
} catch {
  // Directory may be stashed during production build or context unavailable
}

/**
 * InterviewPrep — renders a generated interview-preparation dataset (AD-11:
 * build-time artifact, no runtime AI). Data is committed JSON under
 * docs/generated/interview/, validated against schemas/interview.schema.json in CI.
 * Can be loaded by id (preferred to eliminate MDX imports) or passed data directly.
 */
export default function InterviewPrep({id, data}: {id?: string; data?: InterviewData}): ReactNode {
  const resolved = data || (id ? interviewMap[id] : undefined);
  if (!resolved) {
    return (
      <div className="poc-provenance-banner">
        <em>Interview dataset not loaded or currently on hold.</em>
      </div>
    );
  }

  const g = resolved.generation;
  return (
    <div>
      {g && (
        <div className="poc-provenance-banner">
          <strong>AI-generated content.</strong> Contract {g.contract} v{g.contract_version} (
          {g.prompt_version}), provider {g.provider}, model {g.model}, generated {g.generated_at},
          status <em>{g.approval_status}</em>. Derived from{' '}
          {g.source_documents.map((s) => s.id).join(', ')}; verify against the canonical pages
          linked below.
        </div>
      )}

      <Section title="Elevator pitch (30s)">
        <p>{resolved.elevator_pitch}</p>
      </Section>

      <Section title="Technical explanation (2min)">
        <p>{resolved.technical_explanation}</p>
      </Section>

      <Section title="Key concepts">
        <ul>
          {resolved.concepts.map((c) => (
            <li key={c.name}>
              <strong>{c.name}:</strong> {c.explanation}
            </li>
          ))}
        </ul>
      </Section>

      <Section title="Design decisions">
        <ul>
          {resolved.design_decisions.map((d) => (
            <li key={d.decision}>
              <strong>{d.decision}</strong> — {d.rationale}{' '}
              <em>(evidence: {d.evidence})</em>
            </li>
          ))}
        </ul>
      </Section>

      <Section title="Trade-offs">
        <ul>
          {resolved.tradeoffs.map((t) => (
            <li key={t.choice}>
              <strong>{t.choice}</strong>: + {t.benefit} / − {t.cost}
            </li>
          ))}
        </ul>
      </Section>

      <Section title="Likely questions">
        <ul>
          {resolved.likely_questions.map((q) => (
            <li key={q}>{q}</li>
          ))}
        </ul>
      </Section>

      <Section title="Example answers">
        {resolved.example_answers.map((ea) => (
          <div key={ea.question} style={{marginBottom: '0.75rem'}}>
            <p>
              <strong>Q:</strong> {ea.question}
            </p>
            <p>
              <strong>A:</strong> {ea.answer}
            </p>
          </div>
        ))}
      </Section>

      <Section title="Follow-up topics">
        <ul>
          {resolved.follow_ups.map((f) => (
            <li key={f}>{f}</li>
          ))}
        </ul>
      </Section>

      <h2>Evidence</h2>
      <ul>
        {resolved.evidence_links.map((e) => (
          <li key={e.to}>
            <Link to={e.to} className="poc-evidence-link">
              {e.label}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
