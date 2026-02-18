import React, { useState, useCallback, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../App';
import api from '../api';
import { toast } from 'react-hot-toast';

const students = [
  { name: 'Aalam', avatar: '🎮', age: 13, color: 'from-green-500 to-purple-500', desc: 'AI in Gaming', border: 'border-green-500/50', glow: 'hover:shadow-green-500/20' },
  { name: 'Adham', avatar: '💼', age: 17, color: 'from-amber-500 to-blue-600', desc: 'AI for Business', border: 'border-amber-500/50', glow: 'hover:shadow-amber-500/20' },
  { name: 'Irfan', avatar: '📊', age: 17, color: 'from-amber-500 to-orange-500', desc: 'AI for Business', border: 'border-orange-500/50', glow: 'hover:shadow-orange-500/20' },
  { name: 'Adnan', avatar: '💻', age: 20, color: 'from-cyan-500 to-purple-500', desc: 'AI Developer', border: 'border-cyan-500/50', glow: 'hover:shadow-cyan-500/20' },
  { name: 'Uncle', avatar: '👨‍💼', age: 0, color: 'from-rose-500 to-indigo-500', desc: 'Admin Dashboard', border: 'border-rose-500/50', glow: 'hover:shadow-rose-500/20' },
];

export default function Login() {
  const [selected, setSelected] = useState(null);
  const [pin, setPin] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();
  const pendingLogin = useRef(false);

  const doLogin = useCallback(async (name, pinCode) => {
    if (pendingLogin.current) return;
    pendingLogin.current = true;
    setLoading(true);
    setError('');
    try {
      const user = await api.login(name, pinCode);
      login(user);
      toast.success(`Welcome back, ${user.name}! 🎉`);
      navigate(user.role === 'admin' ? '/admin' : '/dashboard');
    } catch (e) {
      setError('Wrong PIN! Try again 🔒');
      setPin('');
    } finally {
      setLoading(false);
      pendingLogin.current = false;
    }
  }, [login, navigate]);

  const handlePinInput = useCallback((digit) => {
    setPin(prev => {
      if (prev.length >= 4) return prev;
      return prev + digit;
    });
    setError('');
  }, []);

  // Auto-submit when pin reaches 4 digits
  useEffect(() => {
    if (pin.length === 4 && selected && !loading) {
      doLogin(selected.name, pin);
    }
  }, [pin, selected, loading, doLogin]);

  const handleBackspace = () => setPin(prev => prev.slice(0, -1));

  const handleKeyDown = useCallback((e) => {
    if (!selected) return;
    if (e.key >= '0' && e.key <= '9') {
      handlePinInput(e.key);
    } else if (e.key === 'Backspace') {
      handleBackspace();
    } else if (e.key === 'Escape') {
      setSelected(null);
      setPin('');
      setError('');
    }
  }, [selected, handlePinInput]);

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [handleKeyDown]);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4 bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950">
      <div className="text-center mb-8 animate-fade-in">
        <h1 className="text-4xl md:text-5xl font-black mb-2">
          <span className="bg-gradient-to-r from-green-400 via-blue-400 to-purple-400 bg-clip-text text-transparent">
            AI Learning Hub
          </span>
        </h1>
        <p className="text-gray-400 text-lg">Your personalized AI upskilling journey</p>
      </div>

      {!selected ? (
        <div className="animate-slide-up">
          <p className="text-center text-gray-300 mb-6 text-lg">Who's learning today?</p>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4 max-w-4xl mx-auto">
            {students.map((s) => (
              <button key={s.name} onClick={() => { setSelected(s); setPin(''); setError(''); }}
                className={`group flex flex-col items-center p-6 rounded-2xl bg-gray-900/80 border-2 ${s.border} ${s.glow} hover:scale-105 transition-all duration-300 hover:shadow-lg backdrop-blur`}>
                <span className="text-5xl mb-3 group-hover:scale-110 transition-transform duration-300">{s.avatar}</span>
                <span className="font-bold text-white text-lg">{s.name}</span>
                {s.age > 0 && <span className="text-xs text-gray-400 mt-1">Age {s.age}</span>}
                <span className={`text-xs mt-2 bg-gradient-to-r ${s.color} bg-clip-text text-transparent font-semibold`}>{s.desc}</span>
              </button>
            ))}
          </div>
        </div>
      ) : (
        <div className="animate-slide-up w-full max-w-sm">
          <div className="text-center mb-6">
            <span className="text-6xl block mb-3">{selected.avatar}</span>
            <h2 className="text-2xl font-bold text-white">{selected.name}</h2>
            <p className={`text-sm bg-gradient-to-r ${selected.color} bg-clip-text text-transparent font-semibold`}>{selected.desc}</p>
          </div>

          <div className="bg-gray-900/80 backdrop-blur rounded-2xl p-6 border border-gray-800">
            <p className="text-center text-gray-400 mb-4">Enter your PIN</p>

            <div className="flex justify-center gap-3 mb-6">
              {[0,1,2,3].map(i => (
                <div key={i} className={`w-14 h-14 rounded-xl border-2 flex items-center justify-center text-2xl font-bold transition-all duration-200 ${
                  pin.length > i ? `${selected.border} bg-gray-800 text-white` : 'border-gray-700 text-gray-700'
                }`}>
                  {pin.length > i ? '●' : '○'}
                </div>
              ))}
            </div>

            {error && (
              <div className="bg-red-500/10 border border-red-500/30 rounded-lg px-3 py-2 mb-4">
                <p className="text-red-400 text-center text-sm">{error}</p>
              </div>
            )}

            {loading && (
              <div className="flex items-center justify-center gap-2 mb-4 text-gray-400">
                <div className="w-4 h-4 border-2 border-gray-400 border-t-transparent rounded-full animate-spin"></div>
                <span className="text-sm">Logging in...</span>
              </div>
            )}

            <div className="grid grid-cols-3 gap-2 mb-4">
              {[1,2,3,4,5,6,7,8,9,null,0,'back'].map((d, i) => (
                d === null ? <div key={i} /> :
                <button key={i}
                  disabled={loading}
                  onClick={() => d === 'back' ? handleBackspace() : handlePinInput(String(d))}
                  className={`h-14 rounded-xl text-xl font-bold transition-all active:scale-95 disabled:opacity-50 ${
                    d === 'back'
                      ? 'bg-gray-800/50 hover:bg-gray-700 text-gray-400 text-base'
                      : 'bg-gray-800 hover:bg-gray-700 text-white'
                  }`}>
                  {d === 'back' ? '⌫' : d}
                </button>
              ))}
            </div>
          </div>

          <button onClick={() => { setSelected(null); setPin(''); setError(''); }}
            className="mt-4 text-gray-500 hover:text-white text-sm mx-auto block transition-colors">
            ← Choose different student
          </button>
        </div>
      )}
    </div>
  );
}
