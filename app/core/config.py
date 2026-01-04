from pydantic_settings import BaseSettings
from urllib.parse import quote_plus

class Settings(BaseSettings):
    DB_USER: str = "fastapi_user"
    DB_PASSWORD: str = "StrongPassword123!"
    DB_HOST: str = "fastapi-devops-dev-postgres.cluk6yyye4gl.ap-south-1.rds.amazonaws.com"
    DB_PORT: int = 5432
    DB_NAME: str = "fastapi"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://{self.DB_USER}:"
            f"{quote_plus(self.DB_PASSWORD)}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"

settings = Settings()

