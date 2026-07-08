
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # One-to-One relationship with UserProfile
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    # Core information
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    alternate_email = Column(String, nullable=True)
    # Contact information
    phone = Column(String, nullable=True)
    alternate_phone = Column(String, nullable=True)
    # Address information
    address_line1 = Column(String, nullable=True)
    address_line2 = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)

    # File paths (We will store file location strings)
    profile_image_url = Column(String, nullable=True)
    cv_url = Column(String, nullable=True)

    # Extra fields for storing raw CV text later for RAG
    extracted_cv_text = Column(String, nullable=True)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    #Back-reference to User
    user = relationship("User", back_populates="profile")
