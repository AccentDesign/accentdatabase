from typing import Union

from pydantic import BaseSettings, PostgresDsn, PyObject


class AppConfig(BaseSettings):
    url: Union[PostgresDsn, str]
    future: bool = True
    json_serializer: PyObject = "accentdatabase.encoders.json_serializer"
    echo: bool = False

    class Config:
        env_prefix = "database_"


config = AppConfig()
