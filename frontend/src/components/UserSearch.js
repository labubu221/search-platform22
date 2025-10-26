import React, { useState, useEffect } from 'react';
import api from '../config/axios';
import { Search, User, MapPin, Calendar, MessageCircle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

function UserSearch() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const searchUsers = async (searchQuery) => {
    if (!searchQuery || searchQuery.length < 2) {
      setResults([]);
      return;
    }

    setLoading(true);
    try {
      const response = await api.get(`/api/users/search?query=${encodeURIComponent(searchQuery)}&limit=20`);
      setResults(response.data);
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      searchUsers(query);
    }, 300); // Debounce search

    return () => clearTimeout(timeoutId);
  }, [query]);

  const handleUserClick = (userId) => {
    navigate(`/user/${userId}`);
  };

  return (
    <div className="main-content">
      <div className="container">
        <h1 className="mb-4">Search Users</h1>
        
        <div className="search-container mb-4">
          <div className="search-input-container">
            <Search className="search-icon" />
            <input
              type="text"
              placeholder="Search by name..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="search-input"
            />
          </div>
        </div>

        {loading && (
          <div className="loading">
            <div className="spinner"></div>
          </div>
        )}

        {!loading && query.length >= 2 && results.length === 0 && (
          <div className="empty-state">
            <User size={48} className="text-muted mb-2" />
            <h3>No users found</h3>
            <p>Try searching with a different name.</p>
          </div>
        )}

        {!loading && results.length > 0 && (
          <div className="search-results">
            <h3 className="mb-3">Search Results ({results.length})</h3>
            <div className="users-grid">
              {results.map((user) => (
                <div key={user.user_id} className="user-card">
                  <div className="user-avatar">
                    {user.profile_picture ? (
                      <img 
                        src={user.profile_picture.startsWith('http') ? user.profile_picture : `http://localhost:8001${user.profile_picture}`}
                        alt={`${user.first_name} ${user.last_name}`}
                        className="user-avatar-image"
                      />
                    ) : (
                      <div className="user-avatar-placeholder">
                        {user.first_name[0]}{user.last_name[0]}
                      </div>
                    )}
                  </div>
                  
                  <div className="user-info">
                    <h4 className="user-name">
                      {user.first_name} {user.last_name}
                    </h4>
                    
                    <div className="user-details">
                      {user.age && (
                        <div className="user-detail">
                          <Calendar size={14} />
                          <span>{user.age} years old</span>
                        </div>
                      )}
                      
                      {user.city && (
                        <div className="user-detail">
                          <MapPin size={14} />
                          <span>{user.city}</span>
                        </div>
                      )}
                    </div>
                    
                    {user.bio && (
                      <p className="user-bio">
                        {user.bio.length > 100 
                          ? `${user.bio.substring(0, 100)}...`
                          : user.bio
                        }
                      </p>
                    )}
                  </div>
                  
                  <div className="user-actions">
                    <button
                      onClick={() => handleUserClick(user.user_id)}
                      className="btn btn-primary"
                    >
                      <User size={16} />
                      View Profile
                    </button>
                    <button
                      onClick={() => navigate(`/chat/${user.user_id}`)}
                      className="btn btn-secondary"
                    >
                      <MessageCircle size={16} />
                      Message
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {query.length < 2 && (
          <div className="search-hint">
            <Search size={48} className="text-muted mb-2" />
            <h3>Start searching</h3>
            <p>Enter at least 2 characters to search for users.</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default UserSearch;
