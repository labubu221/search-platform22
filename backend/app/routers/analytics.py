from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.database import get_db
from app.models import User, Profile, Match, Interest, Skill
from app.schemas import UserAnalytics, PlatformAnalytics
from app.auth import get_current_user

router = APIRouter()

@router.get("/user", response_model=UserAnalytics)
async def get_user_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get analytics for the current user
    """
    if not current_user.profile:
        # Return default analytics for users without profiles
        return UserAnalytics(
            total_matches=0,
            mutual_matches=0,
            average_compatibility=0.0,
            top_interests=[],
            top_skills=[],
            profile_completion_percentage=0.0
        )
    
    # Total matches
    total_matches = db.query(Match).filter(Match.user_id == current_user.id).count()
    
    # Mutual matches
    mutual_matches = db.query(Match).filter(
        Match.user_id == current_user.id,
        Match.is_mutual == True
    ).count()
    
    # Average compatibility
    avg_compatibility = db.query(func.avg(Match.compatibility_score)).filter(
        Match.user_id == current_user.id
    ).scalar() or 0.0
    
    # Top interests
    top_interests = db.query(Interest.name, func.count(Interest.id)).join(
        Interest.users
    ).filter(User.id == current_user.id).group_by(
        Interest.name
    ).order_by(desc(func.count(Interest.id))).limit(5).all()
    
    top_interests_list = [interest[0] for interest in top_interests]
    
    # Top skills
    top_skills = db.query(Skill.name, func.count(Skill.id)).join(
        Skill.users
    ).filter(User.id == current_user.id).group_by(
        Skill.name
    ).order_by(desc(func.count(Skill.id))).limit(5).all()
    
    top_skills_list = [skill[0] for skill in top_skills]
    
    # Profile completion percentage
    profile = current_user.profile
    completion_fields = [
        profile.first_name, profile.last_name, profile.age,
        profile.city, profile.bio, profile.profile_picture
    ]
    completed_fields = sum(1 for field in completion_fields if field)
    completion_percentage = (completed_fields / len(completion_fields)) * 100
    
    return UserAnalytics(
        total_matches=total_matches,
        mutual_matches=mutual_matches,
        average_compatibility=float(avg_compatibility),
        top_interests=top_interests_list,
        top_skills=top_skills_list,
        profile_completion_percentage=completion_percentage
    )

@router.get("/platform", response_model=PlatformAnalytics)
async def get_platform_analytics(db: Session = Depends(get_db)):
    """
    Get platform-wide analytics
    """
    # Total users
    total_users = db.query(User).count()
    
    # Total matches
    total_matches = db.query(Match).count()
    
    # Popular interests
    popular_interests = db.query(
        Interest.name,
        Interest.category,
        func.count(Interest.id).label('count')
    ).join(Interest.users).group_by(
        Interest.name, Interest.category
    ).order_by(desc('count')).limit(10).all()
    
    popular_interests_list = [
        {"name": interest[0], "category": interest[1], "count": interest[2]}
        for interest in popular_interests
    ]
    
    # Popular skills
    popular_skills = db.query(
        Skill.name,
        Skill.category,
        func.count(Skill.id).label('count')
    ).join(Skill.users).group_by(
        Skill.name, Skill.category
    ).order_by(desc('count')).limit(10).all()
    
    popular_skills_list = [
        {"name": skill[0], "category": skill[1], "count": skill[2]}
        for skill in popular_skills
    ]
    
    # Geographic distribution
    geographic_distribution = db.query(
        Profile.city,
        func.count(Profile.id).label('count')
    ).filter(Profile.city.isnot(None)).group_by(
        Profile.city
    ).order_by(desc('count')).limit(20).all()
    
    geographic_list = [
        {"city": geo[0], "count": geo[1]}
        for geo in geographic_distribution
    ]
    
    return PlatformAnalytics(
        total_users=total_users,
        total_matches=total_matches,
        popular_interests=popular_interests_list,
        popular_skills=popular_skills_list,
        geographic_distribution=geographic_list
    )
