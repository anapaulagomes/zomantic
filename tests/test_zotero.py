import pytest

from zomantic.zotero import append_extra


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
