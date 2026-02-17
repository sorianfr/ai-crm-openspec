"""Password hashing and verification (passlib/bcrypt)."""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Return a one-way hash of the password for storage."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed: str) -> bool:
    """Return True if plain_password matches the stored hash."""
    return pwd_context.verify(plain_password, hashed)
