# app/config/cfg_sql_connection.py
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URL = "sqlite:///./library.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
    future=True,
    connect_args={"check_same_thread": False},
)

SessionLocal: sessionmaker[Session] = sessionmaker(
    bind=engine, autocommit=False, autoflush=False, future=True
)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from app.repository.model import Base

Base.metadata.drop_all(bind=engine)  # drops all tables - DONE JUST FOR SMAPLE PROJECT NO FOR PROD DEV ETC
Base.metadata.create_all(bind=engine)
