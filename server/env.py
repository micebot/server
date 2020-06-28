from pydantic import BaseSettings  # pragma: no cover


class Environment(BaseSettings):  # pragma: no cover
    database_url: str = "sqlite:///local.db"
    production: bool = False
    secret_key: str = "secret-key"


env: Environment = Environment()  # pragma: no cover
