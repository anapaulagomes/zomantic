from zomantic.semantic_scholar import get_paper_ids, store_papers_in_semantic_scholar_library
from zomantic.zotero import fetch_all_items_from_zotero, filter_articles_without_extra_key, \
    add_semantic_scholar_ids_to_items
import re


def get_all_paper_urls(all_items, updated_items):
    urls = []
    pattern = re.compile(r'Semantic Scholar ID\: (.*)$')
    for zotero_key, zotero_item in all_items.items():
        if updated_items.get(zotero_key):
            all_items[zotero_key] = updated_items[zotero_key]
        all_items[zotero_key]['data']['extra']
        match = pattern.search(zotero_item['data']['extra'])
        urls.append(f'https://www.semanticscholar.org/paper/{match.group(1)}')
    return urls


def main():
    all_items = fetch_all_items_from_zotero()

    filtered_articles = filter_articles_without_extra_key(all_items, 'Semantic Scholar ID')
    zotero_semantic_scholar_ids = get_paper_ids(filtered_articles)
    updated_items = add_semantic_scholar_ids_to_items(zotero_semantic_scholar_ids)

    urls = get_all_paper_urls(all_items, updated_items)

    store_papers_in_semantic_scholar_library(urls)


if __name__ == "__main__":
    main()
