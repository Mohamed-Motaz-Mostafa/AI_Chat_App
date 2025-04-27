import React, { useState } from 'react';
import './App.css';
import FileUpload from './components/FileUpload';
import ChatWindow from './components/ChatWindow';
import DocumentList from './components/DocumentList';

function App() {
  const [uploadSuccess, setUploadSuccess] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(true); 

  const handleUploadSuccess = (result) => {
    setUploadSuccess(result);
    setTimeout(() => {
      setUploadSuccess(null);
    }, 3000);
  };

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <div className="App">
      <header className="App-header">
        <a href="https://www.dexalo.com/">
          <img
            src={`${process.env.PUBLIC_URL}/dexalo-logo.png`}
            alt="Logo"
            style={{ position: 'absolute', left: '20px', top: '5px' }}
          />
        </a>
        <h1>AI Chat App</h1>
      </header>
      <main>
        <div className={`sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
          <button className="toggle-button" onClick={toggleSidebar}>
            {sidebarOpen ? '<' : '>'}
          </button>
          {sidebarOpen && (
            <div className="document-section">
              <DocumentList />
            </div>
          )}
        </div>

        <div className="chat-section">
          <div className="upload-section">
            <FileUpload onUploadSuccess={handleUploadSuccess} />
          </div>
          <ChatWindow />
        </div>
      </main>
      <p className="footer-text"
        style={{ fontSize: '12px', color: '#333', marginTop: '40px' }}>
        Developed by: <a href="https://www.linkedin.com/in/mohamed-moataz">Mohamed Motaz</a>
      </p>
    </div>
  );
}

export default App;
