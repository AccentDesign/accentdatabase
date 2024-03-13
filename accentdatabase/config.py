from pydantic import ImportString, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="database_")

    url: PostgresDsn
    future: bool = True
    json_serializer: ImportString = "json.dumps"
    echo: bool = False


config = AppConfig()
