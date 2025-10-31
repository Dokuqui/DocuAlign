import { useState } from 'react';
import axios from 'axios';
import styled from 'styled-components';
import type { TextBlock, TextEdit, DocumentEditRequest, DocumentTextBlocks } from '../api/schemas';

const EditorWrapper = styled.div`
  margin-top: 2rem;
  text-align: left;
  max-height: 400px;
  overflow-y: auto;
  border: 1px solid var(--color-card-border);
  padding: 1rem;
  border-radius: 8px;
`;

const BlockInputWrapper = styled.div`
  display: grid;
  grid-template-columns: 40px 1fr;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;

  label {
    font-size: 0.8em;
    color: #888;
    text-align: right;
  }
  
  input {
    width: 100%;
    padding: 0.4em;
    border: 1px solid #ccc;
    border-radius: 4px;
    background-color: var(--color-background);
    color: var(--color-text);
  }
`;

const SaveButton = styled.button`
  margin-top: 1rem;
  width: 100%;
  background-color: var(--color-primary);
  color: white;
  
  &:hover {
    background-color: var(--color-primary-light);
  }
`;

const LoadButton = styled.button`
  width: 100%;
  font-weight: bold;
`;

const ControlsWrapper = styled.div`
  display: flex;
  gap: 1rem;
  align-items: center;
  margin-bottom: 1rem;
  
  select, input {
    padding: 0.4em;
    border: 1px solid #ccc;
    border-radius: 4px;
    background-color: var(--color-background);
    color: var(--color-text);
  }
`;

type DocumentEditorProps = {
    documentId: string;
};

export function DocumentEditor({ documentId }: DocumentEditorProps) {
    const [originalBlocks, setOriginalBlocks] = useState<TextBlock[]>([]);
    const [editedTexts, setEditedTexts] = useState<Record<number, string>>({});
    const [status, setStatus] = useState<'idle' | 'loading' | 'loaded' | 'error' | 'saving'>('idle');
    const [error, setError] = useState<string | null>(null);

    const [fontName, setFontName] = useState('serif');
    const [fontSize, setFontSize] = useState(10);

    const fetchBlocks = async () => {
        if (!documentId) return;

        setStatus('loading');
        setError(null);
        try {
            const response = await axios.get<DocumentTextBlocks>(`/api/documents/${documentId}/ocr-blocks`);
            setOriginalBlocks(response.data.blocks);

            const initialEdits: Record<number, string> = {};
            response.data.blocks.forEach((block, index) => {
                initialEdits[index] = block.text;
            });
            setEditedTexts(initialEdits);
            setStatus('loaded');

        } catch (err) {
            console.error(err);
            setError('Failed to load text blocks. This can take up to a minute for large PDFs.');
            setStatus('error');
        }
    };

    const handleTextChange = (index: number, newText: string) => {
        setEditedTexts(prev => ({
            ...prev,
            [index]: newText,
        }));
    };

    const handleSave = async () => {
        setStatus('saving');
        setError(null);

        const edits: TextEdit[] = [];
        originalBlocks.forEach((block, index) => {
            const originalText = block.text;
            const editedText = editedTexts[index];

            if (originalText !== editedText) {
                edits.push({
                    page_num: block.page_num,
                    redact_coords: [block.x0, block.y0, block.x1, block.y1],
                    insert_coords: [block.x0, block.y0],
                    new_text: editedText,
                });
            }
        });

        if (edits.length === 0) {
            alert("No changes detected!");
            setStatus('loaded');
            return;
        }

        const payload: DocumentEditRequest = {
            edits,
            fontname: fontName,
            fontsize: fontSize
        };

        try {
            const response = await axios.post(
                `/api/documents/${documentId}/edit`,
                payload,
                { responseType: 'blob' }
            );

            const blob = new Blob([response.data], { type: 'application/pdf' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `edited_document_${documentId}.pdf`;
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);

        } catch (err: any) {
            console.error(err);
            if (err.response && err.response.data) {
                const errorData = await (err.response.data as Blob).text();
                const errorJson = JSON.parse(errorData);
                setError(`Save Failed: ${errorJson.detail}`);
            } else {
                setError('Failed to save document. Check backend logs.');
            }
            setStatus('error');
        } finally {
            if (status !== 'error') {
                setStatus('loaded');
            }
        }
    };

    // --- RENDER LOGIC UPDATED ---

    if (status === 'idle') {
        return (
            <EditorWrapper>
                <LoadButton onClick={fetchBlocks}>
                    Load Text Editor
                </LoadButton>
                <p>Click this button to scan the document for all editable text. (This may take a moment)</p>
            </EditorWrapper>
        );
    }

    if (status === 'loading') {
        return (
            <EditorWrapper>
                <p>Loading text blocks... This can take up to a minute for large or high-res scans.</p>
            </EditorWrapper>
        );
    }

    if (status === 'error') {
        return (
            <EditorWrapper>
                <p style={{ color: 'red' }}>{error}</p>
                <LoadButton onClick={fetchBlocks}>Try Loading Again</LoadButton>
            </EditorWrapper>
        );
    }

    return (
        <EditorWrapper>
            <h3>Editable Text Blocks</h3>

            <ControlsWrapper>
                <div>
                    <label htmlFor="font-select">Font: </label>
                    <select
                        id="font-select"
                        value={fontName}
                        onChange={e => setFontName(e.target.value)}
                    >
                        <option value="serif">Serif (like Times)</option>
                        <option value="sans">Sans-Serif (like Arial)</option>
                        <option value="mono">Monospace (like Courier)</option>
                    </select>
                </div>
                <div>
                    <label htmlFor="font-size">Size: </label>
                    <input
                        id="font-size"
                        type="number"
                        value={fontSize}
                        onChange={e => setFontSize(Number(e.target.value))}
                        style={{ width: '60px' }}
                    />
                </div>
            </ControlsWrapper>

            {originalBlocks.map((block, index) => (
                <BlockInputWrapper key={index}>
                    <label>P.{block.page_num}</label>
                    <input
                        type="text"
                        value={editedTexts[index] || ''}
                        onChange={(e) => handleTextChange(index, e.target.value)}
                    />
                </BlockInputWrapper>
            ))}
            <SaveButton onClick={handleSave} disabled={status === 'saving'}>
                {status === 'saving' ? 'Saving...' : 'Save & Download Edited PDF'}
            </SaveButton>
        </EditorWrapper>
    );
}