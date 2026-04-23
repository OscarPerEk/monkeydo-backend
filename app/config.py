from pydantic_settings import BaseSettings

# Hardcoded single user until AWS Cognito is wired up (Milestone 9)
DEFAULT_USER_ID = "00000000-0000-0000-0000-000000000001"


class Settings(BaseSettings):
    database_url: str
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
