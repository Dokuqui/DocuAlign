import { useState, type ChangeEvent } from 'react';
import axios from 'axios';
import styled from 'styled-components';

const UploadBox = styled.div`
  border: 2px dashed #ccc;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
  cursor: pointer;

  &:hover {
    border-color: #646cff;
  }
`;

const StyledButton = styled.button`
  margin-top: 1rem;
`;

type FileUploadProps = {
    onUploadSuccess: (documentId: string) => void;
};

export function FileUpload({ onUploadSuccess }: FileUploadProps) {
    const [file, setFile] = useState<File | null>(null);
    const [message, setMessage] = useState('Click or drag file to upload');

    const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
            setMessage(`File selected: ${e.target.files[0].name}`);
        }
    };

    const handleUpload = async () => {
        if (!file) {
            setMessage('Please select a file first!');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            setMessage('Uploading...');
            const response = await axios.post('/api/documents/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            const newId = response.data.documentId;
            setMessage(`Upload successful! Document ID: ${newId}`);
            setFile(null);

            onUploadSuccess(newId);
        } catch (error) {
            console.error(error);
            setMessage('Upload failed. See console for details.');
        }
    };

    return (
        <div>
            <UploadBox>
                <input
                    type="file"
                    onChange={handleFileChange}
                    accept="application/pdf"
                    style={{ display: 'none' }}
                    id="file-upload"
                />
                <label htmlFor="file-upload">
                    <p>{message}</p>
                </label>
            </UploadBox>
            <StyledButton onClick={handleUpload} disabled={!file}>
                Upload
            </StyledButton>
        </div>
    );
}