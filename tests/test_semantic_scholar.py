import pytest
from unittest.mock import patch
from zomantic.semantic_scholar import get_recommendations


@pytest.fixture
def semantic_scholar_api_key():
    return "test_semantic_scholar_api_key"


@pytest.fixture
def paper_ids():
    return ["paper1", "paper2"]


@pytest.fixture
def semantic_scholar_response():
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


@patch("requests.post")
def test_get_recommendations(mock_post, semantic_scholar_api_key, paper_ids, semantic_scholar_response):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = semantic_scholar_response

    recommendations = get_recommendations(semantic_scholar_api_key, paper_ids)
    assert recommendations == semantic_scholar_response
