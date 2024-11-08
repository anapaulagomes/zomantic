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
            f'query={item["data"]["title"]}&fields=title,url,paperId',
        )
        if response.ok:
            data = response.json()
            if data:
                items_paper_ids[zotero_key] = {
                    'paper_id': data['data'][0]['paperId'],
                    'url': data['data'][0]['url'],
                    'item': item
                }
    return items_paper_ids


def store_papers_in_semantic_scholar_library(items):
    is_semantic_scholar_logged_in, driver = login()
    if not is_semantic_scholar_logged_in:
        raise Exception("Could not login to Semantic Scholar")

    print(f'Attempt to store {len(items)} items...')
    count = 0
    for item in items:
        url = item['data']['url']
        print(url)
        driver.get(url)
        WebDriverWait(driver, 10).until(expected_conditions.url_to_be(url))

        try:
            save_field = driver.find_element(By.XPATH, "//span[text()='Save to Library']")
            save_field.click()
            WebDriverWait(driver, 10).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, "//span[text()='In Library']")
                )
            )
            close_button = driver.find_element(By.XPATH, '//button[contains(@class, "shelf__close-button')
            close_button.click()
            count += 1
        except NoSuchElementException as e:
            print(e)

    print(f'Finished saving papers to Semantic Scholar Library. Attempted to save {count} papers.')
    print('Check them out: https://www.semanticscholar.org/me/library/all')
