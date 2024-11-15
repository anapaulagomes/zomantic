import random

import requests
from dotenv import load_dotenv
import os

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time

load_dotenv()

options = webdriver.FirefoxOptions()
options.add_argument("-headless")


def login():
    driver = webdriver.Firefox(options=options)
    driver.get('https://www.semanticscholar.org/me/library/all')
    is_logged_in = False
    try:
        login_button = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, "//span[text()='Sign In']"))
        )

        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.XPATH, "//input[@type='password']")

        email_field.send_keys(os.getenv("SEMANTIC_SCHOLAR_LOGIN"))
        password_field.send_keys(os.getenv("SEMANTIC_SCHOLAR_PASSWORD"))

        password_field.send_keys(Keys.RETURN)

        login_button.click()
    except Exception as e:
        print("Login button not found:", e)
        time.sleep(5)
        driver.quit()
    else:
        WebDriverWait(driver, 10).until(expected_conditions.url_to_be("https://www.semanticscholar.org/me/library/all"))
        WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, '//h1[contains(@class, "research__page-header__headline")]')
            )
        )
        print('Logged in successfully')
        is_logged_in = True
    return is_logged_in, driver


def get_paper_ids(items):
    """Search for a paper on Semantic Scholar and return its ID and title.
    The API returns up to 500 papers at time."""
    items_paper_ids = {}
    for zotero_key, item in items.items():
        response = requests.get(
            f'https://api.semanticscholar.org/graph/v1/paper/search/match?'
            f'query={item["data"]["title"]}&fields=title,paperId',
        )
        if response.ok:
            data = response.json()
            if data:
                paper_id = data['data'][0].get('paperId')
                items_paper_ids[zotero_key] = {
                    'paper_id': paper_id,
                    'item': item
                }
    return items_paper_ids


def store_papers_in_semantic_scholar_library(papers):
    print(f'Attempt to store {len(papers)} items...')
    count = 0
    for paper in papers:
        print(paper['url'])
        response = make_request(paper['paper_id'], paper['title'])
        if response.ok:
            count += 1
        time.sleep(random.randint(1, 3))

    print(f'Finished saving papers to Semantic Scholar Library. Attempted to save {count} papers.')
    print('Check them out: https://www.semanticscholar.org/me/library/all')


def make_request(paper_id, paper_title):
    url = "https://www.semanticscholar.org/api/1/library/folders/entries/bulk"
    headers = {
        "Host": "www.semanticscholar.org",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:129.0) Gecko/20100101 Firefox/129.0",
        "Accept": "*/*",
        "Accept-Language": "pt-BR,en-US;q=0.8,en;q=0.5,de;q=0.3",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Prefer": "safe",
        "Cache-Control": "no-cache,no-store,must-revalidate,max-age=-1",
        "Content-Type": "application/json",
        "X-S2-UI-Version": "8c3d74bcd9b3357febf74868a2a34ed576c6fd0b",
        "X-S2-Client": "webapp-browser",
        "Origin": "https://www.semanticscholar.org",
        "Referer": url,
        "Cookie": (),  # TODO test without cookies
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=0",
        "TE": "trailers",
    }

    data = {
        "paperId": paper_id,
        "paperTitle": paper_title,
        "folderIds": [],
        "annotationState": None,
        "sourceType": "Library"
    }

    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    return response
