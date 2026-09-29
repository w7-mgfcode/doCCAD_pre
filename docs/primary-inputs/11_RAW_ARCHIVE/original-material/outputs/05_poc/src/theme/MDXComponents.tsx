import MDXComponents from '@theme-original/MDXComponents';
import InterviewPrep from '@site/src/components/InterviewPrep';
import EvidenceLink from '@site/src/components/EvidenceLink';

// Global MDX scope: generated MDX pages can use <InterviewPrep> and <EvidenceLink>
// without import statements, which keeps model output templates simpler and keeps
// import surface out of the generation contract (AD-6).
export default {
  ...MDXComponents,
  InterviewPrep,
  EvidenceLink,
};
