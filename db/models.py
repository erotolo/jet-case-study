from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text, Date, DateTime
from datetime import datetime

Base = declarative_base()


class Comic(Base):
    """SQLAlchemy model for XKCD raw comics."""

    __tablename__ = "comics"

    num = Column(Integer, primary_key=True, autoincrement=False)
    title = Column(String(500), nullable=False)
    transcript = Column(Text)
    alt = Column(Text)
    img = Column(String(500))
    day = Column(Integer)
    month = Column(Integer)
    year = Column(Integer)
    published_date = Column(Date)
    fetched_at = Column(DateTime, default=lambda: datetime.utcnow(), nullable=False)
