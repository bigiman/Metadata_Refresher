import requests
import time

# Constants
OPENSEA_API_URL = "https://api.opensea.io/v2/collection/arkadians/nfts"
API_KEY = "56d27fddc7ba42b8b17eb06e3f7e9e91"  # Your API key

HEADERS = {
    "accept": "application/json",
    "X-API-KEY": API_KEY,
}

def fetch_assets_from_collection():
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

def main():
    assets = fetch_assets_from_collection()
    print(f"Found {len(assets)} assets in the collection.")
    
    for asset in assets:
        if refresh_metadata(asset):
            print(f"Successfully refreshed metadata for token_id: {asset['identifier']}")
        else:
            print(f"Failed to refresh metadata for token_id: {asset['identifier']}")
        time.sleep(2)  # Be kind to the API and avoid hitting rate limits

if __name__ == "__main__":
    main()
