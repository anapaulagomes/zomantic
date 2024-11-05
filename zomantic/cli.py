from zomantic.semantic_scholar import login as semantic_scholar_login


def main():
    is_semantic_scholar_logged_in, driver = semantic_scholar_login()
    print(is_semantic_scholar_logged_in, driver)


if __name__ == "__main__":
    main()
