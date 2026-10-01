import React from 'react';
import Link from '@docusaurus/Link';
import Layout from '@theme/Layout';
import Translate, {translate} from '@docusaurus/Translate';

export default function Home(): React.JSX.Element {
  return (
    <Layout
      title={translate({id: 'homepage.title', message: 'Home'})}
      description={translate({
        id: 'homepage.description',
        message: 'DOCCAD: GitHub-Native, AI-Augmented Documentation Ecosystem',
      })}
    >
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
            <Translate id="homepage.hero.badge" description="Badge in hero section">
              PROTOTYPE v0.2.0 • OFFLINE DETERMINISTIC DEMO
            </Translate>
          </div>
          <h1 style={{fontSize: '2.75rem', fontWeight: 800, marginBottom: '1rem', letterSpacing: '-0.02em'}}>
            <Translate id="homepage.hero.title" description="Title in hero section">
              DOCCAD Documentation Ecosystem
            </Translate>
          </h1>
          <p style={{fontSize: '1.25rem', color: '#4b5563', maxWidth: '780px', margin: '0 auto 2rem', lineHeight: '1.6'}}>
            <Translate id="homepage.hero.subtitle" description="Subtitle in hero section">
              A GitHub-native, docs-as-code platform transforming canonical engineering knowledge into governed, evidence-backed derived views with hash-based drift detection and zero runtime AI dependencies.
            </Translate>
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
              <Translate id="homepage.hero.button.explore" description="Button to explore canonical docs">
                Explore Canonical Docs (/docs)
              </Translate>
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
              <Translate id="homepage.hero.button.recruiter" description="Button for recruiter briefing">
                Recruiter Briefing (30s / 2m / Deep)
              </Translate>
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
              <Translate id="homepage.hero.button.workbench" description="Button for question workbench">
                Question Workbench &rarr;
              </Translate>
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
            <div style={{fontWeight: 600, color: '#374151', marginTop: '4px'}}>
              <Translate id="homepage.metrics.canonical.title" description="Metric label for canonical documents">
                Canonical Documents
              </Translate>
            </div>
            <div style={{fontSize: '0.8rem', color: '#6b7280'}}>
              <Translate id="homepage.metrics.canonical.desc" description="Metric description for canonical documents">
                Human-authored ground truth under /docs
              </Translate>
            </div>
          </div>
          <div style={{padding: '1.5rem', borderRadius: '8px', backgroundColor: '#f9fafb', border: '1px solid #e5e7eb'}}>
            <div style={{fontSize: '2.25rem', fontWeight: 800, color: '#6f42c1'}}>11</div>
            <div style={{fontWeight: 600, color: '#374151', marginTop: '4px'}}>
              <Translate id="homepage.metrics.derived.title" description="Metric label for derived views">
                Governed Derived Views
              </Translate>
            </div>
            <div style={{fontSize: '0.8rem', color: '#6b7280'}}>
              <Translate id="homepage.metrics.derived.desc" description="Metric description for derived views">
                Recruiter, interview & question pages under /views
              </Translate>
            </div>
          </div>
          <div style={{padding: '1.5rem', borderRadius: '8px', backgroundColor: '#f9fafb', border: '1px solid #e5e7eb'}}>
            <div style={{fontSize: '2.25rem', fontWeight: 800, color: '#059669'}}>100%</div>
            <div style={{fontWeight: 600, color: '#374151', marginTop: '4px'}}>
              <Translate id="homepage.metrics.offline.title" description="Metric label for offline static serving">
                Offline Static Serving
              </Translate>
            </div>
            <div style={{fontSize: '0.8rem', color: '#6b7280'}}>
              <Translate id="homepage.metrics.offline.desc" description="Metric description for offline static serving">
                Zero runtime LLM calls, keys, or outages
              </Translate>
            </div>
          </div>
          <div style={{padding: '1.5rem', borderRadius: '8px', backgroundColor: '#f9fafb', border: '1px solid #e5e7eb'}}>
            <div style={{fontSize: '2.25rem', fontWeight: 800, color: '#d97706'}}>sha256</div>
            <div style={{fontWeight: 600, color: '#374151', marginTop: '4px'}}>
              <Translate id="homepage.metrics.drift.title" description="Metric label for drift tracking">
                Mechanical Drift Tracking
              </Translate>
            </div>
            <div style={{fontSize: '0.8rem', color: '#6b7280'}}>
              <Translate id="homepage.metrics.drift.desc" description="Metric description for drift tracking">
                Targeted regeneration of affected derivatives only
              </Translate>
            </div>
          </div>
        </section>

        {/* Persona Journey Grid */}
        <section style={{marginBottom: '3.5rem'}}>
          <h2 style={{fontSize: '1.75rem', fontWeight: 700, marginBottom: '1.5rem', textAlign: 'center'}}>
            <Translate id="homepage.personas.title" description="Header for persona journeys">
              Audience-Specific Documentation Journeys
            </Translate>
          </h2>
          <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1.5rem'}}>
            <div style={{padding: '1.5rem', borderRadius: '8px', border: '1px solid #e5e7eb', backgroundColor: '#fff'}}>
              <h3 style={{fontSize: '1.2rem', marginBottom: '0.5rem'}}>
                <Translate id="homepage.personas.architect.title" description="Title for architect persona">
                  Architect & Engineer
                </Translate>
              </h3>
              <p style={{fontSize: '0.9rem', color: '#4b5563', lineHeight: '1.5', marginBottom: '1rem'}}>
                <Translate id="homepage.personas.architect.desc" description="Description for architect persona">
                  Inspect canonical architecture spine, ADRs, trust boundaries, and component interaction models.
                </Translate>
              </p>
              <Link to="/docs/architecture/system-overview" style={{fontWeight: 600, color: '#0052cc'}}>
                <Translate id="homepage.personas.architect.link" description="Link text for architect persona">
                  System Architecture &rarr;
                </Translate>
              </Link>
            </div>

            <div style={{padding: '1.5rem', borderRadius: '8px', border: '1px solid #e5e7eb', backgroundColor: '#fff'}}>
              <h3 style={{fontSize: '1.2rem', marginBottom: '0.5rem'}}>
                <Translate id="homepage.personas.recruiter.title" description="Title for recruiter persona">
                  Recruiter & Evaluator
                </Translate>
              </h3>
              <p style={{fontSize: '0.9rem', color: '#4b5563', lineHeight: '1.5', marginBottom: '1rem'}}>
                <Translate id="homepage.personas.recruiter.desc" description="Description for recruiter persona">
                  Review the 30s executive summary, 2m technical walkthrough, and evidence links mapping competencies.
                </Translate>
              </p>
              <Link to="/views/recruiter/project-overview" style={{fontWeight: 600, color: '#0052cc'}}>
                <Translate id="homepage.personas.recruiter.link" description="Link text for recruiter persona">
                  Recruiter Profile &rarr;
                </Translate>
              </Link>
            </div>

            <div style={{padding: '1.5rem', borderRadius: '8px', border: '1px solid #e5e7eb', backgroundColor: '#fff'}}>
              <h3 style={{fontSize: '1.2rem', marginBottom: '0.5rem'}}>
                <Translate id="homepage.personas.interviewer.title" description="Title for interviewer persona">
                  Interviewer & Candidate
                </Translate>
              </h3>
              <p style={{fontSize: '0.9rem', color: '#4b5563', lineHeight: '1.5', marginBottom: '1rem'}}>
                <Translate id="homepage.personas.interviewer.desc" description="Description for interviewer persona">
                  Explore collapsible interview cards detailing system concepts, design trade-offs, and sample Q&A.
                </Translate>
              </p>
              <Link to="/views/interview/architecture-system-overview" style={{fontWeight: 600, color: '#0052cc'}}>
                <Translate id="homepage.personas.interviewer.link" description="Link text for interviewer persona">
                  Interview Preparation &rarr;
                </Translate>
              </Link>
            </div>

            <div style={{padding: '1.5rem', borderRadius: '8px', border: '1px solid #e5e7eb', backgroundColor: '#fff'}}>
              <h3 style={{fontSize: '1.2rem', marginBottom: '0.5rem'}}>
                <Translate id="homepage.personas.reviewer.title" description="Title for reviewer persona">
                  Reviewer & Contributor
                </Translate>
              </h3>
              <p style={{fontSize: '0.9rem', color: '#4b5563', lineHeight: '1.5', marginBottom: '1rem'}}>
                <Translate id="homepage.personas.reviewer.desc" description="Description for reviewer persona">
                  Execute deterministic question generation, inspect source hashes, and simulate review approvals.
                </Translate>
              </p>
              <Link to="/workbench" style={{fontWeight: 600, color: '#0052cc'}}>
                <Translate id="homepage.personas.reviewer.link" description="Link text for reviewer persona">
                  Open Workbench &rarr;
                </Translate>
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
          <h3 style={{fontSize: '1.3rem', marginBottom: '0.75rem'}}>
            <Translate id="homepage.features.title" description="Title for platform tooling section">
              Explore Platform Tooling
            </Translate>
          </h3>
          <p style={{color: '#64748b', fontSize: '0.95rem', maxWidth: '640px', margin: '0 auto 1.5rem'}}>
            <Translate id="homepage.features.desc" description="Description for platform tooling section">
              Access the full catalog of documentation or inspect real-time dependency graph freshness.
            </Translate>
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
              <Translate id="homepage.features.explorer" description="Button label for knowledge explorer">
                🔍 Knowledge Explorer
              </Translate>
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
              <Translate id="homepage.features.inspector" description="Button label for drift inspector">
                🔄 Drift Inspector
              </Translate>
            </Link>
          </div>
        </section>
      </main>
    </Layout>
  );
}
