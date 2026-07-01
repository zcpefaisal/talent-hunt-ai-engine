# Application entry point
from fastapi import FastAPI
from app.api.v1.endpoints import user
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Enterprice Scalable Async Backend", version="1.0.0")

app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])

@app.get("/")
def root():
    return {"message": "Welcome to the Enterprice Scalable Async Backend!"}