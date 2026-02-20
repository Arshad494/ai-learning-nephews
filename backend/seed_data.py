from database import SessionLocal, engine, Base
from models import *
from datetime import datetime


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Clear existing data
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()

    # ── Students ──
    students = [
        Student(name="Aalam", age=13, pin="1313", role="student", path_id="gaming", avatar="🎮", total_xp=0, level="Explorer"),
        Student(name="Adham", age=17, pin="1717", role="student", path_id="business", avatar="💼", total_xp=0, level="Explorer"),
        Student(name="Irfan", age=17, pin="1717", role="student", path_id="business", avatar="📊", total_xp=0, level="Explorer"),
        Student(name="Adnan", age=20, pin="2020", role="student", path_id="developer", avatar="💻", total_xp=0, level="Explorer"),
        Student(name="Arshad", age=25, pin="2025", role="student", path_id="ai_enthusiast", avatar="🤖", total_xp=0, level="Explorer"),
        Student(name="Uncle", age=0, pin="0000", role="admin", path_id="admin", avatar="👨‍💼", total_xp=0, level="Legend"),
    ]
    db.add_all(students)
    db.commit()

    # ── Gaming Topics (Aalam) ──
    gaming_topics = [
        ("What is AI? — Explained Through Game NPCs", "Discover what AI really means using examples of non-player characters in your favorite games. Learn how NPCs make decisions and react to players.", "beginner", 8),
        ("How Game Enemies Think & Move — Pathfinding AI", "Explore A* pathfinding and navigation meshes that make enemies chase you intelligently in games like PUBG and Minecraft.", "beginner", 10),
        ("AI in Minecraft — Mobs & World Generation", "Learn how Minecraft uses procedural generation and mob AI to create infinite worlds and smart creatures.", "beginner", 10),
        ("AI in FIFA/FC25 — Player Behavior & Tactics", "Understand how FIFA's AI controls teammate runs, goalkeeper decisions, and adaptive difficulty.", "beginner", 10),
        ("AI in PUBG & Free Fire — Enemy Bots", "Discover how battle royale games use AI bots that mimic human behavior and get smarter over time.", "beginner", 8),
        ("AI in GTA — Traffic, Pedestrians & Police", "Explore the complex AI systems that make GTA's open world feel alive with realistic traffic and police chases.", "intermediate", 12),
        ("AI in Roblox — Game Creation with AI", "Learn how Roblox is using AI to help creators build games faster and generate content automatically.", "beginner", 10),
        ("Reinforcement Learning — How AI Learns to Play Games", "Understand the trial-and-error method AI uses to master games, just like how you get better by playing more.", "intermediate", 15),
        ("AlphaGo & OpenAI Five — AI Beating Champions", "The epic stories of AI systems that defeated world champions in Go and Dota 2.", "intermediate", 12),
        ("Chess Engines — How Computers Think Moves Ahead", "Learn how chess AI like Stockfish evaluates millions of positions to find the perfect move.", "intermediate", 12),
        ("AI Generating Game Worlds & Characters", "Explore procedural content generation — how AI creates endless unique levels, maps, and characters.", "intermediate", 12),
        ("AI Art for Games — Create Your Own Character", "Use AI art tools to design your own game characters, weapons, and environments.", "beginner", 10),
        ("AI Sound & Music in Games", "Discover how AI creates adaptive soundtracks and realistic sound effects that respond to gameplay.", "intermediate", 10),
        ("Prompt Engineering — Write Your Game Story with AI", "Master the art of prompting AI to write epic game narratives, character backstories, and quests.", "beginner", 12),
        ("Future of Gaming — AI-Generated Open Worlds", "Imagine games where every NPC has a unique personality and the world changes based on your choices.", "intermediate", 10),
        ("How to Use AI Tools as a Gamer Today", "A practical guide to AI tools every gamer can use right now for streaming, editing, and more.", "beginner", 8),
        ("Build a Simple Game Bot — Visual, No Heavy Coding", "Step-by-step guide to creating your own simple game bot using visual tools and basic logic.", "intermediate", 15),
        ("AI in Esports — Coaching & Analysis Tools", "How pro esports teams use AI for strategy analysis, player performance tracking, and coaching.", "intermediate", 12),
        ("Career in AI Game Development", "Explore careers that combine AI and gaming — from game designer to AI programmer.", "beginner", 10),
        ("Ethics — Cheating Bots vs Fair AI", "The important debate about AI cheats, aimbots, and how to keep gaming fair for everyone.", "beginner", 10),
    ]

    for i, (title, desc, diff, rt) in enumerate(gaming_topics):
        db.add(Topic(path_id="gaming", order_num=i+1, title=title, description=desc, difficulty=diff, read_time=rt))

    # ── Business Topics (Adham & Irfan) ──
    business_topics = [
        ("What is AI? — The Business Revolution", "Understanding AI as the most transformative technology for business since the internet. No coding needed.", "beginner", 10),
        ("AI in Banking & Finance", "How banks use AI for fraud detection, credit scoring, algorithmic trading, and customer service.", "intermediate", 12),
        ("AI in Marketing & Advertising", "Learn how AI powers targeted ads, customer segmentation, and personalized marketing campaigns.", "beginner", 10),
        ("AI in Sales — Lead Generation & CRM", "Discover how AI helps sales teams find leads, predict customer behavior, and close deals faster.", "intermediate", 12),
        ("AI in Stock Market & Trading", "Understanding algorithmic trading, AI-powered market analysis, and robo-advisors.", "intermediate", 15),
        ("AI for Entrepreneurs & Startups", "How to leverage AI as a startup founder — from idea validation to scaling operations.", "beginner", 12),
        ("ChatGPT for Business Productivity", "Master ChatGPT for writing emails, creating reports, brainstorming ideas, and automating tasks.", "beginner", 10),
        ("AI in Supply Chain & Logistics", "How companies like Amazon use AI to optimize delivery routes, inventory, and warehousing.", "intermediate", 12),
        ("AI in Customer Service — Chatbots", "Building and deploying AI chatbots that handle customer queries 24/7 with high satisfaction.", "beginner", 10),
        ("AI in E-Commerce — Amazon & Flipkart", "How recommendation engines, dynamic pricing, and AI search power online shopping.", "intermediate", 12),
        ("AI in Digital Marketing — SEO & Content", "Using AI for content creation, SEO optimization, social media management, and analytics.", "beginner", 10),
        ("AI Tools Every Business Student Needs", "A curated list of AI tools for productivity, research, presentations, and business analysis.", "beginner", 8),
        ("Start a Business with AI & No Money", "Practical guide to launching an AI-powered business with free tools and minimal investment.", "beginner", 12),
        ("AI in HR & Recruitment", "How AI screens resumes, conducts initial interviews, and predicts employee success.", "intermediate", 10),
        ("AI in Accounting & Financial Analysis", "Automating bookkeeping, financial forecasting, and expense management with AI.", "intermediate", 12),
        ("Data Analytics for Business Decisions", "Understanding how data-driven insights help businesses make smarter decisions.", "intermediate", 15),
        ("AI in Retail — Personalization Engines", "How stores use AI to personalize shopping experiences both online and offline.", "intermediate", 10),
        ("Future of Jobs — Which Jobs AI Will Change", "An honest look at how AI is transforming careers and what skills matter most.", "beginner", 12),
        ("Business Cases — Companies Winning with AI", "Real stories of Zomato, Amazon, Flipkart, Zerodha and others using AI to dominate.", "intermediate", 12),
        ("Ethics in Business AI — Bias & Privacy", "Understanding AI bias, data privacy concerns, and responsible AI use in business.", "beginner", 10),
    ]

    for i, (title, desc, diff, rt) in enumerate(business_topics):
        db.add(Topic(path_id="business", order_num=i+1, title=title, description=desc, difficulty=diff, read_time=rt))

    # ── Developer Topics (Adnan) ──
    developer_topics = [
        ("ML Fundamentals — Beyond Theory", "Core machine learning concepts with practical intuition — supervised, unsupervised, reinforcement learning.", "intermediate", 15),
        ("Python for AI — NumPy, Pandas, Sklearn", "Essential Python libraries for AI development with hands-on examples and best practices.", "intermediate", 15),
        ("Neural Networks — Architecture Deep Dive", "Understanding perceptrons, activation functions, backpropagation, and network architectures.", "advanced", 20),
        ("Deep Learning — CNNs, RNNs, Transformers", "Convolutional, recurrent, and transformer architectures — when to use what and why.", "advanced", 20),
        ("Large Language Models — How They Really Work", "Tokenization, attention mechanisms, training objectives, and scaling laws of LLMs.", "advanced", 20),
        ("Prompt Engineering — Advanced Techniques", "Chain-of-thought, few-shot, system prompts, and production prompt engineering patterns.", "intermediate", 15),
        ("Building RAG Systems from Scratch", "Retrieval-Augmented Generation — chunking, embedding, retrieval, and generation pipeline.", "advanced", 20),
        ("Vector Databases — Pinecone, Weaviate, ChromaDB", "Understanding vector similarity search, indexing strategies, and choosing the right vector DB.", "advanced", 15),
        ("Fine-Tuning Open Source Models", "LoRA, QLoRA, and full fine-tuning of models like Llama, Mistral using Hugging Face.", "advanced", 20),
        ("AI APIs — OpenAI, Gemini, Anthropic", "Working with major AI APIs — authentication, streaming, function calling, and best practices.", "intermediate", 12),
        ("Deploying ML Models to Production", "Model serving with FastAPI, Docker, cloud deployment, monitoring, and scaling.", "advanced", 20),
        ("FastAPI for AI Applications", "Building production-grade AI APIs with FastAPI — async, streaming, middleware, and testing.", "intermediate", 15),
        ("LangChain & LlamaIndex", "Building AI applications with popular frameworks — chains, agents, tools, and retrieval.", "intermediate", 15),
        ("AI System Design for Interviews", "Designing scalable AI systems — common interview questions and architectural patterns.", "advanced", 20),
        ("Contributing to AI Open Source", "Finding good first issues, understanding codebases, making meaningful contributions.", "intermediate", 12),
        ("AI Internship Preparation", "Resume tips, portfolio projects, interview prep, and networking for AI internships.", "beginner", 12),
        ("Building AI Portfolio Projects", "5 portfolio projects that stand out — from chatbots to ML pipelines.", "intermediate", 15),
        ("Hugging Face Ecosystem", "Models, datasets, spaces, transformers library — the complete Hugging Face guide.", "intermediate", 15),
        ("MLOps Basics", "CI/CD for ML, experiment tracking, model versioning, and monitoring in production.", "advanced", 18),
        ("AI Startup Opportunities for CS Students", "Identifying AI startup ideas, building MVPs, and the landscape of AI entrepreneurship.", "beginner", 12),
    ]

    for i, (title, desc, diff, rt) in enumerate(developer_topics):
        db.add(Topic(path_id="developer", order_num=i+1, title=title, description=desc, difficulty=diff, read_time=rt))

    # ── AI Enthusiast Topics (Arshad) ──
    ai_enthusiast_topics = [
        ("What is AI? The Complete Beginner's Guide", "A thorough introduction to Artificial Intelligence — what it is, what it isn't, and why it's the most important technology of our lifetime. No jargon, just clarity.", "beginner", 12),
        ("History of AI: From Turing to ChatGPT", "Travel through 70+ years of AI history — from Alan Turing's 'Computing Machinery and Intelligence' to the GPT revolution. Understand the winters, the breakthroughs, and where we are now.", "beginner", 10),
        ("How Large Language Models Really Work", "A deep, accessible explanation of how ChatGPT, Claude, and Gemini work under the hood — tokens, transformers, attention, and training at scale. No PhD required.", "intermediate", 18),
        ("The 10 AI Tools Everyone Needs in 2025", "A curated, practical guide to the most powerful AI tools available today — for writing, coding, image generation, research, productivity, and more. With real use cases.", "beginner", 12),
        ("Prompt Engineering: Talk to AI Like a Pro", "Master the art and science of writing prompts. Learn techniques like chain-of-thought, role prompting, few-shot examples, and system instructions to get dramatically better AI outputs.", "beginner", 15),
        ("Machine Learning Explained Simply", "What is machine learning, how does it differ from traditional programming, and why does it matter? Covers supervised, unsupervised, and reinforcement learning with vivid real-world analogies.", "beginner", 12),
        ("Neural Networks: How AI 'Thinks'", "A visual and conceptual tour of neural networks — from the single perceptron to deep networks with billions of parameters. Understand layers, weights, activation, and backpropagation.", "intermediate", 15),
        ("AI in Your Daily Life — You Use It More Than You Know", "AI is already everywhere around you. Discover how AI powers your Spotify recommendations, Gmail spam filter, Google Maps routes, face unlock, and Amazon shopping experience.", "beginner", 10),
        ("ChatGPT vs Gemini vs Claude: What's the Difference?", "A detailed, honest comparison of the leading AI assistants — capabilities, strengths, weaknesses, pricing, and the best use cases for each. Make an informed choice.", "beginner", 12),
        ("AI Art & Creativity: DALL-E, Midjourney, Stable Diffusion", "How generative image AI works, what makes each tool unique, and how artists, designers, and creators are using them today. Covers the creative workflow and best practices.", "beginner", 12),
        ("AI in Healthcare: Saving Lives with Algorithms", "How AI detects cancer earlier than doctors, predicts patient deterioration, accelerates drug discovery, and is transforming diagnosis, treatment, and hospital operations.", "intermediate", 12),
        ("AI in Education: The Future of Learning", "How AI is personalizing education, enabling 24/7 tutoring, grading essays, identifying struggling students, and potentially making quality education accessible to everyone.", "beginner", 10),
        ("Build AI Apps Without Coding: No-Code AI Tools", "A hands-on guide to building real AI applications using no-code and low-code platforms. Create chatbots, automation workflows, AI pipelines, and more — zero coding required.", "beginner", 12),
        ("AI Ethics: Bias, Privacy & Responsibility", "The uncomfortable truths about AI bias, surveillance capitalism, deepfakes, data privacy, and the urgent need for responsible AI development. What YOU can do about it.", "beginner", 12),
        ("The AI Alignment Problem: Making AI Safe", "The most important unsolved problem in AI — how do we ensure AI systems do what we actually want as they become more powerful? Covers RLHF, constitutional AI, and interpretability.", "intermediate", 15),
        ("AI Agents: AI That Acts on Your Behalf", "The next frontier of AI — systems that don't just answer questions but take actions, use tools, browse the web, write code, and complete multi-step tasks autonomously.", "intermediate", 15),
        ("Future of AI: What's Coming in the Next 5 Years", "From multimodal AI and AI scientists to brain-computer interfaces and AGI — an informed, grounded look at the near-future of artificial intelligence and its societal implications.", "intermediate", 12),
        ("How to Stay Updated with AI: Best Resources", "The blogs, newsletters, podcasts, YouTube channels, Twitter accounts, and communities you need to follow to stay at the cutting edge of AI without getting overwhelmed.", "beginner", 10),
        ("Starting Your AI Career or Business", "Practical pathways into the AI field — from AI product manager to prompt engineer to AI entrepreneur. What skills to build, what to learn first, and how to get your first opportunity.", "beginner", 12),
        ("AI and Society: How AI is Changing the World", "A broad view of AI's impact across industries, economies, and civilizations — job displacement, wealth concentration, geopolitical competition, and the human questions at the center of it all.", "intermediate", 12),
    ]

    for i, (title, desc, diff, rt) in enumerate(ai_enthusiast_topics):
        db.add(Topic(path_id="ai_enthusiast", order_num=i+1, title=title, description=desc, difficulty=diff, read_time=rt))

    db.commit()

    # ── Badges (25 total) ──
    badges_data = [
        ("First Steps", "Complete your first login", "👋", "general"),
        ("Quick Learner", "Get 5 correct answers in a row", "⚡", "quiz"),
        ("Perfectionist", "Score 100% on a quiz", "💯", "quiz"),
        ("Knowledge Seeker", "Read 10 concepts", "📚", "general"),
        ("Week Warrior", "Maintain a 7-day streak", "🔥", "streak"),
        ("Legend", "Reach Legend level", "👑", "general"),
        ("AI Whisperer", "Ask the AI tutor 50 questions", "🤖", "general"),
        ("Curious Mind", "Explore all topics in your path", "🧠", "general"),
        ("Game Master", "Aalam's special gaming badge", "🎮", "path_specific"),
        ("Business Brain", "Adham & Irfan's special business badge", "💼", "path_specific"),
        ("Code Wizard", "Adnan's special developer badge", "🧙", "path_specific"),
        ("Leaderboard King", "Reach #1 on the leaderboard", "🏆", "general"),
        ("Night Owl", "Login after 10 PM", "🦉", "general"),
        ("Early Bird", "Login before 8 AM", "🌅", "general"),
        ("Comeback Kid", "Retry after failing a quiz", "💪", "general"),
        ("Graduate", "Complete your full learning path", "🎓", "general"),
        ("Flashcard Master", "Complete 10 flashcard decks", "🃏", "general"),
        ("Challenge Champion", "Complete 30 daily challenges", "⚔️", "general"),
        ("Team Player", "Encourage a cousin", "🤝", "general"),
        ("Deep Thinker", "Ask the AI tutor 100 questions", "🔮", "general"),
        ("Rising Star", "Reach Engineer level", "⭐", "general"),
        ("All Rounder", "Study 5 different topics", "🌍", "general"),
        ("Rocket Start", "Earn 100 XP on day 1", "🚀", "general"),
        ("Diamond Mind", "Get perfect quiz score 5 times", "💎", "quiz"),
        ("Show Off", "Top the leaderboard for 7 days", "🏅", "general"),
        ("AI Pioneer", "Arshad's special AI Enthusiast badge", "🤖", "path_specific"),
    ]

    for name, desc, icon, cat in badges_data:
        db.add(Badge(name=name, description=desc, icon=icon, category=cat))

    db.commit()

    # ── Concepts (20 per path = 60 total) ──
    gaming_concepts = [
        ("NPC (Non-Player Character)", "A character in a game controlled by the computer, not by a player.", "NPCs use finite state machines or behavior trees to make decisions about movement, dialogue, and reactions to player actions.", "In Skyrim, NPCs have daily routines — they eat, sleep, and work, making the world feel alive.", "The first NPC appeared in the 1974 game Maze War!", "beginner", 3),
        ("Pathfinding", "How game characters find their way from point A to point B without bumping into walls.", "A* algorithm evaluates nodes using f(n) = g(n) + h(n) where g is cost so far and h is heuristic estimate to goal.", "Every enemy that chases you in a game uses pathfinding — from Pac-Man ghosts to PUBG bots.", "Pac-Man's ghosts each use different pathfinding strategies — that's why they feel different!", "beginner", 4),
        ("Procedural Generation", "AI creating game content automatically — maps, levels, items — so every playthrough is unique.", "Uses algorithms like Perlin noise, Wave Function Collapse, and L-systems to generate coherent but random content.", "Minecraft's infinite worlds are procedurally generated — no two worlds are exactly the same.", "No Man's Sky has 18 quintillion procedurally generated planets!", "intermediate", 5),
        ("Behavior Tree", "A decision-making system for game AI that works like a flowchart of actions.", "Tree structure with selector, sequence, and decorator nodes that evaluate conditions and execute actions.", "In Halo, enemy AI uses behavior trees to decide whether to attack, take cover, or retreat.", "Behavior trees were first popularized by Halo 2's AI system.", "intermediate", 5),
        ("Finite State Machine", "An AI system where characters switch between states like idle, patrol, chase, and attack.", "Each state has entry/exit actions and transitions triggered by conditions like player proximity.", "In Super Mario, Goombas have simple states: walk left, fall off edge — that's a state machine!", "Most classic game enemies use state machines — they're simple but effective.", "beginner", 4),
        ("Reinforcement Learning", "AI that learns by trying things and getting rewards or penalties — like learning a game by playing it.", "Agent interacts with environment, receives rewards, and updates policy using Q-learning or policy gradient methods.", "OpenAI trained an AI to play Dota 2 using reinforcement learning — it beat pro teams!", "DeepMind's AI learned to play Atari games from scratch, with no instructions!", "intermediate", 6),
        ("Neural Network", "An AI system inspired by the human brain — layers of connected nodes that learn patterns.", "Composed of input, hidden, and output layers with weighted connections trained via backpropagation.", "Neural networks power the AI in racing games that learns your driving style and adapts.", "The first neural network was built in 1958 — it could recognize simple shapes!", "intermediate", 6),
        ("Game Physics Engine", "Software that simulates realistic physics — gravity, collisions, ragdoll effects in games.", "Uses numerical integration, collision detection algorithms, and constraint solvers for real-time simulation.", "When you blow something up in GTA and debris flies everywhere — that's the physics engine!", "Some physics engines calculate millions of collision checks per second.", "intermediate", 5),
        ("Difficulty Scaling", "AI that adjusts how hard the game is based on how well you're playing.", "Dynamic difficulty adjustment uses player performance metrics to modify enemy stats, spawn rates, and resources.", "FIFA uses this — if you're losing badly, the AI might make your shots more accurate.", "Resident Evil 4 pioneered dynamic difficulty — enemies got easier if you died a lot.", "beginner", 4),
        ("Minimax Algorithm", "The AI strategy used in chess and board games — thinking ahead about all possible moves.", "Explores game tree alternating between maximizing own score and minimizing opponent's, with alpha-beta pruning.", "Chess engines use minimax to evaluate millions of future positions before choosing a move.", "Deep Blue evaluated 200 million positions per second to beat chess champion Kasparov!", "intermediate", 6),
        ("Monte Carlo Tree Search", "An AI method that simulates random games to figure out the best move to make.", "Builds a search tree using selection, expansion, simulation, and backpropagation phases.", "AlphaGo used MCTS combined with neural networks to beat the world Go champion.", "MCTS can handle games with more possible moves than atoms in the universe!", "advanced", 6),
        ("Generative AI", "AI that creates new content — images, music, text, game levels — that never existed before.", "Uses models like GANs, VAEs, and diffusion models trained on large datasets to generate novel content.", "AI can now generate entire game levels, character designs, and soundtracks from text descriptions.", "An AI-generated painting sold for $432,500 at Christie's auction house!", "beginner", 5),
        ("Computer Vision", "AI that can see and understand images and video — used for motion tracking in games.", "Uses CNNs and object detection models to process visual input and extract meaningful information.", "Xbox Kinect uses computer vision to track your body and turn you into the game controller!", "Self-driving cars use the same computer vision tech as some gaming systems.", "intermediate", 5),
        ("Natural Language Processing", "AI that understands and generates human language — powers voice commands in games.", "Tokenization, embedding, and transformer models process text to understand meaning and generate responses.", "AI Dungeon uses NLP to create infinite text-based adventures where you can do anything.", "GPT models can write game dialogue that's hard to tell apart from human writing!", "intermediate", 5),
        ("Aimbot Detection", "AI systems used to catch cheaters who use AI-powered aim assistance in games.", "Uses statistical analysis of aim patterns, reaction times, and movement to identify inhuman precision.", "Valorant's Vanguard anti-cheat uses AI to detect subtle cheating patterns.", "Some anti-cheat AI can detect cheaters with 99% accuracy!", "beginner", 4),
        ("Procedural Animation", "AI-generated character movement that adapts in real-time instead of using pre-made animations.", "Uses inverse kinematics, physics simulation, and ML models to generate natural-looking movement.", "In Uncharted, Nathan Drake's hands reach out to walls dynamically — that's procedural animation.", "Some games use AI to make characters walk differently on different terrain!", "intermediate", 5),
        ("AI Director", "An AI system that controls the pace and drama of a game in real-time.", "Monitors player stress, engagement, and performance to dynamically adjust events and encounters.", "Left 4 Dead's AI Director spawns zombies based on how stressed you are!", "The AI Director was so good, players thought the zombie spawns were random!", "intermediate", 5),
        ("Swarm Intelligence", "AI where many simple agents follow simple rules to create complex group behavior.", "Uses algorithms like boids (separation, alignment, cohesion) to simulate flocking and herding.", "When a flock of birds flies in formation in a game, that's swarm intelligence!", "Real ant colonies inspired swarm AI algorithms used in games.", "intermediate", 5),
        ("Terrain Generation", "AI algorithms that create realistic landscapes — mountains, rivers, forests for game worlds.", "Combines Perlin noise, erosion simulation, and biome classification to generate realistic terrain.", "The massive worlds in games like Skyrim use terrain generation to create mountains and valleys.", "Some terrain generators can create worlds the size of Earth!", "beginner", 4),
        ("AI Companions", "AI characters that fight alongside you, help you, and feel like real teammates.", "Use advanced behavior trees, dialogue systems, and relationship tracking to create believable partners.", "Elizabeth in BioShock Infinite is considered one of the best AI companions ever made.", "Good AI companions need to be helpful without being annoying — that's harder than it sounds!", "beginner", 4),
    ]

    for title, simple, tech, real, fun, diff, rt in gaming_concepts:
        db.add(Concept(path_id="gaming", title=title, simple_explanation=simple, technical_explanation=tech, real_world_example=real, fun_fact=fun, difficulty=diff, read_time=rt))

    business_concepts = [
        ("Artificial Intelligence", "Computer systems that can do tasks that normally need human intelligence.", "AI encompasses machine learning, deep learning, NLP, computer vision, and expert systems that process data to make decisions.", "Zomato uses AI to predict delivery times and optimize restaurant recommendations.", "AI contributes over $15 trillion to the global economy!", "beginner", 3),
        ("Machine Learning", "AI that improves automatically by learning from data — without being explicitly programmed.", "Algorithms like regression, decision trees, and neural networks find patterns in training data to make predictions.", "Netflix's recommendation engine uses ML to suggest shows you'll love based on viewing history.", "YouTube's ML recommends 70% of all videos watched on the platform!", "beginner", 4),
        ("Chatbot", "An AI program that can have conversations with humans through text or voice.", "Uses NLP, intent recognition, and dialogue management to understand queries and generate responses.", "Flipkart's chatbot handles millions of customer queries daily, reducing wait times by 90%.", "The first chatbot ELIZA was created in 1966 and mimicked a therapist!", "beginner", 3),
        ("Predictive Analytics", "Using AI to analyze data and predict future outcomes and trends.", "Statistical models and ML algorithms process historical data to forecast future events with confidence intervals.", "Amazon predicts what you'll buy next — sometimes shipping items before you even order!", "Weather forecasting AI is now more accurate than human meteorologists.", "intermediate", 5),
        ("Natural Language Processing", "AI that understands, interprets, and generates human language.", "Combines tokenization, parsing, semantic analysis, and generation models to process text and speech.", "Google Translate uses NLP to translate between 130+ languages instantly.", "GPT-4 can pass the bar exam — it understands legal language!", "intermediate", 5),
        ("Computer Vision", "AI that can see and understand images and videos like humans do.", "Uses CNNs and object detection to identify objects, faces, text, and scenes in visual data.", "Amazon Go stores use computer vision — you just walk in, grab items, and walk out!", "Facebook's face recognition AI is 97% accurate — better than most humans.", "intermediate", 5),
        ("Recommendation Engine", "AI that suggests products, content, or services based on your preferences.", "Collaborative and content-based filtering analyze user behavior patterns to predict preferences.", "Spotify's Discover Weekly uses AI to create personalized playlists for 400 million users.", "35% of Amazon's revenue comes from its recommendation engine!", "beginner", 4),
        ("Robotic Process Automation", "AI-powered software robots that automate repetitive business tasks.", "RPA bots mimic human actions on computer interfaces to process data, fill forms, and manage workflows.", "Banks use RPA to process loan applications 10x faster than human employees.", "RPA can save businesses 25,000+ hours of work per year!", "intermediate", 5),
        ("Sentiment Analysis", "AI that reads text and determines if the feeling is positive, negative, or neutral.", "NLP models classify text polarity using trained classifiers on labeled sentiment datasets.", "Brands monitor Twitter with sentiment analysis to catch PR crises before they go viral.", "AI can detect sarcasm in text with 80% accuracy!", "beginner", 4),
        ("Data-Driven Decision Making", "Using data analysis and AI insights instead of gut feeling to make business choices.", "Combines statistical analysis, visualization, A/B testing, and predictive modeling for evidence-based decisions.", "Zerodha uses data analytics to understand user behavior and improve their trading platform.", "Companies using data-driven decisions are 5% more productive and 6% more profitable!", "beginner", 4),
        ("Algorithmic Trading", "Using AI algorithms to automatically buy and sell stocks at optimal times.", "ML models analyze market data, news sentiment, and patterns to execute trades in milliseconds.", "Over 70% of stock market trades are now done by AI algorithms, not humans.", "A trading AI once made $1 billion in a single day!", "advanced", 6),
        ("Customer Segmentation", "Using AI to group customers into categories based on behavior and preferences.", "Clustering algorithms like K-means analyze purchase history, demographics, and behavior to create segments.", "Zomato segments users into categories to send personalized restaurant recommendations.", "Good segmentation can increase marketing ROI by 760%!", "intermediate", 5),
        ("Fraud Detection", "AI systems that spot suspicious transactions and prevent financial fraud.", "Anomaly detection models learn normal patterns and flag deviations in real-time transaction streams.", "Banks' AI fraud detection prevents billions in fraudulent transactions every year.", "AI can detect credit card fraud in 0.5 seconds!", "intermediate", 5),
        ("Dynamic Pricing", "AI that automatically adjusts prices based on demand, competition, and other factors.", "ML models analyze supply-demand, competitor prices, time factors, and elasticity to optimize pricing.", "Uber's surge pricing is AI-powered — prices go up when demand is high in your area.", "Airlines change prices up to 300 times per day using AI!", "intermediate", 5),
        ("Supply Chain Optimization", "Using AI to make the movement of goods faster, cheaper, and more efficient.", "ML models forecast demand, optimize routes, manage inventory levels, and predict disruptions.", "Amazon's AI predicts demand so accurately, products are already near you before you order.", "AI-optimized supply chains reduce logistics costs by up to 15%.", "intermediate", 5),
        ("Personalization Engine", "AI that customizes every user's experience to be unique to them.", "Uses collaborative filtering, content analysis, and user modeling to tailor content and features.", "YouTube's homepage is completely different for every user — AI personalizes everything you see.", "Personalized experiences increase sales conversion by 20%!", "beginner", 4),
        ("AI Ethics", "The study of right and wrong when it comes to AI decisions and their impact.", "Covers bias in training data, fairness metrics, explainability, privacy, and governance frameworks.", "Amazon had to scrap an AI hiring tool because it was biased against women.", "The EU's AI Act is the world's first comprehensive AI regulation!", "beginner", 4),
        ("Business Intelligence", "Using data tools and AI to turn raw business data into actionable insights.", "Combines ETL, data warehousing, OLAP, and visualization to analyze business performance.", "Walmart processes 2.5 petabytes of data every hour using BI tools for decisions.", "BI market is worth over $33 billion and growing 10% yearly!", "intermediate", 5),
        ("Digital Transformation", "Using AI and technology to fundamentally change how a business operates.", "Strategic adoption of AI, cloud, IoT, and automation to reinvent processes and customer experiences.", "Domino's transformed from a pizza company to a tech company — 65% of orders are digital!", "Companies that embrace digital transformation are 26% more profitable!", "beginner", 4),
        ("AI-Powered Marketing", "Using AI tools to create, optimize, and automate marketing campaigns.", "Combines NLP for content, ML for targeting, computer vision for creatives, and analytics for optimization.", "Coca-Cola uses AI to create personalized ad campaigns for different demographics.", "AI marketing tools can increase click-through rates by 200%!", "beginner", 4),
    ]

    for title, simple, tech, real, fun, diff, rt in business_concepts:
        db.add(Concept(path_id="business", title=title, simple_explanation=simple, technical_explanation=tech, real_world_example=real, fun_fact=fun, difficulty=diff, read_time=rt))

    developer_concepts = [
        ("Supervised Learning", "ML where you train the model with labeled examples — input paired with correct output.", "Minimizes loss function over labeled dataset using gradient descent. Includes classification and regression.", "Gmail's spam filter is supervised learning — trained on millions of labeled spam/not-spam emails.", "ImageNet, a supervised learning benchmark, has 14 million labeled images!", "beginner", 4),
        ("Unsupervised Learning", "ML where the model finds patterns in data without being told what to look for.", "Clustering (K-means, DBSCAN) and dimensionality reduction (PCA, t-SNE) discover structure in unlabeled data.", "Spotify groups similar songs together using unsupervised learning for playlist generation.", "Unsupervised learning discovered a new type of galaxy astronomers had missed!", "beginner", 4),
        ("Neural Network", "Computing system inspired by biological neurons — layers of connected nodes that learn.", "Directed acyclic graph of neurons with weights, biases, activation functions, trained via backpropagation.", "GPT, DALL-E, and self-driving cars all use neural networks at their core.", "The human brain has 86 billion neurons — GPT-4 has ~1.8 trillion parameters!", "intermediate", 5),
        ("Transformer Architecture", "The architecture behind modern AI — processes all data at once using attention.", "Self-attention computes Q, K, V matrices; multi-head attention enables parallel pattern recognition.", "Every modern LLM (GPT, Claude, Gemini) uses the transformer architecture.", "The original 'Attention Is All You Need' paper has 100,000+ citations!", "advanced", 7),
        ("Embeddings", "Converting text, images, or data into numerical vectors that capture meaning.", "Dense vector representations in high-dimensional space where semantic similarity = vector proximity.", "Google Search uses embeddings to understand that 'dog' and 'puppy' mean similar things.", "Word2Vec discovered that king - man + woman = queen!", "intermediate", 5),
        ("RAG (Retrieval-Augmented Generation)", "Combining a search engine with an LLM — retrieve relevant docs, then generate answers.", "Pipeline: query → embed → vector search → retrieve chunks → inject into prompt → generate response.", "Perplexity AI uses RAG to search the web and generate accurate, sourced answers.", "RAG can reduce LLM hallucinations by up to 70%!", "advanced", 6),
        ("Fine-Tuning", "Taking a pre-trained model and training it further on your specific data.", "Adjusts pre-trained weights using domain-specific data via full fine-tuning, LoRA, or QLoRA.", "Companies fine-tune GPT on their support tickets to create custom customer service AI.", "Fine-tuning GPT-3 on just 100 examples can dramatically improve specific task performance!", "advanced", 6),
        ("Vector Database", "A specialized database designed to store and search embedding vectors efficiently.", "Uses ANN algorithms (HNSW, IVF) for approximate nearest neighbor search in high-dimensional space.", "Pinterest uses vector databases to find visually similar images from billions of pins.", "Vector search can find similar items among billions in milliseconds!", "advanced", 5),
        ("Prompt Engineering", "The art of writing instructions for AI to get the best possible output.", "Techniques include few-shot, chain-of-thought, system prompts, and structured output formatting.", "GitHub Copilot users who write better prompts get 2x more useful code suggestions.", "The best prompt engineers can earn $300k+ at top AI companies!", "intermediate", 5),
        ("LLM (Large Language Model)", "A massive neural network trained on text data that can understand and generate language.", "Autoregressive transformer trained on next-token prediction over trillions of tokens of text data.", "ChatGPT, Claude, and Gemini are all LLMs — they power the AI revolution.", "Training GPT-4 is estimated to have cost over $100 million!", "intermediate", 5),
        ("Attention Mechanism", "The key innovation that lets AI focus on the most relevant parts of input.", "Computes compatibility scores between query and key vectors, applies softmax, and weights values.", "When translating 'The cat sat on the mat', attention knows 'cat' relates to 'sat'.", "Attention was inspired by how humans focus — we don't read every word equally!", "advanced", 6),
        ("Backpropagation", "The algorithm that trains neural networks by calculating how to adjust weights.", "Applies chain rule to compute gradients of loss with respect to each weight, then updates via optimizer.", "Every neural network you've ever used was trained using backpropagation.", "Backpropagation was invented in 1986 but didn't become practical until GPUs made it fast!", "intermediate", 5),
        ("CNN (Convolutional Neural Network)", "Neural network designed for processing images using filters that detect patterns.", "Convolutional layers apply learnable filters, pooling layers reduce dimensions, fully connected layers classify.", "Your phone's face unlock uses CNNs to recognize your face from any angle.", "A CNN can analyze a medical X-ray faster and sometimes more accurately than a doctor!", "intermediate", 5),
        ("GAN (Generative Adversarial Network)", "Two neural networks competing — one generates fakes, one detects them, both improve.", "Generator G maps noise to data distribution while discriminator D classifies real vs. fake in a minimax game.", "NVIDIA's StyleGAN generates photorealistic faces of people who don't exist.", "The term 'deepfake' comes from GAN technology!", "advanced", 6),
        ("Transfer Learning", "Using knowledge from one AI task to help with a different but related task.", "Pre-trained model's learned representations are adapted to new domain via fine-tuning or feature extraction.", "ImageNet-trained models can be adapted to identify plant diseases with just 100 new images.", "Transfer learning reduced AI training costs by 90% for many applications!", "intermediate", 5),
        ("MLOps", "DevOps practices applied to machine learning — deploying and maintaining ML in production.", "Covers CI/CD for ML, experiment tracking, model versioning, monitoring, and automated retraining pipelines.", "Uber's Michelangelo platform manages thousands of ML models in production using MLOps.", "Companies with good MLOps deploy models 10x faster!", "advanced", 5),
        ("Tokenization", "Breaking text into smaller pieces (tokens) that AI models can understand.", "Subword tokenization (BPE, WordPiece) balances vocabulary size with representation of rare words.", "When ChatGPT processes your message, it first tokenizes it — 'hello' might be 1 token.", "GPT-4 has a vocabulary of ~100,000 tokens!", "intermediate", 4),
        ("Gradient Descent", "The optimization algorithm that helps neural networks learn — finding the lowest error.", "Iteratively updates parameters in the direction of steepest descent of the loss function: w = w - lr * ∇L.", "Every time an AI model trains on data, gradient descent is working behind the scenes.", "There are 50+ variants of gradient descent — Adam is the most popular!", "intermediate", 5),
        ("API (Application Programming Interface)", "A way for different software systems to talk to each other.", "Defines endpoints, request/response formats, authentication, and rate limits for programmatic access.", "When you use ChatGPT in an app, it's communicating through OpenAI's API.", "Stripe's API processes billions of dollars in payments yearly!", "beginner", 4),
        ("Docker & Containerization", "Packaging your AI application with all its dependencies into a portable container.", "Uses OS-level virtualization to create isolated, reproducible environments with defined dependencies.", "Most AI models in production run inside Docker containers for consistency and scalability.", "Docker Hub has over 100,000 pre-built container images!", "intermediate", 5),
    ]

    for title, simple, tech, real, fun, diff, rt in developer_concepts:
        db.add(Concept(path_id="developer", title=title, simple_explanation=simple, technical_explanation=tech, real_world_example=real, fun_fact=fun, difficulty=diff, read_time=rt))

    ai_enthusiast_concepts = [
        ("Artificial Intelligence", "Computer systems designed to perform tasks that normally require human intelligence.", "Encompasses ML, deep learning, NLP, computer vision, robotics, and expert systems that process data to make decisions, recognize patterns, and generate outputs.", "Google Search uses AI to understand what you mean, not just what you type — searching 'best place for pizza near me tonight' returns relevant local results.", "AI is expected to contribute $15.7 trillion to the global economy by 2030!", "beginner", 3),
        ("Large Language Model (LLM)", "A massive AI trained on vast amounts of text that can understand and generate human language with remarkable fluency.", "Transformer-based models with billions of parameters trained on next-token prediction over trillions of words. Emergent capabilities arise from scale.", "ChatGPT, Claude, and Gemini are all LLMs. When you ask for a recipe, they predict the most likely helpful response based on patterns learned from training data.", "GPT-4 was trained on roughly 1 trillion tokens of text — about a million books worth!", "intermediate", 5),
        ("Prompt Engineering", "The art of crafting instructions that get AI to give you the best possible output.", "Techniques include zero-shot, few-shot, chain-of-thought, role prompting, system instructions, and structured output formatting. Small wording changes can dramatically change output quality.", "A prompt like 'You are an expert nutritionist. Give me a 7-day meal plan for a 30-year-old woman who wants to lose 5kg, preferring vegetarian food.' will produce a far better result than 'give me a meal plan'.", "The best prompt engineers at top AI companies earn $300,000+ per year!", "beginner", 4),
        ("Hallucination", "When AI confidently generates information that sounds right but is factually wrong.", "Occurs because LLMs generate text statistically likely to follow from the prompt, not by retrieving verified facts. The model has no internal fact-checking mechanism.", "An AI might confidently cite a scientific paper that doesn't exist, or give wrong historical dates that sound plausible.", "A lawyer used ChatGPT to research cases — it invented fake court citations, leading to professional consequences!", "beginner", 3),
        ("Generative AI", "AI that creates new content — text, images, music, video, code — that never existed before.", "Uses models like transformers (text), diffusion models (images), and GANs to generate novel outputs from learned distributions of training data.", "Midjourney generates photorealistic images from text. Suno creates music from descriptions. GitHub Copilot writes code from comments.", "The AI-generated image market is projected to reach $917 million by 2030!", "beginner", 4),
        ("Neural Network", "An AI system loosely inspired by the human brain — layers of connected mathematical nodes that learn patterns.", "Directed acyclic graph of neurons with weighted connections. Input layer receives data, hidden layers transform it, output layer produces result. Trained via backpropagation.", "Your phone's face recognition is a neural network trained on millions of faces. It learned to identify you from thousands of examples.", "A single modern AI model can have more 'connections' than there are synapses in a human brain!", "intermediate", 5),
        ("Machine Learning", "AI that learns from data automatically — improving through experience without being explicitly programmed.", "Algorithms find patterns in training data by minimizing loss functions. Types: supervised (labeled data), unsupervised (find structure), reinforcement (reward signals).", "Netflix's recommendation algorithm uses ML to predict which shows you'll watch — it studies millions of users' viewing patterns to personalize your homepage.", "Netflix's recommendation AI saves the company $1 billion per year by reducing cancellations!", "beginner", 4),
        ("Token", "The basic unit of text that AI models process — roughly a word or part of a word.", "LLMs don't process characters or words directly. Text is split into tokens using algorithms like BPE. 'ChatGPT' might be one token; 'unprecedented' might be three.", "Every time you send a message to ChatGPT, it's broken into tokens. Pricing is based on tokens — roughly 750 words = 1,000 tokens.", "GPT-4 can process up to 128,000 tokens at once — roughly a 100,000-word book!", "beginner", 3),
        ("Embedding", "A way of converting words, images, or any data into numbers that capture meaning and relationships.", "Dense vectors in high-dimensional space where semantic similarity corresponds to vector proximity. 'King' - 'Man' + 'Woman' ≈ 'Queen' in vector space.", "Spotify converts songs into audio embeddings to find similar-sounding music for Discover Weekly. Two songs close in embedding space sound similar.", "Word2Vec discovered that the relationship between countries and capitals is consistent across languages in embedding space!", "intermediate", 5),
        ("AI Agent", "An AI system that doesn't just answer questions but takes actions — using tools, browsing the web, writing files, running code.", "Agents have a planning component (LLM), tools (web search, code execution, APIs), memory, and an action loop. They can complete complex multi-step tasks autonomously.", "Devin (AI software engineer) can receive a coding task, write code, run tests, debug errors, and deploy — all without human intervention.", "OpenAI Operator agents can book restaurants, fill forms, and complete purchases on your behalf!", "intermediate", 5),
        ("Multimodal AI", "AI that can understand and generate multiple types of content — text, images, audio, and video together.", "Unified model trained on multiple modalities simultaneously. Cross-attention mechanisms allow the model to relate information across different input types.", "GPT-4V can look at a photo of your fridge and suggest recipes based on what it sees. Gemini can watch a video and answer questions about specific moments.", "GPT-4o processes text and audio in 232 milliseconds — faster than human response time!", "intermediate", 4),
        ("AI Safety", "The field dedicated to ensuring AI systems behave safely, reliably, and in alignment with human values.", "Encompasses technical alignment (RLHF, Constitutional AI, interpretability), governance (regulation, standards), and long-term existential risk from advanced AI.", "Anthropic built Claude with Constitutional AI — training it to refuse harmful requests and explain its reasoning, making it more transparent and safer.", "Over $1 billion has been invested in AI safety research in the last 3 years!", "intermediate", 5),
        ("Fine-Tuning", "Taking a pre-trained AI model and teaching it to specialize in a specific domain or style.", "Adjusts pre-trained model weights on a smaller, domain-specific dataset. Much cheaper than training from scratch. LoRA fine-tuning adjusts only a small fraction of weights.", "Customer service chatbots are often GPT-4 fine-tuned on a company's support tickets, making them experts in that company's products and tone.", "Fine-tuning GPT-3 on just 100 medical examples made it outperform standard GPT-4 on medical questions!", "advanced", 5),
        ("RAG (Retrieval-Augmented Generation)", "Combining an AI with a search engine — first finding relevant information, then using it to generate accurate answers.", "Pipeline: query → embed → vector similarity search → retrieve relevant chunks → inject into context → LLM generates answer. Dramatically reduces hallucination.", "Perplexity AI uses RAG to search the internet in real-time and give you sourced, up-to-date answers instead of relying only on training data.", "RAG can reduce AI hallucinations by up to 70% on factual questions!", "intermediate", 5),
        ("Transformer Architecture", "The foundational AI architecture behind every major modern AI model — ChatGPT, Claude, Gemini, DALL-E.", "Uses self-attention to weigh the importance of different parts of input simultaneously, enabling parallel processing and capturing long-range dependencies.", "Every time you use an LLM, you're using a transformer. The architecture was published in 2017 in 'Attention Is All You Need' and revolutionized AI.", "The original transformer paper has over 100,000 citations — one of the most influential papers ever written!", "advanced", 6),
        ("AI Bias", "Systematic errors in AI decisions that unfairly discriminate against certain groups of people.", "Arises from biased training data, biased labels, or biased model architecture. Can perpetuate and amplify existing societal inequalities at algorithmic scale.", "Amazon's AI recruiting tool learned to penalize resumes that included the word 'women's' because historical hiring data reflected male-dominated tech hiring.", "AI facial recognition has error rates up to 35% higher for dark-skinned women than light-skinned men!", "beginner", 4),
        ("Foundation Model", "A large AI model trained on broad data that can be adapted to many different tasks.", "Pre-trained on massive datasets with self-supervised learning. Emergent capabilities allow zero-shot and few-shot generalization to tasks not seen in training.", "GPT-4 is a foundation model — it can write poetry, debug code, explain science, translate languages, and analyze images without being specifically trained for each.", "Foundation models represent a paradigm shift from task-specific AI to general-purpose AI capabilities!", "intermediate", 4),
        ("Reinforcement Learning from Human Feedback (RLHF)", "The technique used to make AI assistants helpful, harmless, and honest by learning from human preferences.", "Trains a reward model on human preference data, then uses RL to optimize the LLM to produce outputs that would receive high human ratings.", "ChatGPT was trained with RLHF — human raters scored thousands of AI responses, teaching the model what 'helpful and safe' actually means in practice.", "RLHF is why Claude apologizes when it makes mistakes and ChatGPT avoids harmful content!", "advanced", 6),
        ("Artificial General Intelligence (AGI)", "A hypothetical AI that can perform any intellectual task that a human can — with full understanding and adaptability.", "Currently theoretical. Would require common sense reasoning, causal understanding, transfer learning across all domains, and perhaps consciousness.", "We don't have AGI yet. Current AI is 'narrow AI' — superhuman at specific tasks but unable to generalize the way humans can. AGI may be years or decades away.", "OpenAI, DeepMind, and Anthropic all state their mission involves safely developing AGI. It's the Mount Everest of AI research!", "intermediate", 5),
        ("Diffusion Model", "The AI technology behind the most stunning image generators — DALL-E, Midjourney, and Stable Diffusion.", "Learns to reverse a noise-addition process. Training adds noise to images until they're random static; inference reverses this guided by text embeddings.", "When you type 'a cyberpunk cat reading a book in the rain, neon lights reflecting' into Midjourney, a diffusion model generates it from pure noise in seconds.", "Stable Diffusion can generate 512x512 images in under 1 second on a consumer GPU!", "intermediate", 5),
    ]

    for title, simple, tech, real, fun, diff, rt in ai_enthusiast_concepts:
        db.add(Concept(path_id="ai_enthusiast", title=title, simple_explanation=simple, technical_explanation=tech, real_world_example=real, fun_fact=fun, difficulty=diff, read_time=rt))

    db.commit()

    # ── Flashcard Decks ──
    decks = [
        FlashcardDeck(path_id="gaming", title="Game AI Basics", description="Core concepts of AI in gaming"),
        FlashcardDeck(path_id="gaming", title="AI Algorithms in Games", description="Pathfinding, behavior trees, and more"),
        FlashcardDeck(path_id="gaming", title="Famous AI in Games", description="Legendary AI moments in gaming history"),
        FlashcardDeck(path_id="business", title="AI Business Tools", description="Essential AI tools for business"),
        FlashcardDeck(path_id="business", title="AI Industry Terms", description="Key AI vocabulary for business"),
        FlashcardDeck(path_id="business", title="AI Business Cases", description="Real companies using AI successfully"),
        FlashcardDeck(path_id="developer", title="ML Algorithms", description="Core machine learning algorithms"),
        FlashcardDeck(path_id="developer", title="AI Frameworks", description="Popular AI development frameworks"),
        FlashcardDeck(path_id="developer", title="LLM Concepts", description="Large Language Model fundamentals"),
        FlashcardDeck(path_id="ai_enthusiast", title="AI Fundamentals", description="Core AI concepts every enthusiast must know"),
        FlashcardDeck(path_id="ai_enthusiast", title="AI Tools & Apps", description="The best AI tools and how to use them"),
        FlashcardDeck(path_id="ai_enthusiast", title="AI Ethics & Future", description="Safety, ethics, and where AI is headed"),
    ]
    db.add_all(decks)
    db.commit()

    print("Database seeded successfully!")
    print(f"  Students: {db.query(Student).count()}")
    print(f"  Topics: {db.query(Topic).count()}")
    print(f"  Badges: {db.query(Badge).count()}")
    print(f"  Concepts: {db.query(Concept).count()}")
    print(f"  Flashcard Decks: {db.query(FlashcardDeck).count()}")


if __name__ == "__main__":
    seed()
