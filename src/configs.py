from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_DB: str
    DB_USER: str
    DB_PASSWORD: str

    # TEST_DB_HOST: str
    # TEST_DB_PORT: str
    # TEST_DB_DB: str
    # TEST_DB_USER: str
    # TEST_DB_PASSWORD: str

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DB}"

    # @property
    # def TEST_DATABASE_URL_asyncpg(self):
    #     return f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASSWORD}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_DB}"

    @property
    def DATABASE_URL_psycopg(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DB}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
