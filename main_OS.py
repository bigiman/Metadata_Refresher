# !!!!!  Code not working due to page security reasons

import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException

# Safari's driver comes built-in, no need to specify a path
driver = webdriver.Safari()

nfts = [175]
for i in nfts:
    url = f"https://opensea.io/assets/matic/0x3c178321f5bc73494046a46b5a065f9211b7c65e/{i}"
    driver.get(url)

    while True:
        try:
            # wait up to 10 seconds for the '...' button to be clickable
            more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="More"]'))
            )
            ActionChains(driver).move_to_element(more_button).perform()
            time.sleep(random.uniform(1.0, 2.0))  # pause for a random time
            more_button.click()
            break
        except StaleElementReferenceException:
            continue

    time.sleep(random.uniform(2.0, 3.0))  # pause for a random time

    while True:
        try:
            refresh_metadata_option = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.sc-29427738-0.sc-630fc9ab-0.sc-99655001-0.sc-4422a702-0.sc-d386f9ad-1'))
            )
            ActionChains(driver).move_to_element(refresh_metadata_option).perform()
            time.sleep(random.uniform(1.0, 2.0))  # pause for a random time
            refresh_metadata_option.click()
            break
        except StaleElementReferenceException:
            continue

    time.sleep(random.uniform(5.0, 10.0))  # pause for a random time

driver.quit()
