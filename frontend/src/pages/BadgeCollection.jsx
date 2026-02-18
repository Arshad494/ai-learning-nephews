import React, { useState, useEffect } from 'react';
import { useAuth, getTheme } from '../App';
import api from '../api';

export default function BadgeCollection() {
  const { user } = useAuth();
  const theme = getTheme(user?.path_id);
  const [allBadges, setAllBadges] = useState([]);
  const [earned, setEarned] = useState([]);

  useEffect(() => {
    if (user) {
      api.getAllBadges().then(setAllBadges).catch(() => {});
      api.getStudentBadges(user.id).then(setEarned).catch(() => {});
    }
  }, [user]);

  const earnedIds = new Set(earned.map(b => b.id));

  const categories = {
    general: { label: '🌟 General', badges: [] },
    quiz: { label: '🧪 Quiz', badges: [] },
    streak: { label: '🔥 Streak', badges: [] },
    path_specific: { label: '⭐ Special', badges: [] },
  };

  allBadges.forEach(b => {
    if (categories[b.category]) categories[b.category].badges.push(b);
  });

  return (
    <div className="max-w-4xl mx-auto animate-fade-in">
      <h1 className={`text-3xl font-black ${theme.accent} mb-2`}>🏅 Badge Collection</h1>
      <p className="text-gray-400 mb-6">{earned.length}/{allBadges.length} badges earned</p>

      {/* Progress */}
      <div className="w-full bg-gray-800 rounded-full h-3 mb-8 overflow-hidden">
        <div className={`h-full rounded-full bg-gradient-to-r ${theme.gradient} transition-all`}
          style={{ width: `${allBadges.length ? (earned.length / allBadges.length) * 100 : 0}%` }} />
      </div>

      {Object.entries(categories).map(([key, { label, badges }]) => (
        badges.length > 0 && (
          <div key={key} className="mb-8">
            <h2 className="text-lg font-bold text-white mb-3">{label}</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {badges.map(badge => {
                const isEarned = earnedIds.has(badge.id);
                const earnedData = earned.find(e => e.id === badge.id);
                return (
                  <div key={badge.id}
                    className={`${theme.card} rounded-xl p-4 text-center transition-all ${
                      isEarned ? 'ring-2 ring-amber-500/50' : 'opacity-40 grayscale'
                    }`}>
                    <span className="text-4xl block mb-2">{badge.icon}</span>
                    <h3 className={`font-bold text-sm ${isEarned ? 'text-white' : 'text-gray-500'}`}>
                      {badge.name}
                    </h3>
                    <p className="text-xs text-gray-400 mt-1">{badge.description}</p>
                    {isEarned && earnedData && (
                      <p className="text-xs text-amber-400 mt-2">
                        ✨ Earned {new Date(earnedData.earned_at).toLocaleDateString()}
                      </p>
                    )}
                    {!isEarned && <p className="text-xs text-gray-600 mt-2">🔒 Locked</p>}
                  </div>
                );
              })}
            </div>
          </div>
        )
      ))}
    </div>
  );
}
