import { useState } from 'react';
import styled from 'styled-components';
import { FileUpload } from './components/FileUpload';
import { PdfViewer } from './components/PdfViewer';

const AppContainer = styled.main`
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
`;

const Card = styled.section`
  background-color: var(--color-card-bg);
  border: 1px solid var(--color-card-border);
  border-radius: 12px;
  padding: 2rem;
  
  /* Add some nice spacing between cards */
  & + & {
    margin-top: 2rem;
  }
`;

function App() {
  const [documentId, setDocumentId] = useState<string | null>(null);

  return (
    <AppContainer>
      <h1>DocuAlign 📄</h1>

      <Card>
        <FileUpload
          onUploadSuccess={(id) => setDocumentId(id)}
        />
      </Card>

      {documentId && (
        <Card>
          <h2>PDF Preview</h2>
          <PdfViewer documentId={documentId} />
        </Card>
      )}
    </AppContainer>
  )
}

export default App