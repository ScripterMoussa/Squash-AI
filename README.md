# 🎾 Squash AI - Smart Coaching, Completely Free

An intelligent squash coaching platform that provides personalized training plans, drills, and tips based on your age and skill level. **100% free, forever.**

## Features

✨ **AI-Powered Coaching**
- Personalized recommendations tailored to your age and play level
- Different coaching paths for: Beginner, Intermediate, Advanced, and Professional players
- Adaptive difficulty as you improve

📋 **Smart Drill Library**
- Categorized drills (footwork, shot technique, fitness, tactics)
- Drills adapted to your skill level
- Daily recommendations based on your profile

💡 **Coaching Tips**
- Real, actionable tips from squash experts
- Tailored to your current level and goals
- Mental game guidance included

📊 **Progress Tracking**
- Monitor your improvements over time
- Track consistency and skill development
- Visual progress indicators

🔐 **Easy Sign-Up**
- Sign up with Google, Apple, or Email
- No credit card required
- All features free forever

## Getting Started

### Quick Start (Client-Side Only)
1. Open `index.html` in your web browser
2. Click "Get Started" and sign up
3. Select your age and skill level
4. Data saves locally to your browser

### Full Setup with Python Backend (Recommended)

#### Prerequisites
- Python 3.8+
- Node.js (optional, for frontend tooling)

#### Installation

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Start the Flask server:**
```bash
python server.py
```

The server runs on `http://localhost:5000` and automatically creates a SQLite database.

3. **Serve the frontend:**

Option A - Python:
```bash
python -m http.server 8000
```

Option B - Node.js:
```bash
npx http-server
```

4. **Open in browser:** `http://localhost:8000`

#### What the Python Backend Adds

✅ **Persistent Data Storage**
- User accounts with secure password hashing
- Training sessions stored in SQLite database
- Data persists across sessions and devices

✅ **REST API Endpoints**
- `/api/signup` - User registration
- `/api/login` - User authentication
- `/api/users/<id>/sessions` - Log and retrieve training sessions
- `/api/users/<id>/stats` - Get progress statistics
- `/api/users/<id>/recommendations` - Smart AI recommendations

✅ **Smart Recommendation Engine**
- Analyzes your training history
- Detects performance trends (improving/declining/stable)
- Identifies weak areas and focuses drills accordingly
- Personalizes recommendations based on session data

✅ **Session Tracking**
- Stores all training sessions in database
- Calculates consistency streaks
- Tracks which drills you practice most
- Monitors improvement over time

## File Structure

```
squash_ai/
├── Frontend (HTML/CSS/JS)
│   ├── index.html           # Home page with features
│   ├── signup.html          # Sign up page
│   ├── login.html           # Sign in page
│   ├── profile-setup.html   # Age & level selection
│   ├── dashboard.html       # Main coaching dashboard
│   ├── progress.html        # Progress tracking & history
│   ├── styles.css           # All styling
│   └── app.js               # AI recommendation engine (client-side)
│
├── Backend (Python/Flask)
│   ├── server.py            # Flask REST API server
│   ├── recommendation_engine.py  # Smart recommendations
│   ├── api_client.py        # Python API client (for testing)
│   ├── requirements.txt      # Python dependencies
│   └── squash_ai.db         # SQLite database (auto-created)
│
└── README.md                # This file
```

## Python Backend Features

### Database Models
- **User** - Stores user profile (name, email, age, level, goal)
- **TrainingSession** - Logs each training session with drills, duration, intensity, rating

### API Endpoints
```
POST   /api/signup                    # Register new user
POST   /api/login                     # User login
POST   /api/auth/<provider>           # OAuth signup (google/apple)
GET    /api/user/<id>                 # Get user profile
PUT    /api/user/<id>                 # Update user profile
POST   /api/users/<id>/sessions       # Log a training session
GET    /api/users/<id>/sessions       # Get all sessions
GET    /api/users/<id>/stats          # Get progress stats
GET    /api/users/<id>/recommendations # Get AI recommendations
GET    /api/health                    # Health check
```

