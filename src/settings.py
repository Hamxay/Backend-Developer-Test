from os import getenv
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
AUTO_RELOAD = getenv("AUTO_RELOAD", True) != "0"
DB_USERNAME = getenv("DB_USERNAME", "postgres")
DB_PASSWORD = getenv("DB_PASSWORD", "postgres")
DB_HOST = getenv("DB_HOST", "localhost")
DB_PORT = int(getenv("DB_PORT", 5432))
DB_NAME = getenv("DB_NAME", "db_name")
DB_ECHO = getenv("DB_ECHO", "0") != "0"
DB_URL = (
    f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
ACCESS_TOKEN_ALGORITHM = getenv("ACCESS_TOKEN_ALGORITHM", "HS256")
ACCESS_TOKEN_SECRET_KEY = getenv("ACCESS_TOKEN_SECRET_KEY")
ACCESS_TOKEN_ISSUER = getenv("ACCESS_TOKEN_ISSUER")
ACCESS_TOKEN_AUDIENCE = getenv("ACCESS_TOKEN_AUDIENCE")
ACCESS_TOKEN_LEEWAY = int(getenv("ACCESS_TOKEN_LEEWAY", 10))
