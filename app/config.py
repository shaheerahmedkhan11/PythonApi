from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str = "postgres"
    database_port: str = "5432"
    database_password: str = "postgress"
    database_name: str = "fastapi"
    database_username: str = "postgres"
    secret_key: str = "45fd40544cf52be1c8526c2edf6df429413c13d53280afe72ce653e5e3b175eb"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
