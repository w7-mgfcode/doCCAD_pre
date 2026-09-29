import React from 'react';
import Layout from '@theme/Layout';
import DriftInspector from '@site/src/components/DriftInspector';

export default function InspectorPage(): React.JSX.Element {
  return (
    <Layout title="Drift Inspector" description="Cryptographic Provenance & Drift Inspector">
      <DriftInspector />
    </Layout>
  );
}
