import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../config/axios';
import toast from 'react-hot-toast';
import { Send, ArrowLeft, MessageCircle, User } from 'lucide-react';

function Chat() {
  const { userId } = useParams();
  const navigate = useNavigate();
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [conversations, setConversations] = useState([]);
  const [activeChat, setActiveChat] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    fetchConversations();
    if (userId) {
      fetchMessages(userId);
    }
  }, [userId]);

  const fetchConversations = async () => {
    try {
      const response = await api.get('/api/chat/conversations');
      setConversations(response.data);
    } catch (error) {
      console.error('Failed to load conversations:', error);
    }
  };

  const fetchMessages = async (targetUserId) => {
    try {
      setLoading(true);
      const response = await api.get(`/api/chat/messages/${targetUserId}`);
      setMessages(response.data);
      setActiveChat(targetUserId);
    } catch (error) {
      toast.error('Failed to load messages');
    } finally {
      setLoading(false);
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim() || !activeChat) return;

    setSending(true);
    try {
      const response = await api.post('/api/chat/send', {
        recipient_id: parseInt(activeChat),
        content: newMessage.trim()
      });
      
      setMessages([...messages, response.data]);
      setNewMessage('');
      
      // Refresh conversations to update last message
      fetchConversations();
    } catch (error) {
      toast.error('Failed to send message');
    } finally {
      setSending(false);
    }
  };

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;
    
    if (diff < 60000) { // Less than 1 minute
      return 'Just now';
    } else if (diff < 3600000) { // Less than 1 hour
      return `${Math.floor(diff / 60000)}m ago`;
    } else if (diff < 86400000) { // Less than 1 day
      return `${Math.floor(diff / 3600000)}h ago`;
    } else {
      return date.toLocaleDateString();
    }
  };

  if (!userId) {
    // Show conversations list
    return (
      <div className="main-content">
        <div className="container">
          <h1 className="mb-4">Messages</h1>
          
          {conversations.length === 0 ? (
            <div className="empty-state">
              <MessageCircle size={48} className="text-muted mb-2" />
              <h3>No conversations yet</h3>
              <p>Start a conversation by messaging someone you've matched with.</p>
            </div>
          ) : (
            <div className="conversations-list">
              {conversations.map((conversation) => (
                <div 
                  key={conversation.user_id}
                  className="conversation-item"
                  onClick={() => navigate(`/chat/${conversation.user_id}`)}
                >
                  {conversation.profile_picture ? (
                    <img 
                      src={conversation.profile_picture.startsWith('http') ? conversation.profile_picture : `http://localhost:8001${conversation.profile_picture}`}
                      alt={`${conversation.first_name}'s avatar`}
                      className="conversation-avatar"
                      style={{objectFit: 'cover', width: '50px', height: '50px', borderRadius: '50%'}}
                    />
                  ) : (
                    <div className="conversation-avatar">
                      {conversation.first_name[0]}{conversation.last_name[0]}
                    </div>
                  )}
                  
                  <div className="conversation-info">
                    <div className="conversation-header">
                      <h4>{conversation.first_name} {conversation.last_name}</h4>
                      <span className="conversation-time">
                        {formatTime(conversation.last_message_time)}
                      </span>
                    </div>
                    
                    <p className="conversation-preview">
                      {conversation.last_message || 'No messages yet'}
                    </p>
                  </div>
                  
                  {conversation.unread_count > 0 && (
                    <div className="unread-badge">
                      {conversation.unread_count}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="main-content">
      <div className="container">
        <div className="chat-container">
          <div className="chat-header">
            <button 
              onClick={() => navigate('/chat')}
              className="btn btn-secondary"
            >
              <ArrowLeft size={16} />
              Back
            </button>
            <h3>Chat</h3>
            <button 
              onClick={() => navigate(`/user/${userId}`)}
              className="btn btn-primary"
              style={{marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: '8px'}}
            >
              <User size={16} />
              View Profile
            </button>
          </div>

          {loading ? (
            <div className="loading">
              <div className="spinner"></div>
            </div>
          ) : (
            <>
              <div className="messages-container">
                {messages.length === 0 ? (
                  <div className="empty-messages">
                    <MessageCircle size={48} className="text-muted mb-2" />
                    <p>No messages yet. Start the conversation!</p>
                  </div>
                ) : (
                  messages.map((message) => (
                    <div 
                      key={message.id}
                      className={`message ${message.sender_id === parseInt(activeChat) ? 'message-received' : 'message-sent'}`}
                    >
                      <div className="message-content">
                        {message.content}
                      </div>
                      <div className="message-time">
                        {formatTime(message.created_at)}
                      </div>
                    </div>
                  ))
                )}
                <div ref={messagesEndRef} />
              </div>

              <form onSubmit={sendMessage} className="message-form">
                <div className="message-input-container">
                  <input
                    type="text"
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    placeholder="Type a message..."
                    className="message-input"
                    disabled={sending}
                  />
                  <button 
                    type="submit" 
                    className="btn btn-primary"
                    disabled={!newMessage.trim() || sending}
                  >
                    <Send size={16} />
                  </button>
                </div>
              </form>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default Chat;
