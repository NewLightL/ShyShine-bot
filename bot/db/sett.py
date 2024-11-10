'''Settings for db'''

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Create settings db"""
    db_host: str
    db_port: int
    db_user: str
    db_pass: str
    db_name: str


    @property
    def db_url(self) -> str:
        """Create a connection to the database"""
        return f'postgresql+asyncpg://{self.db_user}'\
            f':{self.db_pass}'\
            f'@{self.db_host}:{self.db_port}/{self.db_name}'

    model_config = SettingsConfigDict(env_file=r'bot\db\.env',
                                      env_file_encoding='utf-8')

settings = Settings()  # type: ignore
