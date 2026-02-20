import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth, getTheme } from '../App';
import api from '../api';

const pathLabels = {
  gaming: '🎮 AI in Gaming',
  business: '💼 AI for Business',
  developer: '💻 AI Developer',
  ai_enthusiast: '🤖 AI Enthusiast',
};
const pathGreetings = {
  gaming: (name) => `Yo ${name}! Ready to level up? 🎮`,
  business: (name) => `Welcome back, ${name}! Let's build empires 💼`,
  developer: (name) => `Hey ${name}! Let's build something cool 💻`,
  ai_enthusiast: () => `Welcome, AI Explorer! The revolution starts here 🤖`,
};

export default function Dashboard() {
  const { user, login } = useAuth();
  const theme = getTheme(user?.path_id);
  const [analytics, setAnalytics] = useState(null);
  const [challenge, setChallenge] = useState(null);
  const [leaderboard, setLeaderboard] = useState([]);
  const [freshUser, setFreshUser] = useState(user);

  useEffect(() => {
    if (!user) return;
    // Refresh user data from server
    api.getStudent(user.id).then(data => {
      setFreshUser(data);
      login(data); // update localStorage too
    }).catch(() => {});
    api.getAnalytics(user.id).then(setAnalytics).catch(() => {});
    api.getTodayChallenge(user.id).then(setChallenge).catch(() => {});
    api.getLeaderboard().then(setLeaderboard).catch(() => {});
  }, [user?.id]);

  if (!user) return null;

  const u = freshUser || user;
  const xpForNext = [500, 1500, 3000, 5000, 10000];
  const currentIdx = xpForNext.findIndex(x => u.total_xp < x);
  const nextXP = currentIdx >= 0 ? xpForNext[currentIdx] : 10000;
  const prevXP = currentIdx > 0 ? xpForNext[currentIdx - 1] : 0;
  const progress = Math.min(((u.total_xp - prevXP) / (nextXP - prevXP)) * 100, 100);
  const greeting = (pathGreetings[u.path_id] || pathGreetings.gaming)(u.name);

  return (
    <div className="max-w-6xl mx-auto space-y-6 animate-fade-in">
      {/* Header */}
      <div className={`rounded-2xl p-6 bg-gradient-to-r ${theme.gradient} relative overflow-hidden`}>
        <div className="relative z-10">
          <h1 className="text-2xl md:text-3xl font-black text-white">{greeting}</h1>
          <p className="text-white/80 mt-1">{pathLabels[u.path_id]} · {u.level}</p>
        </div>
        <div className="absolute right-6 top-1/2 -translate-y-1/2 text-8xl opacity-20 select-none">{u.avatar}</div>
      </div>

      {/* Stats Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard icon="⚡" label="Total XP" value={u.total_xp} theme={theme} />
        <StatCard icon="🔥" label="Streak" value={`${u.current_streak} days`} theme={theme} />
        <StatCard icon="📚" label="Topics Done" value={`${analytics?.topics_completed ?? 0}/${analytics?.topics_total ?? 20}`} theme={theme} />
        <StatCard icon="🏆" label="Badges" value={`${analytics?.badges_earned ?? 0}/${analytics?.total_badges ?? 25}`} theme={theme} />
      </div>

      {/* XP Progress Bar */}
      <div className={`${theme.card} rounded-2xl p-5`}>
        <div className="flex justify-between items-center mb-2">
          <span className="font-semibold text-white">Level Progress</span>
          <span className={`text-sm ${theme.accent}`}>{u.level}</span>
        </div>
        <div className="w-full bg-gray-800 rounded-full h-4 overflow-hidden">
          <div className={`h-full rounded-full bg-gradient-to-r ${theme.gradient} transition-all duration-1000 ease-out`}
            style={{ width: `${progress}%` }} />
        </div>
        <p className="text-xs text-gray-400 mt-1">{u.total_xp} / {nextXP} XP</p>
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        {/* Daily Challenge */}
        <Link to="/challenge" className={`${theme.card} rounded-2xl p-5 hover:scale-[1.02] transition-transform`}>
          <div className="flex items-center gap-3 mb-3">
            <span className="text-3xl">⚔️</span>
            <div>
              <h3 className="font-bold text-white">Today's Challenge</h3>
              <span className="text-xs text-gray-400">{challenge?.completed ? '✅ Completed!' : '+100 XP'}</span>
            </div>
          </div>
          {challenge ? (
            <p className="text-sm text-gray-300 overflow-hidden" style={{display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical'}}>{challenge.text}</p>
          ) : (
            <p className="text-sm text-gray-500">Loading today's mission...</p>
          )}
        </Link>

        {/* Mini Leaderboard */}
        <Link to="/leaderboard" className={`${theme.card} rounded-2xl p-5 hover:scale-[1.02] transition-transform`}>
          <h3 className="font-bold text-white mb-3">🏆 Leaderboard</h3>
          <div className="space-y-2">
            {leaderboard.slice(0, 4).map((s, i) => (
              <div key={s.name} className={`flex items-center gap-3 text-sm ${s.name === u.name ? theme.accent + ' font-bold' : 'text-gray-300'}`}>
                <span className="w-6 text-center">{i === 0 ? '🥇' : i === 1 ? '🥈' : i === 2 ? '🥉' : '4️⃣'}</span>
                <span>{s.avatar}</span>
                <span className="flex-1">{s.name}</span>
                <span>{s.total_xp} XP</span>
              </div>
            ))}
            {leaderboard.length === 0 && <p className="text-sm text-gray-500">Loading...</p>}
          </div>
        </Link>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <QuickAction to="/learning-path" icon="🗺️" label="Continue Learning" theme={theme} />
        <QuickAction to="/tutor" icon="🤖" label="Ask AI Tutor" theme={theme} />
        <QuickAction to="/quiz" icon="🧪" label="Take a Quiz" theme={theme} />
        <QuickAction to="/flashcards" icon="🃏" label="Study Flashcards" theme={theme} />
      </div>
    </div>
  );
}

function StatCard({ icon, label, value, theme }) {
  return (
    <div className={`${theme.card} rounded-xl p-4 text-center`}>
      <span className="text-2xl">{icon}</span>
      <p className="text-2xl font-bold text-white mt-1">{value}</p>
      <p className="text-xs text-gray-400">{label}</p>
    </div>
  );
}

function QuickAction({ to, icon, label, theme }) {
  return (
    <Link to={to} className={`${theme.card} rounded-xl p-4 text-center hover:scale-105 transition-transform`}>
      <span className="text-3xl block">{icon}</span>
      <span className="text-sm font-medium text-gray-300 mt-2 block">{label}</span>
    </Link>
  );
}
