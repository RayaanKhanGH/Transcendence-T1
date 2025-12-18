import logging
import asyncio
import aiohttp
import ssl
import certifi
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class Scraper:
    """
    Scraper for OSINT sources using AsyncIO + AioHTTP.
    Designed for massive parallelism to overcome I/O latency bottlenecks.
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
        # No Scrapy fallback needed as we are using pure asyncio now
    
    async def _fetch_url(self, session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
        """Fetch a single URL asynchronously."""
        try:
            async with session.get(url, headers=self.headers, timeout=self.timeout, ssl=False) as response:
                status = response.status
                html = await response.text()
                
                if status == 200:
                    return {
                        'url': url,
                        'html': html,
                        'status_code': 200,
                        'error': None
                    }
                else:
                    return {
                        'url': url,
                        'html': '',
                        'status_code': status,
                        'error': f"HTTP {status}"
                    }
        except Exception as e:
            return {
                'url': url,
                'html': '',
                'status_code': 0,
                'error': str(e)
            }

    async def _scrape_async(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Run fetching tasks concurrently."""
        async with aiohttp.ClientSession() as session:
            tasks = [self._fetch_url(session, url) for url in urls]
            return await asyncio.gather(*tasks)

    def scrape_osint_sources(self, sources: List[str]) -> List[Dict[str, Any]]:
        """
        Synchronous wrapper for the async scraping engine.
        
        Args:
            sources: List of source URLs
            
        Returns:
            List of scraped data dictionaries
        """
        logger.info(f"Scraping {len(sources)} OSINT sources using AsyncIO Parallelism...")
        
        try:
            # Check for existing event loop
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            if loop.is_running():
                # If we are already in an async context (rare for this architecture but possible)
                # usage of nest_asyncio would be needed, but sticking to simple runner:
                future = asyncio.run_coroutine_threadsafe(self._scrape_async(sources), loop)
                results = future.result()
            else:
                results = loop.run_until_complete(self._scrape_async(sources))
                
            return results
        except Exception as e:
            logger.error(f"Async Fetch Failed: {e}")
            return []

