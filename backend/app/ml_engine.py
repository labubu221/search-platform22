import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session
from typing import List, Tuple
from app.models import User, Profile, Interest, Skill, Match
from app.schemas import Recommendation

class CompatibilityEngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
    
    def calculate_compatibility(self, user1: Profile, user2: Profile) -> float:
        """
        Calculate compatibility score between two users based on:
        - Common interests (40% weight)
        - Common skills (30% weight)
        - Age compatibility (10% weight)
        - Location proximity (10% weight)
        - Bio similarity (10% weight)
        """
        score = 0.0
        
        # Common interests (40% weight)
        user1_interests = set([interest.name.lower() for interest in user1.interests])
        user2_interests = set([interest.name.lower() for interest in user2.interests])
        if user1_interests or user2_interests:
            common_interests = len(user1_interests.intersection(user2_interests))
            total_interests = len(user1_interests.union(user2_interests))
            interest_score = common_interests / total_interests if total_interests > 0 else 0
            score += interest_score * 0.4
        
        # Common skills (30% weight)
        user1_skills = set([skill.name.lower() for skill in user1.skills])
        user2_skills = set([skill.name.lower() for skill in user2.skills])
        if user1_skills or user2_skills:
            common_skills = len(user1_skills.intersection(user2_skills))
            total_skills = len(user1_skills.union(user2_skills))
            skill_score = common_skills / total_skills if total_skills > 0 else 0
            score += skill_score * 0.3
        
        # Age compatibility (10% weight)
        if user1.age and user2.age:
            age_diff = abs(user1.age - user2.age)
            age_score = max(0, 1 - (age_diff / 20))  # Penalty for age difference > 20 years
            score += age_score * 0.1
        
        # Location proximity (10% weight)
        if user1.city and user2.city:
            location_score = 1.0 if user1.city.lower() == user2.city.lower() else 0.5
            score += location_score * 0.1
        
        # Bio similarity (10% weight)
        if user1.bio and user2.bio:
            try:
                bios = [user1.bio, user2.bio]
                tfidf_matrix = self.vectorizer.fit_transform(bios)
                bio_similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
                score += bio_similarity * 0.1
            except:
                pass  # Skip bio similarity if vectorization fails
        
        return min(1.0, score)  # Cap at 1.0
    
    def get_recommendations(self, user_id: int, db: Session, limit: int = 10) -> List[Recommendation]:
        """
        Get personalized recommendations for a user
        """
        current_user = db.query(User).filter(User.id == user_id).first()
        if not current_user or not current_user.profile:
            return []
        
        current_profile = current_user.profile
        
        # Get all other users with profiles
        other_users = db.query(User).join(Profile).filter(
            User.id != user_id,
            Profile.is_profile_complete == True
        ).all()
        
        recommendations = []
        
        for user in other_users:
            if not user.profile:
                continue
            
            # Calculate compatibility score
            compatibility_score = self.calculate_compatibility(current_profile, user.profile)
            
            # Get common interests and skills
            current_interests = set([interest.name for interest in current_profile.interests])
            other_interests = set([interest.name for interest in user.profile.interests])
            common_interests = list(current_interests.intersection(other_interests))
            
            current_skills = set([skill.name for skill in current_profile.skills])
            other_skills = set([skill.name for skill in user.profile.skills])
            common_skills = list(current_skills.intersection(other_skills))
            
            recommendation = Recommendation(
                user_id=user.id,
                first_name=user.profile.first_name,
                last_name=user.profile.last_name,
                age=user.profile.age,
                city=user.profile.city,
                bio=user.profile.bio,
                profile_picture=user.profile.profile_picture,
                compatibility_score=compatibility_score,
                common_interests=common_interests,
                common_skills=common_skills
            )
            
            recommendations.append(recommendation)
        
        # Sort by compatibility score and return top recommendations
        recommendations.sort(key=lambda x: x.compatibility_score, reverse=True)
        return recommendations[:limit]
    
    def create_match(self, user_id: int, matched_user_id: int, db: Session) -> Match:
        """
        Create a match record between two users
        """
        # Check if match already exists
        existing_match = db.query(Match).filter(
            Match.user_id == user_id,
            Match.matched_user_id == matched_user_id
        ).first()
        
        if existing_match:
            return existing_match
        
        # Get user profiles for compatibility calculation
        user1 = db.query(User).filter(User.id == user_id).first()
        user2 = db.query(User).filter(User.id == matched_user_id).first()
        
        if not user1 or not user2 or not user1.profile or not user2.profile:
            raise ValueError("User profiles not found")
        
        compatibility_score = self.calculate_compatibility(user1.profile, user2.profile)
        
        match = Match(
            user_id=user_id,
            matched_user_id=matched_user_id,
            compatibility_score=compatibility_score
        )
        
        db.add(match)
        db.commit()
        db.refresh(match)
        
        return match
