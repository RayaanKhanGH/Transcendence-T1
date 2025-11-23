import logging
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup
from src.axis.scrapers.osint_scraper import Scraper
from src.axis.parsers.data_parser import Parser
from src.axis.filters.content_filter import Filter

logger = logging.getLogger(__name__)

class Ingestor:
    """
    Handles data ingestion from various OSINT sources using axis components.
    """

    def __init__(self):
        self.scraper = Scraper()
        self.parser = Parser()
        self.filter = Filter()
        self.seen_hashes = set()

    def fetch_osint(self, urls: List[str]) -> List[Dict[str, Any]]:
        """
        Fetch data from a list of OSINT URLs using the complete axis pipeline.

        Args:
            urls: List of URLs to scrape/fetch

        Returns:
            List of processed data objects
        """
        logger.info(f"Fetching data from {len(urls)} URLs using axis pipeline...")
        
        # Step 1: Scrape using Scrapy
        raw_results = self.scraper.scrape_osint_sources(urls)
        logger.info(f"Scraped {len(raw_results)} URLs")
        
        # Step 2: Parse and extract article content
        parsed_results = []
        for item in raw_results:
            try:
                # Check if scraping was successful
                if item.get('status_code') == 200 and item.get('html'):
                    # Extract article content
                    article_data = self.parser.extract_article_content(
                        item['html'],
                        item['url']
                    )
                    
                    # Merge with original item
                    result = {
                        'url': item['url'],
                        'title': article_data['title'],
                        'content': article_data['content'],
                        'author': article_data.get('author'),
                        'publish_date': article_data.get('publish_date'),
                        'metadata': article_data.get('metadata', {}),
                        'status': 'success'
                    }
                    parsed_results.append(result)
                    logger.info(f"Successfully parsed: {item['url']}")
                else:
                    # Handle failed scrapes
                    error_msg = item.get('error', f"HTTP {item.get('status_code', 'unknown')}")
                    parsed_results.append({
                        'url': item['url'],
                        'status': 'failed',
                        'error': error_msg
                    })
                    logger.warning(f"Failed to scrape {item['url']}: {error_msg}")
                    
            except Exception as e:
                logger.error(f"Error processing {item.get('url', 'unknown')}: {e}")
                parsed_results.append({
                    'url': item.get('url', 'unknown'),
                    'status': 'error',
                    'error': str(e)
                })
        
        # Step 3: Filter results
        filtered_results = []
        for item in parsed_results:
            # Only filter successful items
            if item.get('status') == 'success':
                # Apply quality filter
                if self.filter.filter_by_quality(item):
                    # Check for duplicates
                    if not self.filter.is_duplicate(item, self.seen_hashes):
                        filtered_results.append(item)
                    else:
                        logger.debug(f"Filtered duplicate: {item['url']}")
                else:
                    logger.debug(f"Filtered low quality: {item['url']}")
            else:
                # Keep failed items for reporting
                filtered_results.append(item)
        
        logger.info(f"Filtered to {len([r for r in filtered_results if r.get('status') == 'success'])} quality results")
        
        return filtered_results

    def normalize_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize raw data into a standard format.

        Args:
            raw_data: The raw data object

        Returns:
            Normalized data object
        """
        logger.info("Normalizing data...")
        return {
            "source": raw_data.get("url"),
            "content": raw_data.get("content"),
            "timestamp": raw_data.get("publish_date", "")
        }

    def batch_ingest(self, data_items: List[Dict[str, Any]]) -> bool:
        """
        Ingest a batch of data items into the system.

        Args:
            data_items: List of data items

        Returns:
            bool: True if ingestion was successful
        """
        logger.info(f"Ingesting batch of {len(data_items)} items...")
        # Placeholder logic
        return True
