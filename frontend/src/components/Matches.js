import React, { useState, useEffect } from 'react';
import api from '../config/axios';
import { Heart, MessageCircle, MapPin, Calendar } from 'lucide-react';

function Matches() {
  const [matches, setMatches] = useState([]);
  const [mutualMatches, setMutualMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('all');

  useEffect(() => {
    fetchMatches();
  }, []);

  const fetchMatches = async () => {
    try {
      const [allMatchesResponse, mutualMatchesResponse] = await Promise.all([
        api.get('/api/matches/'),
        api.get('/api/matches/mutual')
      ]);
      
      setMatches(allMatchesResponse.data);
      setMutualMatches(mutualMatchesResponse.data);
    } catch (error) {
      console.error('Failed to load matches:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="main-content">
        <div className="container">
          <div className="loading">
            <div className="spinner"></div>
          </div>
        </div>
      </div>
    );
  }

  const displayMatches = activeTab === 'mutual' ? mutualMatches : matches;

  return (
    <div className="main-content">
      <div className="container">
        <div className="flex-between mb-4">
          <h1>Your Matches</h1>
          <div className="flex gap-2">
            <button
              onClick={() => setActiveTab('all')}
              className={`btn ${activeTab === 'all' ? 'btn-primary' : 'btn-secondary'}`}
            >
              All Matches ({matches.length})
            </button>
            <button
              onClick={() => setActiveTab('mutual')}
              className={`btn ${activeTab === 'mutual' ? 'btn-primary' : 'btn-secondary'}`}
            >
              Mutual Matches ({mutualMatches.length})
            </button>
          </div>
        </div>

        {displayMatches.length === 0 ? (
          <div className="empty-state">
            <Heart size={48} className="text-muted mb-2" />
            <h3>No matches yet</h3>
            <p>
              {activeTab === 'mutual' 
                ? "You don't have any mutual matches yet. Keep swiping to find your perfect match!"
                : "Start discovering people to see your matches here."
              }
            </p>
          </div>
        ) : (
          <div className="matches-grid">
            {displayMatches.map((match) => (
              <div key={match.id} className="match-card">
                <div className="match-avatar">
                  {match.matched_user?.profile?.first_name?.[0] || 'U'}
                  {match.matched_user?.profile?.last_name?.[0] || 'U'}
                </div>
                
                <div className="match-name">
                  {match.matched_user?.profile?.first_name || 'Unknown'} {match.matched_user?.profile?.last_name || 'User'}
                </div>
                
                <div className="match-info">
                  {match.matched_user?.profile?.age && (
                    <div className="flex-center mb-1">
                      <Calendar size={14} />
                      <span className="ml-1">{match.matched_user.profile.age} years old</span>
                    </div>
                  )}
                  
                  {match.matched_user?.profile?.city && (
                    <div className="flex-center mb-1">
                      <MapPin size={14} />
                      <span className="ml-1">{match.matched_user.profile.city}</span>
                    </div>
                  )}
                  
                  {match.matched_user?.profile?.bio && (
                    <p className="text-muted text-center">
                      {match.matched_user.profile.bio.length > 100 
                        ? `${match.matched_user.profile.bio.substring(0, 100)}...`
                        : match.matched_user.profile.bio
                      }
                    </p>
                  )}
                </div>

                <div className="match-score">
                  {Math.round(match.compatibility_score * 100)}% match
                </div>

                {match.is_mutual && (
                  <div className="flex-center mb-2">
                    <Heart size={16} className="text-red-500" />
                    <span className="ml-1 text-red-500 font-semibold">Mutual Match!</span>
                  </div>
                )}

                <div className="flex gap-2">
                  <button className="btn btn-primary flex-1">
                    <MessageCircle size={16} />
                    Message
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Matches;
