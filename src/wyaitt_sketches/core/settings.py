from pydantic import BaseSettings


class Settings(BaseSettings):
    the_guardian_api_key: str
    discord_bot_token: str
    discord_guild_id: int
    openai_token: str

    class Config:
        env_file = ".env"


settings = Settings()
