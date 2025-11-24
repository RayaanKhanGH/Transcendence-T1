#!/usr/bin/env python3
"""
Test the Scrapy fallback mechanism.
"""
import logging
import sys
from src.axis.scrapers.osint_scraper import Scraper

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def test_fallback():
    print("Testing Scrapy fallback...")
    scraper = Scraper()
    
    # Use a URL that might be tricky or just test the mechanism
    # We can simulate a failure by mocking _scrape_single_url, 
    # but let's try a real run with a known tough site or just rely on the logic.
    
    # For this test, let's force the scraper to use fallback by temporarily 
    # breaking the _scrape_single_url method or just trusting the logic if we use a non-existent domain 
    # (which will fail requests, then fail scrapy too, but prove the flow).
    
    # Better: Let's try to scrape a site that blocks simple requests but allows Scrapy (sometimes).
    # Or just verify the code path runs.
    
    urls = ["https://httpbin.org/status/403"] # This will fail requests with 403
    
    print(f"Scraping {urls[0]} (Expect 403 from requests, then Scrapy attempt)")
    results = scraper.scrape_osint_sources(urls)
    
    for res in results:
        print(f"URL: {res['url']}")
        print(f"Status: {res['status_code']}")
        print(f"Error: {res.get('error')}")
        if res.get('html'):
            print(f"Content length: {len(res['html'])}")
        else:
            print("No content")

if __name__ == "__main__":
    test_fallback()
