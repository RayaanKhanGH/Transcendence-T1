# Transcendence T1 - Project Standards & Conventions

**Version:** 1.0.0  
**Date:** 2025-11-22  
**Status:** Official Standard

---

## 1. Directory Structure Standards

### 1.1 Root Level Organization

```
trancsendence/
├── .env                        # Environment variables (gitignored)
├── .gitignore                  # Git ignore rules
├── README.md                   # Project overview
├── requirements.txt            # Python dependencies
├── config/                     # Configuration files
├── docs/                       # All documentation
├── scripts/                    # Utility scripts
├── src/                        # Source code
└── tests/                      # Test files
```

### 1.2 Source Code Structure

```
src/
├── __init__.py
├── agent_manager.py            # Agent orchestration
├── system_core.py              # Main pipeline
├── axis/                       # OSINT layer
│   ├── __init__.py
│   ├── filters/
│   ├── parsers/
│   └── scrapers/
├── core/                       # Core processing
│   ├── __init__.py
│   ├── analysis/
│   ├── embed/
│   ├── ingestion/
│   └── preprocess/
├── models/                     # Data models
│   ├── __init__.py
│   ├── embeddings/
│   └── storage/
└── storage/                    # Storage layer
    ├── __init__.py
    └── cache/
```

### 1.3 Documentation Structure

```
docs/
├── README.md                   # Documentation index
├── USAGE.md                    # User guide
├── QUICK_START.md              # Developer quick start
├── REVIEWER_README.md          # Reviewer guide
├── guides/                     # Detailed guides
│   ├── installation.md
│   ├── configuration.md
│   └── deployment.md
├── api/                        # API documentation
│   └── endpoints.md
└── reports/                    # Project reports
    ├── testing/                # Test reports
    └── performance/            # Performance reports
```

### 1.4 Test Structure

```
tests/
├── __init__.py
├── README.md                   # Test documentation
├── test_imports.py             # Import verification
├── test_all_modules.py         # Full test suite
├── unit/                       # Unit tests
├── integration/                # Integration tests
└── fixtures/                   # Test fixtures
```

---

## 2. Naming Conventions

### 2.1 Python Files & Modules

**Format:** `snake_case`

✅ **Correct:**
- `agent_manager.py`
- `system_core.py`
- `data_storage.py`
- `pinecone_handler.py`

❌ **Incorrect:**
- `agentmanager.py`
- `SystemCore.py`
- `dataStorage.py`

### 2.2 Python Classes

**Format:** `PascalCase`

✅ **Correct:**
```python
class AgentManager:
class SystemCore:
class DataStorage:
class PineconeHandler:
```

❌ **Incorrect:**
```python
class agent_manager:
class systemCore:
class dataStorage:
```

### 2.3 Python Functions & Methods

**Format:** `snake_case`

✅ **Correct:**
```python
def launch_agent():
def schedule_task():
def monitor_agents():
def generate_embeddings():
```

❌ **Incorrect:**
```python
def launchAgent():
def scheduleTask():
def MonitorAgents():
```

### 2.4 Python Variables

**Format:** `snake_case`

✅ **Correct:**
```python
agent_id = "agent_01"
task_details = {}
embedding_vector = []
```

❌ **Incorrect:**
```python
agentId = "agent_01"
TaskDetails = {}
embeddingVector = []
```

### 2.5 Python Constants

**Format:** `UPPER_SNAKE_CASE`

✅ **Correct:**
```python
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30
API_BASE_URL = "https://api.example.com"
```

### 2.6 Documentation Files

**Format:** `UPPER_SNAKE_CASE.md` for root-level, `Title_Case.md` for nested

✅ **Correct:**
- `README.md` (root level)
- `USAGE.md` (root level)
- `QUICK_START.md` (root level)
- `Installation_Guide.md` (nested)
- `API_Reference.md` (nested)

### 2.7 Test Files

**Format:** `test_<module_name>.py`

✅ **Correct:**
- `test_imports.py`
- `test_all_modules.py`
- `test_agent_manager.py`
- `test_system_core.py`

