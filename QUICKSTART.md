# Quick Start Guide

This guide will help you get started with the SVG Downloader quickly.

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Playwright Browser

```bash
playwright install chromium
```

If you encounter dependency issues, try:

```bash
playwright install-deps chromium
playwright install chromium
```

## Basic Usage

### Download SVGs from a Collection

```bash
python main.py "https://www.svgrepo.com/collection/company-logo/"
```

### Download Limited Number of SVGs

```bash
python main.py "https://www.svgrepo.com/collection/company-logo/" --max-downloads 10
```

### Run with Visible Browser (Debug Mode)

```bash
python main.py "https://www.svgrepo.com/collection/company-logo/" --no-headless
```

## Common Issues

### Browser Not Installed

If you see an error about the browser not being installed:

```bash
playwright install chromium
```

### Permission Issues

If you get permission errors on Linux:

```bash
sudo playwright install-deps chromium
playwright install chromium
```

### Site Blocking/CAPTCHA

If the site is blocking you:

1. Try running with slower speed:
   ```bash
   python main.py "URL" --slow-mo 300
   ```

2. Run with visible browser to see what's happening:
   ```bash
   python main.py "URL" --no-headless
   ```

3. Check the logs for specific error messages

## Where Are My SVGs?

Downloaded SVGs are saved in the `downloaded_svgs/` directory in the current folder.

## Testing the Installation

Run the structure tests to verify everything is set up correctly:

```bash
python test_structure.py
```

## Programmatic Usage

See `example_usage.py` for examples of how to use the downloader in your own Python scripts.

## Getting Help

Run the help command to see all available options:

```bash
python main.py --help
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [example_usage.py](example_usage.py) for programmatic usage examples
- Modify [config.py](config.py) to customize default settings
