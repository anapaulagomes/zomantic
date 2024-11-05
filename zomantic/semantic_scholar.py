from dotenv import load_dotenv
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time

load_dotenv()


options = webdriver.FirefoxOptions()
options.add_argument("-headless")
driver = webdriver.Firefox(options=options)

driver.get('https://www.semanticscholar.org/me/library/all')


def login():
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
