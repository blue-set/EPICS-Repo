import React from 'react';
import Message from './Message';
import '../styles/MessageList.css';

const MessageList = ({ messages, loading, messagesEndRef }) => {
  return (
    <div className="message-list">
      {messages.map(message => (
        <Message key={message.id} message={message} />
      ))}
      
      {loading && (
        <div className="message-wrapper assistant">
          <div className="message assistant-message typing">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        </div>
      )}
      
      <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageList; 