import React, { useState, useEffect } from 'react';
import { getDocuments } from '../api';
import './DocumentList.css';


const DocumentList = () => {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchDocuments = async () => {
    setLoading(true);
    try {
      const result = await getDocuments();
      if (result.status === 'success') {
        setDocuments(result.documents || []);
      } else {
        setError(result.message || 'Failed to fetch documents');
      }
    } catch (error) {
      setError('Error loading documents: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);
  

  if (loading && documents.length === 0) {
    return (
      <div className="document-list">
        <h3>Available Documents</h3>
        <p>Loading documents...</p>
      </div>
    );
  }

  if (error && documents.length === 0) {
    return (
      <div className="document-list">
        <h3>Available Documents</h3>
        <p className="error">{error}</p>
        <button onClick={fetchDocuments} className="refresh-button">
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="document-list">
      <h3>Available Documents</h3>
      <button onClick={fetchDocuments} className="refresh-button">
        Refresh
      </button>
      {documents.length === 0 ? (
        <p>No documents available. Upload some files to get started.</p>
      ) : (
        <ul>
          {documents.map((doc, index) => (
            <li key={index}>
              <span className="doc-name">{doc.name}</span>
              <span className="doc-chunks">({doc.chunks} chunks)</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default DocumentList;