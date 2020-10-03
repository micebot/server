from pydantic import BaseSettings


class Environment(BaseSettings):
    """
    This is (some of) the environment variables used by the app.

    In production, we specify different values for this variables
    than what you are seeing here. These "hardcoded" values are
    used only in a development environment. So you don't have to
    worry about specifying these values in your environment.

    """

    version: str = "0.2.0"
    database_url: str = "postgresql://micebot:micebot@localhost:5432/micebot"
    production: bool = False
    secret_key: str = "secret-key"
    token_algorithm: str = "HS256"


env: Environment = Environment()
