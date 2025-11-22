"""
Comprehensive test script for Transcendence T1 modules.
Tests all created modules to ensure they work correctly.
"""

import sys
import os
import logging

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_agentmanager():
    """Test AgentManager module."""
    logger.info("Testing AgentManager...")
    try:
        from src.agent_manager import AgentManager
        
        manager = AgentManager()
        
        # Test launch_agent
        result = manager.launch_agent("test_agent_01", {"type": "osint"})
        assert result == True, "launch_agent should return True"
        
        # Test schedule_task
        result = manager.schedule_task("task_01", {"target": "example.com"})
        assert result == True, "schedule_task should return True"
        
        # Test monitor_agents
        status = manager.monitor_agents()
        assert "test_agent_01" in status, "Agent should be in status report"
        
        logger.info("✓ AgentManager tests passed")
        return True
    except Exception as e:
        logger.error(f"✗ AgentManager test failed: {e}")
        return False

def test_core():
    """Test Core module."""
    logger.info("Testing Core...")
    try:
        from src.system_core import Core
        
        core = Core()
        result = core.run_pipeline({"source": "test.com"})
        assert "status" in result, "Pipeline should return status"
        
        logger.info("✓ Core tests passed")
        return True
    except Exception as e:
        logger.error(f"✗ Core test failed: {e}")
        return False

def test_analyzer():
    """Test Analyzer module."""
    logger.info("Testing Analyzer...")
    try:
        from src.core.analysis.analyzer import Analyzer
        
        analyzer = Analyzer()
        
        # Test detect_patterns
        patterns = analyzer.detect_patterns("test data")
        assert isinstance(patterns, list), "detect_patterns should return list"
        
        # Test score_relevance
        score = analyzer.score_relevance("test data")
        assert 0.0 <= score <= 1.0, "score should be between 0 and 1"
        
        # Test generate_summary
        summary = analyzer.generate_summary("test data")
        assert isinstance(summary, str), "summary should be string"
        
        logger.info("✓ Analyzer tests passed")
        return True
    except Exception as e:
        logger.error(f"✗ Analyzer test failed: {e}")
        return False

def test_embedder():
    """Test Embedder module."""
    logger.info("Testing Embedder...")
    try:
        from src.core.embed.embedder import Embedder
        
        embedder = Embedder()
        
        # Test generate_embeddings
        texts = ["text1", "text2"]
        embeddings = embedder.generate_embeddings(texts)
        assert len(embeddings) == len(texts), "Should generate embedding for each text"
        
        # Test store_embeddings
        result = embedder.store_embeddings(embeddings)
        assert result == True, "store_embeddings should return True"
        
        # Test retrieve_similar
        similar = embedder.retrieve_similar("query")
        assert isinstance(similar, list), "retrieve_similar should return list"
        
        logger.info("✓ Embedder tests passed")
        return True
    except Exception as e:
        logger.error(f"✗ Embedder test failed: {e}")
        return False

def test_ingestor():
    """Test Ingestor module."""
    logger.info("Testing Ingestor...")
    try:
        from src.core.ingestion.ingestor import Ingestor
        
        ingestor = Ingestor()
        
        # Test fetch_osint
        data = ingestor.fetch_osint(["http://example.com"])
        assert isinstance(data, list), "fetch_osint should return list"
        
        # Test normalize_data
        normalized = ingestor.normalize_data({"url": "test", "content": "data"})
        assert "source" in normalized, "normalized data should have source"
        
        # Test batch_ingest
        result = ingestor.batch_ingest([{"data": "test"}])
        assert result == True, "batch_ingest should return True"
        
        logger.info("✓ Ingestor tests passed")
        return True
    except Exception as e:
        logger.error(f"✗ Ingestor test failed: {e}")
        return False

def test_preprocessor():
    """Test Preprocessor module."""
    logger.info("Testing Preprocessor...")
    try:
        from src.core.preprocess.preprocessor import Preprocessor
        
        preprocessor = Preprocessor()
        
        # Test clean_text
        cleaned = preprocessor.clean_text("  test   text  ")
        assert cleaned == "test text", "Should clean whitespace"
        
        # Test tokenize
        tokens = preprocessor.tokenize("hello world")
        assert len(tokens) == 2, "Should tokenize into 2 words"
        
        # Test prepare_for_embedding
        prepared = preprocessor.prepare_for_embedding({"data": "test"})
        assert isinstance(prepared, str), "Should return string"
        
        logger.info("✓ Preprocessor tests passed")
        return True
    except Exception as e:
        logger.error(f"✗ Preprocessor test failed: {e}")
        return False

def test_pinecone_handler():
    """Test PineconeHandler module."""
    logger.info("Testing PineconeHandler...")
    try:
        from src.models.embeddings.pinecone_handler import PineconeHandler
        
        handler = PineconeHandler()
        
        # Test upsert_vectors (should handle missing connection gracefully)
        result = handler.upsert_vectors([("id1", [0.1, 0.2], {})])
        assert isinstance(result, bool), "upsert_vectors should return bool"
        
        # Test query_vectors
        results = handler.query_vectors([0.1, 0.2, 0.3])
        assert isinstance(results, list), "query_vectors should return list"
        
        logger.info("✓ PineconeHandler tests passed")
        return True
    except Exception as e:
        logger.error(f"✗ PineconeHandler test failed: {e}")
        return False

