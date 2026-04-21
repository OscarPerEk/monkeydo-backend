from pydantic_settings import BaseSettings

# Hardcoded single user until AWS Cognito is wired up (Milestone 9)
DEFAULT_USER_ID = "00000000-0000-0000-0000-000000000001"


class Settings(BaseSettings):
    database_url: str

    model_config = {"env_file": ".env"}


settings = Settings()
