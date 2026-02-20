import React, { useState, useEffect, createContext, useContext } from 'react';
import { BrowserRouter, Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom';
import { Toaster, toast } from 'react-hot-toast';

import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import LearningPath from './pages/LearningPath';
import TopicDetail from './pages/TopicDetail';
import AITutor from './pages/AITutor';
import QuizArena from './pages/QuizArena';
import FlashcardStudio from './pages/FlashcardStudio';
import ConceptLibrary from './pages/ConceptLibrary';
import DailyChallengePage from './pages/DailyChallenge';
import Leaderboard from './pages/Leaderboard';
import MyProgress from './pages/MyProgress';
import BadgeCollection from './pages/BadgeCollection';
import AdminDashboard from './pages/AdminDashboard';
import Sidebar from './components/Sidebar';

export const AuthContext = createContext(null);

export function useAuth() {
  return useContext(AuthContext);
}

export function getTheme(pathId) {
  const themes = {
    gaming: { primary: '#00ff88', secondary: '#a855f7', bg: '#0a0e17', card: 'card-gaming', accent: 'text-green-400', accentBg: 'bg-green-500', border: 'border-green-500/30', neon: 'neon-text-green', gradient: 'from-green-500 to-purple-500' },
    business: { primary: '#f59e0b', secondary: '#1e3a5f', bg: '#0f172a', card: 'card-business', accent: 'text-amber-400', accentBg: 'bg-amber-500', border: 'border-amber-500/30', neon: 'neon-text-gold', gradient: 'from-amber-500 to-blue-600' },
    developer: { primary: '#06b6d4', secondary: '#8b5cf6', bg: '#0c0a09', card: 'card-developer', accent: 'text-cyan-400', accentBg: 'bg-cyan-500', border: 'border-cyan-500/30', neon: 'neon-text-cyan', gradient: 'from-cyan-500 to-purple-500' },
    ai_enthusiast: { primary: '#ec4899', secondary: '#8b5cf6', bg: '#0f0a1e', card: 'card-developer', accent: 'text-pink-400', accentBg: 'bg-pink-500', border: 'border-pink-500/30', neon: 'neon-text-cyan', gradient: 'from-pink-500 to-purple-600' },
    admin: { primary: '#f43f5e', secondary: '#6366f1', bg: '#0f172a', card: 'card-business', accent: 'text-rose-400', accentBg: 'bg-rose-500', border: 'border-rose-500/30', neon: '', gradient: 'from-rose-500 to-indigo-500' },
  };
  return themes[pathId] || themes.gaming;
}

function ProtectedRoute({ children }) {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" replace />;
  return children;
}

function AppLayout() {
  const { user } = useAuth();
  const location = useLocation();
  const isLogin = location.pathname === '/login';

  if (isLogin || !user) return <Routes><Route path="*" element={<Login />} /></Routes>;

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-4 md:p-6">
        <Routes>
          <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
          <Route path="/learning-path" element={<ProtectedRoute><LearningPath /></ProtectedRoute>} />
          <Route path="/topic/:topicId" element={<ProtectedRoute><TopicDetail /></ProtectedRoute>} />
          <Route path="/tutor" element={<ProtectedRoute><AITutor /></ProtectedRoute>} />
          <Route path="/quiz" element={<ProtectedRoute><QuizArena /></ProtectedRoute>} />
          <Route path="/quiz/:topicId" element={<ProtectedRoute><QuizArena /></ProtectedRoute>} />
          <Route path="/flashcards" element={<ProtectedRoute><FlashcardStudio /></ProtectedRoute>} />
          <Route path="/concepts" element={<ProtectedRoute><ConceptLibrary /></ProtectedRoute>} />
          <Route path="/challenge" element={<ProtectedRoute><DailyChallengePage /></ProtectedRoute>} />
          <Route path="/leaderboard" element={<ProtectedRoute><Leaderboard /></ProtectedRoute>} />
          <Route path="/progress" element={<ProtectedRoute><MyProgress /></ProtectedRoute>} />
          <Route path="/badges" element={<ProtectedRoute><BadgeCollection /></ProtectedRoute>} />
          <Route path="/admin" element={<ProtectedRoute><AdminDashboard /></ProtectedRoute>} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </main>
    </div>
  );
}

export default function App() {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('ai_learning_user');
    return saved ? JSON.parse(saved) : null;
  });

  const login = (userData) => {
    setUser(userData);
    localStorage.setItem('ai_learning_user', JSON.stringify(userData));
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('ai_learning_user');
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      <BrowserRouter>
        <Toaster position="top-right" toastOptions={{
          style: { background: '#1f2937', color: '#fff', border: '1px solid #374151' },
          duration: 3000,
        }} />
        <AppLayout />
      </BrowserRouter>
    </AuthContext.Provider>
  );
}
