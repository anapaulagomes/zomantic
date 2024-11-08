import os
from typing import Any, Dict

from dotenv import load_dotenv
from pyzotero import zotero
from pyzotero.zotero_errors import InvalidItemFields

load_dotenv()

api_key = os.getenv("ZOTERO_API_KEY")
library_id = os.getenv("ZOTERO_USER_ID")
zot = zotero.Zotero(library_id, "user", api_key)

TO_BE_SKIPPED = [
    "attachment",
    "annotation",
    "artwork",
    "audioRecording",
    "bill",
    "blogPost",
    # "book",
    # "bookSection",
    "case",
    "computerProgram",
    # "conferencePaper",
    "dictionaryEntry",
    "document",
    "email",
    "encyclopediaArticle",
    "film",
    "forumPost",
    "hearing",
    "instantMessage",
    "interview",
    # "journalArticle",
    "letter",
    # "magazineArticle",
    # "manuscript",
    "map",
    "note",
    "newspaperArticle",
    "patent",
    "podcast",
    "presentation",
    "radioBroadcast",
    "report",
    "statute",
    # "thesis",
    "tvBroadcast",
    "videoRecording",
    "webpage"
]


def fetch_all_items_from_zotero():
    all_items = zot.everything(zot.items())
    print(f"{len(all_items)} items retrieved from the library")

    selected_items = {}
    for item in all_items:
        if item["data"]["itemType"] in TO_BE_SKIPPED:
            continue

        selected_items[item['key']] = item
    print(f"{len(selected_items)} items were selected")
    return selected_items


def append_extra(extra: str, new_info: Dict[str, Any]) -> str:
    for key, value in new_info.items():
        extra += f"\n{key}: {value}"
    return extra


def filter_articles_without_extra_key(items, wanted_key):
    filtered_items = {}
    for zotero_key, item in items.items():
        if wanted_key not in item['data']['extra']:
            filtered_items[zotero_key] = item
    return filtered_items


def add_semantic_scholar_ids_to_items(zotero_semantic_scholar_ids):
    to_be_updated = {}
    for zotero_key, paper_id_item in zotero_semantic_scholar_ids.items():
        item = paper_id_item['item']
        paper_id = paper_id_item['paper_id']
        extra = item['data']['extra']
        item['data']['extra'] = append_extra(
            extra,
            {'Semantic Scholar ID': paper_id}
        )
        to_be_updated[zotero_key] = item
    try:
        zot.check_items(to_be_updated.values())
        zot.update_items(to_be_updated.values())
    except InvalidItemFields:
        print(f"Could not update item {item}")
    else:
        print(f"{len(to_be_updated)} items updated successfully")
    return to_be_updated
