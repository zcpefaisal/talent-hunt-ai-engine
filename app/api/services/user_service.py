import os
import shutil
import logging
from sqlalchemy.orm import Session, joinedload
from app.models.user import User, UserProfile
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from fastapi import UploadFile, HTTPException, status
from app.core.config import settings
from app.core.kafka_producer import kafka_manager

logger = logging.getLogger(__name__)

UPLOAD_DIR = "media"

class UserService:

    @staticmethod
    def create_user(db: Session, user_data: UserCreate):
        db_user = db.query(User).filter(User.email == user_data.email).first()
        if db_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        
        # Hash the password before storing it in the database
        hashed_password = get_password_hash(user_data.password)

        # create a new User object
        new_user = User(email=user_data.email, hashed_password=hashed_password)
        db.add(new_user)
        db.flush() # Flush the session to get the new user's ID before committing, so we can use it for the profile
        
        try:
            if user_data.profile:
                profile_dict = user_data.profile.model_dump(exclude_none=True)
                new_profile = UserProfile(user_id=new_user.id, **profile_dict)
                db.add(new_profile)
            else:
                new_profile = UserProfile(user_id=new_user.id)
                db.add(new_profile)
        
            db.commit()
            db.refresh(new_user)
            return new_user
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating user profile: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating user profile: {str(e)}")

    @staticmethod
    def get_all_users_basic(db: Session, skip: int = 0, limit: int = 10):
        return db.query(User).options(joinedload(User.profile)).offset(skip).limit(limit).all()

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        db_user = db.query(User).filter(User.email == email).first()
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return db_user
    


    @staticmethod
    async def upload_documents(db: Session, user_id: int, profile_image: UploadFile = None, cv_file: UploadFile = None):
        # First check if this user's profile is in the database.
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User profile not found")
        
        # Different folder paths based on user ID (eg: media/user_2/)
        user_media_dir = os.path.join(UPLOAD_DIR, f"user_{user_id}")
        os.makedirs(user_media_dir, exist_ok = True)

        # Handle profile image upload
        if profile_image:
            if not profile_image.filename.lower().endswith((".png", ".jpg", ".jpeg")):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid profile image format. Only PNG, JPG, and JPEG are allowed.")
            
            image_path = os.path.join(user_media_dir, f"profile_{profile_image.filename}")
            with open(image_path, "wb") as buffer:
                shutil.copyfileobj(profile_image.file, buffer)
            
            profile.profile_image_url = image_path

        # Handle CV upload
        if cv_file:
            if not cv_file.filename.lower().endswith((".pdf", ".doc", ".docx")):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid CV format. Only PDF, DOC, and DOCX are allowed.")
            
            cv_path = os.path.join(user_media_dir, f"cv_{cv_file.filename}")
            with open(cv_path, "wb") as buffer:
                shutil.copyfileobj(cv_file.file, buffer)
            
            profile.cv_url = cv_path
        
        

        # Update the database with the new file paths
        db.commit()
        db.refresh(profile)

        if cv_file:
            event_payload = {
                "event_type": "CV_UPLOADED",
                "cv_id": profile.id,
                "file_name": cv_file.filename,
                "file_path": cv_path,
                "status": "PENDING_PROCESSING"
            }
            logger.info(f"Sending event to Kafka: {event_payload}")
            await kafka_manager.send_message(topic="cv_upload", message=event_payload)
        
        return {
            "message": "Documents uploaded successfully", 
            "profile_image_url": profile.profile_image_url, 
            "cv_url": profile.cv_url
        }
    

    @staticmethod
    def update_user_profile(db: Session, current_user_id: int, update_data: UserUpdate):
        # Check if this user profile is in the database.
        profile = db.query(UserProfile).filter(UserProfile.user_id == current_user_id).first()
        if not profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User profile not found")
        
        # Update the profile fields with the provided data (only those that are not None)
        data_dict = update_data.model_dump(exclude_unset=True)
        for key, value in data_dict.items():
            setattr(profile, key, value) # Set the attribute of the profile object to the new value

        db.commit()
        db.refresh(profile)
        return profile
    

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str):
        # Find users by email
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return False
        
        # Verify password
        if not verify_password(password, user.hashed_password):
            return False
        
        return user
    

    @staticmethod
    def delete_user_account(db: Session, current_user: User):
        # Delete the user account
        db.delete(current_user)
        db.commit()
        return {"message": "User account and associated profile deleted successfully"}