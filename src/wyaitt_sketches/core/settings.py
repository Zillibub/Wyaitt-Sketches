from pydantic import BaseSettings


class Settings(BaseSettings):
    the_guardian_api_key: str
    discord_bot_token: str
    discord_group_id: int

    class Config:
        env_file = ".env"


settings = Settings()
