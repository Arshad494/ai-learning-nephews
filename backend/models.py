from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    pin = Column(String, nullable=False)
    role = Column(String, default="student")  # student or admin
    path_id = Column(String, nullable=False)  # gaming, business, developer
    avatar = Column(String, default="")
    total_xp = Column(Integer, default=0)
    level = Column(String, default="Explorer")
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_login_date = Column(String, default="")
    streak_freezes = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    progress = relationship("TopicProgress", back_populates="student")
    quiz_results = relationship("QuizResult", back_populates="student")
    badges = relationship("StudentBadge", back_populates="student")
    chat_messages = relationship("ChatMessage", back_populates="student")
    daily_challenges = relationship("DailyChallenge", back_populates="student")
    flashcard_progress = relationship("FlashcardProgress", back_populates="student")
    xp_log = relationship("XPLog", back_populates="student")


class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True, index=True)
    path_id = Column(String, nullable=False)
    order_num = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    difficulty = Column(String, default="beginner")  # beginner, intermediate, advanced
    read_time = Column(Integer, default=10)  # minutes
    content_simple = Column(Text, default="")
    content_normal = Column(Text, default="")
    content_technical = Column(Text, default="")
    fun_fact = Column(Text, default="")
    real_world_example = Column(Text, default="")


class TopicProgress(Base):
    __tablename__ = "topic_progress"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    topic_id = Column(Integer, ForeignKey("topics.id"))
    completed = Column(Boolean, default=False)
    quiz_score = Column(Float, default=0)
    quiz_attempts = Column(Integer, default=0)
    completed_at = Column(DateTime, nullable=True)

    student = relationship("Student", back_populates="progress")
    topic = relationship("Topic")


class QuizResult(Base):
    __tablename__ = "quiz_results"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    topic_id = Column(Integer, ForeignKey("topics.id"))
    score = Column(Float, nullable=False)
    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, nullable=False)
    xp_earned = Column(Integer, default=0)
    taken_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="quiz_results")
    topic = relationship("Topic")


class Badge(Base):
    __tablename__ = "badges"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    icon = Column(String, default="🏆")
    category = Column(String, default="general")  # general, path_specific, streak, quiz


class StudentBadge(Base):
    __tablename__ = "student_badges"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    badge_id = Column(Integer, ForeignKey("badges.id"))
    earned_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="badges")
    badge = relationship("Badge")


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    role = Column(String, nullable=False)  # user or assistant
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="chat_messages")


class DailyChallenge(Base):
    __tablename__ = "daily_challenges"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    challenge_date = Column(String, nullable=False)
    challenge_type = Column(String, nullable=False)  # quiz, explain, apply, debate
    challenge_text = Column(Text, nullable=False)
    completed = Column(Boolean, default=False)
    response = Column(Text, default="")
    xp_earned = Column(Integer, default=0)

    student = relationship("Student", back_populates="daily_challenges")


class FlashcardDeck(Base):
    __tablename__ = "flashcard_decks"
    id = Column(Integer, primary_key=True, index=True)
    path_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, default="")


class FlashcardProgress(Base):
    __tablename__ = "flashcard_progress"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    deck_id = Column(Integer, ForeignKey("flashcard_decks.id"))
    card_index = Column(Integer, nullable=False)
    known = Column(Boolean, default=False)
    reviewed_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="flashcard_progress")
    deck = relationship("FlashcardDeck")


class XPLog(Base):
    __tablename__ = "xp_log"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    amount = Column(Integer, nullable=False)
    reason = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="xp_log")


class Concept(Base):
    __tablename__ = "concepts"
    id = Column(Integer, primary_key=True, index=True)
    path_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    simple_explanation = Column(Text, default="")
    technical_explanation = Column(Text, default="")
    real_world_example = Column(Text, default="")
    fun_fact = Column(Text, default="")
    difficulty = Column(String, default="beginner")
    read_time = Column(Integer, default=5)
