"""
AI Recommendation Engine - Python Version
Generates smart, personalized recommendations based on user level, age, and history
"""

from collections import Counter
from datetime import datetime, timedelta


def generate_smart_recommendations(level, age_range, sessions):
    """
    Generate personalized recommendations based on:
    - User's skill level (beginner, intermediate, advanced, professional)
    - Age group
    - Historical session data (what drills work best, where they struggle)
    """
    
    # Analyze session history
    analysis = analyze_sessions(sessions, level)
    
    # Get base recommendations by level
    base_recs = get_level_recommendations(level)
    
    # Personalize based on history
    personalized = personalize_recommendations(base_recs, analysis, level, age_range)
    
    return personalized


def analyze_sessions(sessions, level):
    """Analyze historical sessions to find patterns"""
    if not sessions:
        return {
            'avg_rating': 5,
            'most_common_intensity': 'moderate',
            'completed_drills': {},
            'weak_areas': [],
            'trending': 'stable'
        }
    
    # Calculate metrics
    ratings = [s.skill_rating for s in sessions if s.skill_rating]
    intensities = [s.intensity for s in sessions if s.intensity]
    
    avg_rating = sum(ratings) / len(ratings) if ratings else 5
    
    # Trending (improving, declining, stable)
    if len(ratings) >= 3:
        recent_avg = sum(ratings[-3:]) / 3
        older_avg = sum(ratings[:-3]) / len(ratings[:-3]) if len(ratings) > 3 else 5
        if recent_avg > older_avg + 0.5:
            trending = 'improving'
        elif recent_avg < older_avg - 0.5:
            trending = 'declining'
        else:
            trending = 'stable'
    else:
        trending = 'stable'
    
    # Most common intensity
    most_common_intensity = Counter(intensities).most_common(1)[0][0] if intensities else 'moderate'
    
    # Drill frequency
    drills = {}
    for session in sessions:
        if session.drills_completed:
            import json
            try:
                completed = json.loads(session.drills_completed) if isinstance(session.drills_completed, str) else session.drills_completed
                for drill in completed:
                    drills[drill] = drills.get(drill, 0) + 1
            except:
                pass
    
    return {
        'avg_rating': round(avg_rating, 1),
        'most_common_intensity': most_common_intensity,
        'completed_drills': drills,
        'weak_areas': get_weak_areas(avg_rating, level),
        'trending': trending,
        'total_sessions': len(sessions)
    }


def get_weak_areas(avg_rating, level):
    """Determine what areas need work based on rating"""
    if avg_rating >= 8:
        return []  # Performing well
    elif avg_rating >= 6:
        return ['Consistency', 'Advanced Techniques']
    elif avg_rating >= 4:
        return ['Footwork', 'Court Control', 'Consistency']
    else:
        return ['Fundamentals', 'Grip', 'Footwork', 'Serve']


