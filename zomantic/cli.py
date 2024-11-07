from zomantic.semantic_scholar import login as semantic_scholar_login, get_paper_ids
from zomantic.zotero import fetch_all_items_from_zotero, filter_articles_without_extra_key


def main():
    is_semantic_scholar_logged_in, driver = semantic_scholar_login()
    print(is_semantic_scholar_logged_in, driver)
    all_articles = fetch_all_items_from_zotero()
    filtered_articles = filter_articles_without_extra_key(all_articles, 'Semantic Scholar ID')
    #zotero_semantic_scholar_ids = get_paper_ids(filtered_articles)

    # TODO update zotero items with semantic scholar ids
    # TODO save the papers in the semantic scholar library
    # TODO show a summary of the process


if __name__ == "__main__":
    main()
