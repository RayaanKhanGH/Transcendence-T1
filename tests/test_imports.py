import unittest
import sys
import os
import importlib

class TestImports(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Add parent directory to path for imports
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    def test_imports(self):
        """Test that all key modules can be imported successfully."""
        modules_to_test = [
            ('src.agent_manager', 'AgentManager'),
            ('src.system_core', 'Core'),
            ('src.core.analysis.analyzer', 'Analyzer'),
            ('src.core.embed.embedder', 'Embedder'),
            ('src.core.ingestion.ingestor', 'Ingestor'),
            ('src.core.preprocess.preprocessor', 'Preprocessor'),
            ('src.models.embeddings.pinecone_handler', 'PineconeHandler'),

            ('src.axis.filters.content_filter', 'Filter'),
            ('src.axis.scrapers.osint_scraper', 'Scraper'),
            ('src.axis.parsers.data_parser', 'Parser'),
            ('src.storage.cache_manager', 'CacheManager'),
        ]

        for module_name, class_name in modules_to_test:
            with self.subTest(module=module_name):
                try:
                    module = importlib.import_module(module_name)
                    self.assertTrue(hasattr(module, class_name), f"{class_name} not found in {module_name}")
                except ImportError as e:
                    self.fail(f"Failed to import {module_name}: {e}")

