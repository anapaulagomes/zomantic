import pytest
from unittest.mock import patch, MagicMock

from zomantic.zotero import append_extra, filter_articles_without_extra_key, fetch_all_collections


class TestAppendExtra:
    @pytest.mark.parametrize('extra', [
        "Accepted: 2020-08-28T08:44:50Z\n"
        "Publisher: World Health Organization = Organisation mondiale de la Santé\n",
        "Number: 3",
        "Accepted: 2020-08-28T08:44:50Z",
        "PMCID: PMC6697516\nPMID: 23741561"
    ])
    def test_append_extra(self, extra):
        semantic_id = {
            'Semantic Scholar ID': '1234567890'
        }
        expected_extra = f"{extra}\nSemantic Scholar ID: {semantic_id['Semantic Scholar ID']}"
        assert append_extra(extra, semantic_id) == expected_extra


class TestFetchAllCollections:
    def test_returns_key_name_mapping(self):
        mock_zot = MagicMock()
        mock_zot.collections.return_value = [
            {"key": "ABC123", "data": {"name": "Machine Learning"}},
            {"key": "DEF456", "data": {"name": "NLP"}},
        ]
        with patch("zomantic.zotero.zot", mock_zot):
            result = fetch_all_collections()
        assert result == {"ABC123": "Machine Learning", "DEF456": "NLP"}

    def test_returns_empty_dict_when_no_collections(self):
        mock_zot = MagicMock()
        mock_zot.collections.return_value = []
        with patch("zomantic.zotero.zot", mock_zot):
            result = fetch_all_collections()
        assert result == {}


class TestFilterArticlesWithoutExtraKey:
    def test_filter_articles_without_extra_key(self):
        items = {
            'xxxx': {'data': {'extra': (
                "Accepted: 2020-08-28T08:44:50Z\n"
                "Publisher: World Health Organization = Organisation mondiale de la Santé"
            )}},
            'aaaa': {'data': {'extra': "PMCID: PMC6697516\nPMID: 23741561"}},
            'bbbb': {'data': {'extra': 'Semantic Scholar ID: 123456'}},
        }

        result = filter_articles_without_extra_key(items, 'Semantic Scholar ID')
        assert len(result) == 2
        assert result.get('xxxx')
        assert result.get('aaaa')
