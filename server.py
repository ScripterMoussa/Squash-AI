import os
import json
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

app = Flask(__name__)
CORS(app)

# Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "squash_ai.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['JWT_SECRET'] = os.environ.get('JWT_SECRET', 'jwt-secret-key-change-in-production')

db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255))
    age_range = db.Column(db.String(20))
    level = db.Column(db.String(20))
    goal = db.Column(db.String(50))
    provider = db.Column(db.String(20), default='email')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sessions = db.relationship('TrainingSession', backref='user', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'age_range': self.age_range,
            'level': self.level,
            'goal': self.goal,
            'provider': self.provider,
            'created_at': self.created_at.isoformat()
        }

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class TrainingSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    duration = db.Column(db.Integer)  # minutes
    intensity = db.Column(db.String(20))  # light, moderate, intense
    skill_rating = db.Column(db.Integer)  # 1-10
    drills_completed = db.Column(db.Text)  # JSON array
    notes = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date.isoformat(),
            'duration': self.duration,
            'intensity': self.intensity,
            'skill_rating': self.skill_rating,
            'drills_completed': json.loads(self.drills_completed) if self.drills_completed else [],
            'notes': self.notes
        }


class Shot(db.Model):
    """Represents a single shot played during practice/match"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('training_session.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    shot_type = db.Column(db.String(20))  # straight, cross_court, boast, drop, volley, lob, serve
    court_zone = db.Column(db.String(30))  # back_left, mid_center, front_right, etc.
    target_zone = db.Column(db.String(30))  # where ball landed
    intensity = db.Column(db.String(20))  # soft, medium, aggressive
    success = db.Column(db.Boolean, default=True)  # ball in court?
    winner = db.Column(db.Boolean, default=False)  # opponent missed?
    unforced_error = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Integer, default=5)  # 1-10 shot quality

    def to_dict(self):
        return {
            'id': self.id,
            'shot_type': self.shot_type,
            'court_zone': self.court_zone,
            'target_zone': self.target_zone,
            'intensity': self.intensity,
            'success': self.success,
            'winner': self.winner,
            'unforced_error': self.unforced_error,
            'rating': self.rating,
            'date': self.date.isoformat()
        }


class Movement(db.Model):
    """Represents player movement on court"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('training_session.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    from_zone = db.Column(db.String(30))  # where player moved from
    to_zone = db.Column(db.String(30))  # where player moved to
    speed = db.Column(db.String(20))  # slow, medium, fast, explosive
    reaction_time = db.Column(db.Float, default=0.3)  # seconds
    efficiency = db.Column(db.Float, default=0.7)  # 0-1 how direct

    def to_dict(self):
        return {
            'id': self.id,
            'from_zone': self.from_zone,
            'to_zone': self.to_zone,
            'speed': self.speed,
            'reaction_time': self.reaction_time,
            'efficiency': self.efficiency,
            'date': self.date.isoformat()
        }


# Auth Endpoints
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    user = User(
        name=data.get('name'),
        email=data.get('email'),
        provider=data.get('provider', 'email')
    )
    
    if data.get('password'):
        user.set_password(data.get('password'))
    
    db.session.add(user)
    db.session.commit()
    
    token = jwt.encode(
        {'user_id': user.id, 'exp': datetime.utcnow() + timedelta(days=30)},
        app.config['JWT_SECRET'],
        algorithm='HS256'
    )
    
    return jsonify({'user': user.to_dict(), 'token': token}), 201


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    
    if not user or not user.check_password(data.get('password')):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token = jwt.encode(
        {'user_id': user.id, 'exp': datetime.utcnow() + timedelta(days=30)},
        app.config['JWT_SECRET'],
        algorithm='HS256'
    )
    
    return jsonify({'user': user.to_dict(), 'token': token}), 200


