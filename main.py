
import time
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

BASE_URL = "https://www.oneplanetnft.io/nfts/0x3c178321f5bc73494046a46b5a065f9211b7c65e/{}"

def refresh_nft_metadata(driver, nft_range):
    for i in nft_range:
        url = BASE_URL.format(i)
        driver.get(url)

        try:
            # Wait up to 20 seconds for the button to be clickable
            refresh_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-btn-type="refresh"]'))
            )
            refresh_button.click()

            # Wait for 3 seconds after clicking the button
            time.sleep(3)
            print(f"Metadata refreshed: {i}")

        except TimeoutException as te:
            print(f"Timeout occurred on NFT {i}: {te}")
        except WebDriverException as we:
            print(f"WebDriver error occurred on NFT {i}: {we}")

        # Wait for 3 seconds before loading the next page
        time.sleep(3)

def main(start_nft, end_nft):
    # Safari's driver comes built-in, no need to specify a path
    driver = webdriver.Safari()

    nft_range = range(start_nft, end_nft+1)
    refresh_nft_metadata(driver, nft_range)

    driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Refresh NFT Metadata')
    parser.add_argument('start_nft', type=int, help='Start of the NFT range')
    parser.add_argument('end_nft', type=int, help='End of the NFT range')

    args = parser.parse_args()

    main(args.start_nft, args.end_nft)
