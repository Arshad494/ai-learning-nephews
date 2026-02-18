import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth, getTheme } from '../App';
import api from '../api';

const diffColors = { beginner: 'bg-green-500/20 text-green-400', intermediate: 'bg-amber-500/20 text-amber-400', advanced: 'bg-red-500/20 text-red-400' };

export default function LearningPath() {
  const { user } = useAuth();
  const theme = getTheme(user?.path_id);
  const [topics, setTopics] = useState([]);
  const [progress, setProgress] = useState({});

  useEffect(() => {
    if (!user) return;
    api.getTopics(user.path_id).then(setTopics).catch(() => {});
    api.getProgress(user.id).then(data => {
      const map = {};
      data.forEach(p => { map[p.topic_id] = p; });
      setProgress(map);
    }).catch(() => {});
  }, [user]);

  const completed = Object.values(progress).filter(p => p.completed).length;

  return (
    <div className="max-w-4xl mx-auto animate-fade-in">
      <div className="mb-6">
        <h1 className={`text-3xl font-black ${theme.accent}`}>
          🗺️ My Learning Path
        </h1>
        <p className="text-gray-400 mt-1">{completed}/{topics.length} topics completed</p>
        <div className="w-full bg-gray-800 rounded-full h-3 mt-3 overflow-hidden">
          <div className={`h-full rounded-full bg-gradient-to-r ${theme.gradient} transition-all duration-700`}
            style={{ width: `${topics.length ? (completed / topics.length) * 100 : 0}%` }} />
        </div>
      </div>

      <div className="space-y-3">
        {topics.map((topic, i) => {
          const prog = progress[topic.id];
          const done = prog?.completed;
          const score = prog?.quiz_score;

          return (
            <Link key={topic.id} to={`/topic/${topic.id}`}
              className={`${theme.card} rounded-xl p-4 flex items-center gap-4 hover:scale-[1.01] transition-all animate-slide-up`}
              style={{ animationDelay: `${i * 50}ms` }}>
              <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm ${
                done ? `bg-gradient-to-r ${theme.gradient} text-white` : 'bg-gray-800 text-gray-400'
              }`}>
                {done ? '✓' : i + 1}
              </div>

              <div className="flex-1 min-w-0">
                <h3 className={`font-semibold truncate ${done ? 'text-white' : 'text-gray-300'}`}>
                  {topic.title}
                </h3>
                <div className="flex items-center gap-3 mt-1">
                  <span className={`text-xs px-2 py-0.5 rounded-full ${diffColors[topic.difficulty]}`}>
                    {topic.difficulty}
                  </span>
                  <span className="text-xs text-gray-500">📖 {topic.read_time} min</span>
                  {score > 0 && (
                    <span className={`text-xs ${score === 100 ? 'text-green-400' : 'text-amber-400'}`}>
                      Quiz: {score}%
                    </span>
                  )}
                </div>
              </div>

              <span className={`text-lg ${done ? theme.accent : 'text-gray-600'}`}>
                {done ? '🏆' : '→'}
              </span>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
