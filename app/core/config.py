from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import computed_field

class Settings(BaseSettings):
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str

    # Using computed_field to dynamically create DATABASE_URL
    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
    # Describe to Pydantic where the .env file is located
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    
# Creating a global object, which will be imported and used throughout the project
settings = Settings()