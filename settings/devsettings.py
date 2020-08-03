from settings.settings import BasteSettings
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta


class DevelopSettings(BasteSettings):
    DEBUG = True
    # "postgresql://username:password@host:port/dbname"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=100)
    SQLALCHEMY_DATABASE_URI = "postgres://postgres:test123@127.0.0.1:5432/userprodDb"
    SQLALCHEMY_ECHO = False
    JWT_SECRET_KEY = os.urandom(32)