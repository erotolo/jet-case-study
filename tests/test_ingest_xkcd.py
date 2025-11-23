from ingest.ingest_xkcd import ingest_latest
from unittest.mock import Mock, patch


class TestIngestPipeline:
    """Basic tests for ingestion logic"""

    @patch("ingest.ingest_xkcd.XkcdClient")
    @patch("ingest.ingest_xkcd.insert_comic_if_not_exists")
    def test_ingest_latest_success(self, mock_insert, mock_client_class):
        """Test successful ingestion"""

        mock_client = Mock()
        mock_client.get_latest_comic.return_value = {
            "num": 2850,
            "title": "Test Comic",
            "year": "2023",
            "month": "11",
            "day": "22",
            "img": "https://example.com/comic.png",
            "alt": "Test alt text",
        }
        mock_client_class.return_value = mock_client
        mock_insert.return_value = True  # Comic was inserted successfully

        # Mock kwargs with task instance
        kwargs = {"ti": Mock()}

        result = ingest_latest(**kwargs)

        assert result == 2850
        mock_insert.assert_called_once()
        kwargs["ti"].xcom_push.assert_called()
