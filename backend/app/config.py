import os

from dotenv import load_dotenv

ENV_FILE = os.getenv("ENV", "dev")
load_dotenv(f".env.{ENV_FILE}")

print(f"Loading environment variables from: .env.{ENV_FILE}")

# Load environment variables from .env file
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")

for key in [
    "DB_USER",
    "DB_PASSWORD",
    "DB_HOST",
    "DB_PORT",
    "DB_NAME",
    "CELERY_BROKER_URL",
    "CELERY_RESULT_BACKEND",
]:
    value = os.getenv(key)
    print(f"{key}: {value}")
