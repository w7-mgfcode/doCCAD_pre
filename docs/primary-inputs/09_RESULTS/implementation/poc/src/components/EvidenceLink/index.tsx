import React, {type ReactNode} from 'react';
import Link from '@docusaurus/Link';

export interface EvidenceLinkProps {
  /** Site-relative route of the canonical page backing the claim, e.g. /docs/architecture/system-overview */
  to: string;
  children: ReactNode;
}

/**
 * EvidenceLink — wraps a claim made in AI-generated content and links it to the
 * canonical page that evidences it (AD-15 / ai_architecture §6: every claim in a
 * recruiter view must be evidence-linked; unevidenced claims are prohibited by contract).
 */
export default function EvidenceLink({to, children}: EvidenceLinkProps): ReactNode {
  return (
    <Link to={to} className="poc-evidence-link" title={`Evidence: ${to}`}>
      {children}
    </Link>
  );
}
