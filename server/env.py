from pydantic import BaseSettings


class Environment(BaseSettings):
    database_url: str = "sqlite:///local.db"
    production: bool = False
    secret_key: str = "secret-key"
    token_algorithm: str = "HS256"


env: Environment = Environment()
