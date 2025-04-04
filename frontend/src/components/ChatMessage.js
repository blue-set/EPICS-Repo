import React from 'react';
import '../Chat.css';
import botAvatar from '../assets/bot-avatar.png';
import userAvatar from '../assets/user-avatar.png';

const ChatMessage = ({ message }) => {
  const { text, sender } = message;
  const isBot = sender === 'bot';
  
  return (
    <div className={`message ${isBot ? 'bot-message' : 'user-message'}`}>
      <div className="avatar-container">
        <img 
          src={isBot ? botAvatar : userAvatar} 
          alt={isBot ? "Bot Avatar" : "User Avatar"} 
          className="avatar"
        />
      </div>
      <div className="message-content">
        <div className="message-text">{text}</div>
      </div>
    </div>
  );
};

export default ChatMessage;