def test_storage():
    """Test Storage module."""
    logger.info("Testing Storage...")
    try:
        from src.models.storage.data_storage import Storage
        
        storage = Storage()
        
        # Test save_to_postgres
        result = storage.save_to_postgres("test_table", {"col": "value"})
        assert result == True, "save_to_postgres should return True"
        
        # Test load_from_postgres
        data = storage.load_from_postgres("test_table", {})
        assert isinstance(data, list), "load_from_postgres should return list"
        
        # Test cache_local
        result = storage.cache_local("key", "data")
        assert result == True, "cache_local should return True"
        
        logger.info("✓ Storage tests passed")
        return True
    except Exception as e:
        logger.error(f"✗ Storage test failed: {e}")
        return False

def test_filter():
    """Test Filter module."""
    logger.info("Testing Filter...")
    try:
        from src.axis.filters.content_filter import Filter
        
        filter_obj = Filter()
        
        # Test apply_rules
        result = filter_obj.apply_rules({"content": "test"})
        assert result == True, "Should pass with content"
        
        result = filter_obj.apply_rules({})
        assert result == False, "Should fail without content"
        
        # Test exclude_irrelevant
        result = filter_obj.exclude_irrelevant({"content": "test"})
        assert isinstance(result, bool), "Should return bool"
        
        logger.info("✓ Filter tests passed")
        return True
    except Exception as e:
        logger.error(f"✗ Filter test failed: {e}")
        return False

def test_scraper():
    """Test Scraper module."""
    logger.info("Testing Scraper...")
    try:
        from src.axis.scrapers.osint_scraper import Scraper
        
        scraper = Scraper()
        
        # Test scrape_osint_sources
        data = scraper.scrape_osint_sources(["source1"])
        assert isinstance(data, list), "Should return list"
        
        # Test scrape_news_rss
        data = scraper.scrape_news_rss(["rss1"])
        assert isinstance(data, list), "Should return list"
        
        # Test scrape_public_datasets
        data = scraper.scrape_public_datasets(["dataset1"])
        assert isinstance(data, list), "Should return list"
        
        logger.info("✓ Scraper tests passed")
        return True
    except Exception as e:
        logger.error(f"✗ Scraper test failed: {e}")
        return False

def test_parser():
    """Test Parser module."""
    logger.info("Testing Parser...")
    try:
        from src.axis.parsers.data_parser import Parser
        
        parser = Parser()
        
        # Test parse_html
        result = parser.parse_html("<html><body>test</body></html>")
        assert isinstance(result, str), "Should return string"
        
        # Test parse_json
        result = parser.parse_json('{"key": "value"}')
        assert result == {"key": "value"}, "Should parse JSON correctly"
        
        # Test parse_csv
        result = parser.parse_csv("col1,col2\nval1,val2")
        assert isinstance(result, list), "Should return list"
        
        logger.info("✓ Parser tests passed")
        return True
    except Exception as e:
        logger.error(f"✗ Parser test failed: {e}")
        return False

def test_cache_manager():
    """Test CacheManager module."""
    logger.info("Testing CacheManager...")
    try:
        from src.storage.cache_manager import CacheManager
        
        cache = CacheManager()
        
        # Test save_temp
        result = cache.save_temp("key1", "data1")
        assert result == True, "Should save successfully"
        
        # Test load_temp
        data = cache.load_temp("key1")
        assert data == "data1", "Should retrieve saved data"
        
        # Test clear_cache
        result = cache.clear_cache()
        assert result == True, "Should clear successfully"
        
        data = cache.load_temp("key1")
        assert data is None, "Data should be cleared"
        
        logger.info("✓ CacheManager tests passed")
        return True
    except Exception as e:
        logger.error(f"✗ CacheManager test failed: {e}")
        return False

def main():
    """Run all tests."""
    logger.info("=" * 60)
    logger.info("Starting Transcendence T1 Module Tests")
    logger.info("=" * 60)
    
    tests = [
        ("AgentManager", test_agentmanager),
        ("Core", test_core),
        ("Analyzer", test_analyzer),
        ("Embedder", test_embedder),
        ("Ingestor", test_ingestor),
        ("Preprocessor", test_preprocessor),
        ("PineconeHandler", test_pinecone_handler),
        ("Storage", test_storage),
        ("Filter", test_filter),
        ("Scraper", test_scraper),
        ("Parser", test_parser),
        ("CacheManager", test_cache_manager),
    ]
    
    results = {}
    for name, test_func in tests:
        results[name] = test_func()
        print()  # Add spacing between tests
    
    # Summary
    logger.info("=" * 60)
    logger.info("Test Summary")
    logger.info("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        logger.info(f"{name:20s}: {status}")
    
    logger.info("=" * 60)
    logger.info(f"Total: {passed}/{total} tests passed")
    logger.info("=" * 60)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
