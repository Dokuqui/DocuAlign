import { useState } from 'react';
import styled from 'styled-components';
import { FileUpload } from './components/FileUpload';
import { PdfViewer } from './components/PdfViewer';
import { DocumentEditor } from './components/DocumentEditor';

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

const EditorLayout = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  text-align: left;
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const PdfPreviewContainer = styled.div`
  width: 100%;
  height: 70vh; /* Give it a fixed height */
  overflow-y: auto; /* Allow scrolling *inside* this box */
  border: 1px solid var(--color-card-border);
  background: #f8f8f8;
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
          <h2>Document Editor</h2>
          <EditorLayout>
            <div>
              <h3>PDF Preview</h3>

              <PdfPreviewContainer>
                <PdfViewer documentId={documentId} />
              </PdfPreviewContainer>
            </div>

            <div>
              <h3>Text Editor</h3>
              <DocumentEditor documentId={documentId} />
            </div>
          </EditorLayout>
        </Card>
      )}
    </AppContainer>
  )
}

export default App