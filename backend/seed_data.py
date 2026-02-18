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
