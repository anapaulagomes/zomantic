from zomantic.semantic_scholar import get_paper_ids, store_papers_in_semantic_scholar_library
from zomantic.zotero import fetch_all_items_from_zotero, filter_articles_without_extra_key, \
    add_semantic_scholar_ids_to_items
import re
import argparse


def get_all_papers(all_items, updated_items):
    papers = []
    pattern = re.compile(r'Semantic Scholar ID\: (.*)$')
    for zotero_key, zotero_item in all_items.items():
        if updated_items.get(zotero_key):
            all_items[zotero_key] = updated_items[zotero_key]

        match = pattern.search(all_items[zotero_key]['data']['extra'])
        paper_id = match.group(1)
        paper_info = {
            'title': zotero_item['data']['title'],
            'paper_id': paper_id
        }
        papers.append(paper_info)
    return papers


def main():
    parser = argparse.ArgumentParser(description='Store Zotero papers in Semantic Scholar library')
    parser.add_argument('-c', '--collection-name', type=str, help='Zotero collection name')
    args = parser.parse_args()
    all_items = fetch_all_items_from_zotero(collection_name=args.collection_name)

    filtered_articles = filter_articles_without_extra_key(all_items, 'Semantic Scholar ID')
    zotero_semantic_scholar_ids = get_paper_ids(filtered_articles)
    updated_items = add_semantic_scholar_ids_to_items(zotero_semantic_scholar_ids)

    urls = get_all_papers(all_items, updated_items)

    store_papers_in_semantic_scholar_library(urls)


if __name__ == "__main__":
    main()
