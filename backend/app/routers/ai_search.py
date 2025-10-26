from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User, Profile, Interest, Skill
from app.schemas import UserSearchRequest, UserSearchResult
from app.auth import get_current_user
from app.ml_engine import CompatibilityEngine

router = APIRouter()
ml_engine = CompatibilityEngine()

@router.post("/ai-search", response_model=List[UserSearchResult])
async def ai_search_people(
    search_request: UserSearchRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    AI-powered search for people based on natural language queries
    """
    if not current_user.profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Complete your profile first to use AI search"
        )
    
    query = search_request.query.lower()
    limit = search_request.limit
    
    # Parse the query to extract search criteria
    search_criteria = parse_ai_query(query)
    
    # Get all users with profiles
    users_query = db.query(User).join(Profile).filter(
        User.id != current_user.id,
        Profile.is_profile_complete == True
    )
    
    # Apply filters based on parsed criteria
    if search_criteria.get('city'):
        users_query = users_query.filter(Profile.city.ilike(f"%{search_criteria['city']}%"))
    
    if search_criteria.get('min_age'):
        users_query = users_query.filter(Profile.age >= search_criteria['min_age'])
    
    if search_criteria.get('max_age'):
        users_query = users_query.filter(Profile.age <= search_criteria['max_age'])
    
    users = users_query.limit(limit * 2).all()  # Get more to filter by interests/skills
    
    results = []
    
    for user in users:
        if not user.profile:
            continue
        
        # Calculate AI relevance score
        relevance_score = calculate_ai_relevance(
            query, user.profile, search_criteria, current_user.profile
        )
        
        # Only include users with reasonable relevance
        if relevance_score > 0.1:
            result = UserSearchResult(
                user_id=user.id,
                first_name=user.profile.first_name,
                last_name=user.profile.last_name,
                age=user.profile.age,
                city=user.profile.city,
                bio=user.profile.bio,
                profile_picture=user.profile.profile_picture
            )
            results.append((result, relevance_score))
    
    # Sort by relevance score and return top results
    results.sort(key=lambda x: x[1], reverse=True)
    return [result[0] for result in results[:limit]]

def parse_ai_query(query: str) -> dict:
    """
    Parse natural language query to extract search criteria
    """
    criteria = {}
    
    # Extract city
    city_keywords = ['in', 'from', 'city', 'location']
    words = query.split()
    for i, word in enumerate(words):
        if word.lower() in city_keywords and i + 1 < len(words):
            criteria['city'] = words[i + 1].strip('.,!?')
            break
    
    # Extract age range
    age_keywords = ['age', 'years old', 'old']
    for i, word in enumerate(words):
        if word.lower() in age_keywords:
            # Look for numbers around this keyword
            for j in range(max(0, i-2), min(len(words), i+3)):
                if words[j].isdigit():
                    age = int(words[j])
                    if age < 18:
                        criteria['min_age'] = age
                    elif age > 65:
                        criteria['max_age'] = age
                    else:
                        criteria['min_age'] = age - 5
                        criteria['max_age'] = age + 5
                    break
    
    # Extract interests/skills from common keywords
    interest_keywords = {
        'music': ['music', 'musician', 'singer', 'guitar', 'piano'],
        'sports': ['sports', 'football', 'basketball', 'tennis', 'running'],
        'art': ['art', 'painting', 'drawing', 'design', 'creative'],
        'technology': ['tech', 'programming', 'coding', 'developer', 'software'],
        'business': ['business', 'entrepreneur', 'startup', 'marketing'],
        'education': ['teacher', 'student', 'education', 'learning'],
        'fitness': ['fitness', 'gym', 'workout', 'yoga', 'exercise']
    }
    
    detected_interests = []
    for interest, keywords in interest_keywords.items():
        if any(keyword in query.lower() for keyword in keywords):
            detected_interests.append(interest)
    
    if detected_interests:
        criteria['interests'] = detected_interests
    
    return criteria

def calculate_ai_relevance(query: str, profile: Profile, criteria: dict, current_profile: Profile) -> float:
    """
    Calculate relevance score for AI search results
    """
    score = 0.0
    
    # Bio relevance (40% weight)
    if profile.bio:
        bio_words = set(profile.bio.lower().split())
        query_words = set(query.lower().split())
        common_words = len(bio_words.intersection(query_words))
        if common_words > 0:
            score += min(0.4, common_words / len(query_words))
    
    # Interest matching (30% weight)
    if criteria.get('interests'):
        profile_interests = [interest.name.lower() for interest in profile.interests]
        for interest in criteria['interests']:
            if interest.lower() in profile_interests:
                score += 0.3 / len(criteria['interests'])
    
    # Skill matching (20% weight)
    if criteria.get('interests'):
        profile_skills = [skill.name.lower() for skill in profile.skills]
        for interest in criteria['interests']:
            if interest.lower() in profile_skills:
                score += 0.2 / len(criteria['interests'])
    
    # Location matching (10% weight)
    if criteria.get('city') and profile.city:
        if criteria['city'].lower() in profile.city.lower():
            score += 0.1
    
    return min(1.0, score)
