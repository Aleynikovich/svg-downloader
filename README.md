# SVG Downloader

A Python tool for automatically downloading SVG files from websites with anti-scraping and anti-bot protection.

## Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get started in 5 minutes
- **[Technical Documentation](TECHNICAL.md)** - Deep dive into anti-bot techniques
- **[Example Usage](example_usage.py)** - Programmatic usage examples

## Features

- **Anti-Bot Protection Handling**: Uses Playwright with anti-detection techniques to bypass basic bot protection
- **Multiple Extraction Strategies**: Employs both static HTML parsing and interactive page interaction to find SVG download links
- **Intelligent Scrolling**: Automatically scrolls pages to load lazy-loaded content
- **Retry Logic**: Built-in retry mechanism for handling temporary failures
- **Human-like Behavior**: Configurable delays and randomization to mimic human browsing patterns
- **Flexible Configuration**: Customizable download limits, browser settings, and more

## Use Cases

This tool is designed for downloading SVGs from collections like:
- https://www.svgrepo.com/collection/company-logo/
- Other SVG gallery/collection sites with similar structures

## Requirements

- Python 3.7+
- Playwright browser automation library
- BeautifulSoup4 for HTML parsing

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Aleynikovich/svg-downloader.git
cd svg-downloader
```

2. Install Python dependencies:

playwright==1.40.0
requests==2.31.0
beautifulsoup4==4.12.2
lxml==4.9.3

If your distro does not allow to run system-wide pip install, create a venv before running:

```bash
pip install -r requirements.txt
```

Or install them manually (Arch):

```bash
pacman -S python-playwright python-requests python-beautifulsoup4 python-lxml
```

3. Install Playwright browsers:
```bash
playwright install chromium
```

## Usage

### Basic Usage

Download all SVGs from a collection:
```bash
python main.py "https://www.svgrepo.com/collection/company-logo/"
```

### Advanced Usage

Download only 10 SVGs:
```bash
python main.py "https://www.svgrepo.com/collection/company-logo/" --max-downloads 10
```

Run with visible browser (for debugging):
```bash
python main.py "https://www.svgrepo.com/collection/company-logo/" --no-headless
```

Adjust speed (slower can help with detection):
```bash
python main.py "https://www.svgrepo.com/collection/company-logo/" --slow-mo 200
```

### Command Line Options

- `url`: (Required) URL of the SVG collection page
- `--max-downloads N`: Maximum number of SVGs to download (default: all)
- `--headless`: Run browser in headless mode (default: True)
- `--no-headless`: Run browser with visible UI (useful for debugging)
- `--slow-mo N`: Slow down operations by N milliseconds (default: 100)

## Configuration

Edit `config.py` to customize:

- `DOWNLOAD_DIR`: Directory where SVGs will be saved (default: "downloaded_svgs")
- `DEFAULT_TIMEOUT`: Page load timeout in milliseconds (default: 30000)
- `PAGE_LOAD_WAIT`: Wait time after page load in milliseconds (default: 2000)
- `HEADLESS`: Whether to run browser in headless mode (default: True)
- `SLOW_MO`: Default slow-mo delay in milliseconds (default: 100)
- `MAX_RETRIES`: Number of retry attempts for failed operations (default: 3)
- `USER_AGENT`: Browser user agent string

## How It Works

### Anti-Bot Protection Techniques

The tool implements several strategies to bypass anti-bot protection:

1. **Browser Fingerprint Masking**:
   - Sets realistic user agent
   - Removes webdriver flag
   - Configures proper viewport size
   - Sets locale and timezone

2. **Human-like Behavior**:
   - Introduces delays between actions
   - Scrolls page naturally
   - Uses slow-mo to pace interactions

3. **Smart Retry Logic**:
   - Retries failed requests with exponential backoff
   - Detects CAPTCHA/blocking pages

### Extraction Strategies

The tool uses multiple methods to find SVG download links:

1. **Static HTML Analysis**:
   - Parses page HTML with BeautifulSoup
   - Finds direct `.svg` links
   - Locates download buttons and links

2. **Interactive Extraction**:
   - Clicks on SVG items to reveal download options
   - Scrolls to load lazy-loaded content
   - Handles modal dialogs and popups

3. **Fallback Mechanisms**:
   - Tries multiple CSS selectors
   - Searches for data attributes
   - Follows common SVG gallery patterns

## Project Structure

```
svg-downloader/
├── main.py              # Main CLI script
├── svg_downloader.py    # Core downloader implementation
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore patterns
├── README.md           # This file
└── downloaded_svgs/    # Downloaded SVG files (created automatically)
```

## Example Output

```
SVG Downloader
==================================================
Target URL: https://www.svgrepo.com/collection/company-logo/
Max downloads: 10
Headless mode: True
==================================================

2024-01-01 12:00:00 - INFO - Starting browser...
2024-01-01 12:00:02 - INFO - Browser started successfully
2024-01-01 12:00:02 - INFO - Starting download from collection: https://...
2024-01-01 12:00:02 - INFO - Navigating to https://... (attempt 1/3)
2024-01-01 12:00:05 - INFO - Successfully navigated to page
2024-01-01 12:00:08 - INFO - Found 10 potential SVG links
2024-01-01 12:00:08 - INFO - Attempting to download 10 SVGs...
2024-01-01 12:00:08 - INFO - Downloading 1/10: https://...
2024-01-01 12:00:09 - INFO - Downloaded: logo1.svg
...
2024-01-01 12:00:20 - INFO - Successfully downloaded 10/10 SVGs
2024-01-01 12:00:20 - INFO - Browser closed

==================================================
Download complete! Successfully downloaded 10 SVGs
==================================================
```

## Troubleshooting

### No SVGs Found

If the tool reports no SVGs found:

1. Run with `--no-headless` to see what the browser is doing
2. Check if the site structure has changed (update selectors in `svg_downloader.py`)
3. Try increasing `--slow-mo` value to give the page more time to load
4. Check if the site requires login or has stronger bot protection

### CAPTCHA/Bot Detection

If you encounter CAPTCHA or bot detection:

1. Increase the `SLOW_MO` value to appear more human-like
2. Add more randomization to delays
3. Try running with `--no-headless` and manually solve CAPTCHA
4. Consider using residential proxies (not implemented in this version)

### Download Failures

If downloads fail:

1. Check your internet connection
2. Verify the URL is accessible
3. Look at the logs for specific error messages
4. Try reducing `--max-downloads` to download fewer files

## Limitations

- Does not handle CAPTCHA challenges automatically
- May not work with sites that have advanced bot detection (e.g., Cloudflare Turnstile)
- Effectiveness depends on the specific site structure
- Requires adjusting selectors for different websites

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

This project is open source and available under the MIT License.

## Disclaimer

This tool is for educational purposes. Always respect websites' terms of service and robots.txt. Use responsibly and ethically. Some websites may prohibit automated access - please review and comply with their policies.