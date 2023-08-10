import time
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

BASE_URL = "https://opensea.io/assets/matic/0x3c178321f5bc73494046a46b5a065f9211b7c65e/{}"

def read_unrevealed(driver, nft_range):
    wait = WebDriverWait(driver, 30)  # Wait for up to 30 seconds

    for i in nft_range:
        url = BASE_URL.format(i)
        driver.get(url)

        try:
            # Wait for the page body to be loaded
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            
            # Get the entire page source
            page_source = driver.page_source

            # Check if the string "Unrevealed" is present in the page source
            if "Unrevealed" in page_source:
                with open("unrevealed_OS.txt", "a") as file:
                    file.write(str(i) + "\\n")
                print(f"Unrevealed Arkadian found: {i}")

        except TimeoutException as te:
            print(f"Timeout occurred on NFT {i}: {te}")
        except WebDriverException as we:
            print(f"WebDriver error occurred on NFT {i}: {we}")

        # Wait for 10 seconds before loading the next page
        time.sleep(10)

def main(start_nft, end_nft):
    # Safari's driver comes built-in, no need to specify a path
    driver = webdriver.Safari()

    nft_range = range(start_nft, end_nft+1)
    read_unrevealed(driver, nft_range)

    driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Read Unrevealed Arkadians from OpenSea')
    parser.add_argument('start_nft', type=int, help='Start of the NFT range')
    parser.add_argument('end_nft', type=int, help='End of the NFT range')

    args = parser.parse_args()

    main(args.start_nft, args.end_nft)
