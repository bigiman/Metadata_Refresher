
import time
import argparse
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

BASE_URL = "https://www.oneplanetnft.io/nfts/0x3c178321f5bc73494046a46b5a065f9211b7c65e/{}"

def show_nft(driver, nft_range, filter_newreveals=None):
    # Load NFTs from newreveals.txt if filter_newreveals is set
    if filter_newreveals:
        with open("newreveals.txt", "r") as file:
            newreveals_nfts = set(map(int, file.readlines()))
        nft_range = [i for i in nft_range if i in newreveals_nfts]

    for i in nft_range:
        url = BASE_URL.format(i)
        try:
            driver.get(url)        
        except WebDriverException as we:
            print(f"WebDriver error occurred on NFT {i}: {we}")

        # Wait for 3 seconds before loading the next page
        time.sleep(3)

def main(start_nft, end_nft, filter_newreveals=None):
    # Safari's driver comes built-in, no need to specify a path
    driver = webdriver.Safari()

    nft_range = range(start_nft, end_nft+1)
    show_nft(driver, nft_range, filter_newreveals)

    driver.quit()

def run_one_planet(start_nft, end_nft, filter_newreveals=False):
    parser = argparse.ArgumentParser(description='Show Arkadians on OnePlanet')
    parser.add_argument('start_nft', type=int, help='Start of the NFT range')
    parser.add_argument('end_nft', type=int, help='End of the NFT range')
    parser.add_argument('--filter-newreveals', action='store_true', help='Filter by NFTs from newreveals.txt')

    args = parser.parse_args()

    main(args.start_nft, args.end_nft, args.filter_newreveals)
