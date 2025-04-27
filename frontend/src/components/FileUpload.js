// frontend/src/components/FileUpload.js
import React, { useState } from 'react';
import { uploadDocument } from '../api';

const FileUpload = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setMessage('');
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage('Please select a file first');
      return;
    }

    setUploading(true);
    try {
      const result = await uploadDocument(file);
      setMessage(result.message);
      setFile(null);
      if (onUploadSuccess) {
        onUploadSuccess(result);
      }
    } catch (error) {
      setMessage('Error uploading file: ' + (error.response?.data?.message || error.message));
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="file-upload">
      <h3>Upload Document</h3>
      <input
        type="file"
        onChange={handleFileChange}
        accept=".txt,.pdf"
        disabled={uploading}
      />
      <button onClick={handleUpload} disabled={!file || uploading}>
        {uploading ? 'Uploading...' : 'Upload'}
      </button>
      {message && <p className={message.includes('Error') ? 'error' : 'success'}>{message}</p>}
    </div>
  );
};

export default FileUpload;


