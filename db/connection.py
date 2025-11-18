import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()


def get_engine():
    """Create and return a SQLAlchemy engine using the DB_URL from environment variables."""

    db_url = os.getenv("DB_URL")
    if not db_url:
        raise ValueError("DB_URL environment variable is not set.")

    return create_engine(
        db_url,
        echo=False,
        future=True,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )


def get_session():
    """Create and return a SQLAlchemy session."""
    engine = get_engine()
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    return Session()
