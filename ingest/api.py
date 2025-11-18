import os
import requests
import time
import json
import logging

logger = logging.getLogger(__name__)


class XkcdClient:
    """
    XKCD API Client with exponential backoff.
    """

    def __init__(
        self, max_retries=5, base_delay=1, max_delay=60, timeout=10, base_url=None
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.timeout = timeout
        self.base_url = base_url or os.getenv("XKCD_BASE_URL", "https://xkcd.com")

    def _request(self, url):
        retries = 0

        while retries < self.max_retries:
            try:
                resp = requests.get(url, timeout=self.timeout)
                resp.raise_for_status()
                return resp.json()
            except requests.exceptions.RequestException as e:
                retries += 1
                if retries == self.max_retries:
                    logger.error(f"Max retries reached: {e}")
                    raise

                # exponential backoff
                delay = min(self.max_delay, self.base_delay * (2 ** (retries - 1)))

                logger.warning(
                    f"Request failed ({e}). "
                    f"Retrying {retries}/{self.max_retries} in {delay:.2f}s"
                )
                time.sleep(delay)

    def get_latest_comic(self):
        url = f"{self.base_url}/info.0.json"
        return self._request(url)

