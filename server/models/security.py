from passlib.context import CryptContext

pw_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
