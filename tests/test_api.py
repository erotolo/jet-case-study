import pytest
from unittest.mock import Mock, patch
from ingest.api import XkcdClient


class TestXkcdClient:
    """XKCD API Client basic unit tests"""

    @patch("requests.get")
    def test_get_latest_comic_success(self, mock_get):
        """Test successful API call"""
        # Mock API response
        mock_response = Mock()
        mock_response.json.return_value = {
            "num": 2850,
            "title": "Test Comic",
            "year": "2023",
            "month": "11",
            "day": "22",
            "img": "https://example.com/comic.png",
            "alt": "Test alt text",
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        client = XkcdClient()
        result = client.get_latest_comic()

        assert result["num"] == 2850
        assert result["title"] == "Test Comic"
        mock_get.assert_called_once_with("https://xkcd.com/info.0.json", timeout=10)

    @patch("requests.get")
    def test_get_latest_comic_api_failure(self, mock_get):
        """Test API failure handling"""
        mock_get.side_effect = Exception("API Error")

        client = XkcdClient()
        with pytest.raises(Exception):
            client.get_latest_comic()
