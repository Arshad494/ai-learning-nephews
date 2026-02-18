import React, { useState, useEffect } from 'react';
import { useAuth, getTheme } from '../App';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, LineChart, Line, CartesianGrid, PieChart, Pie, Cell } from 'recharts';
import api from '../api';

export default function MyProgress() {
  const { user } = useAuth();
  const theme = getTheme(user?.path_id);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user) {
      api.getAnalytics(user.id).then(data => {
        setAnalytics(data);
        setLoading(false);
      }).catch(() => setLoading(false));
    }
  }, [user]);

  if (loading) return <div className="flex items-center justify-center h-64"><div className="text-4xl animate-bounce">📈</div></div>;
  if (!analytics) return <div className="text-gray-400 text-center mt-20">No data yet. Start learning!</div>;

  const colorMap = { gaming: '#00ff88', business: '#f59e0b', developer: '#06b6d4' };
  const accentColor = colorMap[user?.path_id] || '#00ff88';

  const pieData = [
    { name: 'Completed', value: analytics.topics_completed },
    { name: 'Remaining', value: analytics.topics_total - analytics.topics_completed },
  ];
  const COLORS = [accentColor, '#374151'];

  return (
    <div className="max-w-5xl mx-auto animate-fade-in">
      <h1 className={`text-3xl font-black ${theme.accent} mb-6`}>📈 My Progress</h1>

      {/* Stats grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
        <Stat icon="⚡" label="Total XP" value={analytics.total_xp} theme={theme} />
        <Stat icon="🔥" label="Current Streak" value={`${analytics.current_streak} days`} theme={theme} />
        <Stat icon="🏆" label="Longest Streak" value={`${analytics.longest_streak} days`} theme={theme} />
        <Stat icon="📊" label="Avg Quiz Score" value={`${analytics.avg_quiz_score}%`} theme={theme} />
        <Stat icon="📚" label="Topics Done" value={`${analytics.topics_completed}/${analytics.topics_total}`} theme={theme} />
        <Stat icon="🧪" label="Quizzes Taken" value={analytics.total_quizzes} theme={theme} />
        <Stat icon="💯" label="Perfect Scores" value={analytics.perfect_scores} theme={theme} />
        <Stat icon="🏅" label="Badges" value={`${analytics.badges_earned}/${analytics.total_badges}`} theme={theme} />
      </div>

      <div className="grid md:grid-cols-2 gap-4 mb-6">
        {/* XP over time */}
        <div className={`${theme.card} rounded-2xl p-5`}>
          <h3 className="font-bold text-white mb-3">⚡ XP Over Time</h3>
          {analytics.xp_chart.length > 0 ? (
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={analytics.xp_chart}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="date" tick={{ fill: '#9ca3af', fontSize: 10 }} />
                <YAxis tick={{ fill: '#9ca3af', fontSize: 10 }} />
                <Tooltip contentStyle={{ background: '#1f2937', border: '1px solid #374151', borderRadius: 8 }} />
                <Bar dataKey="xp" fill={accentColor} radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : <p className="text-gray-500 text-sm text-center py-8">No XP data yet</p>}
        </div>

        {/* Quiz performance */}
        <div className={`${theme.card} rounded-2xl p-5`}>
          <h3 className="font-bold text-white mb-3">🧪 Quiz Scores</h3>
          {analytics.quiz_chart.length > 0 ? (
            <ResponsiveContainer width="100%" height={200}>
              <LineChart data={analytics.quiz_chart}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="date" tick={{ fill: '#9ca3af', fontSize: 10 }} />
                <YAxis tick={{ fill: '#9ca3af', fontSize: 10 }} domain={[0, 100]} />
                <Tooltip contentStyle={{ background: '#1f2937', border: '1px solid #374151', borderRadius: 8 }} />
                <Line type="monotone" dataKey="score" stroke={accentColor} strokeWidth={2} dot={{ fill: accentColor }} />
              </LineChart>
            </ResponsiveContainer>
          ) : <p className="text-gray-500 text-sm text-center py-8">No quiz data yet</p>}
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        {/* Topic completion pie */}
        <div className={`${theme.card} rounded-2xl p-5`}>
          <h3 className="font-bold text-white mb-3">📚 Topic Completion</h3>
          <div className="flex items-center justify-center">
            <ResponsiveContainer width="100%" height={200}>
              <PieChart>
                <Pie data={pieData} cx="50%" cy="50%" innerRadius={50} outerRadius={80} dataKey="value">
                  {pieData.map((_, i) => <Cell key={i} fill={COLORS[i]} />)}
                </Pie>
                <Tooltip contentStyle={{ background: '#1f2937', border: '1px solid #374151', borderRadius: 8 }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <p className="text-center text-sm text-gray-400">
            {analytics.topics_completed}/{analytics.topics_total} topics ({Math.round((analytics.topics_completed / analytics.topics_total) * 100)}%)
          </p>
        </div>

        {/* Activity summary */}
        <div className={`${theme.card} rounded-2xl p-5`}>
          <h3 className="font-bold text-white mb-3">📊 Activity Summary</h3>
          <div className="space-y-4">
            <ProgressBar label="Topics" current={analytics.topics_completed} max={analytics.topics_total} color={accentColor} />
            <ProgressBar label="Badges" current={analytics.badges_earned} max={analytics.total_badges} color={accentColor} />
            <ProgressBar label="Challenges" current={analytics.challenges_completed} max={30} color={accentColor} />
          </div>
          <div className="mt-4 flex items-center gap-2 text-sm text-gray-400">
            <span>🤖</span>
            <span>{analytics.tutor_questions} questions asked to AI tutor</span>
          </div>
        </div>
      </div>
    </div>
  );
}

function Stat({ icon, label, value, theme }) {
  return (
    <div className={`${theme.card} rounded-xl p-4 text-center`}>
      <span className="text-xl">{icon}</span>
      <p className="text-xl font-bold text-white mt-1">{value}</p>
      <p className="text-xs text-gray-400">{label}</p>
    </div>
  );
}

function ProgressBar({ label, current, max, color }) {
  const pct = max > 0 ? (current / max) * 100 : 0;
  return (
    <div>
      <div className="flex justify-between text-xs text-gray-400 mb-1">
        <span>{label}</span>
        <span>{current}/{max}</span>
      </div>
      <div className="w-full bg-gray-800 rounded-full h-2">
        <div className="h-full rounded-full transition-all" style={{ width: `${pct}%`, backgroundColor: color }} />
      </div>
    </div>
  );
}
