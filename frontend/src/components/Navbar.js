import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useLanguage } from '../contexts/LanguageContext';
import { Users, User, BarChart3, Heart, Search, MessageCircle, Bot, Globe } from 'lucide-react';
import './Navbar.css';

function Navbar() {
  const { user, logout } = useAuth();
  const { language, changeLanguage, availableLanguages, t } = useLanguage();
  const location = useLocation();
  const [showLangMenu, setShowLangMenu] = useState(false);

  const navItems = [
    { path: '/', label: t('nav.discover'), icon: Users, exact: true },
    { path: '/search', label: t('nav.search'), icon: Search },
    { path: '/ai-search', label: t('nav.aiSearch'), icon: Bot },
    { path: '/chat', label: t('nav.chat'), icon: MessageCircle },
    { path: '/profile', label: t('nav.profile'), icon: User },
    { path: '/analytics', label: t('nav.analytics'), icon: BarChart3 },
    { path: '/matches', label: t('nav.matches'), icon: Heart }
  ];

  return (
    <nav className="navbar">
      <div className="container">
        <div className="navbar-content">
          <Link to="/" className="navbar-brand">
            <Users className="navbar-icon" />
            LegitSearch
          </Link>
          
          <div className="navbar-nav">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = item.exact 
                ? location.pathname === item.path
                : location.pathname.startsWith(item.path);
              
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`navbar-link ${isActive ? 'active' : ''}`}
                >
                  {Icon && <Icon className="navbar-link-icon" />}
                  {item.label}
                </Link>
              );
            })}
          </div>
          
          <div className="navbar-user">
            <div style={{position: 'relative', marginRight: '16px'}}>
              <button 
                onClick={() => setShowLangMenu(!showLangMenu)}
                className="btn btn-secondary"
                style={{display: 'flex', alignItems: 'center', gap: '6px'}}
              >
                <Globe size={16} />
                {availableLanguages.find(l => l.code === language)?.flag}
              </button>
              {showLangMenu && (
                <div style={{
                  position: 'absolute',
                  top: '100%',
                  right: 0,
                  marginTop: '8px',
                  background: 'white',
                  borderRadius: '8px',
                  boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
                  padding: '8px',
                  zIndex: 1000,
                  minWidth: '150px'
                }}>
                  {availableLanguages.map(lang => (
                    <button
                      key={lang.code}
                      onClick={() => {
                        changeLanguage(lang.code);
                        setShowLangMenu(false);
                      }}
                      style={{
                        width: '100%',
                        padding: '8px 12px',
                        border: 'none',
                        background: language === lang.code ? '#1a8f6f' : 'transparent',
                        color: language === lang.code ? 'white' : '#333',
                        borderRadius: '6px',
                        cursor: 'pointer',
                        textAlign: 'left',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        fontSize: '14px',
                        transition: 'all 0.2s'
                      }}
                      onMouseEnter={(e) => {
                        if (language !== lang.code) {
                          e.target.style.background = '#f0f0f0';
                        }
                      }}
                      onMouseLeave={(e) => {
                        if (language !== lang.code) {
                          e.target.style.background = 'transparent';
                        }
                      }}
                    >
                      <span>{lang.flag}</span>
                      <span>{lang.name}</span>
                    </button>
                  ))}
                </div>
              )}
            </div>
            <span className="navbar-user-email">{user?.email}</span>
            <button onClick={logout} className="btn btn-secondary">
              {t('nav.logout')}
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
