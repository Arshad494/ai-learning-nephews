from fastapi import FastAPI, Depends, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from pathlib import Path
import json
import os
import random

from database import get_db, engine, Base
from models import *

# Load env vars
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

import urllib.request
import urllib.error

# ── Groq — uses stdlib urllib, NO groq package needed ──
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_AVAILABLE = bool(GROQ_API_KEY)

def groq_chat(messages: list, max_tokens: int = 1024, temperature: float = 0.7) -> str:
    """Call Groq chat completions using stdlib only — zero external deps."""
    payload = json.dumps({
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]

# ── Groq SDK — optional, used if available for convenience ──
groq_client = None
try:
    from groq import Groq as GroqClient
    if GROQ_API_KEY:
        groq_client = GroqClient(api_key=GROQ_API_KEY)
except Exception:
    pass  # Falls back to groq_chat() using urllib

# ── Gemini — for quiz/content generation as secondary ──
try:
    import google.generativeai as genai
    api_key = os.getenv("GEMINI_API_KEY", "")
    if api_key:
        genai.configure(api_key=api_key)
        gemini_model = genai.GenerativeModel("gemini-1.5-flash")
        GEMINI_AVAILABLE = True
    else:
        GEMINI_AVAILABLE = False
except Exception:
    GEMINI_AVAILABLE = False

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Learning Nephews", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ────────────────────────── Pydantic Schemas ──────────────────────────

class LoginRequest(BaseModel):
    name: str
    pin: str

class ChatRequest(BaseModel):
    student_id: int
    message: str
    topic: Optional[str] = None

class QuizSubmit(BaseModel):
    student_id: int
    topic_id: int
    answers: List[dict]  # [{question, selected, correct, is_correct}]

class FlashcardGenRequest(BaseModel):
    student_id: int
    topic: str

class ChallengeSubmitRequest(BaseModel):
    student_id: int
    challenge_id: int
    response: str

class MarkTopicRequest(BaseModel):
    student_id: int
    topic_id: int

class FlashcardProgressRequest(BaseModel):
    student_id: int
    deck_id: int
    card_index: int
    known: bool

# ────────────────────────── Helpers ──────────────────────────

XP_LEVELS = [
    (0, "Explorer"), (500, "Builder"), (1500, "Engineer"),
    (3000, "Scientist"), (5000, "Legend")
]

def get_level(xp: int) -> str:
    level = "Explorer"
    for threshold, name in XP_LEVELS:
        if xp >= threshold:
            level = name
    return level

def add_xp(db: Session, student_id: int, amount: int, reason: str) -> int:
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        return 0
    student.total_xp += amount
    student.level = get_level(student.total_xp)
    db.add(XPLog(student_id=student_id, amount=amount, reason=reason))
    db.commit()
    check_badges(db, student)
    return student.total_xp

def update_streak(db: Session, student: Student):
    today = date.today().isoformat()
    if student.last_login_date == today:
        return
    from datetime import timedelta
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    if student.last_login_date == yesterday:
        student.current_streak += 1
    else:
        if student.current_streak > 0 and student.streak_freezes > 0:
            student.streak_freezes -= 1
            student.current_streak += 1
        else:
            student.current_streak = 1
    if student.current_streak > student.longest_streak:
        student.longest_streak = student.current_streak
    student.last_login_date = today
    db.commit()
    # Streak bonus XP
    if student.current_streak == 7:
        add_xp(db, student.id, 200, "7-day streak bonus!")
    elif student.current_streak == 14:
        add_xp(db, student.id, 400, "14-day streak bonus!")
    elif student.current_streak == 30:
        add_xp(db, student.id, 1000, "30-day streak bonus!")
    # Earn streak freeze at milestones
    if student.current_streak % 7 == 0:
        student.streak_freezes += 1
        db.commit()

def check_badges(db: Session, student: Student):
    existing = {sb.badge_id for sb in db.query(StudentBadge).filter(StudentBadge.student_id == student.id).all()}
    badges = {b.name: b for b in db.query(Badge).all()}

    def award(name):
        badge = badges.get(name)
        if badge and badge.id not in existing:
            db.add(StudentBadge(student_id=student.id, badge_id=badge.id))
            existing.add(badge.id)

    # Level badges
    if student.level == "Engineer":
        award("Rising Star")
    if student.level == "Legend":
        award("Legend")

    # XP badges
    if student.total_xp >= 100:
        award("Rocket Start")

    # Streak badges
    if student.current_streak >= 7:
        award("Week Warrior")

    # Quiz badges
    perfect_count = db.query(QuizResult).filter(
        QuizResult.student_id == student.id,
        QuizResult.score == 100
    ).count()
    if perfect_count >= 1:
        award("Perfectionist")
    if perfect_count >= 5:
        award("Diamond Mind")

    # Topic badges
    completed_topics = db.query(TopicProgress).filter(
        TopicProgress.student_id == student.id,
        TopicProgress.completed == True
    ).count()
    if completed_topics >= 5:
        award("All Rounder")

    total_topics = db.query(Topic).filter(Topic.path_id == student.path_id).count()
    if completed_topics >= total_topics and total_topics > 0:
        award("Curious Mind")
        award("Graduate")
        if student.path_id == "gaming":
            award("Game Master")
        elif student.path_id == "business":
            award("Business Brain")
        elif student.path_id == "developer":
            award("Code Wizard")
        elif student.path_id == "ai_enthusiast":
            award("AI Pioneer")

    # Chat badges
    chat_count = db.query(ChatMessage).filter(
        ChatMessage.student_id == student.id,
        ChatMessage.role == "user"
    ).count()
    if chat_count >= 50:
        award("AI Whisperer")
    if chat_count >= 100:
        award("Deep Thinker")

    # Challenge badges
    challenge_count = db.query(DailyChallenge).filter(
        DailyChallenge.student_id == student.id,
        DailyChallenge.completed == True
    ).count()
    if challenge_count >= 30:
        award("Challenge Champion")

    # Concept badges
    concepts_read = db.query(TopicProgress).filter(
        TopicProgress.student_id == student.id
    ).count()
    if concepts_read >= 10:
        award("Knowledge Seeker")

    # Time-based badges
    now = datetime.now()
    if now.hour >= 22 or now.hour < 4:
        award("Night Owl")
    if 5 <= now.hour < 8:
        award("Early Bird")

    # Leaderboard badges
    students_ranked = db.query(Student).filter(Student.role == "student").order_by(desc(Student.total_xp)).all()
    if students_ranked and students_ranked[0].id == student.id:
        award("Leaderboard King")

    db.commit()

def get_tutor_system_prompt(student: Student) -> str:
    if student.path_id == "gaming":
        return """You are an AI tutor for Aalam, a 13-year-old who LOVES gaming.
Your personality: You're like a cool gamer friend. Use gaming slang naturally (GG, clutch, OP, nerf, buff, noob-friendly, level up).
EVERY explanation must use gaming examples (Minecraft, PUBG, FIFA, GTA, Roblox, Free Fire, Fortnite).
Be encouraging like a supportive teammate. Use emojis generously 🎮🔥⚡💪🏆.
Never be boring or textbook-like. Keep it fun, energetic, and relatable.
If explaining AI concepts, always connect to games Aalam would know.
Example: "Pathfinding AI? That's basically how enemies in PUBG track you down! 🎯"
Keep responses concise but exciting. Max 3-4 paragraphs."""

    elif student.path_id == "business":
        return f"""You are an AI tutor for {student.name}, a 17-year-old interested in business and AI.
Your personality: Professional but engaging. Like a cool business mentor.
Use real business examples: Zomato, Amazon, Flipkart, Zerodha, Swiggy, PhonePe, Uber.
Focus on practical applications — no coding jargon ever.
Career and entrepreneurship focused. Make them feel like future CEOs.
Explain how AI tools like ChatGPT, Canva AI, Notion AI can be used in business.
Keep it professional yet exciting. Use relevant emojis 💼📊🚀💡.
Max 3-4 paragraphs per response."""

    elif student.path_id == "developer":
        return """You are an AI tutor for Adnan, a 20-year-old CS 3rd year student.
Your personality: Like a senior developer or tech lead. Peer-to-peer.
Give deep technical explanations with code examples when relevant.
Reference real projects, GitHub repos, and industry practices.
Interview prep focused — mention what interviewers look for.
Challenge him to think deeper. Suggest projects and resources.
Use developer humor and references. Emojis: 💻🔥🚀⚡.
Be direct, technical, and practical. Max 4-5 paragraphs."""

    elif student.path_id == "ai_enthusiast":
        return f"""You are an AI tutor for an AI Enthusiast who wants deep, comprehensive understanding of artificial intelligence.
Your personality: Like a brilliant, passionate AI researcher who makes complex ideas crystal clear.
Explain concepts thoroughly with real-world examples, case studies, and historical context.
Cover the technical fundamentals accessibly, the societal implications thoughtfully, and the future possibilities excitingly.
Reference real AI systems: ChatGPT, Claude, Gemini, Midjourney, Stable Diffusion, AlphaFold, etc.
Be intellectually stimulating — challenge them to think critically about AI's impact.
Use a mix of analogies, concrete examples, and thought experiments.
Connect AI concepts to philosophy, neuroscience, economics, and society.
Emojis: 🤖🧠💡🌍⚡🔮.
Be thorough and substantive. Max 5-6 paragraphs with genuine depth."""

    return "You are a helpful AI learning tutor. Be encouraging and clear."

# ────────────────────────── Pre-written Daily Challenges ──────────────────────────

DAILY_CHALLENGES = {
    "gaming": [
        {"type": "quiz", "text": "🎮 Quick Fire: What AI technique do Pac-Man ghosts use to chase you? Think about how each ghost has a different strategy!"},
        {"type": "explain", "text": "🎮 Explain Like a Pro: How does Minecraft generate its infinite worlds? Describe the AI behind it in your own words!"},
        {"type": "apply", "text": "🎮 Game Designer Mode: Design an AI system for a zombie game — what behaviors should zombies have? Draw it out!"},
        {"type": "debate", "text": "🎮 Hot Take: Are AI bots in PUBG/Free Fire good for the game or do they make it too easy? Argue your side!"},
        {"type": "quiz", "text": "🎮 Boss Battle: Name 3 games that use procedural generation to create their worlds. Bonus if you explain how!"},
        {"type": "explain", "text": "🎮 Level Up: How does FIFA decide what your AI teammate does during a match? Break it down!"},
        {"type": "apply", "text": "🎮 Mission: Use an AI art tool to create a game character. Describe your prompt and the result!"},
        {"type": "quiz", "text": "🎮 Speed Run: What's the difference between A* pathfinding and a behavior tree? Quick explanation!"},
        {"type": "debate", "text": "🎮 Gamer's Court: Should game companies use AI to replace voice actors? What are the pros and cons?"},
        {"type": "explain", "text": "🎮 Wiki Master: Explain reinforcement learning using only Minecraft examples!"},
        {"type": "apply", "text": "🎮 Creator Quest: Write a game story using ChatGPT. Share the prompt you used and rate the result!"},
        {"type": "quiz", "text": "🎮 Trivia Time: Which AI beat the world champion in Go? And what made it special?"},
        {"type": "explain", "text": "🎮 Deep Dive: How does GTA V make its traffic feel realistic? What AI systems are involved?"},
        {"type": "debate", "text": "🎮 Controversy: Is AI-generated game art as valuable as human-made art? Defend your position!"},
        {"type": "apply", "text": "🎮 Build Challenge: Create a simple flowchart for an enemy AI in any game. What states does it have?"},
        {"type": "quiz", "text": "🎮 Pop Quiz: What is an 'AI Director' in games? Name a famous game that uses one!"},
        {"type": "explain", "text": "🎮 Coach Mode: Explain how esports teams use AI for coaching in 5 bullet points!"},
        {"type": "apply", "text": "🎮 Future Gamer: Describe your dream AI-powered game. What would the AI do differently?"},
        {"type": "debate", "text": "🎮 Ethical Gamer: Should aimbots that use AI be treated differently than regular cheats? Why?"},
        {"type": "quiz", "text": "🎮 Final Boss: Name 5 AI techniques used in modern games and give an example of each!"},
        {"type": "explain", "text": "🎮 Nerd Out: How do chess engines think millions of moves ahead? Explain minimax simply!"},
        {"type": "apply", "text": "🎮 Side Quest: Find an AI tool online and use it to generate game music. Rate the result!"},
        {"type": "quiz", "text": "🎮 Rapid Fire: True or False — AI in games can learn from watching you play?"},
        {"type": "debate", "text": "🎮 Gaming Summit: Will AI eventually make human game designers unnecessary? Share your thoughts!"},
        {"type": "explain", "text": "🎮 Tutorial: Explain what 'difficulty scaling' means in games. Give 3 examples!"},
        {"type": "apply", "text": "🎮 Roblox Lab: Design an AI-powered Roblox game concept. What makes the AI special?"},
        {"type": "quiz", "text": "🎮 Memory Check: What's the difference between procedural animation and pre-made animation?"},
        {"type": "explain", "text": "🎮 Storyteller: Explain swarm intelligence using a game enemy horde as your example!"},
        {"type": "debate", "text": "🎮 Big Question: Should AI-generated NPCs have feelings in games? Would that change how you play?"},
        {"type": "apply", "text": "🎮 BOSS CHALLENGE 👑: Create a complete game concept that uses at least 3 AI techniques you've learned!"},
    ],
    "business": [
        {"type": "quiz", "text": "💼 Business Brief: Name 3 ways Amazon uses AI to dominate e-commerce. Be specific!"},
        {"type": "explain", "text": "💼 Elevator Pitch: Explain how AI chatbots save businesses money in under 60 seconds!"},
        {"type": "apply", "text": "💼 CEO Challenge: Use ChatGPT to write a professional email to a client. Share your prompt!"},
        {"type": "debate", "text": "💼 Boardroom Debate: Will AI replace most customer service jobs? Argue for or against!"},
        {"type": "quiz", "text": "💼 Market Intelligence: What is 'dynamic pricing' and name 2 companies that use it?"},
        {"type": "explain", "text": "💼 Consultant Mode: How does Zomato use AI? List at least 4 AI applications!"},
        {"type": "apply", "text": "💼 Startup Founder: Use an AI tool to create a social media post for a fake business. Share it!"},
        {"type": "quiz", "text": "💼 Finance Flash: How does AI detect fraud in banking? Explain the basics!"},
        {"type": "debate", "text": "💼 Ethics Corner: Should companies tell customers when they're talking to an AI chatbot?"},
        {"type": "explain", "text": "💼 Strategy Session: Explain how recommendation engines work using Netflix as an example!"},
        {"type": "apply", "text": "💼 Marketing Pro: Use Canva AI to create a business banner. Describe the process!"},
        {"type": "quiz", "text": "💼 Rapid Recall: What is sentiment analysis and how do brands use it on social media?"},
        {"type": "explain", "text": "💼 Investor Pitch: Explain AI's impact on the stock market in simple terms!"},
        {"type": "debate", "text": "💼 Think Tank: Is it ethical for companies to use AI to set different prices for different people?"},
        {"type": "apply", "text": "💼 Business Plan: Use AI to outline a business plan for a food delivery startup!"},
        {"type": "quiz", "text": "💼 HR Knowledge: How does AI help in recruitment? Name 3 specific ways!"},
        {"type": "explain", "text": "💼 Supply Chain Expert: Explain how AI optimizes delivery for Flipkart step by step!"},
        {"type": "apply", "text": "💼 Analyst Mode: Use ChatGPT to analyze a business scenario and give recommendations!"},
        {"type": "debate", "text": "💼 Future Forum: Which industry will AI transform the most in 5 years? Make your case!"},
        {"type": "quiz", "text": "💼 AI Tools Test: Name 5 AI tools that every business student should know!"},
        {"type": "explain", "text": "💼 Professor Mode: Explain RPA (Robotic Process Automation) with a real business example!"},
        {"type": "apply", "text": "💼 Notion AI Lab: Use an AI productivity tool to organize a project plan. Share the result!"},
        {"type": "quiz", "text": "💼 Quick Hit: What is customer segmentation and why does it matter for marketing?"},
        {"type": "debate", "text": "💼 Shark Tank: Would you invest in a company that replaces all employees with AI? Why or why not?"},
        {"type": "explain", "text": "💼 Case Study: Pick any Indian startup and explain how they could use more AI!"},
        {"type": "apply", "text": "💼 Data Detective: Find an AI-generated business insight online and evaluate if it's accurate!"},
        {"type": "quiz", "text": "💼 Definition Challenge: Define these in your own words: ML, NLP, Computer Vision, Chatbot!"},
        {"type": "explain", "text": "💼 Trend Spotter: What are the top 3 AI trends that will affect business this year?"},
        {"type": "debate", "text": "💼 Privacy Debate: Should companies collect personal data to improve AI? Where's the line?"},
        {"type": "apply", "text": "💼 BOSS CHALLENGE 👑: Create a complete AI-powered business idea with target market, AI features, and revenue model!"},
    ],
    "developer": [
        {"type": "quiz", "text": "💻 Code Check: What's the difference between supervised and unsupervised learning? Give examples!"},
        {"type": "explain", "text": "💻 Whiteboard: Explain the transformer architecture in your own words with a diagram description!"},
        {"type": "apply", "text": "💻 Build It: Write a Python function that implements a simple K-nearest neighbors from scratch!"},
        {"type": "debate", "text": "💻 Tech Debate: Is fine-tuning or RAG better for most production LLM applications? Argue your side!"},
        {"type": "quiz", "text": "💻 Algorithm Arena: What are the steps of backpropagation? List them in order!"},
        {"type": "explain", "text": "💻 Mentor Mode: Explain embeddings to a non-technical person using a creative analogy!"},
        {"type": "apply", "text": "💻 API Challenge: Write pseudocode for a FastAPI endpoint that uses Gemini to summarize text!"},
        {"type": "quiz", "text": "💻 Architecture Quiz: Name 3 differences between CNNs and RNNs!"},
        {"type": "debate", "text": "💻 Hot Take: Will prompt engineering remain a valuable skill or become obsolete? Defend your view!"},
        {"type": "explain", "text": "💻 Deep Dive: How does attention mechanism work? Explain Q, K, V matrices!"},
        {"type": "apply", "text": "💻 Project Sprint: Design the architecture for a RAG-based chatbot. List all components!"},
        {"type": "quiz", "text": "💻 Rapid Fire: What are LoRA and QLoRA? When would you use each?"},
        {"type": "explain", "text": "💻 System Design: Design an ML pipeline for a recommendation system. Cover data to deployment!"},
        {"type": "debate", "text": "💻 Open Source vs Closed: Should AI models be open source? Pros and cons!"},
        {"type": "apply", "text": "💻 DevOps Mode: Write a Dockerfile for deploying a FastAPI ML application!"},
        {"type": "quiz", "text": "💻 Framework Face-off: Compare LangChain vs LlamaIndex — strengths and use cases!"},
        {"type": "explain", "text": "💻 Interview Prep: Explain gradient descent as if it's a technical interview question!"},
        {"type": "apply", "text": "💻 Hugging Face Lab: Find a model on Hugging Face and write code to use it for text classification!"},
        {"type": "debate", "text": "💻 Career Path: Is specializing in AI better than being a full-stack dev? Make your argument!"},
        {"type": "quiz", "text": "💻 Vector DB Challenge: Compare Pinecone, Weaviate, and ChromaDB on 3 criteria!"},
        {"type": "explain", "text": "💻 Teaching Mode: Explain tokenization using BPE algorithm step by step!"},
        {"type": "apply", "text": "💻 Portfolio Builder: Design a README for an AI portfolio project that would impress recruiters!"},
        {"type": "quiz", "text": "💻 MLOps Quiz: What tools would you use for experiment tracking, model versioning, and monitoring?"},
        {"type": "debate", "text": "💻 Scaling Debate: When should you train your own model vs use an API? Define the criteria!"},
        {"type": "explain", "text": "💻 Paper Review: Summarize the 'Attention Is All You Need' paper's key contributions!"},
        {"type": "apply", "text": "💻 Code Review: Write a production-ready Python function with error handling for calling Gemini API!"},
        {"type": "quiz", "text": "💻 Speed Round: Define GAN, VAE, Diffusion Model — one sentence each!"},
        {"type": "explain", "text": "💻 Startup CTO: Design the tech stack for an AI SaaS startup. Justify each choice!"},
        {"type": "debate", "text": "💻 AI Safety: Should there be regulations on AI model training? What boundaries make sense?"},
        {"type": "apply", "text": "💻 BOSS CHALLENGE 👑: Design a complete AI system architecture — from data pipeline to deployed API with monitoring!"},
    ],
    "ai_enthusiast": [
        {"type": "quiz", "text": "🤖 AI Basics: Explain the difference between Artificial Intelligence, Machine Learning, and Deep Learning. Use a simple analogy!"},
        {"type": "explain", "text": "🤖 LLM Explorer: How does ChatGPT actually generate its responses? Explain the token prediction process in your own words!"},
        {"type": "apply", "text": "🤖 Prompt Lab: Write 3 different prompts for the same task — beginner, intermediate, and expert level. Compare the outputs!"},
        {"type": "debate", "text": "🤖 AI Ethics: Should AI systems like ChatGPT be allowed to generate content without any restrictions? Where's the line?"},
        {"type": "quiz", "text": "🤖 Tool Time: Name 5 AI tools you can use RIGHT NOW for free. What is each one best at?"},
        {"type": "explain", "text": "🤖 Deep Dive: What is a 'hallucination' in AI? Why does it happen and how can you minimize it?"},
        {"type": "apply", "text": "🤖 AI in Action: Use any AI image generator to create an image. Share your prompt and rate the result!"},
        {"type": "quiz", "text": "🤖 Concept Check: What is the difference between supervised and unsupervised learning? Give a real-world example of each!"},
        {"type": "debate", "text": "🤖 Future Watch: Will AI cause mass unemployment or create more jobs than it destroys? Make your case with evidence!"},
        {"type": "explain", "text": "🤖 Technical Tour: Explain what 'training data' is and why its quality matters so much to AI performance!"},
        {"type": "apply", "text": "🤖 Prompt Engineer: Use chain-of-thought prompting to solve a complex problem with ChatGPT. Share the result!"},
        {"type": "quiz", "text": "🤖 Model Showdown: Compare GPT-4, Claude, and Gemini on 3 different tasks. Which wins each?"},
        {"type": "explain", "text": "🤖 Safety First: What is AI alignment and why do researchers consider it the most important problem in AI?"},
        {"type": "apply", "text": "🤖 No-Code Builder: Use a no-code AI tool to build something useful. Document what you built and how!"},
        {"type": "debate", "text": "🤖 Regulation Debate: Should governments regulate AI development? What regulations would you propose?"},
        {"type": "quiz", "text": "🤖 History Quiz: Who invented the first neural network? Name 3 major milestones in AI history!"},
        {"type": "explain", "text": "🤖 Concept Clarity: What is an 'AI Agent' and how is it different from a regular chatbot? Give an example!"},
        {"type": "apply", "text": "🤖 Research Day: Find one recent AI breakthrough from the last 3 months. Explain it in simple terms!"},
        {"type": "debate", "text": "🤖 Creativity Question: Can AI be truly creative, or is it just sophisticated pattern matching? Defend your view!"},
        {"type": "quiz", "text": "🤖 Application Scan: Name one AI application in each field: healthcare, education, finance, art, and transportation!"},
        {"type": "explain", "text": "🤖 Under the Hood: What is a 'token' in the context of LLMs? Why does token limit matter in practice?"},
        {"type": "apply", "text": "🤖 AI Journalist: Write a short article about how AI will change ONE specific industry in the next 5 years!"},
        {"type": "quiz", "text": "🤖 Ethics Exam: Identify 3 ways AI bias can occur and how each can be mitigated!"},
        {"type": "debate", "text": "🤖 Big Question: Should AI have rights as it becomes more sophisticated? What would that even mean?"},
        {"type": "explain", "text": "🤖 Model Types: Explain the difference between foundation models, fine-tuned models, and RAG systems. When use each?"},
        {"type": "apply", "text": "🤖 Case Study: Pick any company (Amazon, Google, etc.) and map out ALL the ways they use AI across their products!"},
        {"type": "quiz", "text": "🤖 Safety Check: What is RLHF? How does it make AI assistants safer and more helpful?"},
        {"type": "explain", "text": "🤖 Future Gaze: What is AGI? How far are we from it? What would change when we get there?"},
        {"type": "debate", "text": "🤖 Existential: Is the risk of advanced AI overstated or understated by the media? What's the real picture?"},
        {"type": "apply", "text": "🤖 BOSS CHALLENGE 👑: Create a comprehensive 'AI in 2025' report covering tools, trends, risks, and opportunities!"},
    ],
}

# ────────────────────────── Auth Routes ──────────────────────────

@app.post("/api/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.name == req.name, Student.pin == req.pin).first()
    if not student:
        raise HTTPException(status_code=401, detail="Invalid name or PIN")

    # Award first login badge
    existing_badges = db.query(StudentBadge).filter(StudentBadge.student_id == student.id).count()
    if existing_badges == 0:
        first_badge = db.query(Badge).filter(Badge.name == "First Steps").first()
        if first_badge:
            db.add(StudentBadge(student_id=student.id, badge_id=first_badge.id))
            db.commit()

    update_streak(db, student)
    add_xp(db, student.id, 20, "Daily login bonus")

    return {
        "id": student.id,
        "name": student.name,
        "age": student.age,
        "role": student.role,
        "path_id": student.path_id,
        "avatar": student.avatar,
        "total_xp": student.total_xp,
        "level": student.level,
        "current_streak": student.current_streak,
        "longest_streak": student.longest_streak,
        "streak_freezes": student.streak_freezes,
    }

# ────────────────────────── Student Routes ──────────────────────────

@app.get("/api/students/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {
        "id": student.id, "name": student.name, "age": student.age,
        "role": student.role, "path_id": student.path_id, "avatar": student.avatar,
        "total_xp": student.total_xp, "level": student.level,
        "current_streak": student.current_streak, "longest_streak": student.longest_streak,
        "streak_freezes": student.streak_freezes,
    }

@app.get("/api/students")
def get_all_students(db: Session = Depends(get_db)):
    students = db.query(Student).filter(Student.role == "student").order_by(desc(Student.total_xp)).all()
    return [{"id": s.id, "name": s.name, "age": s.age, "path_id": s.path_id,
             "avatar": s.avatar, "total_xp": s.total_xp, "level": s.level,
             "current_streak": s.current_streak} for s in students]

# ────────────────────────── Topics Routes ──────────────────────────

@app.get("/api/topics/{path_id}")
def get_topics(path_id: str, db: Session = Depends(get_db)):
    topics = db.query(Topic).filter(Topic.path_id == path_id).order_by(Topic.order_num).all()
    return [{"id": t.id, "order_num": t.order_num, "title": t.title,
             "description": t.description, "difficulty": t.difficulty,
             "read_time": t.read_time} for t in topics]

@app.get("/api/topic/{topic_id}")
def get_topic(topic_id: int, db: Session = Depends(get_db)):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    # Lazy-generate content if missing — use Groq (primary) or Gemini (fallback)
    ai_available = GROQ_AVAILABLE or GEMINI_AVAILABLE
    if ai_available and not topic.content_normal:
        try:
            path_profiles = {
                "gaming": {
                    "audience": "a smart 13-year-old who is obsessed with gaming — Minecraft, PUBG, FIFA, GTA, Roblox, Valorant",
                    "simple_style": "Use super simple language. Relate EVERYTHING to popular games. No jargon at all. Pretend you're explaining it to a friend who's never studied.",
                    "normal_style": "Use gaming examples throughout — specific game mechanics, characters, and scenarios. Be exciting and energetic. Name real games.",
                    "tech_style": "Explain the underlying algorithms and data structures. Include game engine examples. Connect to real game dev concepts.",
                    "sections_normal": ["Introduction", "What Is It Really?", "How It Works In Games", "Real Games Using This Right Now", "The Secret Sauce (Key Mechanisms)", "Why This Changes Gaming", "Try This Challenge"],
                    "sections_tech": ["Technical Foundation", "Core Algorithms", "Data Structures Used", "Real Game Engine Implementation", "Performance Considerations", "State of the Art", "Research Frontiers"],
                },
                "business": {
                    "audience": "a sharp 17-year-old interested in entrepreneurship and AI for business",
                    "simple_style": "Plain English, business scenarios, no tech jargon. Use examples from companies a teen would know.",
                    "normal_style": "Use Indian startup examples (Zomato, Flipkart, Paytm, Swiggy, CRED, Meesho) and global giants. Focus on ROI and practical value.",
                    "tech_style": "Explain the technology behind the business application. Include market data, use cases, implementation considerations.",
                    "sections_normal": ["Introduction", "The Business Problem It Solves", "How Companies Use It Today", "Indian Companies Leading the Way", "The Money Behind It", "How to Build This into a Business", "Your Action Plan"],
                    "sections_tech": ["Technical Overview", "How It Works", "Implementation Strategy", "Data Requirements", "Key Metrics & KPIs", "Case Studies", "Building Your Own"],
                },
                "developer": {
                    "audience": "a 20-year-old CS student who codes and wants to understand AI deeply",
                    "simple_style": "Clear explanation with pseudocode and simple analogies. Assume basic CS knowledge.",
                    "normal_style": "Include algorithm names, complexity analysis, framework mentions (PyTorch, TensorFlow, scikit-learn). Be precise and technical.",
                    "tech_style": "Deep dive: math notation, code snippets, paper references, benchmarks, architectural decisions, tradeoffs.",
                    "sections_normal": ["Concept Overview", "Core Algorithm", "Mathematical Intuition", "Code Implementation Pattern", "Real-World Systems", "Performance & Complexity", "What to Build Next"],
                    "sections_tech": ["Formal Definition", "Mathematical Foundation", "Algorithm Deep-Dive", "Implementation Architecture", "Optimization Techniques", "Production Considerations", "Research Papers to Read"],
                },
                "ai_enthusiast": {
                    "audience": "an adult AI enthusiast who wants complete, nuanced understanding",
                    "simple_style": "Accessible but not dumbed-down. Use clear analogies for complex concepts.",
                    "normal_style": "Comprehensive coverage including history, how it works, applications, limitations, and future. Be intellectually engaging.",
                    "tech_style": "Full technical depth: theory, math, implementation details, current SOTA, open research questions, ethical considerations.",
                    "sections_normal": ["Historical Context", "What It Is & Why It Matters", "How It Actually Works", "Current Applications", "Limitations & Challenges", "Ethical Dimensions", "The Future"],
                    "sections_tech": ["Technical Foundation", "Mathematical Framework", "Architecture & Implementation", "Current State of the Art", "Benchmarks & Comparisons", "Open Problems", "Research Directions"],
                },
            }
            profile = path_profiles.get(topic.path_id, path_profiles["ai_enthusiast"])

            def build_content_prompt(level: str) -> str:
                if level == "simple":
                    style = profile["simple_style"]
                    sections = ["Let's Break It Down Simply", "The Fun Connection", "Real Examples You Know", "Why This Is Cool", "Quick Summary Points"]
                    para_count = "8-10"
                elif level == "normal":
                    style = profile["normal_style"]
                    sections = profile["sections_normal"]
                    para_count = "10-13"
                else:  # technical
                    style = profile["tech_style"]
                    sections = profile["sections_tech"]
                    para_count = "12-15"

                sections_str = "\n".join(f"## {s}" for s in sections)
                return f"""Write a comprehensive {level}-level lesson about "{topic.title}" for {profile['audience']}.

Style guide: {style}

Use EXACTLY these section headers (with ## prefix):
{sections_str}

Requirements:
- Total {para_count} substantial paragraphs across all sections
- Each paragraph must be 3-5 sentences minimum
- Be specific — use real names, real examples, real numbers
- Last section (if "Summary" or "Points"): use bullet points with - prefix
- Write engaging prose, NOT bullet points for the main content
- NO generic statements. Everything must be specific and vivid.

Return ONLY the raw content text. Start directly with the first ## header. No preamble."""

            simple_content = normal_content = tech_content = ""
            fun_fact = real_world = ""

            if GROQ_AVAILABLE:
                for level, attr in [("simple", "simple_content"), ("normal", "normal_content"), ("technical", "tech_content")]:
                    try:
                        locals()[attr] = groq_chat(
                            [{"role": "user", "content": build_content_prompt(level)}],
                            max_tokens=3000, temperature=0.75,
                        )
                    except Exception:
                        pass
            elif GEMINI_AVAILABLE:
                # Gemini generates all levels in one call for efficiency
                prompt = f"""Write comprehensive educational content about "{topic.title}" for {profile['audience']}.
{profile['normal_style']}

Return ONLY valid JSON with these keys:
{{
  "simple": "8-10 paragraph beginner explanation with ## section headers (sections: Let's Break It Down, The Fun Connection, Real Examples, Why This Is Cool, Quick Summary). Use bullet points with - for the summary section.",
  "normal": "11-13 paragraph full explanation with ## section headers ({', '.join(profile['sections_normal'])}). Last section use bullets.",
  "technical": "13-15 paragraph technical deep-dive with ## section headers ({', '.join(profile['sections_tech'])}). Include specific technical details.",
  "fun_fact": "One surprising counterintuitive fact (2 sentences).",
  "real_world": "A specific detailed real-world case study (3-4 sentences)."
}}"""
                try:
                    response = gemini_model.generate_content(prompt)
                    text = response.text.strip()
                    if text.startswith("```"):
                        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
                    data = json.loads(text)
                    simple_content = data.get("simple", "")
                    normal_content = data.get("normal", "")
                    tech_content = data.get("technical", "")
                    fun_fact = data.get("fun_fact", "")
                    real_world = data.get("real_world", "")
                except Exception:
                    pass

            if normal_content:
                topic.content_simple = simple_content or normal_content
                topic.content_normal = normal_content
                topic.content_technical = tech_content or normal_content
                if not topic.fun_fact and fun_fact:
                    topic.fun_fact = fun_fact
                if not topic.real_world_example and real_world:
                    topic.real_world_example = real_world
                db.commit()
        except Exception:
            pass

    return {
        "id": topic.id, "path_id": topic.path_id, "order_num": topic.order_num,
        "title": topic.title, "description": topic.description,
        "difficulty": topic.difficulty, "read_time": topic.read_time,
        "content_simple": topic.content_simple or "",
        "content_normal": topic.content_normal or "",
        "content_technical": topic.content_technical or "",
        "fun_fact": topic.fun_fact or "",
        "real_world_example": topic.real_world_example or "",
    }

@app.get("/api/progress/{student_id}")
def get_progress(student_id: int, db: Session = Depends(get_db)):
    progress = db.query(TopicProgress).filter(TopicProgress.student_id == student_id).all()
    return [{"topic_id": p.topic_id, "completed": p.completed,
             "quiz_score": p.quiz_score, "quiz_attempts": p.quiz_attempts} for p in progress]

@app.post("/api/topics/complete")
def complete_topic(req: MarkTopicRequest, db: Session = Depends(get_db)):
    progress = db.query(TopicProgress).filter(
        TopicProgress.student_id == req.student_id,
        TopicProgress.topic_id == req.topic_id
    ).first()
    if not progress:
        progress = TopicProgress(student_id=req.student_id, topic_id=req.topic_id,
                                  completed=True, completed_at=datetime.utcnow())
        db.add(progress)
    else:
        progress.completed = True
        progress.completed_at = datetime.utcnow()
    db.commit()
    xp = add_xp(db, req.student_id, 50, f"Completed topic")
    return {"message": "Topic completed!", "xp_earned": 50, "total_xp": xp}

# ────────────────────────── Quiz Routes ──────────────────────────

def _build_quiz_prompt(topic_title: str, path_context: str, count: int, easy: int, medium: int, hard: int) -> str:
    return f"""Generate exactly {count} quiz questions about "{topic_title}" for an AI learning platform.
{path_context}

Distribution: {easy} easy (basic recall/definitions), {medium} medium (application/understanding), {hard} hard (analysis/synthesis/edge-cases).
Include True/False questions (about 20% of total) and MCQ for the rest (4 distinct options each).

IMPORTANT: Make questions specific, interesting, and NOT generic. Reference real scenarios.

Return ONLY a valid JSON array, zero markdown, zero explanation. Each element:
{{"question":"engaging question text","type":"mcq","options":["A","B","C","D"],"correct":"exact text matching one option","explanation":"2-3 sentence explanation with context and why wrong options are wrong","difficulty":"easy"}}

True/False example:
{{"question":"True or False: ..?","type":"true_false","options":["True","False"],"correct":"True","explanation":"...","difficulty":"easy"}}"""


@app.get("/api/quiz/generate/{topic_id}")
def generate_quiz(topic_id: int, student_id: int = Query(...), db: Session = Depends(get_db)):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    student = db.query(Student).filter(Student.id == student_id).first()
    if not topic or not student:
        raise HTTPException(status_code=404, detail="Topic or student not found")

    # ── Check cache: if 40+ questions exist, sample 15 and return ──
    cached = db.query(CachedQuizQuestion).filter(CachedQuizQuestion.topic_id == topic_id).all()
    if len(cached) >= 40:
        selected = random.sample(cached, min(15, len(cached)))
        order = {"easy": 0, "medium": 1, "hard": 2}
        selected.sort(key=lambda x: order.get(x.difficulty, 1))
        return {
            "questions": [{
                "question": q.question, "type": q.q_type,
                "options": json.loads(q.options), "correct": q.correct,
                "explanation": q.explanation, "difficulty": q.difficulty,
            } for q in selected],
            "topic": topic.title,
            "pool_size": len(cached),
        }

    path_context = {
        "gaming": "Student is 13 and loves Minecraft, PUBG, FIFA, GTA, Roblox. Use specific game mechanics, characters, and scenarios throughout. Every question should relate to gaming.",
        "business": "Student is 17 and interested in business. Use real Indian companies (Zomato, Flipkart, Paytm, CRED) and global examples (Amazon, Uber). Focus on practical business applications, no coding.",
        "developer": "Student is 20 and studying CS. Use technical examples with algorithms, data structures, code concepts. Include nuanced technical distinctions.",
        "ai_enthusiast": "Student is an adult AI enthusiast wanting deep understanding. Include historical context, ethical dimensions, comparisons between approaches, and future implications.",
    }
    ctx = path_context.get(student.path_id, "Make questions clear and educational with specific examples.")

    all_new_questions = []

    # ── Primary: Groq via stdlib urllib (no groq package needed) ──
    if GROQ_AVAILABLE:
        try:
            batches = [
                (25, 8, 11, 6),   # count, easy, medium, hard
                (25, 5, 10, 10),
            ]
            for count, easy, medium, hard in batches:
                prompt = _build_quiz_prompt(topic.title, ctx, count, easy, medium, hard)
                text = groq_chat([{"role": "user", "content": prompt}], max_tokens=4500)
                text = text.strip()
                if "```" in text:
                    parts = text.split("```")
                    text = parts[1] if len(parts) > 1 else text
                    if text.startswith("json"):
                        text = text[4:]
                    text = text.rsplit("```", 1)[0]
                batch = json.loads(text.strip())
                all_new_questions.extend(batch)
        except Exception:
            all_new_questions = []

    # ── Fallback: Gemini (generate 20 questions) ──
    if not all_new_questions and GEMINI_AVAILABLE:
        try:
            prompt = _build_quiz_prompt(topic.title, ctx, 20, 6, 8, 6)
            response = gemini_model.generate_content(prompt)
            text = response.text.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            all_new_questions = json.loads(text)
        except Exception:
            pass

    # ── Cache all generated questions ──
    if all_new_questions:
        for q in all_new_questions:
            db.add(CachedQuizQuestion(
                topic_id=topic_id,
                question=q.get("question", ""),
                q_type=q.get("type", "mcq"),
                options=json.dumps(q.get("options", [])),
                correct=q.get("correct", ""),
                explanation=q.get("explanation", ""),
                difficulty=q.get("difficulty", "medium"),
            ))
        db.commit()
        # Return 15 sorted by difficulty
        selected = random.sample(all_new_questions, min(15, len(all_new_questions)))
        order = {"easy": 0, "medium": 1, "hard": 2}
        selected.sort(key=lambda x: order.get(x.get("difficulty", "medium"), 1))
        return {"questions": selected, "topic": topic.title, "pool_size": len(all_new_questions)}

    # ── Static fallback ──
    return {"questions": [
        {"question": f"What is the main concept behind {topic.title}?", "type": "mcq",
         "options": ["Machine Learning", "Artificial Intelligence", "Data Processing", "Neural Networks"],
         "correct": "Artificial Intelligence", "difficulty": "easy",
         "explanation": f"{topic.title} is fundamentally about AI — the science of making machines smart."},
        {"question": f"True or False: {topic.title} is an important area in modern AI?", "type": "true_false",
         "options": ["True", "False"], "correct": "True", "difficulty": "easy",
         "explanation": f"Absolutely! {topic.title} is a core pillar of modern AI development."},
        {"question": f"Which best describes a key aspect of {topic.title}?", "type": "mcq",
         "options": ["Pattern Recognition", "Data Storage", "Web Design", "Hardware Manufacturing"],
         "correct": "Pattern Recognition", "difficulty": "medium",
         "explanation": "AI fundamentally works by recognizing patterns in data to make intelligent decisions."},
        {"question": f"What makes {topic.title} powerful?", "type": "mcq",
         "options": ["It automates intelligent tasks", "It replaces all humans", "It only works offline", "It requires no data"],
         "correct": "It automates intelligent tasks", "difficulty": "medium",
         "explanation": "The core power of AI is automating tasks that normally require human intelligence."},
        {"question": "True or False: AI systems improve through learning from experience?", "type": "true_false",
         "options": ["True", "False"], "correct": "True", "difficulty": "easy",
         "explanation": "Yes! Machine learning — a branch of AI — specifically enables systems to improve from experience."},
    ], "topic": topic.title}

@app.post("/api/quiz/submit")
def submit_quiz(req: QuizSubmit, db: Session = Depends(get_db)):
    correct = sum(1 for a in req.answers if a.get("is_correct"))
    total = len(req.answers)
    score = (correct / total * 100) if total > 0 else 0

    xp = correct * 10
    if score == 100:
        xp += 50  # Perfect score bonus

    db.add(QuizResult(
        student_id=req.student_id, topic_id=req.topic_id,
        score=score, total_questions=total, correct_answers=correct, xp_earned=xp
    ))

    # Update topic progress
    progress = db.query(TopicProgress).filter(
        TopicProgress.student_id == req.student_id,
        TopicProgress.topic_id == req.topic_id
    ).first()
    if not progress:
        progress = TopicProgress(student_id=req.student_id, topic_id=req.topic_id,
                                  quiz_score=score, quiz_attempts=1)
        db.add(progress)
    else:
        if score > progress.quiz_score:
            progress.quiz_score = score
        progress.quiz_attempts += 1
    db.commit()

    total_xp = add_xp(db, req.student_id, xp, f"Quiz: {correct}/{total} correct")

    # Check comeback kid badge
    if progress.quiz_attempts > 1 and score > 0:
        student = db.query(Student).filter(Student.id == req.student_id).first()
        if student:
            badge = db.query(Badge).filter(Badge.name == "Comeback Kid").first()
            if badge:
                existing = db.query(StudentBadge).filter(
                    StudentBadge.student_id == student.id,
                    StudentBadge.badge_id == badge.id
                ).first()
                if not existing:
                    db.add(StudentBadge(student_id=student.id, badge_id=badge.id))
                    db.commit()

    pool_size = db.query(CachedQuizQuestion).filter(CachedQuizQuestion.topic_id == req.topic_id).count()
    return {"score": score, "correct": correct, "total": total,
            "xp_earned": xp, "total_xp": total_xp, "perfect": score == 100,
            "pool_size": pool_size if pool_size > 0 else None}

@app.get("/api/quiz/history/{student_id}")
def quiz_history(student_id: int, db: Session = Depends(get_db)):
    results = db.query(QuizResult).filter(QuizResult.student_id == student_id).order_by(desc(QuizResult.taken_at)).limit(50).all()
    out = []
    for r in results:
        topic = db.query(Topic).filter(Topic.id == r.topic_id).first()
        out.append({
            "id": r.id, "topic_id": r.topic_id,
            "topic_title": topic.title if topic else "Unknown",
            "score": r.score, "correct": r.correct_answers,
            "total": r.total_questions, "xp_earned": r.xp_earned,
            "taken_at": r.taken_at.isoformat() if r.taken_at else ""
        })
    return out

# ────────────────────────── AI Tutor Chat Routes ──────────────────────────

@app.post("/api/chat")
def chat_with_tutor(req: ChatRequest, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == req.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.add(ChatMessage(student_id=student.id, role="user", content=req.message))
    db.commit()

    if not GROQ_AVAILABLE:
        fallback_msg = (
            f"Hey {student.name}! 🤖 The AI tutor isn't connected yet — "
            "GROQ_API_KEY is missing from Railway environment variables. "
            "Ask your uncle to add it in Railway → Variables!"
        )
        db.add(ChatMessage(student_id=student.id, role="assistant", content=fallback_msg))
        db.commit()
        return {"response": fallback_msg}

    try:
        system_prompt = get_tutor_system_prompt(student)
        recent_messages = db.query(ChatMessage).filter(
            ChatMessage.student_id == student.id
        ).order_by(desc(ChatMessage.id)).limit(20).all()
        recent_messages.reverse()

        topic_context = f"\n\nCurrent topic context: {req.topic}" if req.topic else ""

        # Build OpenAI-format messages for Groq
        messages = [{"role": "system", "content": system_prompt + topic_context}]
        for msg in recent_messages[:-1]:  # exclude the message we just added
            messages.append({
                "role": "user" if msg.role == "user" else "assistant",
                "content": msg.content,
            })
        messages.append({"role": "user", "content": req.message})

        # Call Groq via stdlib urllib (no groq package required)
        reply = groq_chat(messages, max_tokens=1024)

        db.add(ChatMessage(student_id=student.id, role="assistant", content=reply))
        db.commit()
        add_xp(db, student.id, 0, "")  # trigger badge checks
        return {"response": reply}

    except Exception as e:
        error_msg = "Taking a quick breather 😴 — try again in a moment! (Groq API hiccup)"
        db.add(ChatMessage(student_id=student.id, role="assistant", content=error_msg))
        db.commit()
        return {"response": error_msg}

@app.get("/api/chat/history/{student_id}")
def get_chat_history(student_id: int, db: Session = Depends(get_db)):
    messages = db.query(ChatMessage).filter(
        ChatMessage.student_id == student_id
    ).order_by(ChatMessage.id).limit(100).all()
    return [{"role": m.role, "content": m.content,
             "created_at": m.created_at.isoformat() if m.created_at else ""} for m in messages]

# ────────────────────────── Flashcard Routes ──────────────────────────

@app.get("/api/flashcards/decks/{path_id}")
def get_flashcard_decks(path_id: str, db: Session = Depends(get_db)):
    decks = db.query(FlashcardDeck).filter(FlashcardDeck.path_id == path_id).all()
    return [{"id": d.id, "title": d.title, "description": d.description} for d in decks]

@app.post("/api/flashcards/generate")
def generate_flashcards(req: FlashcardGenRequest, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == req.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # ── Check cache ──
    cached = db.query(CachedFlashcard).filter(
        CachedFlashcard.topic_name == req.topic,
        CachedFlashcard.path_id == student.path_id
    ).all()
    if len(cached) >= 20:
        cards = []
        for c in cached:
            back_text = c.back
            if c.example:
                back_text += f"\n\n🎮 Example: {c.example}"
            if c.mnemonic:
                back_text += f"\n\n🧠 Remember: {c.mnemonic}"
            cards.append({"front": c.front, "back": back_text})
        return {"cards": cards, "topic": req.topic, "cached": True}

    path_context = {
        "gaming": "For a 13-year-old gamer. Every example must reference a real game (Minecraft, PUBG, FIFA, GTA, Roblox, Valorant, etc.). Use gamer language. Make it fun.",
        "business": "For a 17-year-old business student. Use real companies (Zomato, Flipkart, Amazon, Uber, etc.). Focus on practical business value.",
        "developer": "For a 20-year-old CS student. Be technical. Include algorithmic concepts, code patterns, and framework names.",
        "ai_enthusiast": "For an adult AI enthusiast. Be comprehensive and accurate. Include nuance, history, and real-world implications.",
    }
    ctx = path_context.get(student.path_id, "Use clear explanations with concrete examples.")

    new_cards = []

    # ── Primary: Groq (25 flashcards) ──
    if GROQ_AVAILABLE:
        try:
            prompt = f"""Generate exactly 25 comprehensive flashcards about "{req.topic}".
{ctx}

Each flashcard should be memorable and test real understanding — NOT just rote memorization.
Cover the topic from multiple angles: definitions, mechanisms, applications, comparisons, edge cases, history.

Return ONLY valid JSON array. Each object:
{{"front":"concise question or term (max 15 words)","back":"rich explanation (3-4 sentences that really teach)","example":"specific real-world or gaming example (2 sentences)","mnemonic":"memory trick, acronym, or vivid analogy (1-2 sentences, can be empty string if not helpful)"}}"""
            text = groq_chat([{"role": "user", "content": prompt}], max_tokens=5000)
            if "```" in text:
                parts = text.split("```")
                text = parts[1] if len(parts) > 1 else text
                if text.startswith("json"):
                    text = text[4:]
                text = text.rsplit("```", 1)[0]
            new_cards = json.loads(text.strip())
        except Exception:
            new_cards = []

    # ── Fallback: Gemini (15 flashcards) ──
    if not new_cards and GEMINI_AVAILABLE:
        try:
            prompt = f"""Generate exactly 15 flashcards about "{req.topic}". {ctx}
Return ONLY valid JSON array. Each object:
{{"front":"concise question or term","back":"3-4 sentence explanation","example":"real-world example","mnemonic":"memory trick or empty string"}}"""
            response = gemini_model.generate_content(prompt)
            text = response.text.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            new_cards = json.loads(text)
        except Exception:
            pass

    # ── Cache and return ──
    if new_cards:
        for c in new_cards:
            db.add(CachedFlashcard(
                topic_name=req.topic,
                path_id=student.path_id,
                front=c.get("front", ""),
                back=c.get("back", ""),
                example=c.get("example", ""),
                mnemonic=c.get("mnemonic", ""),
            ))
        db.commit()
        cards = []
        for c in new_cards:
            back_text = c.get("back", "")
            if c.get("example"):
                back_text += f"\n\n🎮 Example: {c['example']}"
            if c.get("mnemonic"):
                back_text += f"\n\n🧠 Remember: {c['mnemonic']}"
            cards.append({"front": c.get("front", ""), "back": back_text})
        return {"cards": cards, "topic": req.topic}

    # ── Static fallback ──
    return {"cards": [
        {"front": f"What is {req.topic}?", "back": f"{req.topic} is a core concept in AI. It enables machines to perform tasks that normally require human-level intelligence. Understanding it unlocks the door to building smart applications.\n\n🎮 Example: Game NPCs use similar concepts to decide their behavior.\n\n🧠 Remember: Think of it as 'teaching machines to think'."},
        {"front": f"Why does {req.topic} matter?", "back": "It's one of the foundational building blocks of modern AI systems. Without it, many AI-powered features we use daily wouldn't exist. Mastering this concept opens pathways to advanced AI topics.\n\n🎮 Example: Every game recommendation algorithm relies on concepts like this."},
        {"front": "What is Machine Learning?", "back": "ML is a branch of AI where systems automatically learn patterns from data without being explicitly programmed. The more data it sees, the smarter it gets — like a student who improves through practice.\n\n🧠 Remember: ML = learning from examples, not from rules."},
        {"front": "What is a Neural Network?", "back": "A neural network is a system of interconnected nodes inspired by the human brain. Data flows through layers of nodes, each applying transformations until an answer emerges. Deep learning uses many of these layers.\n\n🎮 Example: The AI that generates Minecraft terrain uses neural network concepts."},
        {"front": "What is Reinforcement Learning?", "back": "RL is how AI learns through trial, error, and rewards. The agent takes actions, observes results, and adjusts its strategy to maximize rewards over time. It's how AI learned to beat humans at chess and Go.\n\n🎮 Example: Game AI that learns to beat players uses RL to improve each match."},
    ], "topic": req.topic}

@app.post("/api/flashcards/progress")
def update_flashcard_progress(req: FlashcardProgressRequest, db: Session = Depends(get_db)):
    progress = db.query(FlashcardProgress).filter(
        FlashcardProgress.student_id == req.student_id,
        FlashcardProgress.deck_id == req.deck_id,
        FlashcardProgress.card_index == req.card_index
    ).first()
    if not progress:
        progress = FlashcardProgress(student_id=req.student_id, deck_id=req.deck_id,
                                      card_index=req.card_index, known=req.known)
        db.add(progress)
    else:
        progress.known = req.known
        progress.reviewed_at = datetime.utcnow()
    db.commit()

    # Check if completed a deck
    deck_progress = db.query(FlashcardProgress).filter(
        FlashcardProgress.student_id == req.student_id,
        FlashcardProgress.deck_id == req.deck_id
    ).count()
    if deck_progress >= 10:
        add_xp(db, req.student_id, 30, "Flashcard session complete")

    return {"message": "Progress saved"}

# ────────────────────────── Concepts Routes ──────────────────────────

@app.get("/api/concepts/{path_id}")
def get_concepts(path_id: str, db: Session = Depends(get_db)):
    concepts = db.query(Concept).filter(Concept.path_id == path_id).all()
    return [{"id": c.id, "title": c.title, "simple_explanation": c.simple_explanation,
             "technical_explanation": c.technical_explanation,
             "real_world_example": c.real_world_example, "fun_fact": c.fun_fact,
             "difficulty": c.difficulty, "read_time": c.read_time} for c in concepts]

# ────────────────────────── Daily Challenge Routes ──────────────────────────

@app.get("/api/challenge/today/{student_id}")
def get_today_challenge(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    today = date.today().isoformat()

    existing = db.query(DailyChallenge).filter(
        DailyChallenge.student_id == student_id,
        DailyChallenge.challenge_date == today
    ).first()

    if existing:
        return {"id": existing.id, "type": existing.challenge_type,
                "text": existing.challenge_text, "completed": existing.completed,
                "response": existing.response, "xp_earned": existing.xp_earned,
                "date": today}

    # Generate new challenge
    challenges = DAILY_CHALLENGES.get(student.path_id, DAILY_CHALLENGES["gaming"])
    day_index = (date.today().toordinal()) % len(challenges)

    # Check if Sunday for boss challenge
    if date.today().weekday() == 6:
        day_index = len(challenges) - 1  # Last one is always boss challenge

    challenge = challenges[day_index]
    new_challenge = DailyChallenge(
        student_id=student_id, challenge_date=today,
        challenge_type=challenge["type"], challenge_text=challenge["text"]
    )
    db.add(new_challenge)
    db.commit()

    return {"id": new_challenge.id, "type": challenge["type"],
            "text": challenge["text"], "completed": False,
            "response": "", "xp_earned": 0, "date": today}

@app.post("/api/challenge/submit")
def submit_challenge(req: ChallengeSubmitRequest, db: Session = Depends(get_db)):
    challenge = db.query(DailyChallenge).filter(DailyChallenge.id == req.challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    challenge.completed = True
    challenge.response = req.response
    challenge.xp_earned = 100
    db.commit()

    total_xp = add_xp(db, req.student_id, 100, "Daily challenge completed!")

    return {"message": "Challenge completed! 🎉", "xp_earned": 100, "total_xp": total_xp}

# ────────────────────────── Leaderboard Routes ──────────────────────────

@app.get("/api/leaderboard")
def get_leaderboard(period: str = "all", db: Session = Depends(get_db)):
    students = db.query(Student).filter(Student.role == "student").order_by(desc(Student.total_xp)).all()

    messages = [
        "👑 The AI King!", "🔥 Almost there, keep pushing!",
        "💪 Time to grind!", "🚀 Last place today, Legend tomorrow!"
    ]

    result = []
    for i, s in enumerate(students):
        result.append({
            "rank": i + 1, "name": s.name, "avatar": s.avatar,
            "total_xp": s.total_xp, "level": s.level,
            "current_streak": s.current_streak, "path_id": s.path_id,
            "message": messages[i] if i < len(messages) else "Keep going! 🌟"
        })
    return result

# ────────────────────────── Badge Routes ──────────────────────────

@app.get("/api/badges")
def get_all_badges(db: Session = Depends(get_db)):
    badges = db.query(Badge).all()
    return [{"id": b.id, "name": b.name, "description": b.description,
             "icon": b.icon, "category": b.category} for b in badges]

@app.get("/api/badges/{student_id}")
def get_student_badges(student_id: int, db: Session = Depends(get_db)):
    student_badges = db.query(StudentBadge).filter(StudentBadge.student_id == student_id).all()
    result = []
    for sb in student_badges:
        badge = db.query(Badge).filter(Badge.id == sb.badge_id).first()
        if badge:
            result.append({
                "id": badge.id, "name": badge.name, "description": badge.description,
                "icon": badge.icon, "category": badge.category,
                "earned_at": sb.earned_at.isoformat() if sb.earned_at else ""
            })
    return result

# ────────────────────────── XP & Analytics Routes ──────────────────────────

@app.get("/api/xp/log/{student_id}")
def get_xp_log(student_id: int, db: Session = Depends(get_db)):
    logs = db.query(XPLog).filter(XPLog.student_id == student_id).order_by(desc(XPLog.created_at)).limit(50).all()
    return [{"amount": l.amount, "reason": l.reason,
             "created_at": l.created_at.isoformat() if l.created_at else ""} for l in logs]

@app.get("/api/analytics/{student_id}")
def get_analytics(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    topics_total = db.query(Topic).filter(Topic.path_id == student.path_id).count()
    topics_completed = db.query(TopicProgress).filter(
        TopicProgress.student_id == student_id, TopicProgress.completed == True
    ).count()

    quiz_results = db.query(QuizResult).filter(QuizResult.student_id == student_id).all()
    avg_score = sum(r.score for r in quiz_results) / len(quiz_results) if quiz_results else 0
    total_quizzes = len(quiz_results)
    perfect_scores = sum(1 for r in quiz_results if r.score == 100)

    badges_earned = db.query(StudentBadge).filter(StudentBadge.student_id == student_id).count()
    total_badges = db.query(Badge).count()

    challenges_done = db.query(DailyChallenge).filter(
        DailyChallenge.student_id == student_id, DailyChallenge.completed == True
    ).count()

    chat_count = db.query(ChatMessage).filter(
        ChatMessage.student_id == student_id, ChatMessage.role == "user"
    ).count()

    # XP by day for chart
    xp_logs = db.query(XPLog).filter(XPLog.student_id == student_id).all()
    xp_by_day = {}
    for log in xp_logs:
        day = log.created_at.strftime("%Y-%m-%d") if log.created_at else "unknown"
        xp_by_day[day] = xp_by_day.get(day, 0) + log.amount
    xp_chart = [{"date": k, "xp": v} for k, v in sorted(xp_by_day.items())]

    # Quiz scores over time
    quiz_chart = [{"date": r.taken_at.strftime("%Y-%m-%d") if r.taken_at else "",
                   "score": r.score} for r in quiz_results]

    return {
        "total_xp": student.total_xp,
        "level": student.level,
        "current_streak": student.current_streak,
        "longest_streak": student.longest_streak,
        "topics_completed": topics_completed,
        "topics_total": topics_total,
        "avg_quiz_score": round(avg_score, 1),
        "total_quizzes": total_quizzes,
        "perfect_scores": perfect_scores,
        "badges_earned": badges_earned,
        "total_badges": total_badges,
        "challenges_completed": challenges_done,
        "tutor_questions": chat_count,
        "xp_chart": xp_chart,
        "quiz_chart": quiz_chart,
    }

# ────────────────────────── Admin Routes ──────────────────────────

@app.get("/api/admin/overview")
def admin_overview(db: Session = Depends(get_db)):
    students = db.query(Student).filter(Student.role == "student").all()
    overview = []
    for s in students:
        topics_completed = db.query(TopicProgress).filter(
            TopicProgress.student_id == s.id, TopicProgress.completed == True
        ).count()
        topics_total = db.query(Topic).filter(Topic.path_id == s.path_id).count()
        quizzes_taken = db.query(QuizResult).filter(QuizResult.student_id == s.id).count()
        badges = db.query(StudentBadge).filter(StudentBadge.student_id == s.id).count()
        challenges = db.query(DailyChallenge).filter(
            DailyChallenge.student_id == s.id, DailyChallenge.completed == True
        ).count()

        overview.append({
            "id": s.id, "name": s.name, "age": s.age, "path_id": s.path_id,
            "avatar": s.avatar, "total_xp": s.total_xp, "level": s.level,
            "current_streak": s.current_streak,
            "topics_completed": topics_completed, "topics_total": topics_total,
            "quizzes_taken": quizzes_taken, "badges_earned": badges,
            "challenges_completed": challenges,
        })
    return overview

@app.get("/api/health")
def health_check():
    return {"status": "ok", "gemini": GEMINI_AVAILABLE}

# ────────────────────────── Serve React Frontend ──────────────────────────

STATIC_DIR = Path(__file__).parent / "static"

if STATIC_DIR.exists():
    app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="static-assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve React app for all non-API routes (SPA fallback)."""
        file_path = STATIC_DIR / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(STATIC_DIR / "index.html")
