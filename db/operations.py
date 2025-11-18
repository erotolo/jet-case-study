from sqlalchemy.orm import sessionmaker
from db.models import Comic
from datetime import date
import logging

logger = logging.getLogger(__name__)


def insert_comic_if_not_exists(engine, comic_data):
    """Insert comic into database if it doesn't already exist."""

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        existing = session.query(Comic).filter(Comic.num == comic_data["num"]).first()
        if existing:
            logger.info(f"Comic {comic_data['num']} already exists")
            return False

        comic = Comic(
            num=comic_data["num"],
            title=comic_data["title"],
            transcript=comic_data.get("transcript", ""),
            alt=comic_data.get("alt", ""),
            img=comic_data.get("img", ""),
            day=int(comic_data["day"]),
            month=int(comic_data["month"]),
            year=int(comic_data["year"]),
            published_date=date(
                int(comic_data["year"]),
                int(comic_data["month"]),
                int(comic_data["day"]),
            ),
        )

        session.add(comic)
        session.commit()
        logger.info(f"Successfully inserted comic {comic_data['num']}")
        return True

    except Exception as e:
        session.rollback()
        logger.error(f"Error inserting comic {comic_data['num']}: {e}")
        raise
    finally:
        session.close()
