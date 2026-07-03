from sqlalchemy.orm import Session
from app.models.user import User, UserProfile
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from fastapi import HTTPException, status

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
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating user profile: {str(e)}")


    @staticmethod
    def get_user_by_email(db: Session, email: str):
        db_user = db.query(User).filter(User.email == email).first()
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return db_user