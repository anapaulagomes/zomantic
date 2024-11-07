import os
from typing import Any, Dict

from dotenv import load_dotenv
from pyzotero import zotero

load_dotenv()

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
    api_key = os.getenv("ZOTERO_API_KEY")
    library_id = os.getenv("ZOTERO_USER_ID")
    zot = zotero.Zotero(library_id, "user", api_key)

    all_items = zot.everything(zot.items())
    print(f"{len(all_items)} items retrieved from the library")

    selected_items = []
    for item in all_items:
        if item["data"]["itemType"] in TO_BE_SKIPPED:
            continue

        selected_items.append(item)
    print(f"{len(selected_items)} items were selected")
    return selected_items


def append_extra(extra: str, new_info: Dict[str, Any]) -> str:
    for key, value in new_info.items():
        extra += f"\n{key}: {value}"
    return extra
