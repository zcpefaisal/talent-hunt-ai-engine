from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.services.user_service import UserService
from app.core.security import create_access_token
from app.schemas.token import Token
# Importing the rate limiter
from app.core.limiter import limiter

router = APIRouter()

# URL: /api/v1/auth/login
@router.post("/login", response_model=Token)
@limiter.limit("10/minute") # Limit to 10 requests per minute
def login_access_token(request: Request, db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):

    # Verify username and password (OAuth2 form takes email as username)
    user = UserService.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    
    # Generating a token (we are sending the user email as the Subject of the token)
    return {"access_token": create_access_token(subject=user.email), "token_type": "bearer"}
