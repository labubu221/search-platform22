from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from typing import List
import os
import shutil
from app.database import get_db
from app.models import User, Profile, Interest, Skill
from app.schemas import (
    ProfileCreate, ProfileUpdate, Profile as ProfileSchema, 
    InterestCreate, SkillCreate, InterestSchema, SkillSchema,
    CustomInterestCreate, CustomSkillCreate, UserSearchResult
)
from app.auth import get_current_user

router = APIRouter()

@router.get("/profile", response_model=ProfileSchema)
async def get_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    from app.models import Profile as ProfileModel
    profile = db.query(ProfileModel).filter(ProfileModel.user_id == current_user.id).first()
    if not profile:
        # Return None so frontend can handle missing profile
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    return profile

@router.post("/profile", response_model=ProfileSchema)
async def create_profile(
    profile_data: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if profile already exists
    existing_profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already exists"
        )
    
    profile = Profile(
        user_id=current_user.id,
        **profile_data.dict()
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

@router.put("/profile", response_model=ProfileSchema)
async def update_profile(
    profile_data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    for field, value in profile_data.dict(exclude_unset=True).items():
        setattr(profile, field, value)
    
    db.commit()
    db.refresh(profile)
    return profile

@router.get("/interests", response_model=List[InterestSchema])
async def get_interests(db: Session = Depends(get_db)):
    interests = db.query(Interest).all()
    return [InterestSchema(id=i.id, name=i.name, category=i.category, created_at=i.created_at) for i in interests]

@router.post("/interests", response_model=InterestSchema)
async def create_interest(
    interest_data: InterestCreate,
    db: Session = Depends(get_db)
):
    interest = Interest(**interest_data.dict())
    db.add(interest)
    db.commit()
    db.refresh(interest)
    return InterestSchema(id=interest.id, name=interest.name, category=interest.category, created_at=interest.created_at)

@router.get("/skills", response_model=List[SkillSchema])
async def get_skills(db: Session = Depends(get_db)):
    skills = db.query(Skill).all()
    return [SkillSchema(id=s.id, name=s.name, category=s.category, created_at=s.created_at) for s in skills]

@router.post("/skills", response_model=SkillSchema)
async def create_skill(
    skill_data: SkillCreate,
    db: Session = Depends(get_db)
):
    skill = Skill(**skill_data.dict())
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return SkillSchema(id=skill.id, name=skill.name, category=skill.category, created_at=skill.created_at)

@router.post("/profile/interests/{interest_id}")
async def add_interest_to_profile(
    interest_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    interest = db.query(Interest).filter(Interest.id == interest_id).first()
    if not interest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interest not found"
        )
    
    if interest not in current_user.interests:
        current_user.interests.append(interest)
        db.commit()
    
    return {"message": "Interest added successfully"}

@router.post("/profile/skills/{skill_id}")
async def add_skill_to_profile(
    skill_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )
    
    if skill not in current_user.skills:
        current_user.skills.append(skill)
        db.commit()
    
    return {"message": "Skill added successfully"}

# Custom interests and skills endpoints
@router.post("/profile/custom-interest", response_model=InterestSchema)
async def add_custom_interest(
    interest_data: CustomInterestCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add a custom interest to the user's profile
    """
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    # Create or find the interest
    interest = db.query(Interest).filter(Interest.name == interest_data.name).first()
    if not interest:
        interest = Interest(
            name=interest_data.name,
            category=interest_data.category or "Custom"
        )
        db.add(interest)
        db.commit()
        db.refresh(interest)
    
    # Add to user's interests if not already added
    if interest not in current_user.interests:
        current_user.interests.append(interest)
        db.commit()
    
    return InterestSchema(id=interest.id, name=interest.name, category=interest.category, created_at=interest.created_at)

@router.post("/profile/custom-skill", response_model=SkillSchema)
async def add_custom_skill(
    skill_data: CustomSkillCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add a custom skill to the user's profile
    """
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    # Create or find the skill
    skill = db.query(Skill).filter(Skill.name == skill_data.name).first()
    if not skill:
        skill = Skill(
            name=skill_data.name,
            category=skill_data.category or "Custom"
        )
        db.add(skill)
        db.commit()
        db.refresh(skill)
    
    # Add to user's skills if not already added
    if skill not in current_user.skills:
        current_user.skills.append(skill)
        db.commit()
    
    return SkillSchema(id=skill.id, name=skill.name, category=skill.category, created_at=skill.created_at)

@router.delete("/profile/interests/{interest_id}")
async def remove_interest_from_profile(
    interest_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Remove an interest from the user's profile
    """
    interest = db.query(Interest).filter(Interest.id == interest_id).first()
    if not interest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interest not found"
        )
    
    if interest in current_user.interests:
        current_user.interests.remove(interest)
        db.commit()
    
    return {"message": "Interest removed successfully"}

@router.delete("/profile/skills/{skill_id}")
async def remove_skill_from_profile(
    skill_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Remove a skill from the user's profile
    """
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )
    
    if skill in current_user.skills:
        current_user.skills.remove(skill)
        db.commit()
    
    return {"message": "Skill removed successfully"}

# Avatar upload endpoint
@router.post("/profile/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload avatar image for user profile
    """
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    # Validate file type
    allowed_extensions = {'jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp', 'svg'}
    file_extension = file.filename.split(".")[-1].lower() if "." in file.filename else ""
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    # Create uploads directory if it doesn't exist
    upload_dir = "uploads/avatars"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    filename = f"user_{current_user.id}_avatar.{file_extension}"
    file_path = os.path.join(upload_dir, filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Update profile with avatar path
    profile.profile_picture = f"/uploads/avatars/{filename}"
    db.commit()
    
    return {"message": "Avatar uploaded successfully", "avatar_url": profile.profile_picture}

# User search endpoint
@router.get("/search", response_model=List[UserSearchResult])
async def search_users(
    query: str,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Search users by name
    """
    if not query or len(query.strip()) < 2:
        return []
    
    # Search in profiles by first name, last name, or full name
    search_term = f"%{query.strip()}%"
    
    users = db.query(User).join(Profile).filter(
        User.id != current_user.id,
        or_(
            Profile.first_name.ilike(search_term),
            Profile.last_name.ilike(search_term),
            func.concat(Profile.first_name, ' ', Profile.last_name).ilike(search_term)
        )
    ).limit(limit).all()
    
    results = []
    for user in users:
        if user.profile:
            results.append(UserSearchResult(
                user_id=user.id,
                first_name=user.profile.first_name,
                last_name=user.profile.last_name,
                age=user.profile.age,
                city=user.profile.city,
                bio=user.profile.bio,
                profile_picture=user.profile.profile_picture
            ))
    
    return results

# Get user profile by ID (for viewing other users' profiles)
@router.get("/profile/{user_id}", response_model=ProfileSchema)
async def get_user_profile(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get another user's profile by ID
    """
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )
    
    return profile

@router.get("/{user_id}")
async def get_user_with_details(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user with interests and skills
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {
        "id": user.id,
        "email": user.email,
        "interests": [{"id": i.id, "name": i.name, "category": i.category} for i in user.interests],
        "skills": [{"id": s.id, "name": s.name, "category": s.category} for s in user.skills]
    }
