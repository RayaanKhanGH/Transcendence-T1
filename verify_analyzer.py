#!/usr/bin/env python3
"""
Direct test of the analyzer module to verify Selenium works.
This will prove the code is correct.
"""

import sys
import importlib

# Force reload of the analyzer module
if 'src.core.analysis.analyzer' in sys.modules:
    del sys.modules['src.core.analysis.analyzer']

from src.core.analysis.analyzer import Analyzer

print("Testing Analyzer with fresh import...")
analyzer = Analyzer()

prompt = "latest fashion trends in luxury footwear"
print(f"\nPrompt: '{prompt}'")
print("Generating URLs...\n")

urls = analyzer.generate_plan(prompt)

print(f"\nResult: {len(urls)} URLs")
for i, url in enumerate(urls, 1):
    print(f"  {i}. {url}")

if 'example.com' in urls[0]:
    print("\n❌ FAILED - Got fallback URLs")
    sys.exit(1)
else:
    print("\n✅ SUCCESS - Got real URLs from Google")
    sys.exit(0)
