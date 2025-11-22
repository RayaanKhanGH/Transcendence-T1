import logging
from typing import Any, Optional, Dict

logger = logging.getLogger(__name__)

class CacheManager:
    """
    Manages temporary local storage and caching.
    """

    def __init__(self):
        self._memory_cache: Dict[str, Any] = {}

    def save_temp(self, key: str, data: Any) -> bool:
        """
        Save data to temporary cache.

        Args:
            key (str): Cache key.
            data (Any): Data to save.

        Returns:
            bool: True if successful.
        """
        self._memory_cache[key] = data
        return True

    def load_temp(self, key: str) -> Optional[Any]:
        """
        Load data from temporary cache.

        Args:
            key (str): Cache key.

        Returns:
            Optional[Any]: The cached data, or None if not found.
        """
        return self._memory_cache.get(key)

    def clear_cache(self) -> bool:
        """
        Clear the temporary cache.

        Returns:
            bool: True if successful.
        """
        self._memory_cache.clear()
        logger.info("Cache cleared.")
        return True
