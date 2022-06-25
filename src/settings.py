from pydantic import BaseSettings


class BotSettings(BaseSettings):
    class Config:
        env_prefix = "bot_"

    prefix: str
    token: str
    guild: str


bot = BotSettings()
