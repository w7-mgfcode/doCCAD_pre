import React from 'react';
import Layout from '@theme/Layout';
import KnowledgeExplorer from '@site/src/components/KnowledgeExplorer';

export default function ExplorerPage(): React.JSX.Element {
  return (
    <Layout title="Knowledge Explorer" description="Searchable Knowledge Explorer for DOCCAD">
      <KnowledgeExplorer />
    </Layout>
  );
}
