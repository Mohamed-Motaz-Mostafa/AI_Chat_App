// frontend/src/components/ChatWindow.js
import React, { useState, useEffect, useRef } from 'react';
import { sendMessage } from '../api';

const ChatWindow = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto-scroll to the bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    
    const userMessage = input;
    setInput('');
    setLoading(true);
    
    // Add user message to chat
    setMessages((prevMessages) => [
      ...prevMessages,
      { text: userMessage, sender: 'user' },
    ]);
    
    try {
      // Send message to backend
      const response = await sendMessage(userMessage);
      
      // Add AI response to chat
      setMessages((prevMessages) => [
        ...prevMessages,
        { 
          text: response.response, 
          sender: 'ai',
          usedTools: response.used_tools 
        },
      ]);
    } catch (error) {
      // Add error message to chat
      setMessages((prevMessages) => [
        ...prevMessages,
        { 
          text: 'Error: Failed to get response', 
          sender: 'system' 
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-window">
      <div className="messages">
        {messages.length === 0 ? (
          <div className="empty-state">
            <p>Start a conversation with the AI assistant!</p>
          </div>
        ) : (
          messages.map((msg, index) => (
            <div 
              key={index} 
              className={`message ${msg.sender}`}
            >
              <p>{msg.text}</p>
              {msg.usedTools && msg.usedTools.length > 0 && (
                <div className="tools-used">
                  <small>Tools used: {msg.usedTools.join(', ')}</small>
                </div>
              )}
            </div>
          ))
        )}
        {loading && (
          <div className="message ai loading">
            <p>Thinking...</p>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <form className="input-container" onSubmit={handleSendMessage}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question..."
          disabled={loading}
        />
        <button type="submit" disabled={loading || !input.trim()}>
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatWindow;