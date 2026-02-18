const BASE = '/api';

async function request(url, options = {}) {
  const { method = 'GET', body, headers: extraHeaders = {} } = options;
  const headers = { ...extraHeaders };

  // Only set Content-Type for requests with a body
  if (body) {
    headers['Content-Type'] = 'application/json';
  }

  const res = await fetch(`${BASE}${url}`, { method, headers, body });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(err.detail || 'Request failed');
  }
  return res.json();
}

const api = {
  login: (name, pin) => request('/login', { method: 'POST', body: JSON.stringify({ name, pin }) }),
  getStudent: (id) => request(`/students/${id}`),
  getAllStudents: () => request('/students'),
  getTopics: (pathId) => request(`/topics/${pathId}`),
  getTopic: (id) => request(`/topic/${id}`),
  getProgress: (studentId) => request(`/progress/${studentId}`),
  completeTopic: (studentId, topicId) => request('/topics/complete', { method: 'POST', body: JSON.stringify({ student_id: studentId, topic_id: topicId }) }),
  generateQuiz: (topicId, studentId) => request(`/quiz/generate/${topicId}?student_id=${studentId}`),
  submitQuiz: (data) => request('/quiz/submit', { method: 'POST', body: JSON.stringify(data) }),
  quizHistory: (studentId) => request(`/quiz/history/${studentId}`),
  chat: (studentId, message, topic) => request('/chat', { method: 'POST', body: JSON.stringify({ student_id: studentId, message, topic }) }),
  chatHistory: (studentId) => request(`/chat/history/${studentId}`),
  getFlashcardDecks: (pathId) => request(`/flashcards/decks/${pathId}`),
  generateFlashcards: (studentId, topic) => request('/flashcards/generate', { method: 'POST', body: JSON.stringify({ student_id: studentId, topic }) }),
  getConcepts: (pathId) => request(`/concepts/${pathId}`),
  getTodayChallenge: (studentId) => request(`/challenge/today/${studentId}`),
  submitChallenge: (studentId, challengeId, response) => request('/challenge/submit', { method: 'POST', body: JSON.stringify({ student_id: studentId, challenge_id: challengeId, response }) }),
  getLeaderboard: (period = 'all') => request(`/leaderboard?period=${period}`),
  getAllBadges: () => request('/badges'),
  getStudentBadges: (studentId) => request(`/badges/${studentId}`),
  getXPLog: (studentId) => request(`/xp/log/${studentId}`),
  getAnalytics: (studentId) => request(`/analytics/${studentId}`),
  adminOverview: () => request('/admin/overview'),
  health: () => request('/health'),
};

export default api;
