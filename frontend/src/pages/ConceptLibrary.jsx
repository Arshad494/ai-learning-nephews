import React, { useState, useEffect } from 'react';
import { useAuth, getTheme } from '../App';
import api from '../api';

const diffColors = { beginner: 'bg-green-500/20 text-green-400', intermediate: 'bg-amber-500/20 text-amber-400', advanced: 'bg-red-500/20 text-red-400' };

export default function ConceptLibrary() {
  const { user } = useAuth();
  const theme = getTheme(user?.path_id);
  const [concepts, setConcepts] = useState([]);
  const [search, setSearch] = useState('');
  const [selected, setSelected] = useState(null);
  const [viewMode, setViewMode] = useState('simple');

  useEffect(() => {
    if (user) api.getConcepts(user.path_id).then(setConcepts).catch(() => {});
  }, [user]);

  const filtered = concepts.filter(c =>
    c.title.toLowerCase().includes(search.toLowerCase())
  );

  if (selected) {
    return (
      <div className="max-w-3xl mx-auto animate-fade-in">
        <button onClick={() => setSelected(null)} className="text-gray-400 hover:text-white mb-4">← Back to Library</button>

        <div className={`rounded-2xl p-6 bg-gradient-to-r ${theme.gradient} mb-6`}>
          <h1 className="text-2xl font-black text-white">{selected.title}</h1>
          <div className="flex items-center gap-3 mt-2 text-white/80 text-sm">
            <span className={`px-2 py-0.5 rounded-full ${diffColors[selected.difficulty]}`}>{selected.difficulty}</span>
            <span>📖 {selected.read_time} min</span>
          </div>
        </div>

        {/* View toggle */}
        <div className="flex gap-2 mb-4">
          {['simple', 'technical'].map(mode => (
            <button key={mode} onClick={() => setViewMode(mode)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                viewMode === mode ? `bg-gradient-to-r ${theme.gradient} text-white` : 'bg-gray-800 text-gray-400'
              }`}>
              {mode === 'simple' ? '🎯 Simple' : '🔬 Technical'}
            </button>
          ))}
        </div>

        <div className={`${theme.card} rounded-2xl p-6 mb-4`}>
          <h3 className={`font-bold ${theme.accent} mb-3`}>
            {viewMode === 'simple' ? '🎯 Simple Explanation' : '🔬 Technical Explanation'}
          </h3>
          <p className="text-gray-300 leading-relaxed">
            {viewMode === 'simple' ? selected.simple_explanation : selected.technical_explanation}
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          <div className={`${theme.card} rounded-2xl p-5`}>
            <h3 className="font-bold text-white mb-2">🌍 Real World Example</h3>
            <p className="text-gray-300 text-sm">{selected.real_world_example}</p>
          </div>
          <div className={`${theme.card} rounded-2xl p-5`}>
            <h3 className="font-bold text-white mb-2">🤯 Fun Fact</h3>
            <p className="text-gray-300 text-sm">{selected.fun_fact}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto animate-fade-in">
      <h1 className={`text-3xl font-black ${theme.accent} mb-2`}>📚 Concept Library</h1>
      <p className="text-gray-400 mb-4">{concepts.length} concepts to explore</p>

      <input value={search} onChange={e => setSearch(e.target.value)}
        placeholder="Search concepts..."
        className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:outline-none mb-6" />

      <div className="grid md:grid-cols-2 gap-3">
        {filtered.map(c => (
          <button key={c.id} onClick={() => setSelected(c)}
            className={`${theme.card} rounded-xl p-4 text-left hover:scale-[1.02] transition-all`}>
            <h3 className="font-bold text-white mb-1">{c.title}</h3>
            <p className="text-xs text-gray-400 line-clamp-2 mb-2">{c.simple_explanation}</p>
            <div className="flex items-center gap-2">
              <span className={`text-xs px-2 py-0.5 rounded-full ${diffColors[c.difficulty]}`}>{c.difficulty}</span>
              <span className="text-xs text-gray-500">📖 {c.read_time} min</span>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
