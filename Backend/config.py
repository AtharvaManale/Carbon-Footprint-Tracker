import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("Key")

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")