"""
seed_content.py — Pre-generates rich content for all topics at deploy time.
Runs as part of Railway build: pip install ... && python seed_data.py && python seed_content.py
"""
import os, json, time, sys

# ── DB setup ──
from database import SessionLocal, engine, Base
from models import *

Base.metadata.create_all(bind=engine)
db = SessionLocal()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()

if not GROQ_API_KEY:
    print("⚠️  No GROQ_API_KEY — skipping content generation")
    db.close()
    sys.exit(0)

try:
    from groq import Groq
    client = Groq(api_key=GROQ_API_KEY)
    print("✅ Groq SDK ready")
except Exception as e:
    print(f"❌ Could not load Groq SDK: {e}")
    db.close()
    sys.exit(0)


def groq_call(prompt: str, max_tokens: int = 4000) -> str | None:
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        return resp.choices[0].message.content
    except Exception as e:
        print(f"    ⚠️  Groq error: {e}")
        return None


def parse_json(text: str):
    if not text:
        return None
    try:
        t = text.strip()
        if "```" in t:
            parts = t.split("```")
            t = parts[1] if len(parts) > 1 else t
            if t.startswith("json"):
                t = t[4:]
            t = t.rsplit("```", 1)[0]
        return json.loads(t.strip())
    except Exception:
        return None


# ══════════════════════════════════════════════════════
#  GAMING TOPICS — full lesson + quiz + flashcards
# ══════════════════════════════════════════════════════

GAMING_CONTEXT = """Student: 13-year-old who LOVES gaming (Minecraft, PUBG, FIFA, GTA, Roblox, Valorant, Free Fire).
Style: Energetic, fun, specific. Use real game names, mechanics, and characters in every explanation.
Never generic. Every sentence should make a gamer say 'Oh that's like in [game]!'"""


def generate_topic_content(topic_title: str) -> dict | None:
    prompt = f"""{GAMING_CONTEXT}

Write comprehensive lesson content about "{topic_title}".

Return ONLY valid JSON with exactly these keys:
{{
  "simple": "8-10 paragraphs. Use ## section headers:\\n## Let's Break It Down Simply\\n## The Gaming Connection\\n## Real Games You Already Know\\n## How It Works (No Jargon)\\n## Why This Is Epic\\n## Quick Recap\\n(Last section: bullet points using - prefix)",
  "normal": "11-13 paragraphs. Use ## section headers:\\n## Introduction\\n## What Is It Really?\\n## How It Works In Games\\n## Real Games Using This RIGHT NOW\\n## The Secret Sauce (Core Mechanism)\\n## Why This Is Changing Gaming Forever\\n## Try This Challenge\\n(Be SPECIFIC: name actual games, mechanics, characters)",
  "technical": "13-15 paragraphs. Use ## section headers:\\n## Technical Foundation\\n## Core Algorithms\\n## Data Structures & Complexity\\n## Real Game Engine Implementation\\n## Performance Considerations\\n## State of the Art\\n## Research Frontiers & Open Problems",
  "fun_fact": "One mind-blowing fact about this topic in gaming context (2 sentences).",
  "real_world": "A specific detailed real game example — name the game, describe exactly how it uses this concept (3-4 sentences)."
}}"""
    text = groq_call(prompt, max_tokens=5000)
    return parse_json(text)


def generate_quiz_questions(topic_title: str) -> list | None:
    prompt = f"""{GAMING_CONTEXT}

Generate exactly 50 quiz questions about "{topic_title}".

Distribution: 15 easy, 20 medium, 15 hard.
Format: 40 MCQ (4 options each) + 10 True/False.

Rules:
- Every question must reference a specific game or gaming scenario
- MCQ options must all be plausible (no obvious wrong answers)
- Explanations must be 2-3 sentences with gaming context
- Hard questions must test analysis, not just recall

Return ONLY a valid JSON array. Each object:
{{"question":"engaging game-themed question text","type":"mcq","options":["Option A","Option B","Option C","Option D"],"correct":"exact text of correct option","explanation":"2-3 sentence explanation with gaming example","difficulty":"easy"}}

For true_false questions:
{{"question":"True or False: statement","type":"true_false","options":["True","False"],"correct":"True","explanation":"explanation","difficulty":"easy"}}"""
    text = groq_call(prompt, max_tokens=8000)
    result = parse_json(text)
    return result if isinstance(result, list) else None


