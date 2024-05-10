import pathlib
import sys

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


sys.path.append(str(pathlib.Path(__file__).resolve().parents[4]))

from src.kernel.fastapi.config import get_app_settings


APP_SETTINGS = get_app_settings()
SQLALCHEMY_DATABASE_URL = APP_SETTINGS.POSTGRES_DSN

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
