import React, { useState, useEffect } from 'react';
import api from '../config/axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

function Analytics() {
  const [userAnalytics, setUserAnalytics] = useState(null);
  const [platformAnalytics, setPlatformAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const [userResponse, platformResponse] = await Promise.all([
        api.get('/api/analytics/user'),
        api.get('/api/analytics/platform')
      ]);
      
      setUserAnalytics(userResponse.data);
      setPlatformAnalytics(platformResponse.data);
    } catch (error) {
      console.error('Failed to load analytics:', error);
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


  return (
    <div className="main-content">
      <div className="container">
        <h1 className="mb-4">Analytics Dashboard</h1>

        {userAnalytics && (
          <div className="analytics-grid">
            <div className="analytics-card">
              <h3>Your Stats</h3>
              <div className="stat-item">
                <span className="stat-label">Total Matches</span>
                <span className="stat-value">{userAnalytics.total_matches}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Mutual Matches</span>
                <span className="stat-value">{userAnalytics.mutual_matches}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Avg Compatibility</span>
                <span className="stat-value">
                  {Math.round(userAnalytics.average_compatibility * 100)}%
                </span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Profile Completion</span>
                <span className="stat-value">
                  {Math.round(userAnalytics.profile_completion_percentage)}%
                </span>
              </div>
            </div>

            <div className="analytics-card">
              <h3>Your Top Interests</h3>
              {userAnalytics.top_interests.length > 0 ? (
                <div className="tags">
                  {userAnalytics.top_interests.map((interest, index) => (
                    <span key={index} className="tag">{interest}</span>
                  ))}
                </div>
              ) : (
                <p className="text-muted">No interests added yet</p>
              )}
            </div>

            <div className="analytics-card">
              <h3>Your Top Skills</h3>
              {userAnalytics.top_skills.length > 0 ? (
                <div className="tags">
                  {userAnalytics.top_skills.map((skill, index) => (
                    <span key={index} className="tag">{skill}</span>
                  ))}
                </div>
              ) : (
                <p className="text-muted">No skills added yet</p>
              )}
            </div>
          </div>
        )}

        {platformAnalytics && (
          <>
            <div className="analytics-grid">
              <div className="analytics-card">
                <h3>Platform Overview</h3>
                <div className="stat-item">
                  <span className="stat-label">Total Users</span>
                  <span className="stat-value">{platformAnalytics.total_users}</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">Total Matches</span>
                  <span className="stat-value">{platformAnalytics.total_matches}</span>
                </div>
              </div>

              <div className="analytics-card">
                <h3>Popular Interests</h3>
                {platformAnalytics.popular_interests.length > 0 ? (
                  <div className="tags">
                    {platformAnalytics.popular_interests.slice(0, 5).map((interest, index) => (
                      <span key={index} className="tag">
                        {interest.name} ({interest.count})
                      </span>
                    ))}
                  </div>
                ) : (
                  <p className="text-muted">No data available</p>
                )}
              </div>

              <div className="analytics-card">
                <h3>Popular Skills</h3>
                {platformAnalytics.popular_skills.length > 0 ? (
                  <div className="tags">
                    {platformAnalytics.popular_skills.slice(0, 5).map((skill, index) => (
                      <span key={index} className="tag">
                        {skill.name} ({skill.count})
                      </span>
                    ))}
                  </div>
                ) : (
                  <p className="text-muted">No data available</p>
                )}
              </div>
            </div>

            {platformAnalytics.popular_interests.length > 0 && (
              <div className="analytics-card">
                <h3>Interest Distribution</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={platformAnalytics.popular_interests.slice(0, 10)}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="count" fill="#667eea" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            )}

            {platformAnalytics.popular_skills.length > 0 && (
              <div className="analytics-card">
                <h3>Skill Distribution</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={platformAnalytics.popular_skills.slice(0, 10)}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="count" fill="#764ba2" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            )}

            {platformAnalytics.geographic_distribution.length > 0 && (
              <div className="analytics-card">
                <h3>Geographic Distribution</h3>
                <div className="grid grid-2">
                  {platformAnalytics.geographic_distribution.slice(0, 10).map((location, index) => (
                    <div key={index} className="stat-item">
                      <span className="stat-label">{location.city}</span>
                      <span className="stat-value">{location.count} users</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default Analytics;
