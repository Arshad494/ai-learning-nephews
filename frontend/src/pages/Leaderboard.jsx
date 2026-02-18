import React, { useState, useEffect } from 'react';
import { useAuth, getTheme } from '../App';
import api from '../api';

const rankIcons = ['🥇', '🥈', '🥉', '4️⃣'];
const pathIcons = { gaming: '🎮', business: '💼', developer: '💻' };

export default function Leaderboard() {
  const { user } = useAuth();
  const theme = getTheme(user?.path_id);
  const [leaderboard, setLeaderboard] = useState([]);
  const [tab, setTab] = useState('all');

  useEffect(() => {
    api.getLeaderboard(tab).then(setLeaderboard).catch(() => {});
  }, [tab]);

  return (
    <div className="max-w-2xl mx-auto animate-fade-in">
      <h1 className={`text-3xl font-black ${theme.accent} mb-2`}>🏆 Leaderboard</h1>
      <p className="text-gray-400 mb-6">Who's the AI King today?</p>

      {/* Tabs */}
      <div className="flex gap-2 mb-6">
        {['all', 'weekly'].map(t => (
          <button key={t} onClick={() => setTab(t)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
              tab === t ? `bg-gradient-to-r ${theme.gradient} text-white` : 'bg-gray-800 text-gray-400'
            }`}>
            {t === 'all' ? '🌟 All Time' : '📅 This Week'}
          </button>
        ))}
      </div>

      {/* Podium for top 3 */}
      {leaderboard.length >= 3 && (
        <div className="flex items-end justify-center gap-4 mb-8">
          <PodiumCard player={leaderboard[1]} rank={2} theme={theme} user={user} />
          <PodiumCard player={leaderboard[0]} rank={1} theme={theme} user={user} isFirst />
          <PodiumCard player={leaderboard[2]} rank={3} theme={theme} user={user} />
        </div>
      )}

      {/* Full list */}
      <div className="space-y-3">
        {leaderboard.map((player, i) => (
          <div key={player.name}
            className={`${theme.card} rounded-xl p-4 flex items-center gap-4 ${
              player.name === user?.name ? `ring-2 ring-offset-2 ring-offset-gray-950 ${theme.border.replace('border', 'ring')}` : ''
            }`}>
            <span className="text-2xl w-10 text-center">{rankIcons[i] || `#${i + 1}`}</span>
            <span className="text-3xl">{player.avatar}</span>
            <div className="flex-1">
              <div className="flex items-center gap-2">
                <h3 className={`font-bold ${player.name === user?.name ? theme.accent : 'text-white'}`}>
                  {player.name}
                </h3>
                <span className="text-xs text-gray-500">{pathIcons[player.path_id]}</span>
              </div>
              <p className="text-xs text-gray-400">{player.level} · 🔥 {player.current_streak} day streak</p>
            </div>
            <div className="text-right">
              <p className={`font-bold text-lg ${theme.accent}`}>{player.total_xp}</p>
              <p className="text-xs text-gray-400">XP</p>
            </div>
          </div>
        ))}
      </div>

      {/* Competitive messages */}
      <div className={`${theme.card} rounded-xl p-4 mt-6`}>
        <h3 className="font-bold text-white mb-2">💬 Competitive Corner</h3>
        <div className="space-y-2 text-sm">
          {leaderboard.map((p, i) => (
            <div key={p.name} className="flex items-center gap-2 text-gray-400">
              <span>{p.avatar}</span>
              <span className="font-medium text-white">{p.name}:</span>
              <span className="italic">{p.message}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function PodiumCard({ player, rank, theme, user, isFirst }) {
  return (
    <div className={`flex flex-col items-center ${isFirst ? 'mb-4' : ''}`}>
      <span className="text-4xl mb-2">{player.avatar}</span>
      <span className={`font-bold text-sm ${player.name === user?.name ? theme.accent : 'text-white'}`}>
        {player.name}
      </span>
      <span className="text-xs text-gray-400">{player.total_xp} XP</span>
      <div className={`mt-2 flex items-center justify-center rounded-t-lg ${
        rank === 1 ? 'bg-amber-500/30 w-20 h-24' :
        rank === 2 ? 'bg-gray-500/30 w-16 h-16' :
        'bg-orange-800/30 w-16 h-12'
      }`}>
        <span className="text-3xl">{rankIcons[rank - 1]}</span>
      </div>
    </div>
  );
}
