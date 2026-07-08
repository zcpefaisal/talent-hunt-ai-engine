from datetime import timedelta, datetime, timezone
from typing import Union, Any
from jose import jwt
from passlib.context import CryptContext
import bcrypt

SECRET_KEY = "SUPER_SECRET_KEY_FOR_DEVELOPMENT_ONLY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_password_hash(password: str) -> str:
    # Will be used to hash the plain password
    # return pwd_context.hash(password)
    password_bytes = password.encode('utf-8')  # Convert to bytes
    salt = bcrypt.gensalt()  # Generate a salt
    hashed_password_bcrypt = bcrypt.hashpw(password_bytes, salt)  # Hash the password with the salt
    return hashed_password_bcrypt.decode('utf-8') # Convert back to string and


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Will be used to verify the plain password against the hashed password
    # return pwd_context.verify(plain_password, hashed_password)
    password_bytes = plain_password.encode('utf-8')  # Convert to bytes
    hashed_password_bytes = hashed_password.encode('utf-8')  # Convert to bytes
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)  # Verify the password


def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
