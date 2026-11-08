from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    POSTGRES_PASSWORD: str

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)
