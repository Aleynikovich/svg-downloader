#!/usr/bin/env python3
"""
Main script to download SVGs from collections.

Usage:
    python main.py <collection_url> [--max-downloads N] [--headless/--no-headless]
    
Example:
    python main.py https://www.svgrepo.com/collection/company-logo/ --max-downloads 10
"""

import argparse
import sys
from svg_downloader import SVGDownloader
from config import HEADLESS


def main():
    """Main entry point for the SVG downloader."""
    parser = argparse.ArgumentParser(
        description='Download SVGs from collections with anti-bot protection handling'
    )
    
    parser.add_argument(
        'url',
        help='URL of the SVG collection page'
    )
    
    parser.add_argument(
        '--max-downloads',
        type=int,
        default=None,
        help='Maximum number of SVGs to download (default: all)'
    )
    
    parser.add_argument(
        '--headless',
        action='store_true',
        default=HEADLESS,
        help='Run browser in headless mode (default: True)'
    )
    
    parser.add_argument(
        '--no-headless',
        action='store_false',
        dest='headless',
        help='Run browser with visible UI'
    )
    
    parser.add_argument(
        '--slow-mo',
        type=int,
        default=100,
        help='Slow down operations by N milliseconds (default: 100)'
    )
    
    args = parser.parse_args()
    
    print(f"SVG Downloader")
    print(f"=" * 50)
    print(f"Target URL: {args.url}")
    print(f"Max downloads: {args.max_downloads or 'All'}")
    print(f"Headless mode: {args.headless}")
    print(f"=" * 50)
    print()
    
    try:
        with SVGDownloader(headless=args.headless, slow_mo=args.slow_mo) as downloader:
            count = downloader.download_from_collection(
                args.url,
                max_downloads=args.max_downloads
            )
            
            print()
            print(f"=" * 50)
            print(f"Download complete! Successfully downloaded {count} SVGs")
            print(f"=" * 50)
            
            return 0 if count > 0 else 1
            
    except KeyboardInterrupt:
        print("\nDownload interrupted by user")
        return 130
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
