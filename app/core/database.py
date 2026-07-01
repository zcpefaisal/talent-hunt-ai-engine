from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = "postgresql://username:password@localhost:5432/mydatabase"

DATABASE_URL = "sqlite:///./test.db"

# engine = create_engine(DATABASE_URL)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# This is a dependency injection, which will open and close the DB session on every request.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()