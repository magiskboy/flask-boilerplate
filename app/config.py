import os
from functools import lru_cache
from secrets import token_bytes
from datetime import timedelta


def get_env(name: str, fallback=None, type_: callable = str, prefix = "ABIC") -> str:
    value = os.getenv(f"{prefix}_{name}")
    if value is None:
        if fallback is None:
            return None
        return fallback

    return type_(value)


class BaseConfig:
    ROOT_DIR = os.getcwd()

    TESTING = False

    DB_HOST = get_env("DB_HOST", "127.0.0.1")
    DB_PORT = get_env("DB_PORT", 3306, int)
    DB_USER = get_env("DB_USER", "app")
    DB_PASS = get_env("DB_PASS", "app")
    DB_NAME = get_env("DB_NAME", "app")

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    JWT_KEY = token_bytes(32)
    JWT_ALGORITHMS = ["HS256"]
    JWT_EXPIRED_TIME = timedelta(days=1)

    __ATTRS = (
        "ROOT_DIR",
        "DB_HOST", 
        "DB_PORT", 
        "DB_USER", 
        "DB_NAME", 
        "JWT_ALGORITHMS", 
        "JWT_EXPIRED_TIME",
    )

    def to_str(self) -> str:
        max_len = max(map(len, self.__ATTRS))
        return "\n".join(map(
            lambda attr: f"{attr:{max_len}} = {getattr(self, attr)}",
            self.__ATTRS
        ))


class DevelopmentConfig(BaseConfig):
    JWT_KEY = "secret_key"


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

    JWT_KEY = "secret_key"

    TESTING = True


class ProductionConfig(BaseConfig):
    ...


@lru_cache
def get_config(config_name: str) -> BaseConfig:
    return {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }.get(config_name, ProductionConfig)()
