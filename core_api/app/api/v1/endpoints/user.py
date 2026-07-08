from fastapi import APIRouter, Depends, UploadFile, File, Request
from typing import List
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse, UserUpdate, UserBasicResponse
from app.models.user import User
from app.core.database import get_db
from app.api.services.user_service import UserService
from app.api.v1.endpoints.deps import get_current_user
# Importing the rate limiter
from app.core.limiter import limiter

router = APIRouter()

# URL: /api/v1/users/
@router.post("/", response_model=UserResponse)
@limiter.limit("5/minute") # Limit to 5 requests per minute
def create_user(request: Request, user_req: UserCreate, db: Session = Depends(get_db)):
    return UserService.create_user(db=db, user_data=user_req)

@router.get("/", response_model=List[UserBasicResponse])
@limiter.limit("20/minute") # Limit to 20 requests per minute
def get_all_users_basic(request: Request, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return UserService.get_all_users_basic(db=db, skip=skip, limit=limit)

# URL: /api/v1/users/{email}
@router.get("/{email}", response_model=UserResponse)
@limiter.limit("10/minute") # Limit to 10 requests per minute
def get_user(request: Request, email: str, db: Session = Depends(get_db)):
    return UserService.get_user_by_email(db=db, email=email)

# URL: /api/v1/users/{user_id}/upload-docs
@router.post("/{user_id}/upload-docs")
async def upload_user_documents(user_id: int, profile_image: UploadFile = File(None), cv_file: UploadFile = File(None), db: Session = Depends(get_db)):
    return await UserService.upload_documents(db=db, user_id=user_id, profile_image=profile_image, cv_file=cv_file)

# URL: /api/v1/users/me
@router.put("/me")
def update_my_profile(update_data: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return UserService.update_user_profile(db=db, current_user_id = current_user.id, update_data = update_data)

# URL: /api/v1/users/me
@router.delete("/me")
def delete_my_account(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return UserService.delete_user_account(db=db, current_user=current_user)