from zomantic.semantic_scholar import login as semantic_scholar_login
from zomantic.zotero import fetch_all_items_from_zotero


def main():
    is_semantic_scholar_logged_in, driver = semantic_scholar_login()
    print(is_semantic_scholar_logged_in, driver)
    all_articles = fetch_all_items_from_zotero()


if __name__ == "__main__":
    main()
