import React, { useState, useEffect } from 'react';
import api from '../config/axios';
import toast from 'react-hot-toast';
import { Heart, X, Search, Filter, MapPin, Calendar } from 'lucide-react';

function Recommendations() {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showFilters, setShowFilters] = useState(false);
  const [filters, setFilters] = useState({
    city: '',
    minAge: '',
    maxAge: '',
    interests: '',
    skills: ''
  });

  useEffect(() => {
    fetchRecommendations();
  }, []);

  const fetchRecommendations = async () => {
    try {
      setLoading(true);
      const response = await api.get('/api/recommendations/');
      setRecommendations(response.data);
    } catch (error) {
      toast.error('Failed to load recommendations');
    } finally {
      setLoading(false);
    }
  };

  const searchWithFilters = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      // Convert camelCase to snake_case for backend
      const backendParams = {
        city: filters.city,
        min_age: filters.minAge,
        max_age: filters.maxAge,
        interests: filters.interests,
        skills: filters.skills
      };
      Object.entries(backendParams).forEach(([key, value]) => {
        if (value) params.append(key, value);
      });
      
      const response = await api.get(`/api/recommendations/search?${params}`);
      setRecommendations(response.data);
      setShowFilters(false);
    } catch (error) {
      toast.error('Search failed');
      console.error('Search error:', error);
    } finally {
      setLoading(false);
    }
  };

  const likeUser = async (userId) => {
    try {
      await api.post(`/api/matches/like/${userId}`);
      toast.success('User liked!');
      // Remove from recommendations
      setRecommendations(prev => prev.filter(rec => rec.user_id !== userId));
    } catch (error) {
      toast.error('Failed to like user');
    }
  };

  const dislikeUser = async (userId) => {
    try {
      await api.post(`/api/matches/dislike/${userId}`);
      toast.success('User disliked');
      // Remove from recommendations
      setRecommendations(prev => prev.filter(rec => rec.user_id !== userId));
    } catch (error) {
      toast.error('Failed to dislike user');
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

  return (
    <div className="main-content">
      <div className="container">
        <div className="flex-between mb-4">
          <h1>Discover People</h1>
          <button
            onClick={() => setShowFilters(!showFilters)}
            className="btn btn-secondary"
          >
            <Filter size={16} />
            Filters
          </button>
        </div>

        {showFilters && (
          <div className="card mb-4">
            <h3>Search Filters</h3>
            <div className="grid grid-2">
              <div className="form-group">
                <label className="form-label">City</label>
                <input
                  type="text"
                  className="form-input"
                  placeholder="Enter city"
                  value={filters.city}
                  onChange={(e) => setFilters({...filters, city: e.target.value})}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Min Age</label>
                <input
                  type="number"
                  className="form-input"
                  placeholder="18"
                  value={filters.minAge}
                  onChange={(e) => setFilters({...filters, minAge: e.target.value})}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Max Age</label>
                <input
                  type="number"
                  className="form-input"
                  placeholder="65"
                  value={filters.maxAge}
                  onChange={(e) => setFilters({...filters, maxAge: e.target.value})}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Interests (comma-separated)</label>
                <input
                  type="text"
                  className="form-input"
                  placeholder="music, sports, technology"
                  value={filters.interests}
                  onChange={(e) => setFilters({...filters, interests: e.target.value})}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Skills (comma-separated)</label>
                <input
                  type="text"
                  className="form-input"
                  placeholder="programming, design, marketing"
                  value={filters.skills}
                  onChange={(e) => setFilters({...filters, skills: e.target.value})}
                />
              </div>
            </div>

            <div className="flex gap-2">
              <button onClick={searchWithFilters} className="btn btn-primary">
                <Search size={16} />
                Search
              </button>
              <button 
                onClick={() => {
                  setFilters({city: '', minAge: '', maxAge: '', interests: '', skills: ''});
                  fetchRecommendations();
                  setShowFilters(false);
                }}
                className="btn btn-secondary"
              >
                Clear
              </button>
            </div>
          </div>
        )}

        {recommendations.length === 0 ? (
          <div className="empty-state">
            <h3>No recommendations found</h3>
            <p>Try adjusting your filters or complete your profile to get better matches.</p>
            <button onClick={fetchRecommendations} className="btn btn-primary">
              Refresh
            </button>
          </div>
        ) : (
          <div className="grid grid-2">
            {recommendations.map((rec) => (
              <div key={rec.user_id} className="recommendation-card">
                <div className="recommendation-header">
                  {rec.profile_picture ? (
                    <img 
                      src={rec.profile_picture.startsWith('http') ? rec.profile_picture : `http://localhost:8001${rec.profile_picture}`}
                      alt={`${rec.first_name}'s avatar`}
                      className="recommendation-avatar"
                      style={{objectFit: 'cover'}}
                    />
                  ) : (
                    <div className="recommendation-avatar">
                      {rec.first_name[0]}{rec.last_name[0]}
                    </div>
                  )}
                  <div className="recommendation-info">
                    <h3>{rec.first_name} {rec.last_name}</h3>
                    <p>
                      {rec.age && <><Calendar size={14} /> {rec.age} years old</>}
                      {rec.city && <><MapPin size={14} /> {rec.city}</>}
                    </p>
                  </div>
                  <div className="compatibility-score">
                    {Math.round(rec.compatibility_score * 100)}% match
                  </div>
                </div>

                {rec.bio && (
                  <div className="recommendation-bio">
                    {rec.bio}
                  </div>
                )}

                {rec.common_interests.length > 0 && (
                  <div className="common-items">
                    <h4>Common Interests</h4>
                    <div className="tags">
                      {rec.common_interests.map((interest, index) => (
                        <span key={index} className="tag">{interest}</span>
                      ))}
                    </div>
                  </div>
                )}

                {rec.common_skills.length > 0 && (
                  <div className="common-items">
                    <h4>Common Skills</h4>
                    <div className="tags">
                      {rec.common_skills.map((skill, index) => (
                        <span key={index} className="tag">{skill}</span>
                      ))}
                    </div>
                  </div>
                )}

                <div className="recommendation-actions">
                  <button
                    onClick={() => dislikeUser(rec.user_id)}
                    className="btn-dislike"
                  >
                    <X size={16} />
                    Pass
                  </button>
                  <button
                    onClick={() => likeUser(rec.user_id)}
                    className="btn-like"
                  >
                    <Heart size={16} />
                    Like
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

export default Recommendations;
