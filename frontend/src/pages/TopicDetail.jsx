import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useAuth, getTheme } from '../App';
import { toast } from 'react-hot-toast';
import api from '../api';

export default function TopicDetail() {
  const { topicId } = useParams();
  const { user } = useAuth();
  const theme = getTheme(user?.path_id);
  const [topic, setTopic] = useState(null);
  const [loading, setLoading] = useState(true);
  const [completing, setCompleting] = useState(false);

  useEffect(() => {
    api.getTopic(parseInt(topicId)).then(data => {
      setTopic(data);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, [topicId]);

  const handleComplete = async () => {
    setCompleting(true);
    try {
      const res = await api.completeTopic(user.id, parseInt(topicId));
      toast.success(`+${res.xp_earned} XP! Topic completed! 🎉`);
    } catch (e) {
      toast.error('Failed to mark complete');
    }
    setCompleting(false);
  };

  if (loading) return <div className="flex items-center justify-center h-64"><div className="text-4xl animate-bounce">📖</div></div>;
  if (!topic) return <div className="text-center text-gray-400 mt-20">Topic not found</div>;

  return (
    <div className="max-w-3xl mx-auto animate-fade-in">
      <div className={`rounded-2xl p-6 bg-gradient-to-r ${theme.gradient} mb-6`}>
        <div className="flex items-center gap-2 text-white/70 text-sm mb-2">
          <Link to="/learning-path" className="hover:text-white">Learning Path</Link>
          <span>→</span>
          <span>Topic {topic.order_num}</span>
        </div>
        <h1 className="text-2xl md:text-3xl font-black text-white">{topic.title}</h1>
        <div className="flex items-center gap-4 mt-3 text-white/80 text-sm">
          <span>📖 {topic.read_time} min read</span>
          <span className="capitalize">📊 {topic.difficulty}</span>
        </div>
      </div>

      <div className={`${theme.card} rounded-2xl p-6 mb-4`}>
        <h2 className={`text-lg font-bold ${theme.accent} mb-3`}>📝 About This Topic</h2>
        <p className="text-gray-300 leading-relaxed">{topic.description}</p>
      </div>

      <div className="grid md:grid-cols-3 gap-3 mb-6">
        <Link to={`/quiz/${topic.id}`}
          className={`${theme.card} rounded-xl p-4 text-center hover:scale-105 transition-transform`}>
          <span className="text-3xl block">🧪</span>
          <span className="text-sm font-semibold text-white mt-2 block">Take Quiz</span>
          <span className="text-xs text-gray-400">+10 XP per correct</span>
        </Link>
        <Link to="/flashcards"
          className={`${theme.card} rounded-xl p-4 text-center hover:scale-105 transition-transform`}>
          <span className="text-3xl block">🃏</span>
          <span className="text-sm font-semibold text-white mt-2 block">Flashcards</span>
          <span className="text-xs text-gray-400">+30 XP per session</span>
        </Link>
        <Link to="/tutor"
          className={`${theme.card} rounded-xl p-4 text-center hover:scale-105 transition-transform`}>
          <span className="text-3xl block">🤖</span>
          <span className="text-sm font-semibold text-white mt-2 block">Ask AI Tutor</span>
          <span className="text-xs text-gray-400">Get help anytime</span>
        </Link>
      </div>

      <button onClick={handleComplete} disabled={completing}
        className={`w-full py-4 rounded-xl font-bold text-lg bg-gradient-to-r ${theme.gradient} text-white hover:opacity-90 transition-all disabled:opacity-50`}>
        {completing ? '⏳ Marking...' : '✅ Mark Topic as Completed (+50 XP)'}
      </button>
    </div>
  );
}
