from passlib.context import CryptContext
import bcrypt

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