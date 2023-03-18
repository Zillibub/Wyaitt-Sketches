from pydantic import BaseSettings


class Settings(BaseSettings):
    the_guardian_api_key: str

    class Config:
        env_file = ".env"


settings = Settings()
