#!/usr/bin/env python3
"""Debug Selenium to see what's happening."""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests

# Setup Chrome
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    query = "latest fashion trends in luxury footwear"
    search_url = f"https://www.google.com/search?q={requests.utils.quote(query)}&num=20"
    
    print(f"Navigating to: {search_url}")
    driver.get(search_url)
    time.sleep(3)
    
    print(f"\nPage title: {driver.title}")
    print(f"Page URL: {driver.current_url}")
    
    # Try different selectors
    print("\n--- Testing selectors ---")
    
    selectors = [
        ('div.g a[href]', 'Standard results'),
        ('div.g a', 'All links in results'),
        ('a[jsname]', 'Links with jsname'),
        ('a[href]', 'All links'),
    ]
    
    for selector, desc in selectors:
        elements = driver.find_elements(By.CSS_SELECTOR, selector)
        print(f"\n{desc} ({selector}): Found {len(elements)} elements")
        
        if elements:
            for i, elem in enumerate(elements[:3], 1):
                try:
                    href = elem.get_attribute('href')
                    if href:
                        print(f"  {i}. {href[:100]}")
                except:
                    print(f"  {i}. (error getting href)")
    
    # Save page source for inspection
    with open('google_page_source.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    print("\n✓ Saved page source to google_page_source.html")
    
finally:
    driver.quit()
