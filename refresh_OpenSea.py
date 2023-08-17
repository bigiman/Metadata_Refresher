import requests
import time
import argparse

# Constants
OPENSEA_API_URL = "https://api.opensea.io/v2/collection/arkadians/nfts"
API_KEY = "56d27fddc7ba42b8b17eb06e3f7e9e91"  # Your API key

HEADERS = {
    "accept": "application/json",
    "X-API-KEY": API_KEY,
}


def fetch_assets_from_collection(start_nft, end_nft, filter_unrevealed=None):

    params = {
        "limit": "50",
    }
    assets = []
    
    while True:
        response = requests.get(OPENSEA_API_URL, headers=HEADERS, params=params)
        
        # Check if the response status is not 200 OK
        if response.status_code != 200:
            print(f"API call failed with status code: {response.status_code}")
            print(f"Response content: {response.text}")
            
            # Handle rate limiting (status code 429)
            if response.status_code == 429:
                try:
                    # Extract the expected wait time from the response
                    wait_time = int(response.json().get("detail", "").split(" ")[-2])
                    print(f"Rate limited. Waiting for {wait_time + 1} seconds.")
                    time.sleep(wait_time + 1)  # Sleep for the suggested time + 1 second buffer
                    continue  # Retry the request after waiting
                except:
                    print("Failed to extract wait time from rate limit response. Sleeping for default duration.")
                    time.sleep(10)  # Default sleep duration if extraction fails
                    continue
            
            break
        
        data = response.json()
        assets_in_page = data.get('nfts', [])
        
        # If there are no assets in the current page, break out of the loop
        if not assets_in_page:
            break
        
        assets.extend(assets_in_page)
        
        # Check if there's a cursor for the next page
        next_cursor = data.get('next')
        
        # If there's no next cursor, break out of the loop
        if not next_cursor:
            break
        
        # Update the 'next' parameter for the next iteration
        params["next"] = next_cursor
        
        time.sleep(2)  # Be kind to the API and avoid hitting rate limits
    
    return assets

def refresh_metadata(asset):
    # Assuming the V2 API has a similar endpoint for refreshing metadata
    chain = "matic"
    token_id = asset["identifier"]
    address = asset["contract"]
    url = f"https://api.opensea.io/v2/chain/{chain}/contract/{address}/nfts/{token_id}/refresh"
    response = requests.post(url, headers=HEADERS)
    return response.status_code == 200

def main(start_nft, end_nft, filter_unrevealed=None):
    assets = fetch_assets_from_collection(start_nft, end_nft, filter_unrevealed)
    print(f"Found {len(assets)} assets in the collection.")
    
    # Filtering assets based on the range
    filtered_assets = [asset for asset in assets if start_nft <= int(asset['identifier']) <= end_nft]
    
    # Further filtering based on "unrevealed.txt" if filter_unrevealed is set
    if filter_unrevealed:
        with open("unrevealed.txt", "r") as file:
            unrevealed_nfts = set(map(int, file.readlines()))
        filtered_assets = [asset for asset in filtered_assets if int(asset['identifier']) in unrevealed_nfts]
    
    for asset in filtered_assets:
        if refresh_metadata(asset):
            print(f"Successfully refreshed metadata for token_id: {asset['identifier']}")
        else:
            print(f"Failed to refresh metadata for token_id: {asset['identifier']}")
        time.sleep(2)  # Be kind to the API and avoid hitting rate limits

def run_open_sea(start_nft, end_nft, filter_unrevealed=False):
    # parser = argparse.ArgumentParser(description='Refresh Arkadians Metadata on OpenSea')
    # parser.add_argument('start_nft', type=int, help='Start of the NFT range')
    # parser.add_argument('end_nft', type=int, help='End of the NFT range')
    # parser.add_argument('--filter-unrevealed', action='store_true', help='Filter by NFTs from unrevealed.txt')

    # args = parser.parse_args()
    
    # main(args.start_nft, args.end_nft, args.filter_unrevealed)
    main(start_nft, end_nft, filter_unrevealed)
