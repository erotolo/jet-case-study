import logging
from datetime import date
from db.models import Base
from db.connection import get_engine
from db.operations import insert_comic_if_not_exists
from ingest.api import XkcdClient

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Ensure PG tables exist (run at import)
engine = get_engine()
Base.metadata.create_all(engine)


def ingest_latest(**kwargs):
    """
    Fetch the latest comic from XKCD and insert it into Postgres.
    Idempotent: will not insert duplicates.
    If DB is empty, ingest the current latest comic immediately.
    """
    client = XkcdClient()

    try:
        latest = client.get_latest_comic()
    except Exception as e:
        logger.error(f"Failed to fetch latest comic: {e}")
        return None

    comic_date = date(int(latest["year"]), int(latest["month"]), int(latest["day"]))
    comic_id = latest["num"]

    inserted = insert_comic_if_not_exists(engine, latest)
    if inserted:
        logger.info(f"Inserted comic ID {comic_id} for date {comic_date}")
    else:
        logger.info(f"Comic ID {comic_id} already exists in database")

    # Pass the date and ID for downstream tasks
    kwargs["ti"].xcom_push(key="comic_date", value=str(comic_date))
    kwargs["ti"].xcom_push(key="comic_id", value=comic_id)

    return comic_id
