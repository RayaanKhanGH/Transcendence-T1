import logging
import os
from typing import List, Dict, Any, Optional

try:
    from pinecone import Pinecone
except ImportError:
    Pinecone = None

logger = logging.getLogger(__name__)

class PineconeHandler:
    """
    Wrapper class for Pinecone Vector Database interactions.
    Uses Pinecone v8 inference API with llama text-embed-v2.
    """

    def __init__(self, index_name: str = "abc", namespace: str = "intelligence"):
        """
        Initialize Pinecone connection.
        
        Args:
            index_name (str): Name of the Pinecone index to use.
            namespace (str): Namespace for organizing vectors.
        """
        self.api_key = os.getenv("PINECONE_API_KEY")
        self.index_name = index_name
        self.namespace = namespace
        self.pc = None
        self.index = None
        
        if self.api_key:
            self._connect()
        else:
            logger.warning("Pinecone credentials not found in environment variables.")

    def _connect(self):
        """Establish connection to Pinecone."""
        if Pinecone is None:
            logger.error("Pinecone client not installed.")
            return

        try:
            self.pc = Pinecone(api_key=self.api_key)
            # Check if index exists
            existing_indexes = [i.name for i in self.pc.list_indexes()]
            if self.index_name not in existing_indexes:
                logger.warning(f"Index {self.index_name} does not exist. Please create it first.")
            else:
                self.index = self.pc.Index(self.index_name)
                logger.info(f"Connected to Pinecone index: {self.index_name}")
        except Exception as e:
            logger.error(f"Failed to connect to Pinecone: {e}")

    def upsert_vectors(self, vectors: List[tuple]) -> bool:
        """
        Upsert vectors into the index using Pinecone's inference API.
        
        Uses index.upsert_records() with text that gets embedded automatically
        by the llama-text-embed-v2 model.

        Args:
            vectors (List[tuple]): List of (id, text, metadata) tuples.

        Returns:
            bool: True if successful.
        """
        if not self.index:
            logger.warning("Pinecone index not initialized.")
            return False
        
        try:
            # Format data for Pinecone v8 inference API
            # Format: [{"id": "...", "text": "..."}]
            # Note: metadata is optional and may cause issues
            records = []
            for item in vectors:
                if len(item) == 3:
                    doc_id, text, metadata = item
                    # Limit text length to avoid API errors
                    truncated_text = text[:8000] if len(text) > 8000 else text
                    
                    # Create record without metadata first (simpler)
                    record = {
                        "id": doc_id,
                        "text": truncated_text
                    }
                    records.append(record)
            
            logger.info(f"Attempting to upsert {len(records)} records to Pinecone...")
            
            # Use upsert_records for inference API
            self.index.upsert_records(
                namespace=self.namespace,
                records=records
            )
            
            logger.info(f"✓ Upserted {len(records)} records to Pinecone namespace '{self.namespace}'.")
            return True
        except Exception as e:
            logger.error(f"Error upserting to Pinecone: {e}")
            logger.debug(f"Sample record: {records[0] if records else 'none'}")
            return False

    def query_vectors(self, query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Query the index for similar vectors using text.
        
        Uses index.search() with text that gets embedded automatically.

        Args:
            query_text (str): The query text (Pinecone will embed it).
            top_k (int): Number of results.

        Returns:
            List[Dict[str, Any]]: List of matches.
        """
        if not self.index:
            logger.warning("Pinecone index not initialized.")
            return []

        try:
            # Use search method for inference API
            results = self.index.search(
                namespace=self.namespace,
                query={
                    "inputs": {"text": query_text},
                    "top_k": top_k
                }
            )
            
            # Extract matches from results
            matches = results.get('matches', [])
            logger.info(f"Found {len(matches)} matches for query.")
            return matches
        except Exception as e:
            logger.error(f"Error querying Pinecone: {e}")
            return []
