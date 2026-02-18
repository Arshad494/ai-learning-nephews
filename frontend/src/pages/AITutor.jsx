import React, { useState, useEffect, useRef } from 'react';
import { useAuth, getTheme } from '../App';
import api from '../api';

export default function AITutor() {
  const { user } = useAuth();
  const theme = getTheme(user?.path_id);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEnd = useRef(null);

  useEffect(() => {
    if (!user) return;
    api.chatHistory(user.id).then(data => {
      if (data.length === 0) {
        const welcomeMap = {
          gaming: `Yo ${user.name}! 🎮⚡ I'm your AI gaming buddy! Ask me anything about AI in games — from Minecraft mob AI to how PUBG bots work. Let's level up your knowledge! What game do you wanna learn about first?`,
          business: `Welcome ${user.name}! 💼🚀 I'm your AI business mentor. I'll help you understand how companies like Zomato, Amazon, and Flipkart use AI to dominate. Ask me anything — no coding needed! What business topic interests you most?`,
          developer: `Hey ${user.name}! 💻🔥 I'm your AI dev mentor — think of me as a senior engineer. We can dive into ML, LLMs, RAG systems, deployment — whatever you need. Ready to build? What's on your mind?`,
        };
        setMessages([{ role: 'assistant', content: welcomeMap[user.path_id] || 'Hi! Ask me anything about AI!' }]);
      } else {
        setMessages(data);
      }
    }).catch(() => {});
  }, [user]);

  useEffect(() => {
    messagesEnd.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;
    const userMsg = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
    setLoading(true);

    try {
      const res = await api.chat(user.id, userMsg);
      setMessages(prev => [...prev, { role: 'assistant', content: res.response }]);
    } catch (e) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Taking a quick breather 😴 — back in a moment! Try again in a few seconds.' }]);
    }
    setLoading(false);
  };

  const quickPrompts = {
    gaming: ['How does AI work in Minecraft? 🎮', 'Explain pathfinding like a game 🗺️', 'How do PUBG bots think? 🎯'],
    business: ['How does Zomato use AI? 🍕', 'AI tools for business students 💼', 'How to start an AI business? 🚀'],
    developer: ['Explain transformers architecture 🧠', 'How to build a RAG system? 🔧', 'Best AI portfolio projects? 💻'],
  };

  return (
    <div className="max-w-3xl mx-auto h-[calc(100vh-3rem)] flex flex-col animate-fade-in">
      <div className="mb-4">
        <h1 className={`text-2xl font-black ${theme.accent}`}>🤖 AI Tutor</h1>
        <p className="text-gray-400 text-sm">
          {user.path_id === 'gaming' ? 'Your gamer buddy who explains everything through games!' :
           user.path_id === 'business' ? 'Your business mentor with real-world examples!' :
           'Your senior dev mentor — technical and practical!'}
        </p>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto space-y-4 mb-4 pr-2">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-slide-up`}>
            <div className={`max-w-[85%] rounded-2xl px-4 py-3 ${
              msg.role === 'user'
                ? `bg-gradient-to-r ${theme.gradient} text-white`
                : 'bg-gray-800 text-gray-200'
            }`}>
              {msg.role === 'assistant' && <span className="text-xs text-gray-400 block mb-1">🤖 AI Tutor</span>}
              <div className="text-sm whitespace-pre-wrap leading-relaxed">{msg.content}</div>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-800 rounded-2xl px-4 py-3">
              <div className="flex gap-1">
                <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{animationDelay:'0ms'}}></span>
                <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{animationDelay:'150ms'}}></span>
                <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{animationDelay:'300ms'}}></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEnd} />
      </div>

      {/* Quick Prompts */}
      {messages.length <= 1 && (
        <div className="flex flex-wrap gap-2 mb-3">
          {(quickPrompts[user.path_id] || []).map((prompt, i) => (
            <button key={i} onClick={() => { setInput(prompt); }}
              className={`text-xs px-3 py-1.5 rounded-full bg-gray-800 ${theme.accent} hover:bg-gray-700 transition-all`}>
              {prompt}
            </button>
          ))}
        </div>
      )}

      {/* Input */}
      <div className="flex gap-2">
        <input value={input} onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && sendMessage()}
          placeholder={user.path_id === 'gaming' ? "Ask about AI in games... 🎮" :
                       user.path_id === 'business' ? "Ask about AI in business... 💼" :
                       "Ask about AI development... 💻"}
          className="flex-1 bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-gray-500"
        />
        <button onClick={sendMessage} disabled={loading || !input.trim()}
          className={`px-6 rounded-xl font-bold bg-gradient-to-r ${theme.gradient} text-white hover:opacity-90 transition-all disabled:opacity-50`}>
          Send
        </button>
      </div>
    </div>
  );
}
