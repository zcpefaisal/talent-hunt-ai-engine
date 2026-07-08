from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Profile Schema for UserProfile
class UserProfileBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    alternate_email: Optional[EmailStr] = None
    phone: Optional[str] = None
    alternate_phone: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None

class UserProfileCreate(UserProfileBase):
    pass

class UserProfileResponse(UserProfileBase):
    id: int
    user_id: int
    profile_image_url: Optional[str] = None
    cv_url: Optional[str] = None
    
    # We will not send the extracted text of RAG in the response (for security and size reasons)
    
    class Config:
        from_attributes = True # It helps convert SQLAlchemy objects to JSON  

# User Schemas
class UserBase(BaseModel):
    email: EmailStr

# Data that the client will send when creating a user (Request Validation)
class UserCreate(UserBase):
    password: str
    # Profile data can be collected together during registration
    profile: Optional[UserProfileCreate] = None  # Nested profile data

# API returns to the user (Response Serialization/DTO)
class UserResponse(BaseModel):
    id: int
    is_active: bool
    created_at: datetime
    # The response will also include the user's profile information.
    profile: Optional[UserProfileResponse] = None  # Nested profile data

    class Config:
        from_attributes = True # It helps convert SQLAlchemy objects to JSON


class UserBasicResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    profile: Optional[UserProfileResponse] = None  # Nested profile data

    class Config:
        from_attributes = True  # It helps convert SQLAlchemy objects to JSON


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    alternate_email: Optional[EmailStr] = None
    phone: Optional[str] = None
    alternate_phone: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None

    class Config:
        from_attributes = True  # It helps convert SQLAlchemy objects to JSON
