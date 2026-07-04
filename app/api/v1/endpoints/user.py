from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.core.database import get_db
from app.api.services.user_service import UserService

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.post("/users/", response_model=UserResponse)
def create_user(user_req: UserCreate, db: Session = Depends(get_db)):
    return UserService.create_user(db=db, user_data=user_req)

@router.get("/users/{email}", response_model=UserResponse)
def get_user(email: str, db: Session = Depends(get_db)):
    return UserService.get_user_by_email(db=db, email=email)

@router.post("/{user_id}/upload-docs")
async def upload_user_documents(user_id: int, profile_image: UploadFile = File(None), cv_file: UploadFile = File(None), db: Session = Depends(get_db)):
    return UserService.upload_documents(db=db, user_id=user_id, profile_image=profile_image, cv_file=cv_file)
