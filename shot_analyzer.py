"""
Squash Shot & Movement Analyzer
Analyzes shot patterns, court positioning, and recommends optimal shots and movements
"""

from typing import List, Dict, Tuple
from enum import Enum
from dataclasses import dataclass
from collections import Counter
import math


class ShotType(Enum):
    """Types of squash shots"""
    STRAIGHT = "straight"  # Down-the-wall
    CROSS_COURT = "cross_court"  # Diagonal
    BOAST = "boast"  # Wall behind you
    DROP = "drop"  # Soft front court
    VOLLEY = "volley"  # Hit before bounce
    LOB = "lob"  # High defensive shot
    SERVE = "serve"
    UNKNOWN = "unknown"


class IntensityLevel(Enum):
    """Shot intensity levels"""
    SOFT = "soft"  # Drop, lob
    MEDIUM = "medium"  # Most rallies
    AGGRESSIVE = "aggressive"  # Drive, attacking


class CourtZone(Enum):
    """Court positioning zones"""
    BACK_LEFT = "back_left"
    BACK_CENTER = "back_center"
    BACK_RIGHT = "back_right"
    MID_LEFT = "mid_left"
    MID_CENTER = "mid_center"
    MID_RIGHT = "mid_right"
    FRONT_LEFT = "front_left"
    FRONT_CENTER = "front_center"
    FRONT_RIGHT = "front_right"
    T_POSITION = "t_position"  # Ideal center position


@dataclass
class Shot:
    """Represents a single shot"""
    shot_type: ShotType
    court_zone: CourtZone  # Where player was when hitting
    target_zone: CourtZone  # Where shot landed
    intensity: IntensityLevel
    success: bool  # Did it land in court?
    winner: bool = False  # Did opponent miss?
    unforced_error: bool = False
    rating: int = 5  # 1-10 quality


@dataclass
class Movement:
    """Represents player movement"""
    from_zone: CourtZone
    to_zone: CourtZone
    speed: str  # slow, medium, fast, explosive
    reaction_time: float  # seconds
    efficiency: float  # 0-1, how direct was the path


