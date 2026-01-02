# Open Notebook Refactoring Design

## Architecture Decision: Hybrid Library + CLI

Based on analysis of the codebase and design principles, the refactored version will be:

**Primary Interface**: Importable Python library
**Secondary Interface**: CLI commands for common operations
**Optional Component**: FastAPI server (can be disabled)

## Rationale

1. **Library-first**: Core functionality accessible via Python API
   - `from open_notebook import Notebook, Source, Chat`
   - Programmable for automation and integration
   - Compatible with design principle: API-first architecture

2. **CLI convenience**: Common operations via command line
   - `python -m open_notebook notebooks list`
   - `python -m open_notebook chat --notebook "My Research"`
   - Quick access without writing code

3. **Optional API server**: FastAPI can run if needed
   - Enable for web access or external integrations
   - Not required for core functionality
   - Reduces dependencies for basic usage

## New Directory Structure

```
open-notebook/
├── open_notebook/              # Core library (KEEP)
│   ├── __init__.py            # Public API exports
│   ├── cli.py                 # CLI commands (NEW)
│   ├── config.py              # Configuration
│   ├── domain/                # Domain models (KEEP)
│   ├── graphs/                # AI services (KEEP)
│   ├── database/              # Database layer (KEEP)
│   ├── utils/                 # Utilities (KEEP)
│   └── exceptions.py          # Exceptions (KEEP)
│
├── api/                       # API server (OPTIONAL)
│   └── ...                    # Keep as separate module
│
├── scripts/                   # Utility scripts (REVIEW)
│   └── ...
│
├── examples/                  # Usage examples (NEW)
│   ├── basic_usage.py
│   ├── chat_example.py
│   └── podcast_example.py
│
├── tests/                     # Tests (KEEP)
│
├── README.md                  # Minimal documentation
├── pyproject.toml             # Dependencies
└── setup.py                   # Installation
```

## Public API Design

### Core Imports

```python
# Simplified imports
from open_notebook import (
    Notebook,      # Notebook management
    Source,        # Source management
    Chat,          # AI chat interface
    Podcast,       # Podcast generation
    config         # Configuration
)

# Initialize configuration
config.init(
    db_url="file:./data.db",
    ai_provider="openai",
    api_key="sk-..."
)

# Create notebook
nb = await Notebook.create(
    name="My Research",
    description="AI research project"
)

# Add sources
source = await nb.add_source(
    type="url",
    content="https://example.com/article"
)

# Chat with context
chat = Chat(notebook=nb)
response = await chat.ask("What are the key findings?")
print(response.content)
```

### CLI Interface

```bash
# Notebook operations
python -m open_notebook notebooks create "My Project"
python -m open_notebook notebooks list
python -m open_notebook notebooks archive <id>

# Source operations
python -m open_notebook sources add <notebook_id> --url <url>
python -m open_notebook sources add <notebook_id> --file <path>
python -m open_notebook sources list <notebook_id>

# Chat
python -m open_notebook chat <notebook_id> "Your question here"

# Podcast
python -m open_notebook podcast generate <notebook_id> --speakers 2
```

## Configuration Approach

### 1. Environment Variables (Primary)
```bash
OPEN_NOTEBOOK_DB_URL="file:./data.db"
OPEN_NOTEBOOK_AI_PROVIDER="openai"
OPEN_NOTEBOOK_API_KEY="sk-..."
OPEN_NOTEBOOK_MODEL="gpt-4"
```

### 2. Configuration File (Optional)
```yaml
# ~/.open-notebook/config.yml
database:
  url: "file:~/notebooks/data.db"

ai:
  provider: "openai"
  api_key: "sk-..."
  model: "gpt-4"
  temperature: 0.7

storage:
  uploads_dir: "~/notebooks/uploads"
  cache_dir: "~/notebooks/cache"
```

### 3. Programmatic (Override)
```python
from open_notebook import config

config.override(
    db_url="custom.db",
    ai_provider="anthropic",
    model="claude-3-opus"
)
```

## Implementation Phases

### Phase 1: Core Library Extraction
**Status**: Ready to start

1. Create `open_notebook/__init__.py` with public API
2. Simplify imports - hide internal details
3. Add convenience methods to domain models
4. Create initialization system

**Files to create/modify**:
- `open_notebook/__init__.py` (new)
- `open_notebook/config.py` (modify)
- `open_notebook/domain/base.py` (add methods)

### Phase 2: CLI Implementation
**Status**: Blocked on Phase 1

1. Create `open_notebook/cli.py`
2. Implement commands using argparse/click
3. Add interactive mode for chat
4. Handle async operations in CLI

**Files to create**:
- `open_notebook/cli.py` (new)

### Phase 3: Simplification
**Status**: Blocked on Phase 1 & 2

1. Make FastAPI optional import
2. Remove hard dependencies on API layer
3. Update `pyproject.toml` dependencies
4. Remove non-essential files

**Files to modify**:
- `pyproject.toml`
- `open_notebook/graphs/*.py` (remove API dependencies if any)
- Deletion list (see SHARED_TASK_NOTES.md)

### Phase 4: Documentation & Examples
**Status**: Blocked on Phase 1-3

1. Create minimal README
2. Add usage examples
3. Add type hints for better IDE support
4. Create migration guide from full version

**Files to create**:
- `README.md` (minimal)
- `examples/*.py`

## Dependencies Review

### Remove After Refactoring:
- FastAPI/Uvicorn (optional, for server mode)
- Starlette (optional, for server mode)
- Pydantic (keep, used in domain models)
- Loguru (keep, logging)

### Must Keep:
- LangChain/LangGraph (AI orchestration)
- SurrealDB (database)
- Content processing libraries
- AI provider SDKs (OpenAI, Anthropic, etc.)

### Add:
- Click or Typer (CLI framework)
- Rich (terminal output formatting)

## Testing Strategy

### Unit Tests
- Domain model operations
- Database queries
- AI service calls (with mocks)

### Integration Tests
- End-to-end workflows
- Database migrations
- CLI commands

### Manual Testing Checklist
- [ ] Create notebook programmatically
- [ ] Add source from URL
- [ ] Add source from file
- [ ] Chat with notebook
- [ ] Generate podcast
- [ ] All CLI commands work
- [ ] Configuration loading from env
- [ ] Configuration loading from file

## Migration Path

### For Current Users
1. Export data from existing installation
2. Install refactored version
3. Import data
4. Update API calls (if using API)

### Breaking Changes
- Direct API calls to `/api/*` endpoints will require running server mode
- Some internal classes may be renamed or moved
- Environment variables may have different names

## Success Criteria

✅ Core functionality accessible via Python API
✅ CLI works for common operations
✅ Can be installed with `pip install open-notebook`
✅ < 10 dependencies (excluding AI providers)
✅ Documentation fits in single README
✅ Tests pass for all core features
✅ Example code works out of the box
