import pytest
import requests
from unittest.mock import patch
from datetime import datetime, timedelta
from zotero import get_items_added_from, get_items_added_this_week

@pytest.fixture
def zotero_api_key():
    return "test_zotero_api_key"

@pytest.fixture
def zotero_user_id():
    return "test_zotero_user_id"

@pytest.fixture
def start_date():
    return datetime.now() - timedelta(days=7)

@pytest.fixture
def zotero_response():
    return [
        {"key": "item1", "title": "Test Item 1"},
        {"key": "item2", "title": "Test Item 2"}
    ]

@patch("requests.get")
def test_get_items_added_from(mock_get, zotero_api_key, zotero_user_id, start_date, zotero_response):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = zotero_response

    items = get_items_added_from(zotero_api_key, zotero_user_id, start_date)
    assert items == zotero_response

@patch("requests.get")
@patch("os.getenv")
def test_get_items_added_this_week(mock_getenv, mock_get, zotero_api_key, zotero_response):
    mock_getenv.return_value = "test_zotero_user_id"
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = zotero_response

    items = get_items_added_this_week(zotero_api_key)
    assert items == zotero_response