class ShotAnalyzer:
    """Analyzes shots and provides recommendations"""
    
    def __init__(self):
        self.shot_patterns = {}
        self.movement_patterns = {}
    
    def analyze_shot_history(self, shots: List[Dict]) -> Dict:
        """Analyze player's shot patterns"""
        if not shots:
            return self._empty_analysis()
        
        shot_objs = [self._dict_to_shot(s) for s in shots]
        
        return {
            'shot_distribution': self._analyze_shot_distribution(shot_objs),
            'success_rates': self._calculate_success_rates(shot_objs),
            'favorite_shots': self._get_favorite_shots(shot_objs),
            'weak_shots': self._get_weak_shots(shot_objs),
            'zone_preferences': self._analyze_zone_preferences(shot_objs),
            'aggressive_vs_defensive': self._analyze_aggression(shot_objs),
            'patterns': self._detect_patterns(shot_objs),
            'recommendations': self._generate_shot_recommendations(shot_objs)
        }
    
    def analyze_movement(self, movements: List[Dict]) -> Dict:
        """Analyze player's court movement"""
        if not movements:
            return self._empty_movement_analysis()
        
        move_objs = [self._dict_to_movement(m) for m in movements]
        
        return {
            'zones_coverage': self._analyze_zone_coverage(move_objs),
            'avg_reaction_time': self._avg_reaction_time(move_objs),
            'movement_efficiency': self._movement_efficiency(move_objs),
            'positioning': self._analyze_positioning(move_objs),
            'movement_weak_areas': self._detect_movement_weaknesses(move_objs),
            'recommendations': self._generate_movement_recommendations(move_objs)
        }
    
    def recommend_next_shot(self, current_zone: str, opponent_zone: str, 
                           level: str, recent_shots: List[Dict]) -> Dict:
        """Recommend best shot in current situation"""
        shot_analysis = self.analyze_shot_history(recent_shots)
        
        # Get zone objects
        current = self._zone_from_string(current_zone)
        opponent = self._zone_from_string(opponent_zone)
        
        recommendations = []
        
        # Recommendation logic based on position
        if self._is_back_court(current):
            recommendations.extend(self._back_court_shots(opponent, level))
        elif self._is_mid_court(current):
            recommendations.extend(self._mid_court_shots(opponent, level))
        else:  # Front court
            recommendations.extend(self._front_court_shots(opponent, level))
        
        # Factor in player's shot history
        for rec in recommendations:
            success_rate = shot_analysis['success_rates'].get(rec['shot'], 0.5)
            rec['confidence'] = success_rate
        
        # Sort by confidence/success rate
        recommendations.sort(key=lambda x: x['confidence'], reverse=True)
        
        return {
            'current_position': current_zone,
            'opponent_position': opponent_zone,
            'recommended_shots': recommendations[:3],  # Top 3
            'reasoning': self._build_reasoning(recommendations[0] if recommendations else None, level)
        }
    
    def recommend_movement(self, current_zone: str, shot_played: str, 
                          level: str, movement_history: List[Dict]) -> Dict:
        """Recommend optimal movement after playing a shot"""
        move_analysis = self.analyze_movement(movement_history)
        current = self._zone_from_string(current_zone)
        
        recommendations = []
        
        # After each shot type, recommend recovery movement
        if shot_played == 'straight':
            recommendations.append({
                'move_to': 'T_POSITION',
                'reason': 'Return to center court for balance',
                'priority': 'HIGH',
                'urgency': 'IMMEDIATE'
            })
        elif shot_played == 'cross_court':
            recommendations.append({
                'move_to': 'T_POSITION',
                'reason': 'Recover center after diagonal shot',
                'priority': 'HIGH',
                'urgency': 'IMMEDIATE'
            })
        elif shot_played == 'boast':
            recommendations.append({
                'move_to': 'MID_CENTER',
                'reason': 'Move forward from boast',
                'priority': 'HIGH',
                'urgency': 'IMMEDIATE'
            })
        elif shot_played == 'drop':
            recommendations.append({
                'move_to': 'MID_CENTER',
                'reason': 'Advance to net after drop',
                'priority': 'MEDIUM',
                'urgency': 'IMMEDIATE'
            })
        
        # Add position-specific tips
        recommendations.append({
            'move_to': 'Stay_ready',
            'reason': f'Small steps, stay balanced, watch opponent',
            'priority': 'MEDIUM',
            'urgency': 'ONGOING'
        })
        
        return {
            'current_position': current_zone,
            'after_shot': shot_played,
            'movements': recommendations,
            'efficiency_tips': self._movement_efficiency_tips(move_analysis, level)
        }
    
    # Helper methods
    
    def _back_court_shots(self, opponent_pos: CourtZone, level: str) -> List[Dict]:
        """Recommend shots from back court"""
        recommendations = [
            {'shot': 'straight', 'desc': 'Hit down wall', 'confidence': 0.7},
            {'shot': 'cross_court', 'desc': 'Diagonal to opposite corner', 'confidence': 0.6},
            {'shot': 'boast', 'desc': 'Defensive wall shot', 'confidence': 0.5},
            {'shot': 'lob', 'desc': 'High defensive shot', 'confidence': 0.4},
        ]
        
        # Advanced players can be more aggressive
        if level in ['advanced', 'professional']:
            recommendations.insert(0, {'shot': 'aggressive_drive', 'desc': 'Power shot down wall', 'confidence': 0.8})
        
        return recommendations
    
    def _mid_court_shots(self, opponent_pos: CourtZone, level: str) -> List[Dict]:
        """Recommend shots from mid court"""
        recommendations = [
            {'shot': 'straight', 'desc': 'Control down wall', 'confidence': 0.8},
            {'shot': 'cross_court', 'desc': 'Attacking diagonal', 'confidence': 0.7},
            {'shot': 'volley', 'desc': 'Cut off in air', 'confidence': 0.6},
            {'shot': 'drop', 'desc': 'Soft short shot', 'confidence': 0.5},
        ]
        
        if level in ['advanced', 'professional']:
            recommendations.insert(0, {'shot': 'attacking_volley', 'desc': 'Aggressive net shot', 'confidence': 0.85})
        
        return recommendations
    
    def _front_court_shots(self, opponent_pos: CourtZone, level: str) -> List[Dict]:
        """Recommend shots from front court"""
        recommendations = [
            {'shot': 'drop', 'desc': 'Finish at net', 'confidence': 0.8},
            {'shot': 'volley', 'desc': 'Quick finish volley', 'confidence': 0.75},
            {'shot': 'straight', 'desc': 'Kill shot down wall', 'confidence': 0.7},
            {'shot': 'lob', 'desc': 'Defensive lob if under pressure', 'confidence': 0.4},
        ]
        
        return recommendations
    
    def _analyze_shot_distribution(self, shots: List[Shot]) -> Dict:
        """What % of shots are each type"""
        if not shots:
            return {}
        
        shot_types = [s.shot_type.value for s in shots]
        counts = Counter(shot_types)
        total = len(shots)
        
        return {shot: (count/total)*100 for shot, count in counts.items()}
    
    def _calculate_success_rates(self, shots: List[Shot]) -> Dict:
        """Success rate per shot type"""
        by_type = {}
        
        for shot in shots:
            st = shot.shot_type.value
            if st not in by_type:
                by_type[st] = {'total': 0, 'successful': 0}
            
            by_type[st]['total'] += 1
            if shot.success:
                by_type[st]['successful'] += 1
        
        return {
            st: by_type[st]['successful'] / by_type[st]['total']
            for st in by_type
        }
    
    def _get_favorite_shots(self, shots: List[Shot]) -> List[str]:
        """Most used shots"""
        shot_types = [s.shot_type.value for s in shots]
        counts = Counter(shot_types)
        return [shot for shot, _ in counts.most_common(3)]
    
    def _get_weak_shots(self, shots: List[Shot]) -> Dict:
        """Shots with low success rates"""
        success_rates = self._calculate_success_rates(shots)
        return {
            shot: rate for shot, rate in success_rates.items()
            if rate < 0.6
        }
    
    def _analyze_zone_preferences(self, shots: List[Shot]) -> Dict:
        """Where player hits from"""
        zones = [s.court_zone.value for s in shots]
        counts = Counter(zones)
        total = len(shots)
        
        return {zone: (count/total)*100 for zone, count in counts.items()}
    
    def _analyze_aggression(self, shots: List[Shot]) -> Dict:
        """Aggressive vs defensive shots"""
        aggressive = sum(1 for s in shots if s.intensity == IntensityLevel.AGGRESSIVE)
        defensive = sum(1 for s in shots if s.intensity == IntensityLevel.SOFT)
        neutral = len(shots) - aggressive - defensive
        
        return {
            'aggressive_pct': (aggressive/len(shots))*100 if shots else 0,
            'defensive_pct': (defensive/len(shots))*100 if shots else 0,
            'neutral_pct': (neutral/len(shots))*100 if shots else 0,
            'recommendation': 'More aggressive' if aggressive < 40 else 'Good balance' if aggressive < 60 else 'Consider more defense'
        }
    
    def _detect_patterns(self, shots: List[Shot]) -> List[Dict]:
        """Detect patterns in play"""
        patterns = []
        
        # Check if player always hits same shot type
        shot_dist = self._analyze_shot_distribution(shots)
        for shot, pct in shot_dist.items():
            if pct > 50:
                patterns.append({
                    'pattern': f'Overuse of {shot}',
                    'severity': 'HIGH',
                    'tip': f'Mix it up! Vary your shots to keep opponent guessing.'
                })
        
        # Check zone preferences
        zones = self._analyze_zone_preferences(shots)
        if zones.get('back_center', 0) > 60:
            patterns.append({
                'pattern': 'Staying too far back',
                'severity': 'MEDIUM',
                'tip': 'Move forward more to attack. Take shots earlier.'
            })
        
        return patterns
    
    def _generate_shot_recommendations(self, shots: List[Shot]) -> List[str]:
        """Recommend shot improvements"""
        success_rates = self._calculate_success_rates(shots)
        recommendations = []
        
        for shot, rate in success_rates.items():
            if rate < 0.5:
                recommendations.append(f'Practice {shot} - only {int(rate*100)}% success rate')
        
        if not recommendations:
            recommendations.append('Great shot selection overall!')
        
        return recommendations
    
    def _analyze_zone_coverage(self, movements: List[Movement]) -> Dict:
        """Which zones does player cover"""
        zones = [m.to_zone.value for m in movements]
        counts = Counter(zones)
        total = len(movements) if movements else 1
        
        return {zone: (count/total)*100 for zone, count in counts.items()}
    
    def _avg_reaction_time(self, movements: List[Movement]) -> float:
        """Average reaction time"""
        if not movements:
            return 0
        return sum(m.reaction_time for m in movements) / len(movements)
    
    def _movement_efficiency(self, movements: List[Movement]) -> float:
        """How efficient are movements (0-1)"""
        if not movements:
            return 0.5
        return sum(m.efficiency for m in movements) / len(movements)
    
    def _analyze_positioning(self, movements: List[Movement]) -> Dict:
        """Check if player returns to T"""
        t_position_count = sum(1 for m in movements if m.to_zone == CourtZone.T_POSITION)
        
        return {
            't_position_recovery_pct': (t_position_count/len(movements))*100 if movements else 0,
            'suggestion': 'Good!' if t_position_count/len(movements) > 0.7 else 'Return to T more often'
        }
    
    def _detect_movement_weaknesses(self, movements: List[Movement]) -> List[str]:
        """Find movement patterns that need work"""
        weaknesses = []
        
        avg_reaction = self._avg_reaction_time(movements)
        if avg_reaction > 0.5:
            weaknesses.append('Slow reaction time - work on explosive movements')
        
        efficiency = self._movement_efficiency(movements)
        if efficiency < 0.7:
            weaknesses.append('Inefficient movement - take more direct paths')
        
        coverage = self._analyze_zone_coverage(movements)
        if coverage.get('back_left', 0) + coverage.get('back_right', 0) > 70:
            weaknesses.append('Too much back-court movement - move forward more')
        
        return weaknesses if weaknesses else ['Movement is solid!']
    
    def _generate_movement_recommendations(self, movements: List[Movement]) -> List[str]:
        """Recommend movement improvements"""
        recommendations = []
        
        reaction = self._avg_reaction_time(movements)
        if reaction > 0.3:
            recommendations.append('Drill explosive footwork - shadowboxing and ghosting')
        
        coverage = self._analyze_zone_coverage(movements)
        if coverage.get('mid_center', 0) < 30:
            recommendations.append('Practice returning to T-position after every shot')
        
        if not recommendations:
            recommendations.append('Excellent movement patterns!')
        
        return recommendations
    
    def _movement_efficiency_tips(self, analysis: Dict, level: str) -> List[str]:
        """Tips for efficient movement"""
        tips = []
        
        if level == 'beginner':
            tips.append('Always return to the T (center court) after each shot')
            tips.append('Small quick steps, not large strides')
            tips.append('Stay on the balls of your feet')
        elif level == 'intermediate':
            tips.append('Split step as opponent prepares to hit')
            tips.append('Move diagonally to save energy')
            tips.append('Anticipate opponent\'s next shot')
        elif level in ['advanced', 'professional']:
            tips.append('Read opponent\'s racket preparation early')
            tips.append('Move minimally - stay in control')
            tips.append('Use court angles to cut off opponent')
        
        return tips
    
    def _build_reasoning(self, recommendation: Dict, level: str) -> str:
        """Explain why this shot is recommended"""
        if not recommendation:
            return "Play your strongest shot"
        
        reasoning = f"Recommended: {recommendation.get('shot', 'N/A')} - {recommendation.get('desc', '')}"
        
        if recommendation.get('confidence', 0) > 0.8:
            reasoning += " (Very high success rate)"
        elif recommendation.get('confidence', 0) > 0.6:
            reasoning += " (Good option)"
        
        return reasoning
    
    def _is_back_court(self, zone: CourtZone) -> bool:
        """Is player in back court"""
        return 'back' in zone.value
    
    def _is_mid_court(self, zone: CourtZone) -> bool:
        """Is player in mid court"""
        return 'mid' in zone.value
    
    def _zone_from_string(self, zone_str: str) -> CourtZone:
        """Convert string to zone"""
        try:
            return CourtZone[zone_str.upper()]
        except:
            return CourtZone.MID_CENTER
    
    def _dict_to_shot(self, shot_dict: Dict) -> Shot:
        """Convert dict to Shot object"""
        return Shot(
            shot_type=ShotType(shot_dict.get('shot_type', 'unknown')),
            court_zone=CourtZone(shot_dict.get('court_zone', 'mid_center')),
            target_zone=CourtZone(shot_dict.get('target_zone', 'back_left')),
            intensity=IntensityLevel(shot_dict.get('intensity', 'medium')),
            success=shot_dict.get('success', True),
            winner=shot_dict.get('winner', False),
            unforced_error=shot_dict.get('unforced_error', False),
            rating=shot_dict.get('rating', 5)
        )
    
    def _dict_to_movement(self, move_dict: Dict) -> Movement:
        """Convert dict to Movement object"""
        return Movement(
            from_zone=CourtZone(move_dict.get('from_zone', 'mid_center')),
            to_zone=CourtZone(move_dict.get('to_zone', 'back_left')),
            speed=move_dict.get('speed', 'medium'),
            reaction_time=float(move_dict.get('reaction_time', 0.3)),
            efficiency=float(move_dict.get('efficiency', 0.7))
        )
    
    def _empty_analysis(self) -> Dict:
        """Return empty analysis"""
        return {
            'shot_distribution': {},
            'success_rates': {},
            'favorite_shots': [],
            'weak_shots': {},
            'zone_preferences': {},
            'aggressive_vs_defensive': {},
            'patterns': [],
            'recommendations': ['Start logging shots to get analysis']
        }
    
    def _empty_movement_analysis(self) -> Dict:
        """Return empty movement analysis"""
        return {
            'zones_coverage': {},
            'avg_reaction_time': 0,
            'movement_efficiency': 0,
            'positioning': {},
            'movement_weak_areas': [],
            'recommendations': ['Start logging movements to get analysis']
        }
