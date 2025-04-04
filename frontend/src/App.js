import React, { useState, useEffect, useRef } from 'react';
import './styles/App.css';
import './styles/SidebarToggle.css';
import ChatHeader from './components/ChatHeader';
import MessageList from './components/MessageList';
import ChatInput from './components/ChatInput';
import SidebarToggle from './components/SidebarToggle';
import { fetchBotResponse } from './services/api';

function App() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    // Add welcome message when component mounts
    if (messages.length === 0) {
      setMessages([
        { 
          id: 1, 
          role: 'assistant', 
          content: 'Hello! How can I assist you with your health concerns today?',
          timestamp: new Date()
        }
      ]);
    }
  }, [messages.length]);

  useEffect(() => {
    // Scroll to bottom whenever messages change
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (message) => {
    if (!message.trim()) return;
    
    // Add user message to chat
    const userMessage = {
      id: messages.length + 1,
      role: 'user',
      content: message,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setLoading(true);
    setError(null);
    
    try {
      // Call API to get bot response
      const response = await fetchBotResponse(message);
      
      // Check if there's an error in the response
      if (response.error) {
        throw new Error(response.error);
      }
      
      // Add bot response to chat
      const botMessage = {
        id: messages.length + 2,
        role: 'assistant',
        content: response.message || "Sorry, I couldn't generate a response.",
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error getting response:', error);
      setError(error.message);
      
      // Add error message
      const errorMessage = {
        id: messages.length + 2,
        role: 'assistant',
        content: `Sorry, I encountered an error: ${error.message || 'Unknown error'}. Please try again later.`,
        timestamp: new Date(),
        isError: true
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleClearChat = () => {
    setMessages([
      {
        id: 1,
        role: 'assistant',
        content: 'Hello! How can I assist you with your health concerns today?',
        timestamp: new Date()
      }
    ]);
    setError(null);
  };

  return (
    <div className="app">
      <SidebarToggle />
      <div className="sidebar">
        <div className="sidebar-header">
          <h2>HealthCare Assistant</h2>
          <p>Your AI-powered medical companion</p>
        </div>
        
        <div className="sidebar-section">
          <h3>Features</h3>
          <ul>
            <li><span className="icon">🏥</span> Medical Information</li>
            <li><span className="icon">💊</span> Treatment Suggestions</li>
            <li><span className="icon">🩺</span> Health Advice</li>
            <li><span className="icon">❓</span> Medical Queries</li>
          </ul>
        </div>
        
        <div className="sidebar-section">
          <h3>Disclaimer</h3>
          <p>This AI assistant provides general information only. Always consult a healthcare professional for medical advice.</p>
        </div>
        
        <button className="clear-button" onClick={handleClearChat}>
          Clear Chat
        </button>
      </div>
      
      <div className="chat-container">
        <ChatHeader />
        <MessageList messages={messages} loading={loading} messagesEndRef={messagesEndRef} />
        <ChatInput onSendMessage={handleSendMessage} disabled={loading} />
        
        {error && (
          <div className="error-notification">
            Server error: {error}. Please check your backend connection.
          </div>
        )}
      </div>
    </div>
  );
}

export default App; 