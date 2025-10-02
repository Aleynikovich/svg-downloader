#!/usr/bin/env python3
"""
Simple tests to verify the SVG downloader structure and imports.
"""

import sys
import os

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        import config
        print("✓ config module imported successfully")
        
        # Check config values
        assert hasattr(config, 'DOWNLOAD_DIR')
        assert hasattr(config, 'DEFAULT_TIMEOUT')
        assert hasattr(config, 'HEADLESS')
        print("✓ config has required attributes")
        
    except Exception as e:
        print(f"✗ Error importing config: {e}")
        return False
    
    try:
        from svg_downloader import SVGDownloader
        print("✓ SVGDownloader class imported successfully")
        
        # Check class methods
        assert hasattr(SVGDownloader, 'start_browser')
        assert hasattr(SVGDownloader, 'close_browser')
        assert hasattr(SVGDownloader, 'navigate_to_page')
        assert hasattr(SVGDownloader, 'extract_svg_links')
        assert hasattr(SVGDownloader, 'download_svg')
        assert hasattr(SVGDownloader, 'download_from_collection')
        print("✓ SVGDownloader has required methods")
        
    except Exception as e:
        print(f"✗ Error importing SVGDownloader: {e}")
        return False
    
    return True


def test_config_values():
    """Test that config values are reasonable."""
    print("\nTesting config values...")
    
    import config
    
    # Check download directory
    assert isinstance(config.DOWNLOAD_DIR, str)
    assert len(config.DOWNLOAD_DIR) > 0
    print(f"✓ DOWNLOAD_DIR = {config.DOWNLOAD_DIR}")
    
    # Check timeout values
    assert isinstance(config.DEFAULT_TIMEOUT, int)
    assert config.DEFAULT_TIMEOUT > 0
    print(f"✓ DEFAULT_TIMEOUT = {config.DEFAULT_TIMEOUT}")
    
    # Check headless flag
    assert isinstance(config.HEADLESS, bool)
    print(f"✓ HEADLESS = {config.HEADLESS}")
    
    # Check user agent
    assert isinstance(config.USER_AGENT, str)
    assert len(config.USER_AGENT) > 0
    print(f"✓ USER_AGENT is set")
    
    return True


def test_main_script():
    """Test that main script can be invoked."""
    print("\nTesting main script...")
    
    import subprocess
    
    result = subprocess.run(
        [sys.executable, 'main.py', '--help'],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✓ main.py --help executed successfully")
        
        # Check that help contains expected text
        assert 'SVG' in result.stdout or 'svg' in result.stdout.lower()
        assert 'url' in result.stdout.lower()
        assert '--max-downloads' in result.stdout
        print("✓ Help text contains expected content")
        
        return True
    else:
        print(f"✗ main.py --help failed with code {result.returncode}")
        print(result.stderr)
        return False


def test_file_structure():
    """Test that all required files exist."""
    print("\nTesting file structure...")
    
    required_files = [
        'config.py',
        'svg_downloader.py',
        'main.py',
        'example_usage.py',
        'requirements.txt',
        '.gitignore',
        'README.md'
    ]
    
    for filename in required_files:
        if os.path.exists(filename):
            print(f"✓ {filename} exists")
        else:
            print(f"✗ {filename} missing")
            return False
    
    return True


def main():
    """Run all tests."""
    print("=" * 50)
    print("SVG Downloader - Structure Tests")
    print("=" * 50)
    print()
    
    tests = [
        test_file_structure,
        test_imports,
        test_config_values,
        test_main_script
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            failed += 1
    
    print()
    print("=" * 50)
    print(f"Tests passed: {passed}/{len(tests)}")
    print(f"Tests failed: {failed}/{len(tests)}")
    print("=" * 50)
    
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
