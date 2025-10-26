import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../config/axios';
import toast from 'react-hot-toast';
import { Search, Bot, Users, MapPin, Calendar, Heart } from 'lucide-react';

function AISearch() {
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) {
      toast.error('Please enter a search query');
      return;
    }

    setLoading(true);
    try {
      const response = await api.post('/api/ai/ai-search', {
        query: query,
        limit: 20
      });
      setResults(response.data);
      if (response.data.length === 0) {
        toast.info('No results found. Try a different search query.');
      }
    } catch (error) {
      toast.error('Failed to search users');
      console.error('AI search error:', error);
    } finally {
      setLoading(false);
    }
  };

  const exampleQueries = [
    "Find developers in San Francisco",
    "Looking for musicians in my city",
    "Artists and designers for a project",
    "Fitness enthusiasts near me",
    "Business professionals for networking",
    "Teachers and educators"
  ];

  return (
    <div className="main-content">
      <div className="container">
      <div className="ai-search-header">
        <div className="ai-search-title">
          <Bot className="ai-search-icon" />
          <h1>AI-Powered People Search</h1>
        </div>
        <p className="ai-search-subtitle">
          Use natural language to find people. Describe what you're looking for and our AI will find the best matches.
        </p>
      </div>

      <div className="ai-search-form">
        <form onSubmit={handleSearch}>
          <div className="search-input-group">
            <Search className="search-icon" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g., 'Find developers in San Francisco' or 'Looking for musicians'"
              className="search-input"
            />
            <button type="submit" disabled={loading} className="btn btn-primary">
              {loading ? 'Searching...' : 'Search'}
            </button>
          </div>
        </form>
      </div>

      <div className="example-queries">
        <h3>Example searches:</h3>
        <div className="query-chips">
          {exampleQueries.map((example, index) => (
            <button
              key={index}
              className="query-chip"
              onClick={() => setQuery(example)}
            >
              {example}
            </button>
          ))}
        </div>
      </div>

      {results.length > 0 && (
        <div className="search-results">
          <h2>Search Results ({results.length})</h2>
          <div className="results-grid">
            {results.map((user) => (
              <div key={user.user_id} className="user-card">
                <div className="user-card-header">
                  {user.profile_picture ? (
                    <img
                      src={user.profile_picture}
                      alt={`${user.first_name} ${user.last_name}`}
                      className="user-avatar"
                    />
                  ) : (
                    <div className="user-avatar-placeholder">
                      <Users className="avatar-icon" />
                    </div>
                  )}
                  <div className="user-info">
                    <h3>{user.first_name} {user.last_name}</h3>
                    <div className="user-details">
                      {user.age && (
                        <span className="detail-item">
                          <Calendar className="detail-icon" />
                          {user.age} years old
                        </span>
                      )}
                      {user.city && (
                        <span className="detail-item">
                          <MapPin className="detail-icon" />
                          {user.city}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
                
                {user.bio && (
                  <div className="user-bio">
                    <p>{user.bio}</p>
                  </div>
                )}

                <div className="user-actions">
                  <button 
                    className="btn btn-primary"
                    onClick={() => navigate(`/user/${user.user_id}`)}
                  >
                    <Heart className="action-icon" />
                    View Profile
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <style jsx>{`
        .ai-search-header {
          text-align: center;
          margin-bottom: 2rem;
        }

        .ai-search-title {
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 1rem;
          margin-bottom: 1rem;
        }

        .ai-search-title h1 {
          font-size: 2.5rem;
          color: #2563eb;
          margin: 0;
        }

        .ai-search-icon {
          width: 3rem;
          height: 3rem;
          color: #2563eb;
        }

        .ai-search-subtitle {
          font-size: 1.2rem;
          color: #6b7280;
          max-width: 600px;
          margin: 0 auto;
        }

        .ai-search-form {
          margin-bottom: 2rem;
        }

        .search-input-group {
          display: flex;
          align-items: center;
          background: white;
          border-radius: 12px;
          padding: 0.5rem;
          box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
          border: 2px solid #e5e7eb;
          transition: border-color 0.2s;
        }

        .search-input-group:focus-within {
          border-color: #2563eb;
        }

        .search-icon {
          width: 1.5rem;
          height: 1.5rem;
          color: #9ca3af;
          margin: 0 1rem;
        }

        .search-input {
          flex: 1;
          border: none;
          outline: none;
          font-size: 1.1rem;
          padding: 1rem 0;
          background: transparent;
        }

        .search-input::placeholder {
          color: #9ca3af;
        }

        .example-queries {
          margin-bottom: 2rem;
        }

        .example-queries h3 {
          margin-bottom: 1rem;
          color: #374151;
        }

        .query-chips {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
        }

        .query-chip {
          background: #f3f4f6;
          border: 1px solid #d1d5db;
          border-radius: 20px;
          padding: 0.5rem 1rem;
          font-size: 0.9rem;
          color: #374151;
          cursor: pointer;
          transition: all 0.2s;
        }

        .query-chip:hover {
          background: #e5e7eb;
          border-color: #9ca3af;
        }

        .search-results h2 {
          margin-bottom: 1.5rem;
          color: #374151;
        }

        .results-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
          gap: 1.5rem;
        }

        .user-card {
          background: white;
          border-radius: 12px;
          padding: 1.5rem;
          box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
          border: 1px solid #e5e7eb;
          transition: transform 0.2s, box-shadow 0.2s;
        }

        .user-card:hover {
          transform: translateY(-2px);
          box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }

        .user-card-header {
          display: flex;
          align-items: center;
          gap: 1rem;
          margin-bottom: 1rem;
        }

        .user-avatar {
          width: 4rem;
          height: 4rem;
          border-radius: 50%;
          object-fit: cover;
        }

        .user-avatar-placeholder {
          width: 4rem;
          height: 4rem;
          border-radius: 50%;
          background: #f3f4f6;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .avatar-icon {
          width: 2rem;
          height: 2rem;
          color: #9ca3af;
        }

        .user-info h3 {
          margin: 0 0 0.5rem 0;
          color: #374151;
          font-size: 1.2rem;
        }

        .user-details {
          display: flex;
          flex-direction: column;
          gap: 0.25rem;
        }

        .detail-item {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 0.9rem;
          color: #6b7280;
        }

        .detail-icon {
          width: 1rem;
          height: 1rem;
        }

        .user-bio {
          margin-bottom: 1rem;
        }

        .user-bio p {
          color: #6b7280;
          line-height: 1.5;
          margin: 0;
        }

        .user-actions {
          display: flex;
          gap: 0.5rem;
        }

        .action-icon {
          width: 1rem;
          height: 1rem;
        }

        @media (max-width: 768px) {
          .ai-search-title h1 {
            font-size: 2rem;
          }

          .search-input-group {
            flex-direction: column;
            gap: 1rem;
          }

          .search-input {
            width: 100%;
          }

          .results-grid {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
      </div>
    </div>
  );
}

export default AISearch;
