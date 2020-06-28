from pydantic import BaseSettings


class Environment(BaseSettings):
    database_url: str = "sqlite:///local.db"
    production: bool = False
    secret_key: str = "secret-key"


env: Environment = Environment()
