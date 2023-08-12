
import argparse
from refresh_OpenSea import run_open_sea
from refresh_MagicEden import run_magic_eden
from refresh_OnePlanet import run_one_planet

def main():
    parser = argparse.ArgumentParser(description='Run NFT Metadata Refresh Scripts')
    parser.add_argument('start_nft', type=int, help='Start of the NFT range')
    parser.add_argument('end_nft', type=int, help='End of the NFT range')
    parser.add_argument('--filter-unrevealed', action='store_true', help='Filter by NFTs from unrevealed.txt')
    parser.add_argument('--script', choices=['all', 'magic_eden', 'open_sea', 'one_planet'], default='all', help='Choose which script to run')

    args = parser.parse_args()

    if args.script in ['all', 'open_sea']:
        print("Refreshing Metadata OpenSea !!!")
        run_open_sea(args.start_nft, args.end_nft, args.filter_unrevealed)
    if args.script in ['all', 'magic_eden']:
        print("Refreshing Metadata MagicEden !!!")
        run_magic_eden(args.start_nft, args.end_nft, args.filter_unrevealed)
    if args.script in ['all', 'one_planet']:
        print("Refreshing Metadata OnePlanet !!!")
        run_one_planet(args.start_nft, args.end_nft, args.filter_unrevealed)

if __name__ == "__main__":
    main()
