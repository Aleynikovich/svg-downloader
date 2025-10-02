#!/usr/bin/env python3
"""
Example script showing programmatic usage of the SVG downloader.

This demonstrates how to use the SVGDownloader class in your own Python code.
"""

from svg_downloader import SVGDownloader


def example_basic_download():
    """Example: Basic download from a collection."""
    print("Example 1: Basic Download")
    print("-" * 50)
    
    collection_url = "https://www.svgrepo.com/collection/company-logo/"
    
    with SVGDownloader(headless=True) as downloader:
        count = downloader.download_from_collection(
            collection_url,
            max_downloads=5  # Download only 5 SVGs for demo
        )
        print(f"\nDownloaded {count} SVGs")


def example_custom_settings():
    """Example: Download with custom settings."""
    print("\nExample 2: Custom Settings")
    print("-" * 50)
    
    collection_url = "https://www.svgrepo.com/collection/company-logo/"
    
    # Create downloader with visible browser and slower operations
    with SVGDownloader(headless=False, slow_mo=200) as downloader:
        count = downloader.download_from_collection(
            collection_url,
            max_downloads=3
        )
        print(f"\nDownloaded {count} SVGs")


def example_manual_control():
    """Example: Manual control over the download process."""
    print("\nExample 3: Manual Control")
    print("-" * 50)
    
    collection_url = "https://www.svgrepo.com/collection/company-logo/"
    
    with SVGDownloader() as downloader:
        # Navigate to the page
        if not downloader.navigate_to_page(collection_url):
            print("Failed to navigate to page")
            return
        
        # Extract links
        svg_links = downloader.extract_svg_links(collection_url)
        print(f"\nFound {len(svg_links)} SVG links")
        
        # Download specific SVGs
        if svg_links:
            print("\nDownloading first 3 SVGs...")
            for i, svg_url in enumerate(svg_links[:3], 1):
                print(f"  {i}. {svg_url}")
                success = downloader.download_svg(svg_url)
                if success:
                    print(f"     ✓ Downloaded")
                else:
                    print(f"     ✗ Failed")


def example_error_handling():
    """Example: Proper error handling."""
    print("\nExample 4: Error Handling")
    print("-" * 50)
    
    try:
        with SVGDownloader() as downloader:
            # Try to download from an invalid URL
            count = downloader.download_from_collection(
                "https://invalid-url-example.com/svgs/",
                max_downloads=1
            )
            
            if count == 0:
                print("No SVGs were downloaded (expected for invalid URL)")
            else:
                print(f"Downloaded {count} SVGs")
                
    except Exception as e:
        print(f"Caught error: {e}")


if __name__ == '__main__':
    print("SVG Downloader - Usage Examples")
    print("=" * 50)
    print()
    
    # Run examples
    # Note: Uncomment the examples you want to run
    
    # example_basic_download()
    # example_custom_settings()
    # example_manual_control()
    # example_error_handling()
    
    print("\nTo run examples, uncomment the desired example function calls in this script.")
    print("\nFor actual usage, run: python main.py <url>")
