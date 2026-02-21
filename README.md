# AI Learning Nephews 🚀

AI Learning Nephews is a comprehensive, personalized AI upskilling platform designed to provide tailored learning paths for different audiences—ranging from young gamers to seasoned developers. The platform uses Gemini and Groq AI to act as a personal tutor, generating quizzes, flashcards, and interactive lessons.

## 🌟 Features

- **Personalized Learning Paths**: Tailored content for Gamers (13+), Business Students (17+), Developers (20+), and AI Enthusiasts.
- **AI-Powered Tutor**: Interactive chat with a persona-driven AI tutor (powered by Groq Llama 3.3).
- **Gamified Progress**: Earn XP, level up (Explorer to Legend), maintain login streaks, and collect badges.
- **Interactive Learning**:
  - **Quizzes**: AI-generated quizzes with varying difficulty and detailed explanations.
  - **Flashcards**: Smart flashcards with mnemonics and real-world examples.
  - **Daily Challenges**: Themed daily tasks to reinforce learning.
- **Concept Library**: Deep dives into AI concepts with simple and technical explanations.
- **Leaderboard**: Compete with others and track your rank.

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11)
- **Database**: SQLAlchemy with SQLite (auto-migrates on startup)
- **AI Integration**: 
  - **Groq**: Primary chat engine (Llama-3.3-70b-versatile via zero-dependency `urllib`).
  - **Gemini**: Content and quiz generation (Gemini 1.5 Flash).
- **Deployment**: Configured for Render and Railway.

### Frontend
- **Framework**: React 18 with Vite
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Visuals**: Recharts (Analytics), React Confetti (Achievements), React Hot Toast (Notifications).

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js 20+
- API Keys: `GEMINI_API_KEY` and `GROQ_API_KEY`

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Arshad494/ai-learning-nephews.git
   cd ai-learning-nephews
   ```

2. **Setup Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   # Create a .env file with your API keys
   python main.py
   ```

3. **Setup Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## 📁 Project Structure

- `backend/`: FastAPI application, database models, and AI logic.
- `frontend/`: React source code, components, and pages.
- `build.sh`: Integrated build script for deployment.
- `render.yaml`: Blueprint for Render.com deployment.

## 📝 License
This project is for educational purposes.
