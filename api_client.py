"""
Squash AI API Client
Used by JavaScript frontend to communicate with Python backend
"""

import json
from typing import Optional, Dict, List


class SquashAIClient:
    """API client for Squash AI backend"""
    
    def __init__(self, base_url: str = "http://localhost:5000", token: Optional[str] = None):
        self.base_url = base_url
        self.token = token
    
    def _get_headers(self):
        """Get request headers with auth token"""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    def signup(self, name: str, email: str, password: str, provider: str = "email") -> Dict:
        """Sign up a new user"""
        import requests
        response = requests.post(
            f"{self.base_url}/api/signup",
            json={"name": name, "email": email, "password": password, "provider": provider},
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def login(self, email: str, password: str) -> Dict:
        """Log in user"""
        import requests
        response = requests.post(
            f"{self.base_url}/api/login",
            json={"email": email, "password": password},
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def oauth_signup(self, provider: str, name: str, email: str) -> Dict:
        """Sign up via OAuth (Google, Apple)"""
        import requests
        response = requests.post(
            f"{self.base_url}/api/auth/{provider}",
            json={"name": name, "email": email},
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def update_profile(self, user_id: int, age_range: str, level: str, goal: str) -> Dict:
        """Update user profile"""
        import requests
        response = requests.put(
            f"{self.base_url}/api/user/{user_id}",
            json={"age_range": age_range, "level": level, "goal": goal},
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def log_session(self, user_id: int, duration: int, intensity: str, 
                    skill_rating: int, drills_completed: List[str], notes: str = "") -> Dict:
        """Log a training session"""
        import requests
        response = requests.post(
            f"{self.base_url}/api/users/{user_id}/sessions",
            json={
                "duration": duration,
                "intensity": intensity,
                "skill_rating": skill_rating,
                "drills_completed": drills_completed,
                "notes": notes
            },
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def get_sessions(self, user_id: int) -> List[Dict]:
        """Get all sessions for a user"""
        import requests
        response = requests.get(
            f"{self.base_url}/api/users/{user_id}/sessions",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def get_stats(self, user_id: int) -> Dict:
        """Get user statistics"""
        import requests
        response = requests.get(
            f"{self.base_url}/api/users/{user_id}/stats",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def get_recommendations(self, user_id: int) -> Dict:
        """Get AI recommendations"""
        import requests
        response = requests.get(
            f"{self.base_url}/api/users/{user_id}/recommendations",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()


# CLI Demo
if __name__ == "__main__":
    client = SquashAIClient()
    
    # Example: Sign up
    try:
        result = client.signup("John Squash", "john@example.com", "password123")
        print("Signup successful:", json.dumps(result, indent=2))
        user_id = result['user']['id']
        token = result['token']
        
        # Update profile
        client.token = token
        profile = client.update_profile(user_id, "21-30", "intermediate", "improve")
        print("\nProfile updated:", json.dumps(profile, indent=2))
        
        # Log a session
        session = client.log_session(
            user_id,
            duration=45,
            intensity="moderate",
            skill_rating=7,
            drills_completed=["Wall Warm-up", "Court Movement"],
            notes="Good practice session"
        )
        print("\nSession logged:", json.dumps(session, indent=2))
        
        # Get stats
        stats = client.get_stats(user_id)
        print("\nStats:", json.dumps(stats, indent=2))
        
        # Get recommendations
        recs = client.get_recommendations(user_id)
        print("\nRecommendations:", json.dumps(recs, indent=2))
        
    except Exception as e:
        print(f"Error: {e}")
