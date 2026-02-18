import React, { useState, useEffect, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import { useAuth, getTheme } from '../App';
import { toast } from 'react-hot-toast';
import ReactConfetti from 'react-confetti';
import api from '../api';

export default function QuizArena() {
  const { topicId } = useParams();
  const { user } = useAuth();
  const theme = getTheme(user?.path_id);
  const [topics, setTopics] = useState([]);
  const [phase, setPhase] = useState(topicId ? 'loading' : 'select'); // select | loading | quiz | result
  const [selectedTopic, setSelectedTopic] = useState(topicId ? parseInt(topicId) : null);
  const [questions, setQuestions] = useState([]);
  const [currentQ, setCurrentQ] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [selected, setSelected] = useState(null);
  const [quizResult, setQuizResult] = useState(null);
  const [streak, setStreak] = useState(0);
  const [showConfetti, setShowConfetti] = useState(false);

  useEffect(() => {
    if (user) api.getTopics(user.path_id).then(setTopics).catch(() => {});
  }, [user?.id]);

  const startQuiz = useCallback(async (tid) => {
    setPhase('loading');
    setSelectedTopic(tid);
    setQuestions([]);
    setCurrentQ(0);
    setAnswers([]);
    setSelected(null);
    setQuizResult(null);
    setStreak(0);
    try {
      const data = await api.generateQuiz(tid, user.id);
      const qs = data.questions || [];
      if (qs.length === 0) {
        toast.error('No questions generated. Try again!');
        setPhase('select');
        return;
      }
      setQuestions(qs);
      setPhase('quiz');
    } catch (e) {
      toast.error('Failed to generate quiz. Try again!');
      setPhase('select');
    }
  }, [user?.id]);

  // Auto-start if topicId from URL
  useEffect(() => {
    if (topicId && user) startQuiz(parseInt(topicId));
  }, [topicId, user?.id]);

  const handleAnswer = (option) => {
    if (selected !== null) return;
    setSelected(option);
    const q = questions[currentQ];
    const isCorrect = option === q.correct;
    if (isCorrect) setStreak(s => s + 1);
    else setStreak(0);

    setAnswers(prev => [...prev, {
      question: q.question, selected: option, correct: q.correct,
      is_correct: isCorrect, explanation: q.explanation,
    }]);
  };

  const nextQuestion = () => {
    if (currentQ < questions.length - 1) {
      setCurrentQ(c => c + 1);
      setSelected(null);
    } else {
      submitQuiz();
    }
  };

  const submitQuiz = async () => {
    try {
      const finalAnswers = [...answers];
      const res = await api.submitQuiz({
        student_id: user.id, topic_id: selectedTopic, answers: finalAnswers
      });
      setQuizResult(res);
      setPhase('result');
      if (res.perfect) {
        setShowConfetti(true);
        toast.success('PERFECT SCORE! +50 bonus XP!');
        setTimeout(() => setShowConfetti(false), 5000);
      } else {
        toast.success(`Quiz complete! +${res.xp_earned} XP`);
      }
    } catch (e) {
      toast.error('Failed to submit quiz');
    }
  };

  // ── SELECT PHASE ──
  if (phase === 'select') {
    return (
      <div className="max-w-4xl mx-auto animate-fade-in">
        <h1 className={`text-3xl font-black ${theme.accent} mb-2`}>🧪 Quiz Arena</h1>
        <p className="text-gray-400 mb-6">Choose a topic to test your knowledge!</p>
        <div className="grid md:grid-cols-2 gap-3">
          {topics.map(t => (
            <button key={t.id} onClick={() => startQuiz(t.id)}
              className={`${theme.card} rounded-xl p-4 text-left hover:scale-[1.02] transition-all`}>
              <div className="flex items-center gap-3">
                <span className={`w-8 h-8 rounded-full bg-gradient-to-r ${theme.gradient} flex items-center justify-center text-white text-sm font-bold shrink-0`}>
                  {t.order_num}
                </span>
                <div className="min-w-0">
                  <h3 className="font-semibold text-white text-sm truncate">{t.title}</h3>
                  <span className="text-xs text-gray-400 capitalize">{t.difficulty}</span>
                </div>
              </div>
            </button>
          ))}
        </div>
      </div>
    );
  }

  // ── LOADING PHASE ──
  if (phase === 'loading') {
    return (
      <div className="flex flex-col items-center justify-center h-64 animate-fade-in">
        <div className="text-5xl animate-bounce mb-4">🧪</div>
        <p className={`${theme.accent} font-semibold`}>Generating your quiz...</p>
        <p className="text-gray-400 text-sm mt-1">AI is crafting questions just for you</p>
      </div>
    );
  }

  // ── RESULT PHASE ──
  if (phase === 'result' && quizResult) {
    return (
      <div className="max-w-2xl mx-auto animate-fade-in">
        {showConfetti && <ReactConfetti recycle={false} numberOfPieces={300} />}
        <div className={`rounded-2xl p-8 text-center bg-gradient-to-r ${theme.gradient} mb-6`}>
          <span className="text-6xl block mb-4">{quizResult.perfect ? '🏆' : quizResult.score >= 60 ? '🌟' : '💪'}</span>
          <h2 className="text-3xl font-black text-white">{quizResult.perfect ? 'PERFECT!' : quizResult.score >= 60 ? 'Great Job!' : 'Keep Trying!'}</h2>
          <p className="text-white/80 text-lg mt-2">{quizResult.correct}/{quizResult.total} correct · {Math.round(quizResult.score)}%</p>
          <p className="text-white font-bold mt-1">+{quizResult.xp_earned} XP earned!</p>
        </div>

        <div className="space-y-3 mb-6">
          {answers.map((a, i) => (
            <div key={i} className={`${theme.card} rounded-xl p-4`}>
              <p className="font-semibold text-white text-sm mb-2">Q{i+1}: {a.question}</p>
              <div className="flex items-center gap-2 mb-1">
                <span>{a.is_correct ? '✅' : '❌'}</span>
                <span className="text-sm text-gray-300">Your answer: {a.selected}</span>
              </div>
              {!a.is_correct && <p className="text-sm text-green-400">Correct: {a.correct}</p>}
              {a.explanation && <p className="text-xs text-gray-400 mt-1">💡 {a.explanation}</p>}
            </div>
          ))}
        </div>

        <div className="flex gap-3">
          <button onClick={() => startQuiz(selectedTopic)}
            className={`flex-1 py-3 rounded-xl font-bold bg-gradient-to-r ${theme.gradient} text-white hover:opacity-90`}>
            🔄 Retry
          </button>
          <button onClick={() => setPhase('select')}
            className="flex-1 py-3 rounded-xl font-bold bg-gray-800 text-white hover:bg-gray-700">
            📋 Different Topic
          </button>
        </div>
      </div>
    );
  }

  // ── QUIZ PHASE ──
  const q = questions[currentQ];
  if (!q) return null;

  return (
    <div className="max-w-2xl mx-auto animate-fade-in">
      <div className="flex items-center justify-between mb-4">
        <span className="text-sm text-gray-400">Question {currentQ + 1}/{questions.length}</span>
        {streak > 1 && <span className="text-sm text-orange-400 font-medium">🔥 {streak} streak!</span>}
      </div>
      <div className="w-full bg-gray-800 rounded-full h-2 mb-6">
        <div className={`h-full rounded-full bg-gradient-to-r ${theme.gradient} transition-all duration-500`}
          style={{ width: `${((currentQ + 1) / questions.length) * 100}%` }} />
      </div>

      <div className={`${theme.card} rounded-2xl p-6 mb-6`}>
        <p className="text-lg font-bold text-white mb-6">{q.question}</p>
        <div className="space-y-3">
          {(q.options || []).map((opt, i) => {
            let style = 'bg-gray-800 border-gray-700 hover:bg-gray-700 text-gray-200';
            if (selected !== null) {
              if (opt === q.correct) style = 'bg-green-500/20 border-green-500 text-green-400';
              else if (opt === selected && opt !== q.correct) style = 'bg-red-500/20 border-red-500 text-red-400';
              else style = 'bg-gray-800/50 border-gray-700 text-gray-500';
            }
            return (
              <button key={i} onClick={() => handleAnswer(opt)} disabled={selected !== null}
                className={`w-full text-left p-4 rounded-xl border transition-all ${style} disabled:cursor-default`}>
                <span className="font-medium">{opt}</span>
              </button>
            );
          })}
        </div>

        {selected !== null && (
          <div className="mt-4 animate-slide-up">
            <div className={`p-3 rounded-lg ${selected === q.correct ? 'bg-green-500/10 border border-green-500/30' : 'bg-red-500/10 border border-red-500/30'}`}>
              <p className={`text-sm font-semibold ${selected === q.correct ? 'text-green-400' : 'text-red-400'}`}>
                {selected === q.correct ? '✅ Correct! +10 XP' : `❌ Wrong! Correct: ${q.correct}`}
              </p>
              {q.explanation && <p className="text-xs text-gray-400 mt-1">💡 {q.explanation}</p>}
            </div>
          </div>
        )}
      </div>

      {selected !== null && (
        <button onClick={nextQuestion}
          className={`w-full py-3 rounded-xl font-bold bg-gradient-to-r ${theme.gradient} text-white hover:opacity-90 transition-all`}>
          {currentQ < questions.length - 1 ? 'Next Question →' : '🏁 Finish Quiz'}
        </button>
      )}
    </div>
  );
}