@app.route('/api/auth/<provider>', methods=['POST'])
def oauth_signup(provider):
    """Simulate OAuth signup (Google, Apple)"""
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    
    if not user:
        user = User(
            name=data.get('name'),
            email=data.get('email'),
            provider=provider
        )
        db.session.add(user)
        db.session.commit()
    
    token = jwt.encode(
        {'user_id': user.id, 'exp': datetime.utcnow() + timedelta(days=30)},
        app.config['JWT_SECRET'],
        algorithm='HS256'
    )
    
    return jsonify({'user': user.to_dict(), 'token': token}), 200


# User Profile
@app.route('/api/user/<int:user_id>', methods=['GET', 'PUT'])
def get_update_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'PUT':
        data = request.get_json()
        user.age_range = data.get('age_range', user.age_range)
        user.level = data.get('level', user.level)
        user.goal = data.get('goal', user.goal)
        db.session.commit()
    
    return jsonify(user.to_dict()), 200


# Training Sessions
@app.route('/api/users/<int:user_id>/sessions', methods=['GET', 'POST'])
def user_sessions(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        data = request.get_json()
        session = TrainingSession(
            user_id=user_id,
            duration=data.get('duration'),
            intensity=data.get('intensity'),
            skill_rating=data.get('skill_rating'),
            drills_completed=json.dumps(data.get('drills_completed', [])),
            notes=data.get('notes')
        )
        db.session.add(session)
        db.session.commit()
        return jsonify(session.to_dict()), 201
    
    # GET - return all sessions
    sessions = TrainingSession.query.filter_by(user_id=user_id).order_by(TrainingSession.date.desc()).all()
    return jsonify([s.to_dict() for s in sessions]), 200


@app.route('/api/users/<int:user_id>/stats', methods=['GET'])
def user_stats(user_id):
    """Get progress stats for a user"""
    user = User.query.get_or_404(user_id)
    sessions = TrainingSession.query.filter_by(user_id=user_id).all()
    
    if not sessions:
        return jsonify({
            'total_sessions': 0,
            'total_minutes': 0,
            'avg_rating': 0,
            'consistency_streak': 0,
            'sessions_this_week': 0
        }), 200
    
    # Calculate stats
    total_minutes = sum(s.duration or 0 for s in sessions)
    avg_rating = sum(s.skill_rating or 5 for s in sessions) / len(sessions)
    
    # This week
    week_ago = datetime.utcnow() - timedelta(days=7)
    sessions_this_week = [s for s in sessions if s.date >= week_ago]
    
    # Consistency streak
    streak = calculate_consistency_streak(sessions)
    
    return jsonify({
        'total_sessions': len(sessions),
        'total_minutes': total_minutes,
        'avg_rating': round(avg_rating, 1),
        'consistency_streak': streak,
        'sessions_this_week': len(sessions_this_week),
        'total_minutes_this_week': sum(s.duration or 0 for s in sessions_this_week),
        'recent_sessions': [s.to_dict() for s in sessions[-5:]]
    }), 200


@app.route('/api/users/<int:user_id>/recommendations', methods=['GET'])
def get_recommendations(user_id):
    """Get personalized AI recommendations"""
    user = User.query.get_or_404(user_id)
    sessions = TrainingSession.query.filter_by(user_id=user_id).all()
    
    from recommendation_engine import generate_smart_recommendations
    recs = generate_smart_recommendations(user.level, user.age_range, sessions)
    
    return jsonify(recs), 200


# Helper functions
def calculate_consistency_streak(sessions):
    """Calculate consecutive days of training"""
    if not sessions:
        return 0
    
    sorted_sessions = sorted(sessions, key=lambda s: s.date.date(), reverse=True)
    today = datetime.utcnow().date()
    streak = 0
    current_date = today
    
    for session in sorted_sessions:
        session_date = session.date.date()
        if session_date == current_date or session_date == current_date - timedelta(days=streak):
            streak += 1
            current_date = session_date
        else:
            break
    
    return streak


# Shot & Movement Analysis Endpoints
@app.route('/api/users/<int:user_id>/shots', methods=['GET', 'POST'])
def user_shots(user_id):
    """Log and retrieve shots"""
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        data = request.get_json()
        shot = Shot(
            user_id=user_id,
            session_id=data.get('session_id'),
            shot_type=data.get('shot_type'),
            court_zone=data.get('court_zone'),
            target_zone=data.get('target_zone'),
            intensity=data.get('intensity'),
            success=data.get('success', True),
            winner=data.get('winner', False),
            unforced_error=data.get('unforced_error', False),
            rating=data.get('rating', 5)
        )
        db.session.add(shot)
        db.session.commit()
        return jsonify(shot.to_dict()), 201
    
    # GET - return shots
    shots = Shot.query.filter_by(user_id=user_id).order_by(Shot.date.desc()).all()
    return jsonify([s.to_dict() for s in shots]), 200


@app.route('/api/users/<int:user_id>/movements', methods=['GET', 'POST'])
def user_movements(user_id):
    """Log and retrieve movements"""
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        data = request.get_json()
        move = Movement(
            user_id=user_id,
            session_id=data.get('session_id'),
            from_zone=data.get('from_zone'),
            to_zone=data.get('to_zone'),
            speed=data.get('speed', 'medium'),
            reaction_time=data.get('reaction_time', 0.3),
            efficiency=data.get('efficiency', 0.7)
        )
        db.session.add(move)
        db.session.commit()
        return jsonify(move.to_dict()), 201
    
    # GET - return movements
    movements = Movement.query.filter_by(user_id=user_id).order_by(Movement.date.desc()).all()
    return jsonify([m.to_dict() for m in movements]), 200


@app.route('/api/users/<int:user_id>/shot-analysis', methods=['GET'])
def get_shot_analysis(user_id):
    """Get analysis of player's shots"""
    user = User.query.get_or_404(user_id)
    shots = Shot.query.filter_by(user_id=user_id).all()
    
    from shot_analyzer import ShotAnalyzer
    analyzer = ShotAnalyzer()
    shot_dicts = [s.to_dict() for s in shots]
    analysis = analyzer.analyze_shot_history(shot_dicts)
    
    return jsonify(analysis), 200


@app.route('/api/users/<int:user_id>/movement-analysis', methods=['GET'])
def get_movement_analysis(user_id):
    """Get analysis of player's movement"""
    user = User.query.get_or_404(user_id)
    movements = Movement.query.filter_by(user_id=user_id).all()
    
    from shot_analyzer import ShotAnalyzer
    analyzer = ShotAnalyzer()
    move_dicts = [m.to_dict() for m in movements]
    analysis = analyzer.analyze_movement(move_dicts)
    
    return jsonify(analysis), 200


@app.route('/api/users/<int:user_id>/shot-recommendation', methods=['POST'])
def get_shot_recommendation(user_id):
    """Get recommended shot for current situation"""
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    shots = Shot.query.filter_by(user_id=user_id).all()
    shot_dicts = [s.to_dict() for s in shots[-50:]]  # Last 50 shots
    
    from shot_analyzer import ShotAnalyzer
    analyzer = ShotAnalyzer()
    recommendation = analyzer.recommend_next_shot(
        data.get('current_zone'),
        data.get('opponent_zone'),
        user.level,
        shot_dicts
    )
    
    return jsonify(recommendation), 200


@app.route('/api/users/<int:user_id>/movement-recommendation', methods=['POST'])
def get_movement_recommendation(user_id):
    """Get recommended movement after a shot"""
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    movements = Movement.query.filter_by(user_id=user_id).all()
    move_dicts = [m.to_dict() for m in movements[-50:]]  # Last 50 movements
    
    from shot_analyzer import ShotAnalyzer
    analyzer = ShotAnalyzer()
    recommendation = analyzer.recommend_movement(
        data.get('current_zone'),
        data.get('shot_played'),
        user.level,
        move_dicts
    )
    
    return jsonify(recommendation), 200


# Health check
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
