from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    MONGODB_DATABASE: str

    class Config:
        env_file = './.env'


settings = Settings()
