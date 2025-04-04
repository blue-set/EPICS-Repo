import React from 'react';
import '../styles/Message.css';

const Message = ({ message }) => {
  const { role, content, isError } = message;
  const isUser = role === 'user';
  
  return (
    <div className={`message-wrapper ${isUser ? 'user' : 'assistant'}`}>
      <div className={`message ${isUser ? 'user-message' : 'assistant-message'} ${isError ? 'error' : ''}`}>
        <span className="message-icon">
          {isUser ? '👤' : '🤖'}
        </span>
        <div className="message-content" dangerouslySetInnerHTML={{ __html: formatContent(content) }} />
      </div>
    </div>
  );
};

// Function to format the content
const formatContent = (content) => {
  return content
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold text
    .replace(/\*(.*?)\*/g, '<em>$1</em>') // Italics
    .replace(/^\s*-\s+(.*)$/gm, '<li>$1</li>') // List items
    .replace(/<li>(.*?)<\/li>/g, '<ul><li>$1</li></ul>') // Wrap list items in <ul>
    .replace(/\n/g, '<br />'); // Line breaks
};

export default Message; 