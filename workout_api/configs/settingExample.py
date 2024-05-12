from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sgbd = "postgresql"
    user = ""
    password = ""
    host = ""
    database = ""
    DB_URL: str = Field(default=f"{sgbd}+asyncpg://{user}:{password}@{host}/{database}")


settings = Settings()