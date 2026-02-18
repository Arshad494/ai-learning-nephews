#!/bin/bash
echo "🧠 AI Learning Hub - Starting Up..."
echo ""

# Backend
echo "📦 Setting up backend..."
cd backend
pip install -r requirements.txt
echo "🌱 Seeding database..."
python seed_data.py
echo "🚀 Starting backend on port 8000..."
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

# Frontend
echo "📦 Setting up frontend..."
cd frontend
npm install
echo "🚀 Starting frontend on port 5173..."
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ AI Learning Hub is running!"
echo "   Frontend: http://localhost:5173"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT
wait
