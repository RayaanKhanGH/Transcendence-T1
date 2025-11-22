# Transcendence T1 - Quick Start Guide

## Running Tests

```bash
# Test all modules
python test_all_modules.py

# Quick import verification
python test_imports.py
```

## Using the Modules

### 1. Agent Manager
```python
from src.agentmanager import AgentManager

manager = AgentManager()
manager.launch_agent("agent_01", {"type": "osint_scraper"})
manager.schedule_task("task_01", {"target": "example.com"})
status = manager.monitor_agents()
```

### 2. System Core (Pipeline Orchestration)
```python
from src.system_core import Core

core = Core()
result = core.run_pipeline({"source": "https://example.com"})
```

### 3. Analysis
```python
from src.core.analysis.analyzer import Analyzer

analyzer = Analyzer()
patterns = analyzer.detect_patterns(data)
score = analyzer.score_relevance(data)
summary = analyzer.generate_summary(data)
```

### 4. Embeddings
```python
from src.core.embed.embedder import Embedder

embedder = Embedder()
embeddings = embedder.generate_embeddings(["text1", "text2"])
embedder.store_embeddings(embeddings)
similar = embedder.retrieve_similar("query text")
```

### 5. Data Ingestion
```python
from src.core.ingestion.ingestor import Ingestor

ingestor = Ingestor()
data = ingestor.fetch_osint(["https://example.com"])
normalized = ingestor.normalize_data(data[0])
ingestor.batch_ingest([normalized])
```

### 6. Preprocessing
```python
from src.core.preprocess.preprocessor import Preprocessor

preprocessor = Preprocessor()
clean = preprocessor.clean_text("  messy   text  ")
tokens = preprocessor.tokenize(clean)
prepared = preprocessor.prepare_for_embedding(tokens)
```

### 7. Vector Database (Pinecone)
```python
from src.models.embeddings.pinecone_handler import PineconeHandler

handler = PineconeHandler(index_name="my-index")
handler.upsert_vectors([("id1", [0.1, 0.2, 0.3], {"meta": "data"})])
results = handler.query_vectors([0.1, 0.2, 0.3], top_k=5)
```

### 8. Storage
```python
from src.models.storage.data_storage import Storage

storage = Storage()
storage.save_to_postgres("table_name", {"col": "value"})
data = storage.load_from_postgres("table_name", {"id": 1})
storage.cache_local("key", data)
```

### 9. Content Filtering
```python
from src.axis.filters.content_filter import Filter

filter_obj = Filter()
if filter_obj.apply_rules(data):
    # Data passed filters
    pass
```

### 10. OSINT Scraping
```python
from src.axis.scrapers.osint_scraper import Scraper

scraper = Scraper()
osint_data = scraper.scrape_osint_sources(["source1", "source2"])
news = scraper.scrape_news_rss(["https://example.com/rss"])
datasets = scraper.scrape_public_datasets(["https://data.gov/..."])
```

### 11. Data Parsing
```python
from src.axis.parsers.data_parser import Parser

parser = Parser()
text = parser.parse_html("<html><body>Content</body></html>")
data = parser.parse_json('{"key": "value"}')
rows = parser.parse_csv("col1,col2\\nval1,val2")
```

### 12. Cache Management
```python
from src.storage.cache_manager import CacheManager

cache = CacheManager()
cache.save_temp("key", {"data": "value"})
data = cache.load_temp("key")
cache.clear_cache()
```

## Environment Variables

Create a `.env` file with:

```env
# Pinecone Vector DB
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENV=your_pinecone_environment

# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Gemini LLM
GEMINI_API_KEY=your_gemini_api_key
```

## Project Structure

```
trancsendence/
├── src/
│   ├── agentmanager.py          # Agent orchestration
│   ├── system_core.py           # Main pipeline
│   ├── core/                    # Core processing modules
│   │   ├── analysis/            # Pattern detection, scoring
│   │   ├── embed/               # Embedding generation
│   │   ├── ingestion/           # Data ingestion
│   │   └── preprocess/          # Text preprocessing
│   ├── models/                  # Data models
│   │   ├── embeddings/          # Vector DB handlers
│   │   └── storage/             # Storage connectors
│   ├── axis/                    # OSINT layer
│   │   ├── filters/             # Content filtering
│   │   ├── scrapers/            # Web scraping
│   │   └── parsers/             # Data parsing
│   └── storage/                 # Cache management
├── docs/                        # Documentation
├── test_all_modules.py          # Test suite
└── test_imports.py              # Import verification
```

## Development Workflow

1. **Set up environment variables** in `.env`
2. **Activate virtual environment**: Already active in your shell
3. **Run tests**: `python test_all_modules.py`
4. **Start developing**: Import and use modules as needed
5. **Add new features**: Follow the modular structure

## Notes

- All modules use Python logging for debugging
- Type hints are included for better IDE support
- Error handling is implemented throughout
- Modules are designed to be extended and customized
