from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User, Profile
from app.schemas import Recommendation
from app.auth import get_current_user
from app.ml_engine import CompatibilityEngine

router = APIRouter()
ml_engine = CompatibilityEngine()

@router.get("/", response_model=List[Recommendation])
async def get_recommendations(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get personalized recommendations for the current user
    """
    if not current_user.profile:
        # Return empty list if no profile exists
        return []
    
    recommendations = ml_engine.get_recommendations(current_user.id, db, limit)
    return recommendations

@router.get("/search")
async def search_users(
    city: str = None,
    min_age: int = None,
    max_age: int = None,
    interests: str = None,  # Comma-separated list
    skills: str = None,     # Comma-separated list
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Advanced search with filters
    """
    if not current_user.profile:
        # Return empty list if no profile exists
        return []
    
    # Start with all users except current user
    query = db.query(User).join(Profile).filter(User.id != current_user.id)
    
    # Apply filters
    if city:
        query = query.filter(Profile.city.ilike(f'%{city}%'))
    
    if min_age:
        query = query.filter(Profile.age >= min_age)
    
    if max_age:
        query = query.filter(Profile.age <= max_age)
    
    # Get filtered users
    filtered_users = query.all()
    
    # Get recommendations for filtered users
    recommendations = []
    for user in filtered_users:
        if not user.profile:
            continue
        
        # Calculate compatibility
        compatibility_score = ml_engine.calculate_compatibility(
            current_user.profile, user.profile
        )
        
        # Get common interests and skills
        current_interests = set([interest.name for interest in current_user.profile.interests])
        other_interests = set([interest.name for interest in user.profile.interests])
        common_interests = list(current_interests.intersection(other_interests))
        
        current_skills = set([skill.name for skill in current_user.profile.skills])
        other_skills = set([skill.name for skill in user.profile.skills])
        common_skills = list(current_skills.intersection(other_skills))
        
        # Apply interest filter if specified
        if interests:
            interest_list = [i.strip().lower() for i in interests.split(',')]
            user_interests = [i.name.lower() for i in user.interests]
            # Check if user has any of the requested interests
            if not any(interest in user_interests for interest in interest_list):
                continue
        
        # Apply skill filter if specified
        if skills:
            skill_list = [s.strip().lower() for s in skills.split(',')]
            user_skills = [s.name.lower() for s in user.skills]
            # Check if user has any of the requested skills
            if not any(skill in user_skills for skill in skill_list):
                continue
        
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
    
    # Sort by compatibility score
    recommendations.sort(key=lambda x: x.compatibility_score, reverse=True)
    return recommendations[:limit]
