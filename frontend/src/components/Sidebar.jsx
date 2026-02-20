import React, { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth, getTheme } from '../App';

const navItems = {
  student: [
    { to: '/dashboard', icon: '📊', label: 'Dashboard' },
    { to: '/learning-path', icon: '🗺️', label: 'My Learning Path' },
    { to: '/tutor', icon: '🤖', label: 'AI Tutor' },
    { to: '/quiz', icon: '🧪', label: 'Quiz Arena' },
    { to: '/flashcards', icon: '🃏', label: 'Flashcard Studio' },
    { to: '/concepts', icon: '📚', label: 'Concept Library' },
    { to: '/challenge', icon: '⚔️', label: 'Daily Challenge' },
    { to: '/leaderboard', icon: '🏆', label: 'Leaderboard' },
    { to: '/progress', icon: '📈', label: 'My Progress' },
    { to: '/badges', icon: '🏅', label: 'Badge Collection' },
  ],
  admin: [
    { to: '/admin', icon: '👨‍💼', label: 'Admin Dashboard' },
    { to: '/leaderboard', icon: '🏆', label: 'Leaderboard' },
  ],
};

const activeStyles = {
  gaming: 'bg-green-500/15 text-green-400 font-semibold',
  business: 'bg-amber-500/15 text-amber-400 font-semibold',
  developer: 'bg-cyan-500/15 text-cyan-400 font-semibold',
  ai_enthusiast: 'bg-pink-500/15 text-pink-400 font-semibold',
  admin: 'bg-rose-500/15 text-rose-400 font-semibold',
};

export default function Sidebar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);
  const theme = getTheme(user?.path_id);

  const links = user?.role === 'admin' ? navItems.admin : navItems.student;
  const activeClass = activeStyles[user?.path_id] || activeStyles.gaming;

  const handleLogout = () => { logout(); navigate('/login'); };

  return (
    <>
      {/* Mobile hamburger */}
      <button onClick={() => setOpen(true)}
        className="md:hidden fixed top-4 left-4 z-50 bg-gray-800 p-2.5 rounded-lg text-lg border border-gray-700">
        ☰
      </button>

      {/* Mobile overlay */}
      {open && <div className="md:hidden fixed inset-0 bg-black/60 z-40" onClick={() => setOpen(false)} />}

      {/* Sidebar */}
      <aside className={`fixed md:static z-50 h-full w-64 bg-gray-900/95 backdrop-blur-lg border-r border-gray-800 flex flex-col transform transition-transform duration-300 ${open ? 'translate-x-0' : '-translate-x-full'} md:translate-x-0`}>
        {/* Profile header */}
        <div className="p-4 border-b border-gray-800">
          <button onClick={() => setOpen(false)} className="md:hidden float-right text-gray-400 hover:text-white text-lg">✕</button>
          <div className="flex items-center gap-3">
            <span className="text-3xl">{user?.avatar}</span>
            <div className="min-w-0">
              <h2 className={`font-bold truncate ${theme.accent}`}>{user?.name}</h2>
              <p className="text-xs text-gray-400">{user?.level} · {user?.total_xp} XP</p>
            </div>
          </div>
          {user?.current_streak > 0 && (
            <div className="mt-2 flex items-center gap-1 text-sm text-orange-400">
              🔥 {user.current_streak} day streak
            </div>
          )}
        </div>

        {/* Nav links */}
        <nav className="flex-1 overflow-y-auto p-3 space-y-1">
          {links.map(({ to, icon, label }) => (
            <NavLink key={to} to={to} onClick={() => setOpen(false)}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-all ${
                  isActive ? activeClass : 'text-gray-400 hover:text-white hover:bg-gray-800/60'
                }`
              }>
              <span className="text-lg w-6 text-center">{icon}</span>
              {label}
            </NavLink>
          ))}
        </nav>

        {/* Logout */}
        <div className="p-3 border-t border-gray-800">
          <button onClick={handleLogout}
            className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-gray-400 hover:text-red-400 hover:bg-red-500/10 w-full transition-all">
            <span className="text-lg w-6 text-center">🚪</span> Logout
          </button>
        </div>
      </aside>
    </>
  );
}
