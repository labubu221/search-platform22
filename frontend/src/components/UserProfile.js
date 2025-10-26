import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../config/axios';
import toast from 'react-hot-toast';
import { ArrowLeft, MapPin, Calendar, MessageCircle, Heart, X } from 'lucide-react';

function UserProfile() {
  const { userId } = useParams();
  const navigate = useNavigate();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [userInterests, setUserInterests] = useState([]);
  const [userSkills, setUserSkills] = useState([]);

  useEffect(() => {
    fetchUserProfile();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [userId]);

  const fetchUserProfile = async () => {
    try {
      setLoading(true);
      const response = await api.get(`/api/users/profile/${userId}`);
      setProfile(response.data);
      
      // Fetch user's interests and skills
      const user = await api.get(`/api/users/${userId}`);
      setUserInterests(user.data.interests || []);
      setUserSkills(user.data.skills || []);
    } catch (error) {
      toast.error('Failed to load user profile');
      navigate('/');
    } finally {
      setLoading(false);
    }
  };

  const likeUser = async () => {
    try {
      const response = await api.post(`/api/matches/like/${userId}`);
      toast.success(response.data.message || 'User liked!');
    } catch (error) {
      console.error('Like error:', error);
      const message = error.response?.data?.detail || 'Failed to like user';
      toast.error(message);
    }
  };

  const dislikeUser = async () => {
    try {
      const response = await api.post(`/api/matches/dislike/${userId}`);
      toast.success(response.data.message || 'User disliked');
    } catch (error) {
      console.error('Dislike error:', error);
      const message = error.response?.data?.detail || 'Failed to dislike user';
      toast.error(message);
    }
  };

  const startChat = () => {
    navigate(`/chat/${userId}`);
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

  if (!profile) {
    return (
      <div className="main-content">
        <div className="container">
          <div className="empty-state">
            <h3>User not found</h3>
            <p>The user profile you're looking for doesn't exist.</p>
            <button onClick={() => navigate('/')} className="btn btn-primary">
              Go Home
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="main-content">
      <div className="container">
        <div className="user-profile-container">
          <div className="user-profile-header">
            <button 
              onClick={() => navigate(-1)}
              className="btn btn-secondary"
            >
              <ArrowLeft size={16} />
              Back
            </button>
            <h1>User Profile</h1>
          </div>

          <div className="user-profile-card">
            <div className="user-profile-info">
              {profile.profile_picture ? (
                <img 
                  src={profile.profile_picture.startsWith('http') ? profile.profile_picture : `http://localhost:8001${profile.profile_picture}`}
                  alt={`${profile.first_name} ${profile.last_name}`}
                  className="user-avatar-image-large"
                />
              ) : (
                <div className="user-avatar-placeholder-large">
                  {profile.first_name[0]}{profile.last_name[0]}
                </div>
              )}
              
              <div className="user-details">
                <h2>{profile.first_name} {profile.last_name}</h2>
                
                <div className="user-meta">
                  {profile.age && (
                    <div className="user-meta-item">
                      <Calendar size={16} />
                      <span>{profile.age} years old</span>
                    </div>
                  )}
                  
                  {profile.city && (
                    <div className="user-meta-item">
                      <MapPin size={16} />
                      <span>{profile.city}</span>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {profile.bio && (
              <div className="user-bio-section">
                <h3>About</h3>
                <p>{profile.bio}</p>
              </div>
            )}

            {profile.search_goals && (
              <div className="user-goals-section">
                <h3>Looking For</h3>
                <p>{profile.search_goals}</p>
              </div>
            )}

            {userInterests.length > 0 && (
              <div className="user-interests-section">
                <h3>Interests</h3>
                <div className="tags">
                  {userInterests.map(interest => (
                    <span key={interest.id} className="tag">{interest.name}</span>
                  ))}
                </div>
              </div>
            )}

            {userSkills.length > 0 && (
              <div className="user-skills-section">
                <h3>Skills</h3>
                <div className="tags">
                  {userSkills.map(skill => (
                    <span key={skill.id} className="tag">{skill.name}</span>
                  ))}
                </div>
              </div>
            )}

            <div className="user-actions">
              <button
                onClick={dislikeUser}
                className="btn btn-danger"
              >
                <X size={16} />
                Pass
              </button>
              <button
                onClick={startChat}
                className="btn btn-secondary"
              >
                <MessageCircle size={16} />
                Message
              </button>
              <button
                onClick={likeUser}
                className="btn btn-primary"
              >
                <Heart size={16} />
                Like
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default UserProfile;
