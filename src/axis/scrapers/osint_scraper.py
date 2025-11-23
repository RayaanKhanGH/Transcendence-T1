import logging
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class Scraper:
    """
    Scraper for OSINT sources using requests + BeautifulSoup.
    Simplified approach to avoid Scrapy reactor issues.
    """
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
        }
        self.timeout = 15
        self.max_retries = 2
    
    def scrape_osint_sources(self, sources: List[str]) -> List[Dict[str, Any]]:
        """
        Scrape generic OSINT sources.
        
        Args:
            sources: List of source URLs
            
        Returns:
            List of scraped data dictionaries
        """
        logger.info(f"Scraping {len(sources)} OSINT sources...")
        results = []
        
        for url in sources:
            result = self._scrape_single_url(url)
            results.append(result)
        
        return results
    
    def _scrape_single_url(self, url: str) -> Dict[str, Any]:
        """Scrape a single URL with retry logic."""
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Scraping {url} (attempt {attempt + 1}/{self.max_retries})")
                
                # Create a session to handle cookies and redirects better
                session = requests.Session()
                session.headers.update(self.headers)
                
                response = session.get(
                    url,
                    timeout=self.timeout,
                    allow_redirects=True,
                    verify=True  # Verify SSL certificates
                )
                
                if response.status_code == 200:
                    # Get the text content (requests automatically handles decompression)
                    html_content = response.text
                    
                    # Verify we got actual HTML, not binary garbage
                    if html_content and len(html_content) > 0:
                        # Check if it looks like HTML
                        if '<html' in html_content.lower() or '<!doctype' in html_content.lower() or '<body' in html_content.lower():
                            return {
                                'url': url,
                                'html': html_content,
                                'status_code': response.status_code,
                                'error': None
                            }
                        else:
                            logger.warning(f"Response from {url} doesn't appear to be HTML")
                            # Try to decode anyway
                            return {
                                'url': url,
                                'html': html_content,
                                'status_code': response.status_code,
                                'error': None
                            }
                    else:
                        logger.warning(f"Empty response from {url}")
                        if attempt == self.max_retries - 1:
                            return {
                                'url': url,
                                'html': '',
                                'status_code': response.status_code,
                                'error': "Empty response"
                            }
                else:
                    logger.warning(f"HTTP {response.status_code} for {url}")
                    if attempt == self.max_retries - 1:
                        return {
                            'url': url,
                            'html': '',
                            'status_code': response.status_code,
                            'error': f"HTTP {response.status_code}"
                        }
                        
            except requests.exceptions.Timeout:
                logger.warning(f"Timeout for {url}")
                if attempt == self.max_retries - 1:
                    return {
                        'url': url,
                        'html': '',
                        'status_code': 0,
                        'error': "Timeout"
                    }
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Error scraping {url}: {e}")
                if attempt == self.max_retries - 1:
                    return {
                        'url': url,
                        'html': '',
                        'status_code': 0,
                        'error': str(e)
                    }
        
        # Fallback (should not reach here)
        return {
            'url': url,
            'html': '',
            'status_code': 0,
            'error': "Unknown error"
        }
