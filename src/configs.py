from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    TEST_POSTGRES_HOST: str
    TEST_POSTGRES_PORT: str
    TEST_POSTGRES_DB: str
    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASSWORD: str

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def TEST_DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.TEST_POSTGRES_USER}:{self.TEST_POSTGRES_PASSWORD}@{self.TEST_POSTGRES_HOST}:{self.TEST_POSTGRES_PORT}/{self.TEST_POSTGRES_DB}"

    @property
    def DATABASE_URL_psycopg(self):
        return f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
