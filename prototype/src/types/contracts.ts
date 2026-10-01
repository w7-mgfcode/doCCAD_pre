/**
 * Shared DOCCAD Contracts & Types
 */

export interface SourceReference {
  id: string;
  path: string;
  content_hash: string;
}

export interface DocumentFrontmatter {
  id: string;
  slug?: string;
  title: string;
  type: 'canonical' | 'generated' | 'stub';
  stub_version?: number;
  hold_reason?: string;
  audience: Array<'developer' | 'architect' | 'operator' | 'user' | 'recruiter' | 'interviewer' | 'reviewer'>;
  sources?: string[];
  owners: string[];
  related?: string[];
  ai_generation?: {
    allowed: boolean;
    derived_pages?: string[];
  };
  last_validated?: string;
  generated?: boolean;
  generation?: {
    contract: string;
    contract_version: number;
    prompt_version: string;
    source_documents: SourceReference[];
    repo_evidence?: string[];
    provider: 'anthropic' | 'gemini' | 'openai' | 'local' | 'fixture';
    model: string;
    generation_mode?: 'production' | 'demo';
    generated_at: string;
    approval_status: 'draft' | 'in-review' | 'approved' | 'approved-for-demo' | 'rejected';
  };
}

export interface QuestionRequest {
  question: string;
  audience: 'developer' | 'architect' | 'operator' | 'user' | 'recruiter' | 'interviewer' | 'reviewer';
  privacy_class: 'public' | 'private';
  target_id?: string;
}

export interface ReviewRecord {
  artifact_id: string;
  path: string;
  approval_state: 'draft' | 'in-review' | 'approved-for-demo' | 'rejected';
  reviewed_by: string;
  reviewed_at: string;
  notes?: string;
  is_simulated: boolean;
  eligible_for_production: boolean;
}

export interface ValidationResult {
  artifact_id: string;
  path: string;
  valid: boolean;
  errors: string[];
  warnings: string[];
  checked_at: string;
}

export interface GenerationRun {
  run_id: string;
  contract: string;
  contract_version: number;
  prompt_version: string;
  provider: string;
  model: string;
  mode: 'production' | 'demo';
  target_id?: string;
  evidence_files: SourceReference[];
  rejected_files: string[];
  started_at: string;
  completed_at: string;
  status: 'success' | 'insufficient_evidence' | 'failed';
  candidate_path?: string;
  output_text?: string;
}

export interface DependencyManifest {
  pages: Array<{
    id: string;
    path: string;
    type: 'canonical' | 'generated' | 'generated-data' | 'stub';
    content_hash: string;
    sources: string[];
    related: string[];
    derived_pages?: string[];
    generation?: {
      contract: string;
      source_documents: SourceReference[];
    };
  }>;
}
