import React, { useState, useEffect } from 'react';
import { useAuth, getTheme } from '../App';
import { toast } from 'react-hot-toast';
import ReactConfetti from 'react-confetti';
import api from '../api';

const typeIcons = { quiz: '🧪', explain: '📝', apply: '🛠️', debate: '💬' };
const typeLabels = { quiz: 'Quiz Challenge', explain: 'Explain It', apply: 'Apply It', debate: 'Debate Time' };

export default function DailyChallengePage() {
  const { user } = useAuth();
  const theme = getTheme(user?.path_id);
  const [challenge, setChallenge] = useState(null);
  const [response, setResponse] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [showConfetti, setShowConfetti] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user) {
      api.getTodayChallenge(user.id).then(data => {
        setChallenge(data);
        setResponse(data.response || '');
        setLoading(false);
      }).catch(() => setLoading(false));
    }
  }, [user]);

  const handleSubmit = async () => {
    if (!response.trim() || !challenge) return;
    setSubmitting(true);
    try {
      const res = await api.submitChallenge(user.id, challenge.id, response);
      setChallenge(prev => ({ ...prev, completed: true }));
      setShowConfetti(true);
      toast.success(`Challenge complete! +${res.xp_earned} XP! 🎉`);
      setTimeout(() => setShowConfetti(false), 4000);
    } catch (e) {
      toast.error('Failed to submit');
    }
    setSubmitting(false);
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-64">
        <div className="text-5xl animate-bounce">⚔️</div>
        <p className="text-gray-400 mt-4">Loading today's mission...</p>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto animate-fade-in">
      {showConfetti && <ReactConfetti recycle={false} numberOfPieces={200} />}

      <h1 className={`text-3xl font-black ${theme.accent} mb-2`}>⚔️ Daily Challenge</h1>
      <p className="text-gray-400 mb-6">Complete daily missions to earn bonus XP!</p>

      {challenge && (
        <div className={`${theme.card} rounded-2xl p-6`}>
          <div className="flex items-center gap-3 mb-4">
            <span className="text-4xl">{typeIcons[challenge.type] || '⚔️'}</span>
            <div>
              <span className={`text-xs px-2 py-1 rounded-full bg-gradient-to-r ${theme.gradient} text-white`}>
                {typeLabels[challenge.type] || 'Challenge'}
              </span>
              <p className="text-xs text-gray-400 mt-1">{challenge.date}</p>
            </div>
            <div className="ml-auto">
              {challenge.completed
                ? <span className="text-green-400 font-bold">✅ Completed!</span>
                : <span className="text-amber-400 font-bold">+100 XP</span>
              }
            </div>
          </div>

          <p className="text-lg text-white font-semibold mb-6 leading-relaxed">{challenge.text}</p>

          {!challenge.completed ? (
            <>
              <textarea value={response} onChange={e => setResponse(e.target.value)}
                placeholder="Write your response here... Be creative and detailed!"
                rows={6}
                className="w-full bg-gray-800 border border-gray-700 rounded-xl p-4 text-white placeholder-gray-500 focus:outline-none resize-none mb-4" />
              <button onClick={handleSubmit} disabled={submitting || !response.trim()}
                className={`w-full py-3 rounded-xl font-bold bg-gradient-to-r ${theme.gradient} text-white hover:opacity-90 disabled:opacity-50`}>
                {submitting ? '⏳ Submitting...' : '🚀 Submit Response'}
              </button>
            </>
          ) : (
            <div className="bg-green-500/10 border border-green-500/30 rounded-xl p-4">
              <p className="text-green-400 font-semibold mb-2">Your Response:</p>
              <p className="text-gray-300 text-sm">{challenge.response}</p>
              <p className="text-xs text-gray-500 mt-2">+{challenge.xp_earned} XP earned!</p>
            </div>
          )}
        </div>
      )}

      <div className={`${theme.card} rounded-xl p-4 mt-4`}>
        <h3 className="font-bold text-white mb-2">📅 Challenge Types</h3>
        <div className="grid grid-cols-2 gap-2 text-sm">
          {Object.entries(typeLabels).map(([key, label]) => (
            <div key={key} className="flex items-center gap-2 text-gray-400">
              <span>{typeIcons[key]}</span> {label}
            </div>
          ))}
        </div>
        <p className="text-xs text-gray-500 mt-2">👑 Boss Challenge every Sunday!</p>
      </div>
    </div>
  );
}
