import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Safari's driver comes built-in, no need to specify a path
driver = webdriver.Safari()

# nfts = [11, 15, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 51, 52, 53, 55, 69, 93, 95, 113, 140, 141, 146, 147, 150, 155, 167, 173, 175, 210, 221, 229, 234, 236, 238, 240, 243, 297, 324, 328, 331, 333, 363, 365, 374, 377, 394, 396, 449, 454, 464, 466, 468, 470, 472, 479, 489, 491, 493, 499, 514, 521, 523, 533, 539, 547, 619, 622, 624, 631, 636, 726, 734, 737, 741, 744, 784, 786, 807, 811, 830, 900, 903, 907, 921, 925, 968, 970, 972, 977, 980, 981, 982, 983, 985, 989, 991, 994, 997, 999, 1000]
# nfts = [174, 204, 214, 351, 353, 153, 355, 460, 462, 315, 495, 497, 573, 597, 332, 703, 447, 710, 732, 736, 770, 891, 896, 487, 904, 489, 953, 955, 956, 960]
# nfts = [114]
# for i in nfts:
for i in range(701, 801):
    url = f"https://www.oneplanetnft.io/nfts/0x3c178321f5bc73494046a46b5a065f9211b7c65e/{i}"
    driver.get(url)

    try:
        # wait up to 20 seconds for the button to be clickable
        refresh_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-btn-type="refresh"]'))
        )
        refresh_button.click()
        
        # wait for 10 seconds after clicking the button
        time.sleep(3)
        print(f"Metadata refreshed: {i}")
        
    except Exception as e:
        print(f"An error occurred on NFT {i}: {e}")

    # wait for 5 seconds before loading the next page
    time.sleep(3)

driver.quit()

