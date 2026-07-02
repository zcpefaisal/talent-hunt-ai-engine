from pydantic import BaseModel, EmailStr

# Data that the client will send when creating a user (Request Validation)
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# API returns to the user (Response Serialization/DTO)
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True # It helps convert SQLAlchemy objects to JSON