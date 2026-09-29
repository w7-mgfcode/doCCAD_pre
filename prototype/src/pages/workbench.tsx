import React from 'react';
import Layout from '@theme/Layout';
import QuestionWorkbench from '@site/src/components/QuestionWorkbench';

export default function WorkbenchPage(): React.JSX.Element {
  return (
    <Layout title="Question Workbench" description="Interactive DOCCAD Question & Governance Workbench">
      <QuestionWorkbench />
    </Layout>
  );
}
