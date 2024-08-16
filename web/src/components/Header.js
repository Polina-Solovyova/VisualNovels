import React from 'react';
import { useNavigate, Link } from 'react-router-dom';
import '../css/Header.css';

const Header = ({ onLogout }) => {
  const navigate = useNavigate();

  const handleLogoutClick = () => {
    onLogout(navigate);
  };

  return (
    <header className="header">
      <div className="header-container">

        {/* Логотип слева */}
        <div className="header-logo">
          <Link to="/">
            <img src="/logo.svg" alt="Logo" className="logo"/>
          </Link>
        </div>

        {/* Ссылки справа */}
        <div className="header-text">
          <Link to="/profile">Profile</Link>
          <Link to="/">Novels</Link>
          <Link to="/logout">Logout</Link>
        </div>
      </div>
    </header>
  );
};

export default Header;
