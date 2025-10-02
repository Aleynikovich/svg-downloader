#!/usr/bin/env python3
"""
Troubleshooting script to diagnose common issues.
"""

import sys
import os
import subprocess


def check_python_version():
    """Check if Python version is compatible."""
    print("Checking Python version...")
    version = sys.version_info
    
    if version.major == 3 and version.minor >= 7:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} (compatible)")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (requires 3.7+)")
        return False


def check_dependencies():
    """Check if required dependencies are installed."""
    print("\nChecking dependencies...")
    
    dependencies = [
        'playwright',
        'requests',
        'bs4',
        'lxml'
    ]
    
    all_installed = True
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✓ {dep} installed")
        except ImportError:
            print(f"✗ {dep} not installed")
            all_installed = False
    
    return all_installed


def check_playwright_browsers():
    """Check if Playwright browsers are installed."""
    print("\nChecking Playwright browsers...")
    
    try:
        result = subprocess.run(
            ['playwright', 'install', '--dry-run', 'chromium'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        output = result.stdout + result.stderr
        
        if 'is already installed' in output.lower() or result.returncode == 0:
            print("✓ Chromium browser appears to be installed")
            return True
        else:
            print("✗ Chromium browser not installed")
            print("  Run: playwright install chromium")
            return False
            
    except subprocess.TimeoutExpired:
        print("⚠ Timeout checking browser installation")
        return False
    except FileNotFoundError:
        print("✗ playwright command not found")
        print("  Make sure playwright is installed: pip install playwright")
        return False
    except Exception as e:
        print(f"⚠ Error checking browsers: {e}")
        return False


def check_permissions():
    """Check file and directory permissions."""
    print("\nChecking permissions...")
    
    # Check if we can create download directory
    download_dir = "downloaded_svgs"
    
    try:
        os.makedirs(download_dir, exist_ok=True)
        print(f"✓ Can create/access {download_dir} directory")
        
        # Check if we can write to it
        test_file = os.path.join(download_dir, ".test_write")
        try:
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            print(f"✓ Can write to {download_dir} directory")
            return True
        except Exception as e:
            print(f"✗ Cannot write to {download_dir} directory: {e}")
            return False
            
    except Exception as e:
        print(f"✗ Cannot create {download_dir} directory: {e}")
        return False


def check_imports():
    """Check if our modules can be imported."""
    print("\nChecking module imports...")
    
    try:
        import config
        print("✓ config module imports successfully")
    except Exception as e:
        print(f"✗ config module import failed: {e}")
        return False
    
    try:
        from svg_downloader import SVGDownloader
        print("✓ SVGDownloader imports successfully")
    except Exception as e:
        print(f"✗ SVGDownloader import failed: {e}")
        return False
    
    return True


def check_network():
    """Check network connectivity."""
    print("\nChecking network connectivity...")
    
    try:
        import requests
        
        # Try to connect to a common site
        response = requests.head('https://www.google.com', timeout=5)
        
        if response.status_code < 400:
            print("✓ Network connectivity OK")
            return True
        else:
            print(f"⚠ Network returned status {response.status_code}")
            return True  # Still connected, just got an error
            
    except requests.RequestException as e:
        print(f"✗ Network connectivity issue: {e}")
        return False
    except Exception as e:
        print(f"⚠ Error checking network: {e}")
        return False


def provide_recommendations(results):
    """Provide recommendations based on check results."""
    print("\n" + "=" * 50)
    print("RECOMMENDATIONS")
    print("=" * 50)
    
    if not results['python_version']:
        print("\n⚠ Python version issue:")
        print("  Install Python 3.7 or higher")
        print("  Download from: https://www.python.org/downloads/")
    
    if not results['dependencies']:
        print("\n⚠ Missing dependencies:")
        print("  Run: pip install -r requirements.txt")
    
    if not results['browsers']:
        print("\n⚠ Playwright browser not installed:")
        print("  Run: playwright install chromium")
        print("  If that fails, try:")
        print("    playwright install-deps chromium")
        print("    playwright install chromium")
    
    if not results['permissions']:
        print("\n⚠ Permission issues:")
        print("  Make sure you have write access to the current directory")
        print("  On Linux/Mac, you may need to use sudo or change directory permissions")
    
    if not results['imports']:
        print("\n⚠ Module import issues:")
        print("  Make sure all files are in the same directory")
        print("  Check that config.py and svg_downloader.py exist")
    
    if not results['network']:
        print("\n⚠ Network issues:")
        print("  Check your internet connection")
        print("  Check if you're behind a proxy or firewall")
        print("  Some networks may block Playwright browser downloads")
    
    if all(results.values()):
        print("\n✓ All checks passed!")
        print("  You should be able to run the SVG downloader")
        print("  Try: python main.py --help")


def main():
    """Run all troubleshooting checks."""
    print("=" * 50)
    print("SVG Downloader - Troubleshooting")
    print("=" * 50)
    print()
    
    results = {
        'python_version': check_python_version(),
        'dependencies': check_dependencies(),
        'browsers': check_playwright_browsers(),
        'permissions': check_permissions(),
        'imports': check_imports(),
        'network': check_network()
    }
    
    provide_recommendations(results)
    
    print("\n" + "=" * 50)
    
    # Return 0 if all passed, 1 otherwise
    return 0 if all(results.values()) else 1


if __name__ == '__main__':
    sys.exit(main())