### Recommendation Engine Logic
The Python engine analyzes:
- **Trending** - Is user improving, declining, or stable?
- **Weak Areas** - Where do they need work based on ratings?
- **Drill History** - Which drills do they practice most/least?
- **Age & Level** - Personalize recommendations to their profile

Example: If a user is declining in ratings, the engine will suggest back-to-basics drills and tips.

## How It Works

### Age Groups
- **5-10 years**: Fun fundamentals, build love for the game
- **11-15 years**: Develop solid techniques and consistency
- **16-20 years**: Peak learning, competitive skills
- **21-30 years**: Reach your peak performance
- **31-40 years**: Competitive longevity, smart play
- **40+ years**: Experience-based advantages

### Skill Levels

**Beginner**
- Learning grip, footwork, basic shots
- Wall practice and shadow drills
- Focus on consistency

**Intermediate**
- Building court control and shot variety
- Tactical thinking
- Conditioning for longer rallies

**Advanced**
- Match tactics and strategy
- Advanced techniques (deception, volleys)
- Tournament preparation

**Professional**
- Elite-level conditioning and mental toughness
- Opponent analysis and game planning
- Data-driven training optimization

## Using the Python API Client

Test the backend with the provided Python client:

```bash
# Make sure Flask server is running first
python server.py

# In another terminal:
python api_client.py
```

This will demo: signup → update profile → log session → get stats → get recommendations

## Environment Variables

Create a `.env` file (optional):
```
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret
FLASK_ENV=development
```

## Customization

### Add More Drills (Python)
Edit `recommendation_engine.py`, update `get_level_recommendations()` function

### Customize Tips
Modify the `tips` arrays in `recommendation_engine.py`

### Change Colors
Edit CSS variables in `styles.css`:
```css
:root {
  --primary: #0066cc;      /* Main brand color */
  --secondary: #00a651;    /* Success/accent color */
  --dark: #1a1a1a;         /* Text color */
  --light: #f5f5f5;        /* Background color */
}
```

## Authentication (Python Backend)

Uses **JWT tokens** with Flask:
- Passwords hashed with Werkzeug
- JWT tokens valid for 30 days
- Secure token storage in `Authorization` header
- OAuth simulation for Google/Apple (implement real OAuth in production)

For production:
1. Implement real OAuth with Google/Apple SDKs
2. Use HTTPS/SSL
3. Add rate limiting
4. Use stronger SECRET_KEY and JWT_SECRET

## Technology Stack

**Frontend:**
- HTML5, CSS3, Vanilla JavaScript
- localStorage for session data (demo mode)
- Responsive design (mobile-friendly)

**Backend:**
- Python 3.8+
- Flask web framework
- SQLAlchemy ORM
- SQLite database
- JWT authentication
- CORS for cross-origin requests

**AI/ML:**
- Rule-based recommendation engine (Python)
- Session history analysis
- Trend detection (improving/declining/stable)
- Weak area identification

## Future Enhancements

- 📱 Mobile app (React Native / Flutter)
- 🎥 Video tutorials for each drill
- 📊 Advanced analytics with charts
- 🏆 Leaderboards and challenges
- 👥 Social coaching groups
- 💬 AI chat coach (GPT-based)
- 🎬 Form analysis with computer vision
- 🔔 Push notifications
- 📅 Auto-generated training schedules
- ⌚ Wearable integration (Apple Watch, Fitbit)
- 🤖 Machine learning for better personalization

## Free vs Premium (Future)

Currently **100% free**. Potential premium features:
- Video analysis with AI
- Professional coach consultations
- Advanced analytics dashboards
- Exclusive training programs

*Core coaching will always be free.*

## Support & Feedback

To improve the platform:
- Add custom drills for your training
- Extend the recommendation logic
- Integrate with real OAuth providers
- Add video tutorials
- Connect to wearable devices

## License

Free to use and modify. Built with ❤️ for squash lovers.

---

**Start your AI coaching journey today. It's free. It's smart. It's Squash AI.** 🎾
