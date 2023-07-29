import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Safari's driver comes built-in, no need to specify a path
driver = webdriver.Safari()

for i in range(1, 1001):
    url = f"https://www.oneplanetnft.io/nfts/0x3c178321f5bc73494046a46b5a065f9211b7c65e/{i}"
    driver.get(url)

    try:
        # wait up to 10 seconds for the button to be clickable
        refresh_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-btn-type="refresh"]'))
        )
        refresh_button.click()
        
        # wait for 10 seconds after clicking the button
        time.sleep(10)
        print(f"Metadata refreshed: {i}")
        
    except Exception as e:
        print(f"An error occurred on NFT {i}: {e}")

    # wait for 5 seconds before loading the next page
    time.sleep(5)

driver.quit()

