import { useEffect, useRef, useState } from 'react';
import { Document, Page } from 'react-pdf';
import 'react-pdf/dist/Page/AnnotationLayer.css';
import 'react-pdf/dist/Page/TextLayer.css';
import styled from 'styled-components';

const PdfWrapper = styled.div`
      width: 100%;
      position: relative;
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
    const wrapperRef = useRef<HTMLDivElement>(null);
    const [containerWidth, setContainerWidth] = useState<number | null>(null);

    useEffect(() => {
        const observer = new ResizeObserver(entries => {
            const entry = entries[0];
            if (entry) {
                setContainerWidth(entry.contentRect.width);
            }
        });

        if (wrapperRef.current) {
            observer.observe(wrapperRef.current);
        }

        return () => {
            observer.disconnect();
        };
    }, []);

    function onDocumentLoadSuccess({ numPages }: { numPages: number }) {
        setNumPages(numPages);
    }

    const fileUrl = `/api/documents/${documentId}`;

    return (
        <PdfWrapper ref={wrapperRef}>
            <Document
                file={fileUrl}
                onLoadSuccess={onDocumentLoadSuccess}
                loading={<LoadingWrapper>Loading PDF...</LoadingWrapper>}
                error={<LoadingWrapper>Failed to load PDF.</LoadingWrapper>}
            >

                {Array.from(new Array(numPages || 0), (el, index) => (
                    <Page
                        key={`page_${index + 1}`}
                        pageNumber={index + 1}
                        width={containerWidth ? containerWidth : undefined}
                        renderAnnotationLayer={false}
                        renderTextLayer={false}
                    />
                ))}
            </Document>
        </PdfWrapper>
    );
}