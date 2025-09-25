// ChatApp.js
import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

// Connect to the backend server
const socket = io('http://llama-31-70b-instruct.nim-service:8000/v1/chat/completions'); // Change to your backend URL in production

const ChatApp = () => {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);
  
  // Listen for incoming messages from the server
  useEffect(() => {
    socket.on('receive_message', (msg) => {
      setMessages((prevMessages) => [...prevMessages, msg]);
    });

    return () => {
      socket.off('receive_message');
    };
  }, []);

  const sendMessage = () => {
    if (message) {
      socket.emit('send_message', message); // Send message to the backend
      setMessage(''); // Clear the input field
    }
  };

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((msg, index) => (
          <div key={index} className="message">{msg}</div>
        ))}
      </div>
      <input 
        type="text" 
        value={message} 
        onChange={(e) => setMessage(e.target.value)} 
        placeholder="Type a message..." 
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
};

export default ChatApp;