### 2.8 Script Files

**Format:** `<action>_<target>.py`

✅ **Correct:**
- `quick_demo.py`
- `demo_cli.py`
- `run_tests.py`
- `setup_database.py`

---

## 3. Timestamp Formats

### 3.1 File Timestamps

**Format:** `YYYY-MM-DD`

✅ **Correct:**
- `VERIFICATION_REPORT_2025-11-22.md`
- `TEST_RESULTS_2025-11-22.txt`
- `BACKUP_2025-11-22.sql`

❌ **Incorrect:**
- `VERIFICATION_REPORT_11-22-2025.md`
- `TEST_RESULTS_22-11-2025.txt`
- `BACKUP_2025_11_22.sql`

### 3.2 Code Timestamps

**Format:** ISO 8601 - `YYYY-MM-DDTHH:MM:SS+TZ`

✅ **Correct:**
```python
timestamp = "2025-11-22T15:52:16+07:00"
created_at = "2025-11-22T08:30:00Z"
```

❌ **Incorrect:**
```python
timestamp = "11/22/2025 3:52 PM"
created_at = "22-11-2025 08:30:00"
```

### 3.3 Log Timestamps

**Format:** `YYYY-MM-DD HH:MM:SS`

✅ **Correct:**
```
2025-11-22 15:52:16 - INFO - System started
2025-11-22 15:52:17 - DEBUG - Loading configuration
```

### 3.4 Database Timestamps

**Format:** ISO 8601 UTC

✅ **Correct:**
```sql
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
```

---

## 4. Code Style Standards

### 4.1 Python Style Guide

**Base:** PEP 8

**Line Length:** 100 characters (relaxed from 79)

**Indentation:** 4 spaces (no tabs)

**Imports:**
```python
# Standard library
import os
import sys
from typing import List, Dict, Any

# Third-party
import pandas as pd
from rich.console import Console

# Local
from src.agent_manager import AgentManager
from src.core.analysis.analyzer import Analyzer
```

**Docstrings:**
```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of function.

    Args:
        param1 (str): Description of param1.
        param2 (int): Description of param2.

    Returns:
        bool: Description of return value.

    Raises:
        ValueError: When param2 is negative.
    """
    pass
```

**Type Hints:**
```python
def process_data(
    data: List[Dict[str, Any]],
    threshold: float = 0.5
) -> Dict[str, List[float]]:
    """Process data and return results."""
    pass
```

### 4.2 Markdown Style Guide

**Headers:**
```markdown
# H1 - Document Title
## H2 - Major Section
### H3 - Subsection
#### H4 - Minor Section
```

**Lists:**
```markdown
- Unordered item 1
- Unordered item 2
  - Nested item

1. Ordered item 1
2. Ordered item 2
   1. Nested ordered item
```

**Code Blocks:**
````markdown
```python
def example():
    """Always specify language."""
    pass
```
````

**Tables:**
```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Value 1  | Value 2  | Value 3  |
```

**Links:**
```markdown
[Link Text](https://example.com)
[Relative Link](./docs/guide.md)
```

---

## 5. Version Control Standards

### 5.1 Commit Messages

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Maintenance tasks

**Examples:**
```
feat(agent): Add multi-agent orchestration

Implemented AgentManager class with launch, schedule, and monitor capabilities.

Closes #123
```

```
fix(embedder): Handle empty text input

Added validation to prevent errors when processing empty strings.
```

### 5.2 Branch Naming

**Format:** `<type>/<description>`

✅ **Correct:**
- `feature/agent-manager`
- `fix/embedding-error`
- `docs/api-reference`
- `refactor/storage-layer`

❌ **Incorrect:**
- `AgentManager`
- `fix_embedding`
- `docs`

---

## 6. Configuration Standards

### 6.1 Environment Variables

**Format:** `UPPER_SNAKE_CASE`

✅ **Correct:**
```bash
PINECONE_API_KEY=your_key
DATABASE_URL=postgresql://...
GEMINI_API_KEY=your_key
LOG_LEVEL=INFO
```

