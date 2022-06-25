from pydantic import BaseSettings


class DBsettings(BaseSettings):
    class Config:
        env_prefix = "connection_"

    string: str


db = DBsettings()
