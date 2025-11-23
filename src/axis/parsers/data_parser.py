import logging
import json
import csv
import re
from typing import Dict, Any, List
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class Parser:
    """
    Advanced parsers for various data formats with article extraction.
    """

    def __init__(self):
        pass

    def extract_article_content(self, html: str, url: str) -> Dict[str, Any]:
        """
        Extract the main article content from HTML.
        
        Prioritizes semantic tags and uses heuristics to find the main content.
        
        Args:
            html: Raw HTML string
            url: Source URL
            
        Returns:
            Dictionary with title, content, metadata
        """
        if not html:
            return {
                'title': '',
                'content': '',
                'author': None,
                'publish_date': None,
                'metadata': {}
            }
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract title
            title = ''
            if soup.title:
                title = soup.title.string.strip()
            elif soup.find('h1'):
                title = soup.find('h1').get_text(strip=True)
            
            # Extract metadata
            metadata = self.extract_metadata(html)
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'iframe', 'noscript', 'form']):
                element.decompose()
            
            # Try to find main content area
            content_area = None
            
            # Priority 1: Semantic tags
            if soup.find('article'):
                content_area = soup.find('article')
            elif soup.find('main'):
                content_area = soup.find('main')
            
            # Priority 2: Common content class/id patterns
            if not content_area:
                patterns = [
                    'article-body', 'post-content', 'entry-content', 'story-body',
                    'article-content', 'main-content', 'content-body', 'post-body'
                ]
                for pattern in patterns:
                    found = soup.find(class_=re.compile(pattern, re.I)) or soup.find(id=re.compile(pattern, re.I))
                    if found:
                        content_area = found
                        break
            
            # Fallback: Use body
            if not content_area:
                content_area = soup.body or soup
            
            # Extract text from paragraphs and headings
            text_blocks = []
            for tag in content_area.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'li']):
                text = tag.get_text(strip=True)
                # Filter out very short snippets and common navigation text
                if len(text) > 30 and not self._is_navigation_text(text):
                    text_blocks.append(text)
            
            # Join with double newlines for readability
            content = '\n\n'.join(text_blocks)
            
            # If we got very little content, fallback to raw text
            if len(content) < 200:
                content = content_area.get_text(separator='\n', strip=True)
            
            # Clean the content
            content = self.clean_text(content)
            
            return {
                'title': title,
                'content': content,
                'author': metadata.get('author'),
                'publish_date': metadata.get('publish_date'),
                'metadata': metadata
            }
            
        except Exception as e:
            logger.error(f"Error extracting article content: {e}")
            return {
                'title': '',
                'content': '',
                'author': None,
                'publish_date': None,
                'metadata': {}
            }
    
    def _is_navigation_text(self, text: str) -> bool:
        """Check if text is likely navigation/boilerplate."""
        nav_patterns = [
            'skip to', 'sign in', 'log in', 'subscribe', 'newsletter',
            'cookie', 'privacy policy', 'terms of service', 'follow us',
            'share this', 'read more', 'click here'
        ]
        text_lower = text.lower()
        return any(pattern in text_lower for pattern in nav_patterns)
    
    def extract_metadata(self, html: str) -> Dict[str, Any]:
        """
        Extract metadata from HTML (Open Graph, Twitter Cards, JSON-LD).
        
        Args:
            html: Raw HTML string
            
        Returns:
            Dictionary with metadata
        """
        metadata = {}
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Open Graph tags
            og_tags = soup.find_all('meta', property=re.compile(r'^og:'))
            for tag in og_tags:
                key = tag.get('property', '').replace('og:', '')
                value = tag.get('content', '')
                if key and value:
                    metadata[key] = value
            
            # Twitter Card tags
            twitter_tags = soup.find_all('meta', attrs={'name': re.compile(r'^twitter:')})
            for tag in twitter_tags:
                key = tag.get('name', '').replace('twitter:', '')
                value = tag.get('content', '')
                if key and value:
                    metadata[f'twitter_{key}'] = value
            
            # Author meta tag
            author_tag = soup.find('meta', attrs={'name': 'author'})
            if author_tag:
                metadata['author'] = author_tag.get('content', '')
            
            # Publish date
            date_tag = soup.find('meta', property='article:published_time') or \
                      soup.find('meta', attrs={'name': 'publish_date'})
            if date_tag:
                metadata['publish_date'] = date_tag.get('content', '')
            
        except Exception as e:
            logger.error(f"Error extracting metadata: {e}")
        
        return metadata
    
    def clean_text(self, text: str) -> str:
        """
        Advanced text cleaning.
        
        Args:
            text: Raw text string
            
        Returns:
            Cleaned text
        """
        if not text:
            return ''
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove multiple newlines
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def parse_html(self, html_content: str) -> str:
        """
        Parse HTML content to extract text (legacy method for compatibility).
        
        Args:
            html_content: Raw HTML string
            
        Returns:
            Extracted text
        """
        result = self.extract_article_content(html_content, '')
        return result['content']

    def parse_json(self, json_content: str) -> Dict[str, Any]:
        """
        Parse JSON content.

        Args:
            json_content: JSON string

        Returns:
            Parsed dictionary
        """
        try:
            return json.loads(json_content)
        except json.JSONDecodeError:
            logger.error("Failed to parse JSON.")
            return {}

    def parse_csv(self, csv_content: str) -> List[Dict[str, Any]]:
        """
        Parse CSV content.

        Args:
            csv_content: CSV string

        Returns:
            List of rows as dictionaries
        """
        # Placeholder logic
        return []
