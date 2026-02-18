import React, { useState, useEffect } from 'react';
import { useAuth, getTheme } from '../App';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';
import api from '../api';

const pathColors = { gaming: '#00ff88', business: '#f59e0b', developer: '#06b6d4' };
const pathIcons = { gaming: '🎮', business: '💼', developer: '💻' };

export default function AdminDashboard() {
  const { user } = useAuth();
  const theme = getTheme('admin');
  const [overview, setOverview] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.adminOverview().then(data => {
      setOverview(data);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="flex items-center justify-center h-64"><div className="text-4xl animate-bounce">👨‍💼</div></div>;

  const xpData = overview.map(s => ({ name: s.name, xp: s.total_xp }));

  const radarData = overview.map(s => ({
    name: s.name,
    Topics: s.topics_total > 0 ? Math.round((s.topics_completed / s.topics_total) * 100) : 0,
    Quizzes: Math.min(s.quizzes_taken * 10, 100),
    Badges: Math.round((s.badges_earned / 25) * 100),
    Challenges: Math.round((s.challenges_completed / 30) * 100),
    Streak: Math.min(s.current_streak * 10, 100),
  }));

  return (
    <div className="max-w-6xl mx-auto animate-fade-in">
      <div className="rounded-2xl p-6 bg-gradient-to-r from-rose-500 to-indigo-500 mb-6">
        <h1 className="text-3xl font-black text-white">👨‍💼 Admin Dashboard</h1>
        <p className="text-white/80">Monitor all nephews' progress in one place</p>
      </div>

      {/* Student Cards */}
      <div className="grid md:grid-cols-2 gap-4 mb-6">
        {overview.map(s => (
          <div key={s.id} className={`bg-gray-900 border border-gray-800 rounded-2xl p-5`}>
            <div className="flex items-center gap-3 mb-4">
              <span className="text-4xl">{s.avatar}</span>
              <div>
                <h3 className="font-bold text-white text-lg">{s.name}</h3>
                <p className="text-sm text-gray-400">
                  Age {s.age} · {pathIcons[s.path_id]} {s.path_id} · {s.level}
                </p>
              </div>
              <div className="ml-auto text-right">
                <p className="font-bold text-lg" style={{ color: pathColors[s.path_id] }}>{s.total_xp} XP</p>
                <p className="text-xs text-orange-400">🔥 {s.current_streak} streak</p>
              </div>
            </div>

            <div className="grid grid-cols-4 gap-2 text-center text-xs">
              <div className="bg-gray-800 rounded-lg p-2">
                <p className="font-bold text-white">{s.topics_completed}/{s.topics_total}</p>
                <p className="text-gray-500">Topics</p>
              </div>
              <div className="bg-gray-800 rounded-lg p-2">
                <p className="font-bold text-white">{s.quizzes_taken}</p>
                <p className="text-gray-500">Quizzes</p>
              </div>
              <div className="bg-gray-800 rounded-lg p-2">
                <p className="font-bold text-white">{s.badges_earned}</p>
                <p className="text-gray-500">Badges</p>
              </div>
              <div className="bg-gray-800 rounded-lg p-2">
                <p className="font-bold text-white">{s.challenges_completed}</p>
                <p className="text-gray-500">Challenges</p>
              </div>
            </div>

            <div className="mt-3">
              <div className="flex justify-between text-xs text-gray-400 mb-1">
                <span>Path Progress</span>
                <span>{s.topics_total > 0 ? Math.round((s.topics_completed / s.topics_total) * 100) : 0}%</span>
              </div>
              <div className="w-full bg-gray-800 rounded-full h-2">
                <div className="h-full rounded-full transition-all"
                  style={{
                    width: `${s.topics_total > 0 ? (s.topics_completed / s.topics_total) * 100 : 0}%`,
                    backgroundColor: pathColors[s.path_id]
                  }} />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Charts */}
      <div className="grid md:grid-cols-2 gap-4">
        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-5">
          <h3 className="font-bold text-white mb-3">⚡ XP Comparison</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={xpData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="name" tick={{ fill: '#9ca3af' }} />
              <YAxis tick={{ fill: '#9ca3af' }} />
              <Tooltip contentStyle={{ background: '#1f2937', border: '1px solid #374151', borderRadius: 8 }} />
              <Bar dataKey="xp" radius={[8, 8, 0, 0]}>
                {xpData.map((_, i) => {
                  const student = overview[i];
                  return <rect key={i} fill={pathColors[student?.path_id] || '#666'} />;
                })}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-5">
          <h3 className="font-bold text-white mb-3">📊 Overall Activity</h3>
          <div className="space-y-4">
            {overview.map(s => (
              <div key={s.id} className="flex items-center gap-3">
                <span className="text-2xl">{s.avatar}</span>
                <div className="flex-1">
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-white font-medium">{s.name}</span>
                    <span className="text-gray-400">{s.level}</span>
                  </div>
                  <div className="w-full bg-gray-800 rounded-full h-2.5">
                    <div className="h-full rounded-full transition-all"
                      style={{
                        width: `${Math.min((s.total_xp / 5000) * 100, 100)}%`,
                        backgroundColor: pathColors[s.path_id]
                      }} />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
