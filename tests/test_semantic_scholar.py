import pytest
from unittest.mock import MagicMock, ANY

from zomantic.semantic_scholar import get_or_create_folder, save_paper_to_library


FOLDERS_RESPONSE = {
    "folders": [
        {
            "id": 11479452,
            "name": "Decolonial AI",
            "sourceType": "Library",
            "recommendationStatus": {"id": "On"},
            "entries": [],
        },
        {
            "id": 9273136,
            "name": "Unsupervised Learning",
            "sourceType": "Library",
            "recommendationStatus": {"id": "On"},
            "entries": [],
        },
    ],
    "unsortedLibraryEntries": [],
}

CREATE_RESPONSE = {
    "folder": {
        "id": 14212178,
        "name": "NLP",
        "createdAtUtc": 1774862036.597,
        "modifiedAtUtc": 1774862036.597,
        "recommendationStatus": {"id": "On"},
        "sourceType": {"id": "Library"},
    }
}


@pytest.fixture
def mock_session():
    return MagicMock()


class TestGetOrCreateFolder:
    def test_returns_existing_folder_id_without_post(self, mock_session):
        mock_session.get.return_value.json.return_value = FOLDERS_RESPONSE

        result = get_or_create_folder("Decolonial AI", mock_session)

        assert result == 11479452
        mock_session.post.assert_not_called()

    def test_returns_correct_id_for_second_folder(self, mock_session):
        mock_session.get.return_value.json.return_value = FOLDERS_RESPONSE

        result = get_or_create_folder("Unsupervised Learning", mock_session)

        assert result == 9273136
        mock_session.post.assert_not_called()

    def test_creates_folder_when_not_found(self, mock_session):
        mock_session.get.return_value.json.return_value = FOLDERS_RESPONSE
        mock_session.post.return_value.json.return_value = CREATE_RESPONSE

        result = get_or_create_folder("NLP", mock_session)

        assert result == 14212178

    def test_create_posts_correct_payload(self, mock_session):
        mock_session.get.return_value.json.return_value = FOLDERS_RESPONSE
        mock_session.post.return_value.json.return_value = CREATE_RESPONSE

        get_or_create_folder("NLP", mock_session)

        mock_session.post.assert_called_once_with(
            "https://www.semanticscholar.org/api/1/library/folders",
            json={"name": "NLP", "recommendationStatus": "On"},
            headers=ANY,
        )

    def test_get_calls_correct_endpoint(self, mock_session):
        mock_session.get.return_value.json.return_value = FOLDERS_RESPONSE

        get_or_create_folder("Decolonial AI", mock_session)

        call_url = mock_session.get.call_args[0][0]
        assert "semanticscholar.org/api/1/library/folders" in call_url


class TestSavePaperToLibrary:
    def test_includes_folder_ids_in_payload(self, mock_session):
        save_paper_to_library("paper123", "Some Title", mock_session, folder_ids=[11479452])

        payload = mock_session.post.call_args.kwargs["json"]
        assert payload["folderIds"] == [11479452]

    def test_defaults_to_empty_folder_ids(self, mock_session):
        save_paper_to_library("paper123", "Some Title", mock_session)

        payload = mock_session.post.call_args.kwargs["json"]
        assert payload["folderIds"] == []
