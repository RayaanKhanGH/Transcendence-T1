#!/usr/bin/env python3
"""
Final verification that everything is installed and working.
"""

print("="*60)
print("FINAL SYSTEM VERIFICATION")
print("="*60)

# Check 1: Selenium
print("\n1. Checking Selenium...")
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    print("   ✅ Selenium installed")
except ImportError as e:
    print(f"   ❌ Selenium NOT installed: {e}")
    exit(1)

# Check 2: Other dependencies
print("\n2. Checking other dependencies...")
try:
    import requests
    from bs4 import BeautifulSoup
    print("   ✅ requests, BeautifulSoup installed")
except ImportError as e:
    print(f"   ❌ Missing dependency: {e}")
    exit(1)

# Check 3: Core modules
print("\n3. Checking core modules...")
try:
    from src.core.analysis.analyzer import Analyzer
    from src.core.ingestion.ingestor import Ingestor
    print("   ✅ Core modules importable")
except ImportError as e:
    print(f"   ❌ Core module error: {e}")
    exit(1)

# Check 4: Quick functionality test
print("\n4. Testing Analyzer...")
try:
    analyzer = Analyzer()
    print("   ✅ Analyzer initialized")
except Exception as e:
    print(f"   ❌ Analyzer error: {e}")
    exit(1)

print("\n" + "="*60)
print("✅ ALL CHECKS PASSED")
print("="*60)
print("\nThe system is ready to use!")
print("\nTo use the CLI:")
print("  1. Close the current CLI (Ctrl+C if running)")
print("  2. Run: python cli.py")
print("  3. Enter any research prompt")
print("\nThe system will:")
print("  - Search DuckDuckGo for relevant URLs")
print("  - Scrape and parse the content")
print("  - Generate summaries with Gemini")
print("  - Save a structured JSON report")
print("="*60)