def get_level_recommendations(level):
    """Get base drill recommendations by level"""
    
    recommendations = {
        'beginner': {
            'todaysDrills': [
                {'name': 'Wall Warm-up', 'description': 'Hit ball against wall for 5 min, focus on grip'},
                {'name': 'Shadow Practice', 'description': '10 min shadow swings, focus on footwork'},
                {'name': 'Short Rally Drill', 'description': 'Rally with partner in front court only'}
            ],
            'tips': [
                {'category': 'Grip', 'message': 'Use a firm but relaxed grip. Thumb under the handle for control.'},
                {'category': 'Footwork', 'message': 'Small steps between shots. Always return to the T position.'},
                {'category': 'Serve', 'message': 'Focus on consistency over power. Aim for center court.'}
            ]
        },
        'intermediate': {
            'todaysDrills': [
                {'name': 'Boast & Drive', 'description': '10 min alternating boasts and drives from mid-court'},
                {'name': 'Rally Conditioning', 'description': '5 rallies focusing on court control'},
                {'name': 'Volley Practice', 'description': 'Front court volley exchanges with partner'}
            ],
            'tips': [
                {'category': 'Court Control', 'message': 'Push opponent to back, move forward to attack.'},
                {'category': 'Shot Selection', 'message': 'Mix up pace and angles to keep opponent guessing.'},
                {'category': 'Fitness', 'message': 'Work on explosive movements. Conditioning is key at this level.'}
            ]
        },
        'advanced': {
            'todaysDrills': [
                {'name': 'Advanced Court Movement', 'description': 'Game-pace footwork across all court areas'},
                {'name': 'Aggressive Rally Drill', 'description': '10 min intense rallies, focus on attacking'},
                {'name': 'Serve & Pressure', 'description': 'Aggressive serves followed by net domination'}
            ],
            'tips': [
                {'category': 'Tactics', 'message': 'Use serve placement to set up your attacking shots.'},
                {'category': 'Mental Game', 'message': 'Stay focused on your game plan. Adapt mid-match.'},
                {'category': 'Technique', 'message': 'Refine your timing on power shots. Consistency under pressure.'}
            ]
        },
        'professional': {
            'todaysDrills': [
                {'name': 'Pro-Level Conditioning', 'description': 'Game-intensity intervals, 45 min sessions'},
                {'name': 'Tactical Match Play', 'description': 'Head-to-head competitive matches'},
                {'name': 'Tournament Simulation', 'description': 'Best-of-5 or best-of-3 sets'}
            ],
            'tips': [
                {'category': 'Tournament Prep', 'message': 'Scout opponents. Develop detailed game plans.'},
                {'category': 'Physical Peak', 'message': 'Monitor recovery. Avoid overtraining before big events.'},
                {'category': 'Elite Mindset', 'message': 'Visualize success. Build mental resilience for high pressure.'}
            ]
        }
    }
    
    return recommendations.get(level, recommendations['beginner'])


def personalize_recommendations(base_recs, analysis, level, age_range):
    """
    Personalize recommendations based on:
    - User's performance trend
    - Weak areas
    - Drill history
    """
    
    personalized = base_recs.copy()
    
    # Adjust difficulty based on trending
    if analysis['trending'] == 'improving':
        # User improving - slightly increase difficulty
        pass  # Keep base recommendations
    elif analysis['trending'] == 'declining':
        # User declining - focus on fundamentals
        if level == 'intermediate' or level == 'advanced':
            personalized['tips'].insert(0, {
                'category': 'Focus',
                'message': 'Your ratings have been declining. Let\'s focus on fundamentals and rebuild consistency.'
            })
    
    # Add tips based on weak areas
    if analysis['weak_areas']:
        weak_tip = {
            'category': 'Focus Area',
            'message': f'Work on: {", ".join(analysis["weak_areas"])}. These will unlock better performance.'
        }
        personalized['tips'].append(weak_tip)
    
    # Recommend most-needed drill
    if analysis['completed_drills']:
        least_practiced = min(analysis['completed_drills'], key=analysis['completed_drills'].get)
        personalized['tips'].append({
            'category': 'Suggestion',
            'message': f'You haven\'t practiced {least_practiced} much. Try it today!'
        })
    
    # Add age-based tip
    age_tips = {
        '5-10': 'Great job starting young! Focus on having fun and building love for the game.',
        '11-15': 'You\'re at the perfect age to develop solid fundamentals. Consistency is key!',
        '16-20': 'Peak learning years! Now\'s the time to build advanced skills and competitive drive.',
        '21-30': 'Great time to reach your peak. Combine experience with modern techniques.',
        '31-40': 'Stay competitive! Your experience beats younger players\' physical advantages.',
        '40+': 'Age is just a number. Smart play and consistency win matches!'
    }
    
    personalized['welcomeMessage'] = age_tips.get(age_range, 'Let\'s improve your squash game!')
    personalized['analysis'] = analysis
    
    return personalized
