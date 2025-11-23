import os
import mysql.connector
from contextlib import contextmanager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", 3306)),
}

@contextmanager
def get_cursor(commit=False):
    conn = mysql.connector.connect(**DB)
    cursor = conn.cursor(dictionary=True)
    try:
        yield cursor
        if commit:
            conn.commit()
    finally:
        cursor.close()
        conn.close()
