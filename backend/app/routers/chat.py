from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List
from app.database import get_db
from app.models import User, Message, Profile
from app.schemas import MessageCreate, Message as MessageSchema, Chat
from app.auth import get_current_user

router = APIRouter()

@router.post("/send", response_model=MessageSchema)
async def send_message(
    message_data: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Send a message to another user
    """
    # Check if recipient exists
    recipient = db.query(User).filter(User.id == message_data.recipient_id).first()
    if not recipient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipient not found"
        )
    
    # Check if users have matched (optional - you can remove this if you want to allow messaging without matching)
    # match = db.query(Match).filter(
    #     ((Match.user_id == current_user.id) & (Match.matched_user_id == message_data.recipient_id)) |
    #     ((Match.user_id == message_data.recipient_id) & (Match.matched_user_id == current_user.id)),
    #     Match.is_mutual == True
    # ).first()
    # 
    # if not match:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="You can only message users you have matched with"
    #     )
    
    message = Message(
        sender_id=current_user.id,
        recipient_id=message_data.recipient_id,
        content=message_data.content
    )
    
    db.add(message)
    db.commit()
    db.refresh(message)
    
    return message

@router.get("/conversations", response_model=List[Chat])
async def get_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all conversations for the current user
    """
    # Get all unique users the current user has messaged with
    conversations = db.query(
        User.id,
        User.email,
        Profile.first_name,
        Profile.last_name,
        func.max(Message.created_at).label('last_message_time'),
        func.count(Message.id).filter(Message.is_read == False).label('unread_count')
    ).join(Profile, User.id == Profile.user_id).join(
        Message, 
        ((Message.sender_id == current_user.id) & (Message.recipient_id == User.id)) |
        ((Message.recipient_id == current_user.id) & (Message.sender_id == User.id))
    ).filter(User.id != current_user.id).group_by(
        User.id, User.email, Profile.first_name, Profile.last_name
    ).order_by(desc('last_message_time')).all()
    
    result = []
    for conv in conversations:
        # Get the last message content
        last_message = db.query(Message.content).filter(
            ((Message.sender_id == current_user.id) & (Message.recipient_id == conv.id)) |
            ((Message.recipient_id == current_user.id) & (Message.sender_id == conv.id))
        ).order_by(desc(Message.created_at)).first()
        
        result.append(Chat(
            user_id=conv.id,
            first_name=conv.first_name or "Unknown",
            last_name=conv.last_name or "User",
            last_message=last_message[0] if last_message else None,
            last_message_time=conv.last_message_time,
            unread_count=conv.unread_count or 0
        ))
    
    return result

@router.get("/messages/{user_id}", response_model=List[MessageSchema])
async def get_messages(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get messages between current user and another user
    """
    messages = db.query(Message).filter(
        ((Message.sender_id == current_user.id) & (Message.recipient_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.recipient_id == current_user.id))
    ).order_by(Message.created_at).all()
    
    # Mark messages as read
    db.query(Message).filter(
        Message.recipient_id == current_user.id,
        Message.sender_id == user_id,
        Message.is_read == False
    ).update({"is_read": True})
    db.commit()
    
    return messages

@router.get("/unread-count")
async def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get total unread message count for current user
    """
    count = db.query(Message).filter(
        Message.recipient_id == current_user.id,
        Message.is_read == False
    ).count()
    
    return {"unread_count": count}
