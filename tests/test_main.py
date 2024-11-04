import pytest
from unittest.mock import patch
from zomantic.main import main


@pytest.fixture
def zotero_items():
    return [
        {"data": {"key": "item1"}},
        {"data": {"key": "item2"}}
    ]


@pytest.fixture
def recommendations():
    return {
        "recommendedPapers": [
            {
                "title": "Test Paper 1",
                "authors": [{"name": "Author 1"}, {"name": "Author 2"}],
                "url": "http://example.com/paper1"
            },
            {
                "title": "Test Paper 2",
                "authors": [{"name": "Author 3"}, {"name": "Author 4"}],
                "url": "http://example.com/paper2"
            }
        ]
    }


@patch("zomantic.main.get_items_added_this_week")
@patch("zomantic.main.get_recommendations")
def test_main(mock_get_recommendations, mock_get_items_added_this_week, zotero_items, recommendations):
    mock_get_items_added_this_week.return_value = zotero_items
    mock_get_recommendations.return_value = recommendations

    with patch("builtins.print") as mock_print:
        main()
        assert mock_print.call_count == 6
        mock_print.assert_any_call("Title: Test Paper 1")
        mock_print.assert_any_call("Authors: Author 1, Author 2")
        mock_print.assert_any_call("URL: http://example.com/paper1")
        mock_print.assert_any_call("Title: Test Paper 2")
        mock_print.assert_any_call("Authors: Author 3, Author 4")
        mock_print.assert_any_call("URL: http://example.com/paper2")
