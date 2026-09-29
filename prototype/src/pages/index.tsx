import React from 'react';
import Link from '@docusaurus/Link';
import Layout from '@theme/Layout';

export default function Home(): React.JSX.Element {
  return (
    <Layout title="Home" description="DOCCAD: GitHub-Native, AI-Augmented Documentation Ecosystem">
      <main style={{padding: '3rem 1rem', maxWidth: '1200px', margin: '0 auto'}}>
        {/* Hero Section */}
        <section style={{textAlign: 'center', marginBottom: '3.5rem'}}>
          <div
            style={{
              display: 'inline-block',
              padding: '4px 12px',
              borderRadius: '20px',
              backgroundColor: '#e1f0ff',
              color: '#0052cc',
              fontWeight: 700,
              fontSize: '0.85rem',
              marginBottom: '1rem',
            }}
          >
            PROTOTYPE v0.2.0 &bull; OFFLINE DETERMINISTIC DEMO
          </div>
          <h1 style={{fontSize: '2.75rem', fontWeight: 800, marginBottom: '1rem', letterSpacing: '-0.02em'}}>
            DOCCAD Documentation Ecosystem
          </h1>
          <p style={{fontSize: '1.25rem', color: '#4b5563', maxWidth: '780px', margin: '0 auto 2rem', lineHeight: '1.6'}}>
            A GitHub-native, docs-as-code platform transforming canonical engineering knowledge into governed,
            evidence-backed derived views with hash-based drift detection and zero runtime AI dependencies.
          </p>

          <div style={{display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap'}}>
            <Link
              to="/docs/overview"
              style={{
                backgroundColor: '#0052cc',
                color: '#fff',
                padding: '12px 24px',
                borderRadius: '6px',
                fontWeight: 600,
                textDecoration: 'none',
                fontSize: '1rem',
              }}
            >
              Explore Canonical Docs (/docs)
            </Link>
            <Link
              to="/views/recruiter/project-overview"
              style={{
                backgroundColor: '#f3f4f6',
                color: '#1f2937',
                padding: '12px 24px',
                borderRadius: '6px',
                fontWeight: 600,
                textDecoration: 'none',
                fontSize: '1rem',
                border: '1px solid #d1d5db',
              }}
            >
              Recruiter Briefing (30s / 2m / Deep)
            </Link>
            <Link
              to="/workbench"
              style={{
                backgroundColor: '#10b981',
                color: '#fff',
                padding: '12px 24px',
                borderRadius: '6px',
                fontWeight: 600,
                textDecoration: 'none',
                fontSize: '1rem',
              }}
            >
              Question Workbench &rarr;
            </Link>
          </div>
        </section>

        {/* Metric Highlights */}
        <section
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
            gap: '1.5rem',
            marginBottom: '3.5rem',
            textAlign: 'center',
          }}
        >
          <div style={{padding: '1.5rem', borderRadius: '8px', backgroundColor: '#f9fafb', border: '1px solid #e5e7eb'}}>
            <div style={{fontSize: '2.25rem', fontWeight: 800, color: '#0052cc'}}>29</div>
            <div style={{fontWeight: 600, color: '#374151', marginTop: '4px'}}>Canonical Documents</div>
            <div style={{fontSize: '0.8rem', color: '#6b7280'}}>Human-authored ground truth under /docs</div>
          </div>
          <div style={{padding: '1.5rem', borderRadius: '8px', backgroundColor: '#f9fafb', border: '1px solid #e5e7eb'}}>
            <div style={{fontSize: '2.25rem', fontWeight: 800, color: '#6f42c1'}}>11</div>
            <div style={{fontWeight: 600, color: '#374151', marginTop: '4px'}}>Governed Derived Views</div>
            <div style={{fontSize: '0.8rem', color: '#6b7280'}}>Recruiter, interview & question pages under /views</div>
          </div>
          <div style={{padding: '1.5rem', borderRadius: '8px', backgroundColor: '#f9fafb', border: '1px solid #e5e7eb'}}>
            <div style={{fontSize: '2.25rem', fontWeight: 800, color: '#059669'}}>100%</div>
            <div style={{fontWeight: 600, color: '#374151', marginTop: '4px'}}>Offline Static Serving</div>
            <div style={{fontSize: '0.8rem', color: '#6b7280'}}>Zero runtime LLM calls, keys, or outages</div>
          </div>
          <div style={{padding: '1.5rem', borderRadius: '8px', backgroundColor: '#f9fafb', border: '1px solid #e5e7eb'}}>
            <div style={{fontSize: '2.25rem', fontWeight: 800, color: '#d97706'}}>sha256</div>
            <div style={{fontWeight: 600, color: '#374151', marginTop: '4px'}}>Mechanical Drift Tracking</div>
            <div style={{fontSize: '0.8rem', color: '#6b7280'}}>Targeted regeneration of affected derivatives only</div>
          </div>
        </section>

        {/* Persona Journey Grid */}
        <section style={{marginBottom: '3.5rem'}}>
          <h2 style={{fontSize: '1.75rem', fontWeight: 700, marginBottom: '1.5rem', textAlign: 'center'}}>
            Audience-Specific Documentation Journeys
          </h2>
          <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1.5rem'}}>
            <div style={{padding: '1.5rem', borderRadius: '8px', border: '1px solid #e5e7eb', backgroundColor: '#fff'}}>
              <h3 style={{fontSize: '1.2rem', marginBottom: '0.5rem'}}>Architect & Engineer</h3>
              <p style={{fontSize: '0.9rem', color: '#4b5563', lineHeight: '1.5', marginBottom: '1rem'}}>
                Inspect canonical architecture spine, ADRs, trust boundaries, and component interaction models.
              </p>
              <Link to="/docs/architecture/system-overview" style={{fontWeight: 600, color: '#0052cc'}}>
                System Architecture &rarr;
              </Link>
            </div>

            <div style={{padding: '1.5rem', borderRadius: '8px', border: '1px solid #e5e7eb', backgroundColor: '#fff'}}>
              <h3 style={{fontSize: '1.2rem', marginBottom: '0.5rem'}}>Recruiter & Evaluator</h3>
              <p style={{fontSize: '0.9rem', color: '#4b5563', lineHeight: '1.5', marginBottom: '1rem'}}>
                Review the 30s executive summary, 2m technical walkthrough, and evidence links mapping competencies.
              </p>
              <Link to="/views/recruiter/project-overview" style={{fontWeight: 600, color: '#0052cc'}}>
                Recruiter Profile &rarr;
              </Link>
            </div>

            <div style={{padding: '1.5rem', borderRadius: '8px', border: '1px solid #e5e7eb', backgroundColor: '#fff'}}>
              <h3 style={{fontSize: '1.2rem', marginBottom: '0.5rem'}}>Interviewer & Candidate</h3>
              <p style={{fontSize: '0.9rem', color: '#4b5563', lineHeight: '1.5', marginBottom: '1rem'}}>
                Explore collapsible interview cards detailing system concepts, design trade-offs, and sample Q&A.
              </p>
              <Link to="/views/interview/architecture-system-overview" style={{fontWeight: 600, color: '#0052cc'}}>
                Interview Preparation &rarr;
              </Link>
            </div>

            <div style={{padding: '1.5rem', borderRadius: '8px', border: '1px solid #e5e7eb', backgroundColor: '#fff'}}>
              <h3 style={{fontSize: '1.2rem', marginBottom: '0.5rem'}}>Reviewer & Contributor</h3>
              <p style={{fontSize: '0.9rem', color: '#4b5563', lineHeight: '1.5', marginBottom: '1rem'}}>
                Execute deterministic question generation, inspect source hashes, and simulate review approvals.
              </p>
              <Link to="/workbench" style={{fontWeight: 600, color: '#0052cc'}}>
                Open Workbench &rarr;
              </Link>
            </div>
          </div>
        </section>

        {/* Feature Strip */}
        <section
          style={{
            backgroundColor: '#f8fafc',
            borderRadius: '12px',
            padding: '2rem',
            border: '1px solid #e2e8f0',
            textAlign: 'center',
          }}
        >
          <h3 style={{fontSize: '1.3rem', marginBottom: '0.75rem'}}>Explore Platform Tooling</h3>
          <p style={{color: '#64748b', fontSize: '0.95rem', maxWidth: '640px', margin: '0 auto 1.5rem'}}>
            Access the full catalog of documentation or inspect real-time dependency graph freshness.
          </p>
          <div style={{display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap'}}>
            <Link
              to="/explorer"
              style={{
                padding: '8px 18px',
                borderRadius: '6px',
                backgroundColor: '#fff',
                border: '1px solid #cbd5e1',
                fontWeight: 600,
                color: '#1e293b',
                textDecoration: 'none',
              }}
            >
              🔍 Knowledge Explorer
            </Link>
            <Link
              to="/inspector"
              style={{
                padding: '8px 18px',
                borderRadius: '6px',
                backgroundColor: '#fff',
                border: '1px solid #cbd5e1',
                fontWeight: 600,
                color: '#1e293b',
                textDecoration: 'none',
              }}
            >
              🔄 Drift Inspector
            </Link>
          </div>
        </section>
      </main>
    </Layout>
  );
}
