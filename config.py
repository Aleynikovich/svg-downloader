"""Configuration for SVG downloader."""

import os

# Download settings
DOWNLOAD_DIR = "downloaded_svgs"
DEFAULT_TIMEOUT = 30000  # 30 seconds in milliseconds
PAGE_LOAD_WAIT = 2000    # 2 seconds in milliseconds

# Browser settings
HEADLESS = True
SLOW_MO = 100  # Slow down operations by 100ms to appear more human-like

# Retry settings
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

# User agent to use
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Create download directory if it doesn't exist
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
