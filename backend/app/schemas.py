from pydantic import BaseModel
from pydantic import EmailStr
from typing import List, Optional
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Profile schemas
class ProfileBase(BaseModel):
    first_name: str
    last_name: str
    age: Optional[int] = None
    city: Optional[str] = None
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    search_goals: Optional[str] = None

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(ProfileBase):
    pass

class Profile(ProfileBase):
    id: int
    user_id: int
    is_profile_complete: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Interest schemas
class InterestBase(BaseModel):
    name: str
    category: Optional[str] = None

class InterestCreate(InterestBase):
    pass

class InterestSchema(InterestBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Skill schemas
class SkillBase(BaseModel):
    name: str
    category: Optional[str] = None

class SkillCreate(SkillBase):
    pass

class SkillSchema(SkillBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Match schemas
class MatchBase(BaseModel):
    matched_user_id: int
    compatibility_score: float

class MatchCreate(MatchBase):
    pass

class Match(MatchBase):
    id: int
    user_id: int
    is_mutual: bool
    user_liked: bool
    matched_user_liked: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Recommendation schemas
class Recommendation(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    age: Optional[int]
    city: Optional[str]
    bio: Optional[str]
    profile_picture: Optional[str]
    compatibility_score: float
    common_interests: List[str]
    common_skills: List[str]

# Analytics schemas
class UserAnalytics(BaseModel):
    total_matches: int
    mutual_matches: int
    average_compatibility: float
    top_interests: List[str]
    top_skills: List[str]
    profile_completion_percentage: float

class PlatformAnalytics(BaseModel):
    total_users: int
    total_matches: int
    popular_interests: List[dict]
    popular_skills: List[dict]
    geographic_distribution: List[dict]

# Custom Interest/Skill schemas for unlimited entries
class CustomInterestCreate(BaseModel):
    name: str
    category: Optional[str] = None

class CustomSkillCreate(BaseModel):
    name: str
    category: Optional[str] = None

# User search schemas
class UserSearchRequest(BaseModel):
    query: str
    limit: int = 10

class UserSearchResult(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    age: Optional[int]
    city: Optional[str]
    bio: Optional[str]
    profile_picture: Optional[str]

# Chat schemas
class MessageCreate(BaseModel):
    recipient_id: int
    content: str

class Message(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    content: str
    created_at: datetime
    is_read: bool
    
    class Config:
        from_attributes = True

class Chat(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    last_message: Optional[str]
    last_message_time: Optional[datetime]
    unread_count: int
