import os
import json
import unittest
from unittest import mock
from datetime import datetime

# Import the pipeline function and EntityExtractor
from src.core.pipeline.intelligence_pipeline import run_intelligence_cycle, all_entities
from src.core.analysis.entity_extractor import EntityExtractor

# Import the pipeline function
from src.core.pipeline.intelligence_pipeline import run_intelligence_cycle, all_entities

# Mock classes for dependencies
class MockAnalyzer:
    def __init__(self):
        self.client = None
    def generate_plan(self, prompt: str):
        # Return a deterministic list of URLs for testing
        return [
            "https://example.com/article1",
            "https://example.com/article2",
            "https://example.com/article3",
        ]
    def generate_summary(self, data: str):
        return f"Summary of {data[:30]}..."

class MockIngestor:
    def fetch_osint(self, urls):
        # Return mock successful fetch results
        return [
            {"url": url, "status": "success", "content": f"Content from {url}"}
            for url in urls
        ]

class MockPreprocessor:
    def clean_text(self, text: str) -> str:
        # Simple cleaning: strip whitespace
        return text.strip()

class MockPineconeHandler:
    def __init__(self):
        self.upsert_calls = []
    def upsert_vectors(self, vectors):
        self.upsert_calls.extend(vectors)
        return True



class MockConsole:
    def print(self, *args, **kwargs):
        # Suppress console output during tests
        pass

class TestIntelligencePipeline(unittest.TestCase):
    def setUp(self):
        # Ensure a clean state for global entities list
        global all_entities
        all_entities.clear()
        # Prepare mocks
        self.analyzer = MockAnalyzer()
        self.ingestor = MockIngestor()
        self.preprocessor = MockPreprocessor()
        self.pinecone = MockPineconeHandler()

        self.console = MockConsole()
        # Set up temporary directory with docs subfolder
        self.original_cwd = os.getcwd()
        self.test_dir = os.path.abspath(os.path.join(self.original_cwd, "tests", "tmp"))
        os.makedirs(self.test_dir, exist_ok=True)
        self.docs_dir = os.path.join(self.test_dir, "docs")
        os.makedirs(self.docs_dir, exist_ok=True)
        os.chdir(self.test_dir)
        extractor = EntityExtractor()
        text = "The CVE-2024-12345 vulnerability was reported by Example Corp. More info at https://example.com/vuln"
        entities = extractor.extract(text)
        # Expect at least one CVE, one Entity, and one URL
        types = {e['type'] for e in entities}
        self.assertIn('CVE', types)
        self.assertIn('Entity', types)
        self.assertIn('URL', types)

    def test_run_intelligence_cycle(self):
        # Run the pipeline with mocked dependencies
        report_path = run_intelligence_cycle(
            user_prompt="Test research topic",
            analyzer=self.analyzer,
            ingestor=self.ingestor,
            preprocessor=self.preprocessor,
            pinecone=self.pinecone,
            console=self.console,
        )
        # Verify a report file was created
        self.assertTrue(report_path)
        self.assertTrue(os.path.isfile(report_path))
        # Load the JSON report and validate key sections
        with open(report_path, "r", encoding="utf-8") as f:
            report = json.load(f)
        self.assertIn("report_metadata", report)
        self.assertIn("executive_summary", report)
        self.assertIn("detailed_findings", report)
        # Verify that Pinecone upsert was called for each URL
        self.assertEqual(len(self.pinecone.upsert_calls), 3)

        # Verify that global entity list was populated
        self.assertGreater(len(all_entities), 0)
        # Clean up generated files
        os.remove(report_path)

if __name__ == "__main__":
    unittest.main()
