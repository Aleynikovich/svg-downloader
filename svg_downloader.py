"""
SVG Downloader with anti-bot protection handling.

This module provides functionality to download SVGs from websites that have
anti-scraping and anti-bot protection using Playwright for browser automation.
"""

import os
import time
import logging
from pathlib import Path
from typing import List, Optional
from urllib.parse import urljoin, urlparse
import re

from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
from bs4 import BeautifulSoup

from config import (
    DOWNLOAD_DIR,
    DEFAULT_TIMEOUT,
    PAGE_LOAD_WAIT,
    HEADLESS,
    SLOW_MO,
    MAX_RETRIES,
    RETRY_DELAY,
    USER_AGENT
)


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SVGDownloader:
    """Downloads SVGs from websites with anti-bot protection."""

    def __init__(self, headless: bool = HEADLESS, slow_mo: int = SLOW_MO):
        """
        Initialize the SVG downloader.

        Args:
            headless: Whether to run browser in headless mode
            slow_mo: Milliseconds to slow down operations to appear more human-like
        """
        self.headless = headless
        self.slow_mo = slow_mo
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    def __enter__(self):
        """Context manager entry."""
        self.start_browser()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close_browser()

    def start_browser(self):
        """Start the Playwright browser."""
        logger.info("Starting browser...")
        self.playwright = sync_playwright().start()
        
        # Launch browser with anti-detection settings
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            slow_mo=self.slow_mo,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox'
            ]
        )
        
        # Create context with realistic settings
        self.context = self.browser.new_context(
            user_agent=USER_AGENT,
            viewport={'width': 1920, 'height': 1080},
            locale='en-US',
            timezone_id='America/New_York',
        )
        
        # Add script to mask automation
        self.context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        self.page = self.context.new_page()
        self.page.set_default_timeout(DEFAULT_TIMEOUT)
        logger.info("Browser started successfully")

    def close_browser(self):
        """Close the browser and clean up resources."""
        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if hasattr(self, 'playwright'):
            self.playwright.stop()
        logger.info("Browser closed")

    def navigate_to_page(self, url: str, retries: int = MAX_RETRIES) -> bool:
        """
        Navigate to a URL with retry logic.

        Args:
            url: The URL to navigate to
            retries: Number of retry attempts

        Returns:
            True if navigation successful, False otherwise
        """
        for attempt in range(retries):
            try:
                logger.info(f"Navigating to {url} (attempt {attempt + 1}/{retries})")
                self.page.goto(url, wait_until='domcontentloaded')
                
                # Wait for page to load
                time.sleep(PAGE_LOAD_WAIT / 1000)
                
                # Check if we're blocked
                page_content = self.page.content().lower()
                if any(keyword in page_content for keyword in ['captcha', 'blocked', 'access denied']):
                    logger.warning("Potential bot detection on page")
                    if attempt < retries - 1:
                        time.sleep(RETRY_DELAY * (attempt + 1))
                        continue
                
                logger.info("Successfully navigated to page")
                return True
                
            except Exception as e:
                logger.error(f"Error navigating to page: {e}")
                if attempt < retries - 1:
                    time.sleep(RETRY_DELAY)
                    continue
                    
        return False

    def extract_svg_links(self, url: str) -> List[str]:
        """
        Extract SVG download links from a collection page.

        Args:
            url: The collection page URL

        Returns:
            List of SVG download URLs
        """
        if not self.navigate_to_page(url):
            logger.error("Failed to navigate to page")
            return []

        # Wait for SVGs to load
        try:
            # Wait for common SVG container elements
            self.page.wait_for_selector('svg, img[src*=".svg"], a[href*=".svg"]', timeout=10000)
        except Exception as e:
            logger.warning(f"Timeout waiting for SVG elements: {e}")

        # Get page content
        content = self.page.content()
        soup = BeautifulSoup(content, 'lxml')
        
        svg_links = []
        
        # Strategy 1: Find direct SVG links
        for link in soup.find_all('a', href=True):
            href = link['href']
            if '.svg' in href or 'download' in href.lower():
                full_url = urljoin(url, href)
                svg_links.append(full_url)
        
        # Strategy 2: Find SVG preview images and try to get download links
        for img in soup.find_all('img', src=True):
            if '.svg' in img['src']:
                full_url = urljoin(url, img['src'])
                svg_links.append(full_url)
        
        # Strategy 3: Look for data attributes or specific patterns
        for element in soup.find_all(attrs={'data-svg': True}):
            svg_url = element.get('data-svg')
            if svg_url:
                full_url = urljoin(url, svg_url)
                svg_links.append(full_url)
        
        # Remove duplicates
        svg_links = list(set(svg_links))
        
        logger.info(f"Found {len(svg_links)} potential SVG links")
        return svg_links

    def extract_svg_links_interactive(self, url: str) -> List[str]:
        """
        Extract SVG download links by interacting with the page.
        
        This method clicks on SVG items to reveal download buttons/links.
        
        Args:
            url: The collection page URL
            
        Returns:
            List of SVG download URLs
        """
        if not self.navigate_to_page(url):
            logger.error("Failed to navigate to page")
            return []
        
        svg_links = []
        
        try:
            # Wait for page to be ready
            self.page.wait_for_load_state('networkidle', timeout=10000)
            
            # Scroll to load lazy-loaded content
            logger.info("Scrolling to load all content...")
            self._scroll_to_bottom()
            
            # Find all SVG item containers (adjust selectors based on actual site)
            # Common patterns for SVG gallery sites
            selectors = [
                '.svg-item',
                '.icon-item', 
                'div[class*="svg"]',
                'div[class*="icon"]',
                'a[href*="/svg/"]',
                'a[href*="/download/"]'
            ]
            
            for selector in selectors:
                try:
                    elements = self.page.query_selector_all(selector)
                    if elements:
                        logger.info(f"Found {len(elements)} elements with selector: {selector}")
                        
                        for i, element in enumerate(elements[:50]):  # Limit to first 50 to avoid timeout
                            try:
                                # Click to reveal download options
                                element.click(timeout=2000)
                                time.sleep(0.5)
                                
                                # Look for download button/link
                                download_selectors = [
                                    'a[download]',
                                    'button[class*="download"]',
                                    'a[class*="download"]',
                                    'a[href*=".svg"]'
                                ]
                                
                                for dl_selector in download_selectors:
                                    dl_element = self.page.query_selector(dl_selector)
                                    if dl_element:
                                        href = dl_element.get_attribute('href')
                                        if href:
                                            full_url = urljoin(url, href)
                                            svg_links.append(full_url)
                                            break
                                
                                # Close modal/popup if it appeared
                                close_selectors = ['button[class*="close"]', '.modal-close', '[aria-label="Close"]']
                                for close_sel in close_selectors:
                                    try:
                                        close_btn = self.page.query_selector(close_sel)
                                        if close_btn and close_btn.is_visible():
                                            close_btn.click(timeout=1000)
                                            break
                                    except:
                                        pass
                                        
                            except Exception as e:
                                logger.debug(f"Error processing element {i}: {e}")
                                continue
                        
                        break  # Found elements with one selector, no need to try others
                        
                except Exception as e:
                    logger.debug(f"No elements found for selector {selector}: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Error in interactive extraction: {e}")
        
        # Remove duplicates
        svg_links = list(set(svg_links))
        logger.info(f"Found {len(svg_links)} SVG links via interactive method")
        return svg_links

    def _scroll_to_bottom(self):
        """Scroll to the bottom of the page to load lazy-loaded content."""
        try:
            previous_height = self.page.evaluate("document.body.scrollHeight")
            
            while True:
                # Scroll down
                self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(1)
                
                # Calculate new height
                new_height = self.page.evaluate("document.body.scrollHeight")
                
                if new_height == previous_height:
                    break
                    
                previous_height = new_height
                
        except Exception as e:
            logger.warning(f"Error during scrolling: {e}")
    
    def _filter_svg_links(self, svg_links: List[str]) -> List[str]:
        """Filter out unwanted SVG links like the site's own logo."""
        filtered_links = []
        
        for link in svg_links:
            # Skip the site's own logo
            if link.lower().endswith('/logo.svg') or link.lower() == 'logo.svg':
                logger.info(f"Skipping site logo: {link}")
                continue
                
            filtered_links.append(link)
        
        return filtered_links
    
    def _has_valid_svgs(self, svg_links: List[str]) -> bool:
        """Check if the page has valid SVGs (not just the site logo)."""
        filtered_links = self._filter_svg_links(svg_links)
        return len(filtered_links) > 0
    
    def _build_page_url(self, base_url: str, page_number: int) -> str:
        """Build URL for a specific page number."""
        # Remove trailing slash and page number if present
        base_url = base_url.rstrip('/')
        
        # Remove existing page number from URL
        base_url = re.sub(r'/\d+$', '', base_url)
        
        if page_number == 1:
            return base_url + '/'
        else:
            return f"{base_url}/{page_number}"

    def download_svg(self, url: str, filename: Optional[str] = None) -> bool:
        """
        Download a single SVG file.

        Args:
            url: The URL of the SVG to download
            filename: Optional custom filename (will be generated from URL if not provided)

        Returns:
            True if download successful, False otherwise
        """
        try:
            if not filename:
                # Generate filename from URL
                parsed = urlparse(url)
                filename = os.path.basename(parsed.path)
                if not filename.endswith('.svg'):
                    filename = f"{filename}.svg"
            
            # Skip downloading logo.svg (site's own logo)
            if filename.lower() == 'logo.svg':
                logger.info(f"Skipping site logo: {filename}")
                return False
            
            filepath = os.path.join(DOWNLOAD_DIR, filename)
            
            # Skip if file already exists
            if os.path.exists(filepath):
                logger.info(f"File already exists, skipping: {filename}")
                return True
            
            # Navigate to the SVG URL
            response = self.page.goto(url)
            
            if response and response.ok:
                content = response.body()
                
                # Verify it's SVG content
                if content.startswith(b'<?xml') or content.startswith(b'<svg'):
                    with open(filepath, 'wb') as f:
                        f.write(content)
                    logger.info(f"Downloaded: {filename}")
                    return True
                else:
                    logger.warning(f"URL does not contain SVG content: {url}")
                    return False
            else:
                logger.error(f"Failed to download {url}: Response not OK")
                return False
                
        except Exception as e:
            logger.error(f"Error downloading {url}: {e}")
            return False

    def download_from_collection(self, collection_url: str, max_downloads: Optional[int] = None) -> int:
        """
        Download all SVGs from a collection, automatically handling multiple pages.

        Args:
            collection_url: The URL of the collection page
            max_downloads: Maximum number of SVGs to download (None for all)

        Returns:
            Number of successfully downloaded SVGs
        """
        logger.info(f"Starting download from collection: {collection_url}")
        
        total_downloaded = 0
        page_number = 1
        max_empty_pages = 3  # Stop after 3 consecutive pages with no valid SVGs
        empty_page_count = 0
        
        while True:
            # Build URL for current page
            page_url = self._build_page_url(collection_url, page_number)
            logger.info(f"Processing page {page_number}: {page_url}")
            
            # Try both extraction methods
            svg_links = self.extract_svg_links(page_url)
            
            if not svg_links:
                logger.info("Trying interactive extraction method...")
                svg_links = self.extract_svg_links_interactive(page_url)
            
            # Filter out unwanted links (like logo.svg)
            filtered_links = self._filter_svg_links(svg_links)
            
            # Check if this page has valid SVGs
            if not filtered_links:
                empty_page_count += 1
                logger.info(f"Page {page_number} has no valid SVGs (empty page count: {empty_page_count})")
                
                if empty_page_count >= max_empty_pages:
                    logger.info(f"Stopping after {max_empty_pages} consecutive empty pages")
                    break
                    
                page_number += 1
                continue
            else:
                empty_page_count = 0  # Reset counter when we find valid SVGs
            
            logger.info(f"Found {len(filtered_links)} valid SVGs on page {page_number}")
            
            # Apply max_downloads limit across all pages
            remaining_downloads = None
            if max_downloads is not None:
                remaining_downloads = max_downloads - total_downloaded
                if remaining_downloads <= 0:
                    logger.info(f"Reached maximum download limit of {max_downloads}")
                    break
                    
                if remaining_downloads < len(filtered_links):
                    filtered_links = filtered_links[:remaining_downloads]
            
            # Download SVGs from current page
            page_downloads = 0
            for i, svg_url in enumerate(filtered_links, 1):
                logger.info(f"Downloading page {page_number} - {i}/{len(filtered_links)}: {svg_url}")
                
                if self.download_svg(svg_url):
                    page_downloads += 1
                    total_downloaded += 1
                
                # Small delay between downloads
                time.sleep(0.5)
            
            logger.info(f"Downloaded {page_downloads}/{len(filtered_links)} SVGs from page {page_number}")
            
            # Check if we've reached the download limit
            if max_downloads is not None and total_downloaded >= max_downloads:
                logger.info(f"Reached maximum download limit of {max_downloads}")
                break
            
            # Move to next page
            page_number += 1
        
        logger.info(f"Collection download complete! Successfully downloaded {total_downloaded} SVGs from {page_number - 1} pages")
        return total_downloaded
