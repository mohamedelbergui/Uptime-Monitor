import os
from pathlib import Path
from dotenv import load_dotenv

# Locate and load the .env file from the project root
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")


class DevelopmentConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "default-dev-key")

    DB_USER = os.getenv("POSTGRES_USER")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    DB_HOST = os.getenv("POSTGRES_HOST")
    DB_PORT = os.getenv("POSTGRES_PORT")
    DB_NAME = os.getenv("POSTGRES_DB")

    # Construct the PostgreSQL URI
    DEFAULT_DB_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", DEFAULT_DB_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True




# class ProductionConfig(Config):
#     DEBUG = False


# class TestingConfig(Config):
#     TESTING = True