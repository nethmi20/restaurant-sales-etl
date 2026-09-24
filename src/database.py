import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


def get_connection():
    """Connect to the PostgreSQL database."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )