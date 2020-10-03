from pydantic import BaseSettings


class Environment(BaseSettings):
    """
    This is (some of) the environment variables used by the app.

    In PRODUCTION, we specify different values for this variables
    than what you are seeing here. These "hardcoded" values are
    used only in a development environment. So you don't have to
    worry about specifying these values in your environment.

    """

    DATABASE_URL: str = "postgresql://micebot:micebot@localhost:5432/micebot"
    PRODUCTION: bool = False
    SECRET_KEY: str = "secret-key"
    TOKEN_ALGORITHM: str = "HS256"
    TOKEN_EXPIRATION: int = 20

    class Config:
        case_sensitive = True

env: Environment = Environment()
