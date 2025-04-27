import React, { useState } from 'react';
import { uploadDocument, deleteAllDocuments } from '../api';

const FileUpload = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [deleting, setDeleting] = useState(false);
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
      
      // Clear the file input
      const fileInput = document.querySelector('input[type="file"]');
      if (fileInput) {
        fileInput.value = '';
      }
      
      if (onUploadSuccess) {
        onUploadSuccess({ ...result, action: 'upload' });
      }
    } catch (error) {
      setMessage('Error uploading file: ' + (error.response?.data?.message || error.message));
    } finally {
      setUploading(false);
    }
  };

  const handleDeleteAll = async () => {
    if (window.confirm('Are you sure you want to delete all uploaded documents?')) {
      setDeleting(true);
      try {
        const result = await deleteAllDocuments();
        setMessage(result.message);
        if (onUploadSuccess) {
          onUploadSuccess({ ...result, action: 'delete' });
        }
      } catch (error) {
        setMessage('Error deleting documents: ' + (error.response?.data?.message || error.message));
      } finally {
        setDeleting(false);
      }
    }
  };

  return (
    <div className="file-upload">
      <h3>Document Management</h3>
      <div className="upload-controls">
        <input
          type="file"
          onChange={handleFileChange}
          accept=".txt,.pdf"
          disabled={uploading || deleting}
        />
        <button 
          onClick={handleUpload} 
          disabled={!file || uploading || deleting}
          className="upload-button"
        >
          {uploading ? 'Uploading...' : 'Upload'}
        </button>
        <button 
          onClick={handleDeleteAll} 
          disabled={uploading || deleting}
          className="delete-button"
        >
          {deleting ? 'Deleting...' : 'Delete All Documents'}
        </button>
      </div>
      {message && <p className={message.includes('Error') ? 'error' : 'success'}>{message}</p>}
    </div>
  );
};

export default FileUpload;