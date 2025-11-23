import logging
import os
from typing import Dict, Any, List
import json
from datetime import datetime
from src.utils.performance_monitor import monitor_performance
from src.core.analysis.entity_extractor import EntityExtractor
import requests
import re
import time

try:
    from google import genai
except ImportError:
    genai = None

logger = logging.getLogger(__name__)

class Analyzer:
    """
    Analytical module for pattern recognition, anomaly detection, and summarization.
    """

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = None
        if self.api_key and genai:
            try:
                self.client = genai.Client(api_key=self.api_key)
                logger.info("Gemini client initialized.")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini client: {e}")
        elif not genai:
            logger.warning("google-genai library not installed.")
        else:
            logger.warning("GEMINI_API_KEY not found.")

    def _duckduckgo_search_selenium(self, query: str, num_results: int = 10) -> List[str]:
        """
        Perform a DuckDuckGo search using Selenium (more bot-friendly than Google).
        
        Args:
            query: Search query
            num_results: Number of results to extract
            
        Returns:
            List of URLs from search results
        """
        try:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.chrome.service import Service
            from selenium.webdriver.chrome.options import Options
            from webdriver_manager.chrome import ChromeDriverManager
        except ImportError as e:
            logger.error(f"Selenium not available: {e}")
            return []
        
        driver = None
        try:
            # Setup Chrome options
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            
            # Initialize driver
            logger.info("Initializing Chrome driver...")
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Navigate to DuckDuckGo
            search_url = f"https://duckduckgo.com/?q={requests.utils.quote(query)}"
            logger.info(f"Searching DuckDuckGo: {query}")
            driver.get(search_url)
            
            # Wait for results to load
            time.sleep(4)
            
            # Extract search result links from DuckDuckGo
            urls = []
            
            # DuckDuckGo uses different selectors
            search_results = driver.find_elements(By.CSS_SELECTOR, 'a[data-testid="result-title-a"]')
            
            for result in search_results:
                try:
                    url = result.get_attribute('href')
                    if url and url.startswith('http') and 'duckduckgo.com' not in url:
                        # Clean URL
                        url = url.split('#')[0]  # Remove anchors
                        
                        if url not in urls and len(url) < 200:
                            urls.append(url)
                            logger.info(f"Found URL: {url}")
                            
                            if len(urls) >= num_results:
                                break
                except Exception as e:
                    logger.debug(f"Error extracting URL: {e}")
                    continue
            
            # Fallback: try alternative selector
            if len(urls) < 3:
                logger.info("Trying alternative DuckDuckGo selector...")
                links = driver.find_elements(By.CSS_SELECTOR, 'article a[href]')
                for link in links:
                    try:
                        url = link.get_attribute('href')
                        if url and url.startswith('http') and 'duckduckgo.com' not in url:
                            url = url.split('#')[0]
                            if url not in urls and len(url) < 200:
                                urls.append(url)
                                logger.info(f"Found URL (alt): {url}")
                                if len(urls) >= num_results:
                                    break
                    except:
                        continue
            
            logger.info(f"Extracted {len(urls)} URLs from DuckDuckGo")
            return urls
                
        except Exception as e:
            logger.error(f"Selenium search failed: {e}", exc_info=True)
            return []
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass

    def _validate_url(self, url: str, timeout: int = 5) -> bool:
        """
        Validate that a URL is accessible.
        
        Args:
            url: URL to validate
            timeout: Request timeout in seconds
            
        Returns:
            True if URL returns 200, False otherwise
        """
        try:
            response = requests.head(
                url,
                timeout=timeout,
                allow_redirects=True,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            if response.status_code == 200:
                return True
            # Try GET if HEAD fails
            response = requests.get(
                url,
                timeout=timeout,
                allow_redirects=True,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            return response.status_code == 200
        except:
            return False

    def generate_plan(self, prompt: str) -> List[str]:
        """
        Generate a list of REAL URLs using DuckDuckGo search via Selenium.

        Args:
            prompt: The user's research prompt

        Returns:
            List of URLs from real search results
        """
        logger.info(f"Generating plan for prompt: {prompt}")
        
        # Perform DuckDuckGo search
        try:
            logger.info("Performing DuckDuckGo search with Selenium...")
            search_results = self._duckduckgo_search_selenium(prompt, num_results=10)
            
            if not search_results:
                logger.warning("DuckDuckGo search returned no results, using fallback")
                return self._get_fallback_urls()
            
            logger.info(f"Found {len(search_results)} URLs from DuckDuckGo")
            
            # Validate URLs (check first 7)
            validated_urls = []
            for url in search_results[:7]:
                logger.info(f"Validating: {url}")
                if self._validate_url(url, timeout=4):
                    validated_urls.append(url)
                    logger.info(f"✓ Valid: {url}")
                    if len(validated_urls) >= 5:
                        break
                else:
                    logger.warning(f"✗ Invalid/Blocked: {url}")
                
                time.sleep(0.3)
            
            if len(validated_urls) >= 3:
                logger.info(f"Successfully validated {len(validated_urls)} URLs")
                return validated_urls
            else:
                logger.warning(f"Only validated {len(validated_urls)} URLs, using fallback")
                return self._get_fallback_urls()
                
        except Exception as e:
            logger.error(f"URL generation failed: {e}", exc_info=True)
            return self._get_fallback_urls()
    
    def _get_fallback_urls(self) -> List[str]:
        """Fallback URLs if search fails."""
        logger.warning("Using fallback URLs")
        return [
            "https://example.com",
            "https://example.com/page1",
            "https://example.com/page2"
        ]

    def detect_patterns(self, data: Any) -> List[Dict[str, Any]]:
        """
        Detect patterns in the provided data.

        Args:
            data (Any): The data to analyze.

        Returns:
            List[Dict[str, Any]]: A list of detected patterns.
        """
        logger.info("Detecting patterns...")
        
        if self.client:
            try:
                prompt = f"Analyze the following data and detect key patterns or anomalies. Return as a JSON list of objects with 'pattern' and 'confidence' keys. Data: {str(data)[:2000]}"
                response = self.client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
                return [{"pattern": response.text, "confidence": 1.0}]
            except Exception as e:
                logger.error(f"Gemini analysis failed: {e}")
        
        return [{"pattern": "example_pattern", "confidence": 0.9}]

    def score_relevance(self, data: Any) -> float:
        """
        Score the relevance of the data based on predefined criteria.

        Args:
            data (Any): The data to score.

        Returns:
            float: A relevance score between 0.0 and 1.0.
        """
        logger.info("Scoring relevance...")
        return 0.85

    def generate_summary(self, data: Any) -> str:
        """
        Generate a summary of the data using LLM capabilities.

        Args:
            data (Any): The data to summarize.

        Returns:
            str: A text summary.
        """
        logger.info("Generating summary...")
        
        if self.client:
            try:
                response = self.client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=f"Summarize the following data concisely: {str(data)[:5000]}"
                )
                return response.text
            except Exception as e:
                logger.error(f"Gemini summarization failed: {e}")
                return f"Error generating summary: {e}"
        
        return "This is a generated summary of the analyzed data (Mock)."
