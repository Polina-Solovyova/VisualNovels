// src/App.js
import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, useNavigate, useLocation } from 'react-router-dom';
import NovelListPage from '@pages/NovelListPage';
import NovelReaderPage from '@pages/NovelReaderPage';
import ProfilePage from './pages/ProfilePage';
import NovelDetail from "./pages/NovelDetail";
import AuthPage, { handleLogout } from "@pages/AuthPage";
import Header from './components/Header';
import { UserProvider } from '@providers/UserProvider';

const App = () => {
  const [isAuth, setIsAuth] = useState(false);

  return (
    <UserProvider>
      <Router>
        <AppContent isAuth={isAuth} setIsAuth={setIsAuth} />
      </Router>
    </UserProvider>
  );
};

const AppContent = ({ isAuth, setIsAuth }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleAppLogout = async () => {
    await handleLogout();
    setIsAuth(false);
    navigate('/login');
  };

  const hideHeaderPaths = ['/profile', '/'];
  const isHeaderVisible = hideHeaderPaths.includes(location.pathname);
  

  return (
    <>
      {isHeaderVisible && <Header onLogout={handleAppLogout} />}
      <Routes>
        <Route path="/" element={<NovelListPage />} />
        <Route path="/login" element={<AuthPage setIsAuth={setIsAuth} isRegistration={false} />} />
        <Route path="/register" element={<AuthPage setIsAuth={setIsAuth} isRegistration={true} />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/novel/:id/current-dialogue" element={<NovelReaderPage />} />
        <Route path="/novel/:id" element={<NovelDetail />} />
        <Route path="/logout" element={<Logout />} />
      </Routes>
    </>
  );
};

const Logout = () => {
  const navigate = useNavigate();

  React.useEffect(() => {
    const performLogout = async () => {
      await handleLogout();
      navigate('/login');
    };

    performLogout();
  }, [navigate]);

  return <p>Logging out...</p>;
};

export default App;
