import React, { useState, useEffect } from 'react';
import { useAuth, getTheme } from '../App';
import { toast } from 'react-hot-toast';
import api from '../api';

export default function FlashcardStudio() {
  const { user } = useAuth();
  const theme = getTheme(user?.path_id);
  const [decks, setDecks] = useState([]);
  const [customTopic, setCustomTopic] = useState('');
  const [cards, setCards] = useState([]);
  const [currentCard, setCurrentCard] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [known, setKnown] = useState(new Set());
  const [studying, setStudying] = useState(false);
  const [loading, setLoading] = useState(false);
  const [deckTitle, setDeckTitle] = useState('');

  useEffect(() => {
    if (user) api.getFlashcardDecks(user.path_id).then(setDecks).catch(() => {});
  }, [user]);

  const generateCards = async (topic) => {
    setLoading(true);
    setDeckTitle(topic);
    try {
      const data = await api.generateFlashcards(user.id, topic);
      setCards(data.cards || []);
      setCurrentCard(0);
      setFlipped(false);
      setKnown(new Set());
      setStudying(true);
    } catch (e) {
      toast.error('Failed to generate flashcards');
    }
    setLoading(false);
  };

  const handleCustomGenerate = () => {
    if (customTopic.trim()) generateCards(customTopic.trim());
  };

  const markCard = (isKnown) => {
    const newKnown = new Set(known);
    if (isKnown) newKnown.add(currentCard);
    else newKnown.delete(currentCard);
    setKnown(newKnown);

    if (currentCard < cards.length - 1) {
      setCurrentCard(c => c + 1);
      setFlipped(false);
    } else {
      toast.success(`Session complete! ${newKnown.size}/${cards.length} known! +30 XP 🃏`);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-64">
        <div className="text-5xl animate-bounce mb-4">🃏</div>
        <p className={`${theme.accent} font-semibold`}>Creating your flashcards...</p>
      </div>
    );
  }

  if (studying && cards.length > 0) {
    const card = cards[currentCard];
    const isDone = currentCard === cards.length - 1 && known.size > 0;

    return (
      <div className="max-w-xl mx-auto animate-fade-in">
        <div className="flex items-center justify-between mb-4">
          <button onClick={() => setStudying(false)} className="text-gray-400 hover:text-white">← Back</button>
          <span className="text-sm text-gray-400">{currentCard + 1}/{cards.length}</span>
          <span className="text-sm text-green-400">{known.size} known</span>
        </div>

        <h2 className={`text-lg font-bold ${theme.accent} mb-4 text-center`}>{deckTitle}</h2>

        {/* Progress */}
        <div className="w-full bg-gray-800 rounded-full h-2 mb-6">
          <div className={`h-full rounded-full bg-gradient-to-r ${theme.gradient} transition-all`}
            style={{ width: `${((currentCard + 1) / cards.length) * 100}%` }} />
        </div>

        {/* Card */}
        <div className="flashcard-container h-72 mb-6 cursor-pointer" onClick={() => setFlipped(!flipped)}>
          <div className={`flashcard-inner w-full h-full relative ${flipped ? 'flipped' : ''}`}>
            <div className={`flashcard-front absolute inset-0 ${theme.card} rounded-2xl p-8 flex flex-col items-center justify-center`}>
              <span className="text-4xl mb-4">❓</span>
              <p className="text-lg font-bold text-white text-center">{card.front}</p>
              <p className="text-xs text-gray-500 mt-4">Tap to flip</p>
            </div>
            <div className={`flashcard-back absolute inset-0 rounded-2xl p-8 flex flex-col items-center justify-center bg-gradient-to-br ${theme.gradient}`}>
              <span className="text-4xl mb-4">💡</span>
              <p className="text-white text-center leading-relaxed">{card.back}</p>
            </div>
          </div>
        </div>

        {flipped && (
          <div className="flex gap-3 animate-slide-up">
            <button onClick={() => markCard(false)}
              className="flex-1 py-3 rounded-xl font-bold bg-red-500/20 text-red-400 border border-red-500/30 hover:bg-red-500/30">
              😅 Still Learning
            </button>
            <button onClick={() => markCard(true)}
              className="flex-1 py-3 rounded-xl font-bold bg-green-500/20 text-green-400 border border-green-500/30 hover:bg-green-500/30">
              ✅ Got It!
            </button>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto animate-fade-in">
      <h1 className={`text-3xl font-black ${theme.accent} mb-2`}>🃏 Flashcard Studio</h1>
      <p className="text-gray-400 mb-6">Generate flashcards on any AI topic!</p>

      {/* Custom topic */}
      <div className={`${theme.card} rounded-2xl p-6 mb-6`}>
        <h2 className="font-bold text-white mb-3">✨ Generate Custom Flashcards</h2>
        <div className="flex gap-2">
          <input value={customTopic} onChange={e => setCustomTopic(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleCustomGenerate()}
            placeholder="Enter any AI topic (e.g. Neural Networks, AI in Marketing...)"
            className="flex-1 bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:outline-none" />
          <button onClick={handleCustomGenerate} disabled={!customTopic.trim()}
            className={`px-6 rounded-xl font-bold bg-gradient-to-r ${theme.gradient} text-white hover:opacity-90 disabled:opacity-50`}>
            Generate
          </button>
        </div>
      </div>

      {/* Pre-made decks */}
      <h2 className="font-bold text-white mb-3">📚 Pre-made Decks</h2>
      <div className="grid md:grid-cols-3 gap-3">
        {decks.map(deck => (
          <button key={deck.id} onClick={() => generateCards(deck.title)}
            className={`${theme.card} rounded-xl p-5 text-left hover:scale-105 transition-transform`}>
            <span className="text-3xl block mb-2">🃏</span>
            <h3 className="font-bold text-white">{deck.title}</h3>
            <p className="text-xs text-gray-400 mt-1">{deck.description}</p>
          </button>
        ))}
      </div>
    </div>
  );
}
