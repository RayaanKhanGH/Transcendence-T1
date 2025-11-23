import logging
import hashlib
from typing import Dict, Any, List, Set

logger = logging.getLogger(__name__)

class Filter:
    """
    Filters incoming OSINT data based on quality, relevance, and duplication.
    """

    def __init__(self):
        self.min_content_length = 200
        self.min_word_count = 50
    
    def filter_by_quality(self, data: Dict[str, Any]) -> bool:
        """
        Apply quality filtering rules to the data.
        
        Args:
            data: The data item with 'content' field
            
        Returns:
            True if data passes quality filters, False otherwise
        """
        content = data.get('content', '')
        
        # Check if content exists
        if not content or not content.strip():
            logger.debug(f"Filtered out {data.get('url', 'unknown')}: empty content")
            return False
        
        # Check minimum length
        if len(content) < self.min_content_length:
            logger.debug(f"Filtered out {data.get('url', 'unknown')}: content too short ({len(content)} chars)")
            return False
        
        # Check word count
        word_count = len(content.split())
        if word_count < self.min_word_count:
            logger.debug(f"Filtered out {data.get('url', 'unknown')}: too few words ({word_count})")
            return False
        
        # Check for error indicators
        if data.get('status') == 'error' or data.get('error'):
            logger.debug(f"Filtered out {data.get('url', 'unknown')}: error status")
            return False
        
        return True
    
    def calculate_relevance_score(self, data: Dict[str, Any], keywords: List[str] = None) -> float:
        """
        Calculate relevance score based on keyword matching.
        
        Args:
            data: The data item
            keywords: List of keywords to match (optional)
            
        Returns:
            Relevance score between 0.0 and 1.0
        """
        if not keywords:
            return 1.0  # No keywords specified, assume relevant
        
        content = data.get('content', '').lower()
        title = data.get('title', '').lower()
        
        if not content:
            return 0.0
        
        # Count keyword matches
        matches = 0
        for keyword in keywords:
            keyword_lower = keyword.lower()
            # Weight title matches higher
            if keyword_lower in title:
                matches += 2
            if keyword_lower in content:
                matches += 1
        
        # Normalize score
        max_possible = len(keywords) * 3  # 2 for title + 1 for content
        score = min(matches / max_possible, 1.0) if max_possible > 0 else 0.0
        
        return score
    
    def is_duplicate(self, data: Dict[str, Any], seen_hashes: Set[str]) -> bool:
        """
        Check if data is a duplicate based on content hash.
        
        Args:
            data: The data item
            seen_hashes: Set of previously seen content hashes
            
        Returns:
            True if duplicate, False otherwise
        """
        content = data.get('content', '')
        url = data.get('url', '')
        
        if not content:
            return False
        
        # Create hash of content
        content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
        
        # Also hash URL to catch exact URL duplicates
        url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
        
        # Check if we've seen this content or URL before
        if content_hash in seen_hashes or url_hash in seen_hashes:
            logger.debug(f"Filtered out {url}: duplicate content")
            return True
        
        # Add to seen hashes
        seen_hashes.add(content_hash)
        seen_hashes.add(url_hash)
        
        return False
    
    def apply_rules(self, data: Dict[str, Any]) -> bool:
        """
        Apply all filtering rules to the data.
        
        Args:
            data: The data item
            
        Returns:
            True if data passes all filters, False otherwise
        """
        # For now, just use quality filter
        return self.filter_by_quality(data)
    
    def exclude_irrelevant(self, data: Dict[str, Any]) -> bool:
        """
        Exclude data deemed irrelevant.
        
        Args:
            data: The data item
            
        Returns:
            True if data is relevant (kept), False if excluded
        """
        # Use quality filter as relevance check
        return self.filter_by_quality(data)
