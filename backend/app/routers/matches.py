from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User, Match
from app.schemas import Match as MatchSchema
from app.auth import get_current_user
from app.ml_engine import CompatibilityEngine

router = APIRouter()
ml_engine = CompatibilityEngine()

@router.post("/like/{matched_user_id}")
async def like_user(
    matched_user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Like a user (swipe right)
    """
    if current_user.id == matched_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot like yourself"
        )
    
    # Check if match already exists
    existing_match = db.query(Match).filter(
        Match.user_id == current_user.id,
        Match.matched_user_id == matched_user_id
    ).first()
    
    if existing_match:
        if existing_match.user_liked:
            # User already liked, just return success
            return {"message": "User already liked", "already_liked": True}
        existing_match.user_liked = True
        current_match = existing_match
    else:
        # Create new match
        current_match = ml_engine.create_match(current_user.id, matched_user_id, db)
        current_match.user_liked = True
        db.add(current_match)
        db.flush()  # Flush to get the match in the session
    
    # Check for mutual like
    reverse_match = db.query(Match).filter(
        Match.user_id == matched_user_id,
        Match.matched_user_id == current_user.id
    ).first()
    
    if reverse_match and reverse_match.user_liked:
        # Mutual match!
        current_match.is_mutual = True
        reverse_match.is_mutual = True
        reverse_match.matched_user_liked = True
    
    db.commit()
    
    return {"message": "User liked successfully"}

@router.post("/dislike/{matched_user_id}")
async def dislike_user(
    matched_user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Dislike a user (swipe left)
    """
    if current_user.id == matched_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot dislike yourself"
        )
    
    # Create or update match record
    existing_match = db.query(Match).filter(
        Match.user_id == current_user.id,
        Match.matched_user_id == matched_user_id
    ).first()
    
    if existing_match:
        existing_match.user_liked = False
    else:
        # Create new match with dislike
        match = ml_engine.create_match(current_user.id, matched_user_id, db)
        match.user_liked = False
    
    db.commit()
    
    return {"message": "User disliked"}

@router.get("/", response_model=List[MatchSchema])
async def get_matches(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all matches for the current user
    """
    matches = db.query(Match).filter(Match.user_id == current_user.id).all()
    return matches

@router.get("/mutual", response_model=List[MatchSchema])
async def get_mutual_matches(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get mutual matches for the current user
    """
    matches = db.query(Match).filter(
        Match.user_id == current_user.id,
        Match.is_mutual == True
    ).all()
    return matches
