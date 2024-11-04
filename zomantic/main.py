from zomantic.zotero import get_items_added_this_week
from zomantic.semantic_scholar import get_recommendations
from dotenv import load_dotenv
import os

load_dotenv()


def main():
    zotero_api_key = os.getenv("ZOTERO_API_KEY")
    semantic_scholar_api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")

    items = get_items_added_this_week(zotero_api_key)
    item_ids = [item['data']['key'] for item in items]

    recommendations = get_recommendations(semantic_scholar_api_key, item_ids)

    for recommendation in recommendations['recommendedPapers']:
        print(f"Title: {recommendation['title']}")
        print(f"Authors: {', '.join(author['name'] for author in recommendation['authors'])}")
        print(f"URL: {recommendation['url']}")
        print()


if __name__ == "__main__":
    main()
