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
  const [contentLevel, setContentLevel] = useState('normal');

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

  const getContent = () => {
    if (!topic) return '';
    if (contentLevel === 'simple') return topic.content_simple;
    if (contentLevel === 'technical') return topic.content_technical;
    return topic.content_normal;
  };

  const hasContent = topic && (topic.content_simple || topic.content_normal || topic.content_technical);

  if (loading) return (
    <div className="flex flex-col items-center justify-center h-64 gap-4">
      <div className="text-4xl animate-bounce">📖</div>
      <p className="text-gray-400 text-sm animate-pulse">Loading content...</p>
    </div>
  );
  if (!topic) return <div className="text-center text-gray-400 mt-20">Topic not found</div>;

  const levels = [
    { id: 'simple', label: 'Simple', icon: '🌱', desc: 'Plain English' },
    { id: 'normal', label: 'Standard', icon: '📖', desc: 'Full Explanation' },
    { id: 'technical', label: 'Technical', icon: '⚡', desc: 'Deep Dive' },
  ];

  return (
    <div className="max-w-3xl mx-auto animate-fade-in">
      {/* Header Banner */}
      <div className={`rounded-2xl p-6 bg-gradient-to-r ${theme.gradient} mb-6`}>
        <div className="flex items-center gap-2 text-white/70 text-sm mb-2">
          <Link to="/learning-path" className="hover:text-white transition-colors">Learning Path</Link>
          <span>→</span>
          <span>Topic {topic.order_num}</span>
        </div>
        <h1 className="text-2xl md:text-3xl font-black text-white leading-tight">{topic.title}</h1>
        <div className="flex flex-wrap items-center gap-4 mt-3 text-white/80 text-sm">
          <span>📖 {topic.read_time} min read</span>
          <span className="capitalize">📊 {topic.difficulty}</span>
          {hasContent && <span className="bg-white/20 rounded-full px-2 py-0.5 text-xs">✨ Full Content Available</span>}
        </div>
      </div>

      {/* Overview */}
      <div className={`${theme.card} rounded-2xl p-6 mb-4`}>
        <h2 className={`text-lg font-bold ${theme.accent} mb-3`}>📝 What You'll Learn</h2>
        <p className="text-gray-300 leading-relaxed">{topic.description}</p>
      </div>

      {/* Content Section */}
      {hasContent && (
        <div className={`${theme.card} rounded-2xl p-6 mb-4`}>
          {/* Level Selector */}
          <div className="flex gap-2 mb-6 flex-wrap">
            {levels.map(lvl => (
              <button
                key={lvl.id}
                onClick={() => setContentLevel(lvl.id)}
                className={`flex items-center gap-1.5 px-3 py-2 rounded-xl text-sm font-semibold transition-all ${
                  contentLevel === lvl.id
                    ? `bg-gradient-to-r ${theme.gradient} text-white shadow-lg`
                    : 'bg-gray-800/50 text-gray-400 hover:text-gray-200'
                }`}
              >
                <span>{lvl.icon}</span>
                <span>{lvl.label}</span>
                <span className="text-xs opacity-70 hidden sm:inline">· {lvl.desc}</span>
              </button>
            ))}
          </div>

          {/* Content Body */}
          <div className="prose prose-invert max-w-none">
            {getContent() ? (
              getContent().split('\n').filter(p => p.trim()).map((paragraph, i) => (
                <p key={i} className="text-gray-200 leading-relaxed mb-4 text-base">
                  {paragraph}
                </p>
              ))
            ) : (
              <p className="text-gray-400 italic">Content loading... Ask the AI Tutor below!</p>
            )}
          </div>
        </div>
      )}

      {/* Fun Fact & Real World */}
      {(topic.fun_fact || topic.real_world_example) && (
        <div className="grid md:grid-cols-2 gap-4 mb-4">
          {topic.fun_fact && (
            <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-xl p-4">
              <h3 className="text-yellow-400 font-bold mb-2">🌟 Fun Fact</h3>
              <p className="text-gray-300 text-sm leading-relaxed">{topic.fun_fact}</p>
            </div>
          )}
          {topic.real_world_example && (
            <div className="bg-blue-500/10 border border-blue-500/30 rounded-xl p-4">
              <h3 className="text-blue-400 font-bold mb-2">🌍 Real World</h3>
              <p className="text-gray-300 text-sm leading-relaxed">{topic.real_world_example}</p>
            </div>
          )}
        </div>
      )}

      {/* Quick Actions */}
      <div className="grid md:grid-cols-3 gap-3 mb-6">
        <Link to={`/quiz/${topic.id}`}
          className={`${theme.card} rounded-xl p-4 text-center hover:scale-105 transition-transform`}>
          <span className="text-3xl block">🧪</span>
          <span className="text-sm font-semibold text-white mt-2 block">Take Quiz</span>
          <span className="text-xs text-gray-400">10 questions · +XP</span>
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
