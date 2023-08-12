
import time
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

BASE_URL = "https://magiceden.io/item-details/polygon/0x3c178321f5bc73494046a46b5a065f9211b7c65e/{}"

def refresh_nft_metadata(driver, nft_range, filter_unrevealed=None):
    # Load NFTs from unrevealed.txt if filter_unrevealed is set
    if filter_unrevealed:
        with open("unrevealed.txt", "r") as file:
            unrevealed_nfts = set(map(int, file.readlines()))
        nft_range = [i for i in nft_range if i in unrevealed_nfts]

    for i in nft_range:
        url = BASE_URL.format(i)
        driver.get(url)

        try:
            # Wait up to 20 seconds for the button to be clickable
            refresh_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'svg[xmlns="http://www.w3.org/2000/svg"][style="color: rgb(228, 37, 117);"]'))
            )
            refresh_button.click()
            print(f"Metadata refreshed: {i}")

        except TimeoutException as te:
            print(f"Timeout occurred on NFT {i}: {te}")
        except WebDriverException as we:
            print(f"WebDriver error occurred on NFT {i}: {we}")

        # Wait for 3 seconds before loading the next page
        time.sleep(3)

def main(start_nft, end_nft, filter_unrevealed=None):
    # Safari's driver comes built-in, no need to specify a path
    driver = webdriver.Safari()

    nft_range = range(start_nft, end_nft+1)
    refresh_nft_metadata(driver, nft_range, filter_unrevealed)

    driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Refresh Arkadians Metadata on OnePlanet')
    parser.add_argument('start_nft', type=int, help='Start of the NFT range')
    parser.add_argument('end_nft', type=int, help='End of the NFT range')
    parser.add_argument('--filter-unrevealed', action='store_true', help='Filter by NFTs from unrevealed.txt')

    args = parser.parse_args()

    main(args.start_nft, args.end_nft, args.filter_unrevealed)
