from pydantic import BaseSettings


class Settings(BaseSettings):
    # server
    jwt_secret: str

    # game
    max_character_by_account: int = 5


settings = Settings()