import React, { useState, useEffect } from 'react';
import api from '../config/axios';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import { MapPin, Calendar, Edit3, Save, X, Upload, Plus } from 'lucide-react';

function Profile() {
  const [profile, setProfile] = useState(null);
  const [interests, setInterests] = useState([]);
  const [skills, setSkills] = useState([]);
  const [userInterests, setUserInterests] = useState([]);
  const [userSkills, setUserSkills] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [newInterest, setNewInterest] = useState('');
  const [newSkill, setNewSkill] = useState('');
  const [uploadingAvatar, setUploadingAvatar] = useState(false);
  const { register, handleSubmit, formState: { errors } } = useForm();

  useEffect(() => {
    fetchProfile();
    fetchInterests();
    fetchSkills();
  }, []);

  const fetchProfile = async () => {
    try {
      const response = await api.get('/api/users/profile');
      setProfile(response.data);
      setUserInterests(response.data.user?.interests || []);
      setUserSkills(response.data.user?.skills || []);
    } catch (error) {
      // Don't show error toast if profile doesn't exist (404)
      if (error.response?.status !== 404) {
        toast.error('Failed to load profile');
      }
      // Profile doesn't exist, setProfile will remain null
    } finally {
      setLoading(false);
    }
  };

  const fetchInterests = async () => {
    try {
      const response = await api.get('/api/users/interests');
      setInterests(response.data);
    } catch (error) {
      toast.error('Failed to load interests');
    }
  };

  const fetchSkills = async () => {
    try {
      const response = await api.get('/api/users/skills');
      setSkills(response.data);
    } catch (error) {
      toast.error('Failed to load skills');
    }
  };

  const onSubmit = async (data) => {
    try {
      let response;
      if (!profile) {
        // Creating new profile
        response = await api.post('/api/users/profile', data);
        toast.success('Profile created successfully!');
      } else {
        // Updating existing profile
        response = await api.put('/api/users/profile', data);
        toast.success('Profile updated successfully!');
      }
      setProfile(response.data);
      setEditing(false);
    } catch (error) {
      const action = !profile ? 'create' : 'update';
      toast.error(`Failed to ${action} profile`);
    }
  };

  const addInterest = async (interestId) => {
    try {
      await api.post(`/api/users/profile/interests/${interestId}`);
      const interest = interests.find(i => i.id === interestId);
      setUserInterests([...userInterests, interest]);
      toast.success('Interest added!');
    } catch (error) {
      toast.error('Failed to add interest');
    }
  };

  const addSkill = async (skillId) => {
    try {
      await api.post(`/api/users/profile/skills/${skillId}`);
      const skill = skills.find(s => s.id === skillId);
      setUserSkills([...userSkills, skill]);
      toast.success('Skill added!');
    } catch (error) {
      toast.error('Failed to add skill');
    }
  };

  const addCustomInterest = async () => {
    if (!newInterest.trim()) return;
    
    try {
      const response = await api.post('/api/users/profile/custom-interest', {
        name: newInterest.trim(),
        category: 'Custom'
      });
      setUserInterests([...userInterests, response.data]);
      setNewInterest('');
      toast.success('Custom interest added!');
    } catch (error) {
      toast.error('Failed to add custom interest');
    }
  };

  const addCustomSkill = async () => {
    if (!newSkill.trim()) return;
    
    try {
      const response = await api.post('/api/users/profile/custom-skill', {
        name: newSkill.trim(),
        category: 'Custom'
      });
      setUserSkills([...userSkills, response.data]);
      setNewSkill('');
      toast.success('Custom skill added!');
    } catch (error) {
      toast.error('Failed to add custom skill');
    }
  };

  const removeInterest = async (interestId) => {
    try {
      await api.delete(`/api/users/profile/interests/${interestId}`);
      setUserInterests(userInterests.filter(i => i.id !== interestId));
      toast.success('Interest removed!');
    } catch (error) {
      toast.error('Failed to remove interest');
    }
  };

  const removeSkill = async (skillId) => {
    try {
      await api.delete(`/api/users/profile/skills/${skillId}`);
      setUserSkills(userSkills.filter(s => s.id !== skillId));
      toast.success('Skill removed!');
    } catch (error) {
      toast.error('Failed to remove skill');
    }
  };

  const handleAvatarUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    // Validate file type - accept common image formats
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp', 'image/bmp', 'image/svg+xml'];
    if (!allowedTypes.includes(file.type)) {
      toast.error('Please select a valid image file (JPG, PNG, GIF, WebP, BMP, SVG)');
      return;
    }

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      toast.error('File size must be less than 10MB');
      return;
    }

    setUploadingAvatar(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await api.post('/api/users/profile/avatar', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      setProfile({...profile, profile_picture: response.data.avatar_url});
      toast.success('Avatar uploaded successfully!');
    } catch (error) {
      toast.error('Failed to upload avatar');
    } finally {
      setUploadingAvatar(false);
    }
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  if (!profile && !editing) {
    return (
      <div className="main-content">
        <div className="container">
          <div className="card">
            <h2>Complete Your Profile</h2>
            <p>Please complete your profile to start finding matches.</p>
            <button 
              onClick={() => setEditing(true)}
              className="btn btn-primary"
            >
              Create Profile
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!profile && editing) {
    return (
      <div className="main-content">
        <div className="container">
          <div className="profile-card">
            <div className="profile-header">
              <h2>Create Your Profile</h2>
              <button
                onClick={() => setEditing(false)}
                className="btn btn-secondary"
              >
                <X size={16} />
                Cancel
              </button>
            </div>

            <form onSubmit={handleSubmit(onSubmit)}>
              <div className="grid grid-2">
                <div className="form-group">
                  <label className="form-label">First Name</label>
                  <input
                    type="text"
                    className="form-input"
                    {...register('first_name', { required: 'First name is required' })}
                  />
                  {errors.first_name && <span className="error">{errors.first_name.message}</span>}
                </div>

                <div className="form-group">
                  <label className="form-label">Last Name</label>
                  <input
                    type="text"
                    className="form-input"
                    {...register('last_name', { required: 'Last name is required' })}
                  />
                  {errors.last_name && <span className="error">{errors.last_name.message}</span>}
                </div>
              </div>

              <div className="grid grid-2">
                <div className="form-group">
                  <label className="form-label">Age</label>
                  <input
                    type="number"
                    className="form-input"
                    {...register('age')}
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">City</label>
                  <input
                    type="text"
                    className="form-input"
                    {...register('city')}
                  />
                </div>
              </div>

              <div className="form-group">
                <label className="form-label">Bio</label>
                <textarea
                  className="form-input"
                  rows="4"
                  {...register('bio')}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Search Goals</label>
                <textarea
                  className="form-input"
                  rows="3"
                  placeholder="What are you looking for? (e.g., friends, business partners, mentors)"
                  {...register('search_goals')}
                />
              </div>

              <div className="form-actions">
                <button type="submit" className="btn btn-primary">
                  <Save size={16} />
                  Create Profile
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="main-content">
      <div className="container">
        <div className="profile-card">
          <div className="profile-header">
            <div className="profile-avatar-container">
              {profile.profile_picture ? (
                <img 
                  src={profile.profile_picture.startsWith('http') ? profile.profile_picture : `http://localhost:8001${profile.profile_picture}`}
                  alt="Profile" 
                  className="profile-avatar-image"
                />
              ) : (
                <div className="profile-avatar">
                  {profile.first_name?.[0]}{profile.last_name?.[0]}
                </div>
              )}
              <label className="avatar-upload-btn" htmlFor="avatar-upload">
                <Upload size={16} />
                {uploadingAvatar ? 'Uploading...' : 'Upload'}
              </label>
              <input
                id="avatar-upload"
                type="file"
                accept="image/*"
                onChange={handleAvatarUpload}
                style={{ display: 'none' }}
                disabled={uploadingAvatar}
              />
            </div>
            <div className="profile-info">
              <h2>{profile.first_name} {profile.last_name}</h2>
              <p>{profile.city && <><MapPin size={16} /> {profile.city}</>}</p>
              <p>{profile.age && <><Calendar size={16} /> {profile.age} years old</>}</p>
            </div>
            <button
              onClick={() => setEditing(!editing)}
              className="btn btn-secondary"
            >
              {editing ? <X size={16} /> : <Edit3 size={16} />}
              {editing ? 'Cancel' : 'Edit'}
            </button>
          </div>

          {editing ? (
            <form onSubmit={handleSubmit(onSubmit)}>
              <div className="grid grid-2">
                <div className="form-group">
                  <label className="form-label">First Name</label>
                  <input
                    type="text"
                    className="form-input"
                    defaultValue={profile.first_name}
                    {...register('first_name', { required: 'First name is required' })}
                  />
                  {errors.first_name && <span className="error">{errors.first_name.message}</span>}
                </div>

                <div className="form-group">
                  <label className="form-label">Last Name</label>
                  <input
                    type="text"
                    className="form-input"
                    defaultValue={profile.last_name}
                    {...register('last_name', { required: 'Last name is required' })}
                  />
                  {errors.last_name && <span className="error">{errors.last_name.message}</span>}
                </div>

                <div className="form-group">
                  <label className="form-label">Age</label>
                  <input
                    type="number"
                    className="form-input"
                    defaultValue={profile.age}
                    {...register('age')}
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">City</label>
                  <input
                    type="text"
                    className="form-input"
                    defaultValue={profile.city}
                    {...register('city')}
                  />
                </div>
              </div>

              <div className="form-group">
                <label className="form-label">About Me</label>
                <textarea
                  className="form-textarea"
                  defaultValue={profile.bio}
                  placeholder="Tell us about yourself..."
                  {...register('bio')}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Search Goals</label>
                <textarea
                  className="form-textarea"
                  defaultValue={profile.search_goals}
                  placeholder="What are you looking for? (friends, work partners, etc.)"
                  {...register('search_goals')}
                />
              </div>

              <button type="submit" className="btn btn-primary">
                <Save size={16} />
                Save Profile
              </button>
            </form>
          ) : (
            <>
              {profile.bio && (
                <div className="profile-bio">
                  <h3>About Me</h3>
                  <p>{profile.bio}</p>
                </div>
              )}

              {profile.search_goals && (
                <div className="profile-goals">
                  <h3>What I'm Looking For</h3>
                  <p>{profile.search_goals}</p>
                </div>
              )}

              <div className="profile-interests">
                <h3>My Interests</h3>
                <div className="tags">
                  {userInterests.map(interest => (
                    <span key={interest.id} className="tag">
                      {interest.name}
                      <button 
                        onClick={() => removeInterest(interest.id)}
                        className="tag-remove"
                        type="button"
                      >
                        <X size={12} />
                      </button>
                    </span>
                  ))}
                </div>
                <div className="mt-2">
                  <div className="flex gap-2">
                    <input
                      type="text"
                      placeholder="Add custom interest..."
                      value={newInterest}
                      onChange={(e) => setNewInterest(e.target.value)}
                      className="form-input flex-1"
                      onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addCustomInterest())}
                    />
                    <button 
                      type="button"
                      onClick={addCustomInterest}
                      className="btn btn-primary"
                      disabled={!newInterest.trim()}
                    >
                      <Plus size={16} />
                    </button>
                  </div>
                  <select 
                    onChange={(e) => e.target.value && addInterest(parseInt(e.target.value))}
                    className="form-input mt-2"
                  >
                    <option value="">Or select from existing interests...</option>
                    {interests
                      .filter(interest => !userInterests.some(ui => ui.id === interest.id))
                      .map(interest => (
                        <option key={interest.id} value={interest.id}>
                          {interest.name}
                        </option>
                      ))}
                  </select>
                </div>
              </div>

              <div className="profile-skills">
                <h3>My Skills</h3>
                <div className="tags">
                  {userSkills.map(skill => (
                    <span key={skill.id} className="tag">
                      {skill.name}
                      <button 
                        onClick={() => removeSkill(skill.id)}
                        className="tag-remove"
                        type="button"
                      >
                        <X size={12} />
                      </button>
                    </span>
                  ))}
                </div>
                <div className="mt-2">
                  <div className="flex gap-2">
                    <input
                      type="text"
                      placeholder="Add custom skill..."
                      value={newSkill}
                      onChange={(e) => setNewSkill(e.target.value)}
                      className="form-input flex-1"
                      onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addCustomSkill())}
                    />
                    <button 
                      type="button"
                      onClick={addCustomSkill}
                      className="btn btn-primary"
                      disabled={!newSkill.trim()}
                    >
                      <Plus size={16} />
                    </button>
                  </div>
                  <select 
                    onChange={(e) => e.target.value && addSkill(parseInt(e.target.value))}
                    className="form-input mt-2"
                  >
                    <option value="">Or select from existing skills...</option>
                    {skills
                      .filter(skill => !userSkills.some(us => us.id === skill.id))
                      .map(skill => (
                        <option key={skill.id} value={skill.id}>
                          {skill.name}
                        </option>
                      ))}
                  </select>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default Profile;
