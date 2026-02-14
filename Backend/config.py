import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("Key")

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

    JWT_SECRET_KEY = os.getenv("JKey")
    JWT_ACCESS_TOKEN_EXPIRY  = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRY = timedelta(days=7)