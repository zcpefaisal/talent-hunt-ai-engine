from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# connection string for PostgreSQL database
# DATABASE_URL = "postgresql://my_firstapi_pg_user:my_firstapi_pg_password@localhost:5432/my_firstapi_pg_db"

# Now the URL will come dynamically from .env as config
engine = create_engine(settings.DATABASE_URL)

# Uncomment the following lines to use SQLite instead of PostgreSQL
# DATABASE_URL = "sqlite:///./test.db"
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# This is a dependency injection, which will open and close the DB session on every request.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()