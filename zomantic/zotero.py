import os
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

    articles = []
    for item in all_items:
        if item["data"]["itemType"] in TO_BE_SKIPPED:
            continue

        keywords = [tag["tag"] for tag in item["data"]["tags"]]
        authors = []
        for creator in item["data"].get("creators", []):
            first_last_names = {'firstName', 'lastName'}
            creator_keys = creator.keys()
            if creator_keys & first_last_names:
                authors.append(f"{creator['firstName']} {creator['lastName']}")

        article = {
            "title": item["data"]["title"],
            "abstract": item["data"].get("abstractNote"),
            "journal": item["data"].get("journalAbbreviation"),
            "doi": item["data"].get("DOI"),
            "authors": authors,
            "year": item["data"]["date"],
            "keywords": keywords,
            "key": item["data"]["key"],
            "article_type": item["data"]["itemType"],
            "language": item["data"].get("language"),
            "url": item["data"]["url"],
        }
        articles.append(article)
    print(f"{len(articles)} articles were found")
    return articles
