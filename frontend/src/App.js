// frontend/src/App.js
import React, { useState } from 'react';
import './App.css';
import FileUpload from './components/FileUpload';
import ChatWindow from './components/ChatWindow';

function App() {
  const [uploadSuccess, setUploadSuccess] = useState(null);

  const handleUploadSuccess = (result) => {
    setUploadSuccess(result);
    // Reset success message after 3 seconds
    setTimeout(() => {
      setUploadSuccess(null);
    }, 3000);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Chat App</h1>
      </header>
      <main>
        <div className="upload-section">
          <FileUpload onUploadSuccess={handleUploadSuccess} />
        </div>
        <div className="chat-section">
          <ChatWindow />
        </div>
      </main>
    </div>
  );
}

export default App;