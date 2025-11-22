"""Simple test to identify import errors."""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Testing imports...")

try:
    from src.agent_manager import AgentManager
    print("✓ AgentManager imported")
except Exception as e:
    print(f"✗ AgentManager failed: {e}")

try:
    from src.system_core import Core
    print("✓ Core imported")
except Exception as e:
    print(f"✗ Core failed: {e}")

try:
    from src.core.analysis.analyzer import Analyzer
    print("✓ Analyzer imported")
except Exception as e:
    print(f"✗ Analyzer failed: {e}")

try:
    from src.core.embed.embedder import Embedder
    print("✓ Embedder imported")
except Exception as e:
    print(f"✗ Embedder failed: {e}")

try:
    from src.core.ingestion.ingestor import Ingestor
    print("✓ Ingestor imported")
except Exception as e:
    print(f"✗ Ingestor failed: {e}")

try:
    from src.core.preprocess.preprocessor import Preprocessor
    print("✓ Preprocessor imported")
except Exception as e:
    print(f"✗ Preprocessor failed: {e}")

try:
    from src.models.embeddings.pinecone_handler import PineconeHandler
    print("✓ PineconeHandler imported")
except Exception as e:
    print(f"✗ PineconeHandler failed: {e}")

try:
    from src.models.storage.data_storage import Storage
    print("✓ Storage imported")
except Exception as e:
    print(f"✗ Storage failed: {e}")

try:
    from src.axis.filters.content_filter import Filter
    print("✓ Filter imported")
except Exception as e:
    print(f"✗ Filter failed: {e}")

try:
    from src.axis.scrapers.osint_scraper import Scraper
    print("✓ Scraper imported")
except Exception as e:
    print(f"✗ Scraper failed: {e}")

try:
    from src.axis.parsers.data_parser import Parser
    print("✓ Parser imported")
except Exception as e:
    print(f"✗ Parser failed: {e}")

try:
    from src.storage.cache_manager import CacheManager
    print("✓ CacheManager imported")
except Exception as e:
    print(f"✗ CacheManager failed: {e}")