### 6.2 Configuration Files

**Format:** YAML or JSON

**YAML Example:**
```yaml
# config/app.yaml
app:
  name: transcendence-t1
  version: 1.0.0
  environment: development

database:
  host: localhost
  port: 5432
  name: transcendence_db

logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

---

## 7. Documentation Standards

### 7.1 README Structure

```markdown
# Project Name

Brief description

## Features
## Installation
## Quick Start
## Usage
## Documentation
## Contributing
## License
```

### 7.2 Code Documentation

**Required:**
- Module docstring
- Class docstring
- Public method docstrings
- Complex function docstrings

**Optional:**
- Private method docstrings
- Inline comments for complex logic

---

## 8. Testing Standards

### 8.1 Test Naming

```python
def test_<function>_<scenario>_<expected_result>():
    """Test that function does X when Y."""
    pass
```

**Examples:**
```python
def test_launch_agent_with_valid_config_returns_true():
def test_generate_embeddings_with_empty_list_raises_error():
def test_cache_manager_clear_removes_all_items():
```

### 8.2 Test Structure

```python
def test_example():
    """Test description."""
    # Arrange
    setup_data = create_test_data()
    
    # Act
    result = function_under_test(setup_data)
    
    # Assert
    assert result == expected_value
```

---

## 9. Logging Standards

### 9.1 Log Levels

- `DEBUG`: Detailed diagnostic information
- `INFO`: General informational messages
- `WARNING`: Warning messages
- `ERROR`: Error messages
- `CRITICAL`: Critical errors

### 9.2 Log Format

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

**Example Output:**
```
2025-11-22 15:52:16 - agent_manager - INFO - Agent launched successfully
2025-11-22 15:52:17 - embedder - DEBUG - Generating embeddings for 10 texts
2025-11-22 15:52:18 - storage - ERROR - Failed to connect to database
```

---

## 10. API Standards

### 10.1 REST API Endpoints

**Format:** `/api/v1/<resource>/<action>`

✅ **Correct:**
- `GET /api/v1/agents`
- `POST /api/v1/agents`
- `GET /api/v1/agents/{id}`
- `PUT /api/v1/agents/{id}`
- `DELETE /api/v1/agents/{id}`

### 10.2 Response Format

```json
{
  "status": "success",
  "data": {
    "id": "agent_01",
    "name": "OSINT Agent",
    "status": "active"
  },
  "timestamp": "2025-11-22T15:52:16+07:00"
}
```

---

## 11. Security Standards

### 11.1 Secrets Management

- ✅ Use environment variables
- ✅ Use `.env` files (gitignored)
- ✅ Use secret management services
- ❌ Never commit secrets to git
- ❌ Never hardcode API keys

### 11.2 Input Validation

- ✅ Validate all user input
- ✅ Sanitize data before processing
- ✅ Use type hints and validation
- ✅ Handle errors gracefully

---

## 12. Performance Standards

### 12.1 Code Optimization

- Use generators for large datasets
- Implement caching where appropriate
- Avoid unnecessary loops
- Use async/await for I/O operations

### 12.2 Database Optimization

- Use indexes on frequently queried columns
- Implement connection pooling
- Use batch operations
- Optimize queries

---

## Compliance Checklist

### Code
- [ ] Follows PEP 8
- [ ] Has type hints
- [ ] Has docstrings
- [ ] Has error handling
- [ ] Has logging

### Documentation
- [ ] Has README
- [ ] Has usage guide
- [ ] Has API docs
- [ ] Has inline comments

### Testing
- [ ] Has unit tests
- [ ] Has integration tests
- [ ] All tests passing
- [ ] Coverage > 80%

### Version Control
- [ ] Proper commit messages
- [ ] Proper branch naming
- [ ] No secrets in commits
- [ ] Clean history

---

**Last Updated:** 2025-11-22T15:52:16+07:00  
**Version:** 1.0.0  
**Status:** ✅ Official Standard
