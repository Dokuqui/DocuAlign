import { useState } from 'react';
import { Document, Page } from 'react-pdf';
import 'react-pdf/dist/Page/AnnotationLayer.css';
import 'react-pdf/dist/Page/TextLayer.css';
import styled from 'styled-components';

const PdfWrapper = styled.div`
      border: 1px solid #eee;
      margin-top: 2rem;
      max-height: 70vh;
      overflow-y: auto;
    `;

const LoadingWrapper = styled.div`
      padding: 2rem;
      color: #888;
    `;

type PdfViewerProps = {
    documentId: string;
};

export function PdfViewer({ documentId }: PdfViewerProps) {
    const [numPages, setNumPages] = useState<number | null>(null);

    function onDocumentLoadSuccess({ numPages }: { numPages: number }) {
        setNumPages(numPages);
    }

    const fileUrl = `/api/documents/${documentId}`;

    return (
        <PdfWrapper>
            <Document
                file={fileUrl}
                onLoadSuccess={onDocumentLoadSuccess}
                loading={<LoadingWrapper>Loading PDF...</LoadingWrapper>}
                error={<LoadingWrapper>Failed to load PDF.</LoadingWrapper>}
            >
                <Page pageNumber={1} />
            </Document>
            <p>
                Page 1 of {numPages}
            </p>
        </PdfWrapper>
    );
}