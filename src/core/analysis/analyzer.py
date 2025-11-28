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

    def _duckduckgo_search_selenium(self, query: str, time_filter: str = None) -> List[str]:
        """
        Perform a DuckDuckGo search using Selenium with optional time filtering.
        
        Args:
            query: Search query
            num_results: Number of results to extract
            time_filter: 'd' (day), 'w' (week), 'm' (month), 'y' (year)
            
        Returns:
            List of URLs from search results
        """
        num_results = 15
        try:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.chrome.service import Service
            from selenium.webdriver.chrome.options import Options
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.common.keys import Keys
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
            
            # Construct URL with time filter if specified
            base_url = "https://duckduckgo.com/?q=" + requests.utils.quote(query)
            if time_filter:
                base_url += f"&df={time_filter}&ia=web"
                logger.info(f"Applying time filter: {time_filter}")
            
            logger.info(f"Searching DuckDuckGo: {query}")
            driver.get(base_url)
            
            # Wait for results to load
            time.sleep(3)
            
            # Scroll down to load more results
            logger.info("Scrolling for more results...")
            body = driver.find_element(By.TAG_NAME, 'body')
            for _ in range(3):
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(1)
            
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
                            
                            if len(urls) >= num_results:
                                break
                except Exception as e:
                    logger.debug(f"Error extracting URL: {e}")
                    continue
            
            # Fallback: try alternative selector
            if len(urls) < 5:
                logger.info("Trying alternative DuckDuckGo selector...")
                links = driver.find_elements(By.CSS_SELECTOR, 'article a[href]')
                for link in links:
                    try:
                        url = link.get_attribute('href')
                        if url and url.startswith('http') and 'duckduckgo.com' not in url:
                            url = url.split('#')[0]
                            if url not in urls and len(url) < 200:
                                urls.append(url)
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
        
        # Determine if we need strict time filtering
        time_filter = None
        now = datetime.now()
        current_year = str(now.year)
        prompt_lower = prompt.lower()
        
        # Dynamic time filtering logic
        if any(keyword in prompt_lower for keyword in ['latest', 'news', 'current', 'recent', 'today', 'now', 'update']):
            # For "latest" news, prefer past month to get very recent results (approx 3-6 mo relevance)
            # DuckDuckGo supports 'd' (day), 'w' (week), 'm' (month), 'y' (year)
            # We'll default to 'm' (month) for "latest" to ensure high freshness, or 'y' for general "2025" queries
            if 'year' in prompt_lower:
                time_filter = 'y'
            else:
                time_filter = 'm' # Default to past month for "latest" to ensure freshness
            
            # Append dynamic current year to query if not present to force relevance
            if current_year not in prompt:
                prompt += f" {current_year}"
                logger.info(f"Appended current year to prompt: {prompt}")
        
        # Perform DuckDuckGo search
        try:
            logger.info(f"Performing DuckDuckGo search with Selenium (Filter: {time_filter})...")
            # Request more results initially to account for validation failures
            search_results = self._duckduckgo_search_selenium(prompt, time_filter=time_filter)
            
            if not search_results:
                logger.warning("DuckDuckGo search returned no results, using fallback")
                return self._get_fallback_urls()
            
            logger.info(f"Found {len(search_results)} URLs from DuckDuckGo")
            
            # Validate URLs
            validated_urls = []
            target_count = 20  # Aim for up to 20 URLs
            
            for url in search_results:
                logger.info(f"Validating: {url}")
                if self._validate_url(url, timeout=4):
                    validated_urls.append(url)
                    logger.info(f"✓ Valid: {url}")
                    if len(validated_urls) >= target_count:
                        break
                else:
                    logger.warning(f"✗ Invalid/Blocked: {url}")
                
                time.sleep(0.2)
            
            # Ensure we have at least a decent number, but return whatever we found if > 0
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
        Detect patterns in the provided data using advanced LLM analysis.

        Args:
            data (Any): The data to analyze.

        Returns:
            List[Dict[str, Any]]: A list of detected patterns.
        """
        logger.info("Detecting patterns...")
        
        if self.client:
            try:
                prompt = (
                    "Analyze the following data and detect key patterns, anomalies, or trends. "
                    "Focus on:\n"
                    "1. Temporal patterns (timing, frequency)\n"
                    "2. Behavioral patterns (actions, sentiment)\n"
                    "3. Structural patterns (relationships, clusters)\n"
                    "Return the result as a JSON list of objects, where each object has 'pattern' (description) "
                    "and 'confidence' (0.0-1.0). "
                    f"Data: {str(data)[:10000]}"
                )
                response = self.client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
                # In a real implementation, we would parse the JSON. 
                # For now, we return the raw text if it's not strict JSON, wrapped in a structure.
                return [{"pattern": response.text, "confidence": 1.0}]
            except Exception as e:
                logger.error(f"Gemini analysis failed: {e}")
        
        return [{"pattern": "Pattern detection unavailable (LLM error)", "confidence": 0.0}]

    def score_relevance(self, data: Any) -> float:
        """
        Score the relevance of the data based on predefined criteria.

        Args:
            data (Any): The data to score.

        Returns:
            float: A relevance score between 0.0 and 1.0.
        """
        logger.info("Scoring relevance...")
        # Placeholder logic - could be enhanced with LLM scoring in future
        return 0.85

    def generate_summary(self, data: Any) -> str:
        """
        Generate a comprehensive intelligence summary using LLM capabilities.

        Args:
            data (Any): The data to summarize.

        Returns:
            str: A comprehensive text summary.
        """
        logger.info("Generating comprehensive summary...")
        
        if self.client:
            try:
                prompt = (
                    "You are an elite intelligence analyst. Analyze the following text and provide a comprehensive report.\n"
                    "Structure your response exactly as follows:\n\n"
                    "### 1. Intelligence Extraction\n"
                    "A comprehensive narrative paragraph that synthesizes the key findings, context, and nuances of the information. "
                    "Do not use bullet points here. Tell the story of the data.\n\n"
                    "### 2. Strategic Implications\n"
                    "Analyze what this information means for the broader context (e.g., industry trends, future risks, opportunities).\n\n"
                    "### 3. Key Entities\n"
                    "List important people, organizations, and locations mentioned.\n\n"
                    f"Data to Analyze:\n{str(data)[:15000]}"
                )
                
                response = self.client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
                return response.text
            except Exception as e:
                logger.error(f"Gemini summarization failed: {e}")
                return f"Error generating summary: {e}"
        
        return "This is a generated summary of the analyzed data (Mock - No API Key)."

    def generate_executive_report(self, summaries: List[str], prompt: str) -> str:
        """
        Synthesize multiple summaries into a single executive intelligence report.
        
        Args:
            summaries: List of individual article summaries
            prompt: The original research prompt
            
        Returns:
            str: A synthesized executive summary
        """
        logger.info("Generating executive report...")
        
        if not summaries:
            return "No data available for executive summary."
            
        combined_text = "\n\n".join(summaries)
        
        if self.client:
            try:
                prompt_text = (
                    f"You are a Chief Intelligence Officer. Synthesize the following {len(summaries)} intelligence reports "
                    f"regarding '{prompt}' into a single, high-level Executive Briefing.\n\n"
                    "Your response MUST be a single, cohesive narrative paragraph (200-400 words) that:\n"
                    "1. Synthesizes the most important findings from all sources.\n"
                    "2. Identifies the overarching narrative or trend.\n"
                    "3. Highlights the critical strategic implication.\n"
                    "4. Does NOT use bullet points.\n"
                    "5. Starts directly with the narrative (no 'Here is the report' preamble).\n\n"
                    f"Source Reports:\n{combined_text[:25000]}"
                )
                
                response = self.client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt_text
                )
                return response.text
            except Exception as e:
                logger.error(f"Executive report generation failed: {e}")
                return f"Error generating executive report: {e}"
        
        return "Executive summary unavailable (Mock - No API Key)."