def generate_flashcards(topic_title: str) -> list | None:
    prompt = f"""{GAMING_CONTEXT}

Generate exactly 25 comprehensive flashcards about "{topic_title}".

Each card must:
- Test real understanding, not just memorization
- Include a specific gaming example from a named game
- Have a memorable mnemonic or analogy where helpful
- Cover diverse aspects: definitions, mechanisms, applications, comparisons, history

Return ONLY a valid JSON array. Each object:
{{"front":"concise question or term (max 15 words)","back":"rich explanation (3-4 sentences that truly teach the concept)","example":"specific example from Minecraft/PUBG/FIFA/GTA/Roblox naming exact mechanics (2 sentences)","mnemonic":"memory trick, acronym, or vivid analogy (1-2 sentences, or empty string)"}}"""
    text = groq_call(prompt, max_tokens=5000)
    result = parse_json(text)
    return result if isinstance(result, list) else None


# ── Process all gaming topics ──
topics = db.query(Topic).filter(Topic.path_id == "gaming").order_by(Topic.order_num).all()
print(f"\n🎮 Processing {len(topics)} gaming topics...\n")

for idx, topic in enumerate(topics, 1):
    print(f"[{idx}/{len(topics)}] {topic.title}")

    # 1. Lesson content
    if not topic.content_normal:
        print("    → Generating lesson content...")
        data = generate_topic_content(topic.title)
        if data:
            topic.content_simple   = data.get("simple", "")
            topic.content_normal   = data.get("normal", "")
            topic.content_technical = data.get("technical", "")
            if not topic.fun_fact:
                topic.fun_fact = data.get("fun_fact", "")
            if not topic.real_world_example:
                topic.real_world_example = data.get("real_world", "")
            db.commit()
            print(f"    ✓ Content: {len(topic.content_normal)} chars")
        else:
            print("    ✗ Content generation failed")
        time.sleep(1.5)
    else:
        print(f"    → Content exists ({len(topic.content_normal)} chars)")

    # 2. Quiz questions
    existing_q = db.query(CachedQuizQuestion).filter(CachedQuizQuestion.topic_id == topic.id).count()
    if existing_q < 40:
        print("    → Generating 50 quiz questions...")
        questions = generate_quiz_questions(topic.title)
        if questions:
            for q in questions[:50]:
                db.add(CachedQuizQuestion(
                    topic_id=topic.id,
                    question=q.get("question", ""),
                    q_type=q.get("type", "mcq"),
                    options=json.dumps(q.get("options", [])),
                    correct=q.get("correct", ""),
                    explanation=q.get("explanation", ""),
                    difficulty=q.get("difficulty", "medium"),
                ))
            db.commit()
            print(f"    ✓ Quiz: {min(len(questions), 50)} questions")
        else:
            print("    ✗ Quiz generation failed")
        time.sleep(1.5)
    else:
        print(f"    → Quiz exists ({existing_q} questions)")

    # 3. Flashcards
    existing_fc = db.query(CachedFlashcard).filter(
        CachedFlashcard.topic_name == topic.title,
        CachedFlashcard.path_id == "gaming"
    ).count()
    if existing_fc < 20:
        print("    → Generating 25 flashcards...")
        cards = generate_flashcards(topic.title)
        if cards:
            for c in cards[:25]:
                db.add(CachedFlashcard(
                    topic_name=topic.title,
                    path_id="gaming",
                    front=c.get("front", ""),
                    back=c.get("back", ""),
                    example=c.get("example", ""),
                    mnemonic=c.get("mnemonic", ""),
                ))
            db.commit()
            print(f"    ✓ Flashcards: {min(len(cards), 25)} cards")
        else:
            print("    ✗ Flashcard generation failed")
        time.sleep(1.5)
    else:
        print(f"    → Flashcards exist ({existing_fc} cards)")

    print()

db.close()

# ── Summary ──
db2 = SessionLocal()
total_content  = db2.query(Topic).filter(Topic.path_id == "gaming", Topic.content_normal != "").count()
total_quiz     = db2.query(CachedQuizQuestion).join(Topic, CachedQuizQuestion.topic_id == Topic.id).filter(Topic.path_id == "gaming").count()
total_cards    = db2.query(CachedFlashcard).filter(CachedFlashcard.path_id == "gaming").count()
db2.close()

print("=" * 50)
print(f"✅ DONE!")
print(f"   Topics with content : {total_content}/{len(topics)}")
print(f"   Total quiz questions: {total_quiz}")
print(f"   Total flashcards    : {total_cards}")
print("=" * 50)
