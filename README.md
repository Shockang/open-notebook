<a id="readme-top"></a>

# Open Notebook

<div align="center">
  <h3 align="center">Open Notebook</h3>

  <p align="center">
    A Python library for privacy-focused, AI-powered research assistance
    <br />
    <a href="https://github.com/lfnovo/open-notebook"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="#installation">Installation</a>
    ·
    <a href="#usage">Usage</a>
    ·
    <a href="#examples">Examples</a>
    ·
    <a href="#api-reference">API Reference</a>
  </p>
</div>

## About Open Notebook

**Open Notebook** is a Python library that provides privacy-focused, AI-powered research assistance. It helps you organize research materials, generate insights, create podcasts, and chat with your documents using configurable AI providers.

### Key Features

- **🔒 Privacy-First**: Your data stays under your control - use self-hosted databases and local AI models
- **🤖 Multi-Model AI Support**: Support for 16+ AI providers including OpenAI, Anthropic, Ollama, LM Studio, Groq, and more
- **📚 Universal Content Support**: Process PDFs, videos, audio, web pages, Office docs, and more
- **🎙️ Podcast Generation**: Create professional multi-speaker podcasts from your research
- **🔍 Intelligent Search**: Full-text and vector search across all your content
- **💬 Context-Aware Chat**: AI conversations powered by your research materials
- **📝 AI-Assisted Notes**: Generate insights or write notes manually
- **🎯 Python Library**: Simple, async Python API for easy integration

### What's Different from v1.x?

This version (v2.0) is a **complete refactor** that focuses on providing a Python library rather than a web application. The web UI, API server, and Docker deployment have been removed in favor of a clean library API with CLI support.

If you're looking for the web application, please use the v1.x releases.

## Installation

### Requirements

- Python 3.11 or 3.12
- SurrealDB (for data storage)

### Install SurrealDB

**macOS/Linux:**
```bash
curl -sSf https://install.surrealdb.com | sh
```

**With Docker:**
```bash
docker run -d --name surrealdb \
  -p 8000:8000 \
  surrealdb/surrealdb:latest \
  start --user root --pass root memory
```

### Install Open Notebook

```bash
pip install open-notebook
```

Or install from source:
```bash
git clone https://github.com/lfnovo/open-notebook
cd open-notebook
pip install -e .
```

### Configuration

Set the following environment variables:

```bash
# SurrealDB connection (required)
export SURREAL_URL="ws://localhost:8000/rpc"
export SURREAL_USER="root"
export SURREAL_PASSWORD="root"
export SURREAL_NAMESPACE="open_notebook"
export SURREAL_DATABASE="production"

# AI provider (choose one or more)
export OPENAI_API_KEY="your-key-here"  # For OpenAI models
export ANTHROPIC_API_KEY="your-key-here"  # For Claude models
# Or use local models with Ollama (no API key needed)
```

## Usage

### Quick Start

```python
import asyncio
from open_notebook import create_notebook, Source, Notebook

async def main():
    # Create a notebook
    notebook = await create_notebook(
        name="AI Research",
        description="Research on latest AI developments"
    )

    # Add a source
    source = Source(
        title="AI Overview",
        full_text="Artificial Intelligence is revolutionizing many industries..."
    )
    await source.save()
    await source.add_to_notebook(notebook.id)

    # List sources
    sources = await notebook.get_sources()
    print(f"Added {len(sources)} source(s)")

asyncio.run(main())
```

### Chat with Your Research

```python
from open_notebook import Notebook
from open_notebook.graphs.chat import ThreadState
from langchain_core.messages import HumanMessage

async def chat_with_notebook(notebook_id: str, question: str):
    # Load notebook
    notebook = await Notebook.get(notebook_id)

    # Create chat state
    state = ThreadState(
        messages=[HumanMessage(content=question)],
        notebook=notebook,
    )

    # Get AI response
    from open_notebook.graphs.chat import call_model_with_messages
    response = await call_model_with_messages(state, None)
    ai_message = response["messages"][-1]

    return ai_message.content

# Usage
answer = await chat_with_notebook("notebook:abc123", "What are the key findings?")
print(answer)
```

### Add Different Source Types

```python
from open_notebook import Source
from open_notebook.domain.notebook import Asset

# From URL
asset = Asset(url="https://example.com/article")
source = Source(title="Article", asset=asset)
await source.save()
await source.add_to_notebook(notebook_id)

# From file
asset = Asset(file_path="/path/to/document.pdf")
source = Source(title="Document", asset=asset)
await source.save()
await source.add_to_notebook(notebook_id)

# From text
source = Source(title="Notes", full_text="Your text content here...")
await source.save()
await source.add_to_notebook(notebook_id)
```

## CLI Usage

Open Notebook includes a command-line interface for common operations:

```bash
# List notebooks
python -m open_notebook.cli notebooks list

# Create a notebook
python -m open_notebook.cli notebooks create "My Research" --description "AI research project"

# Archive a notebook
python -m open_notebook.cli notebooks archive <notebook_id>

# Add sources
python -m open_notebook.cli sources add <notebook_id> --text "Some text content"
python -m open_notebook.cli sources add <notebook_id> --url "https://example.com"
python -m open_notebook.cli sources add <notebook_id> --file /path/to/file.txt

# List sources in a notebook
python -m open_notebook.cli sources list <notebook_id>

# Chat with a notebook
python -m open_notebook.cli chat <notebook_id> "What are the key findings?"
```

## Examples

The `examples/` directory contains detailed examples:

- **basic_usage.py**: Basic notebook operations
- **chat_example.py**: Chat with your research using AI

Run examples:
```bash
python examples/basic_usage.py
python examples/chat_example.py
```

## AI Provider Support

Open Notebook supports 16+ AI providers through the [Esperanto](https://github.com/lfnovo/esperanto) library:

| Provider | LLM | Embeddings | Speech-to-Text | Text-to-Speech |
|----------|-----|------------|----------------|----------------|
| OpenAI | ✅ | ✅ | ✅ | ✅ |
| Anthropic | ✅ | ❌ | ❌ | ❌ |
| Groq | ✅ | ❌ | ✅ | ❌ |
| Google (GenAI) | ✅ | ✅ | ❌ | ✅ |
| Ollama | ✅ | ✅ | ❌ | ❌ |
| Mistral | ✅ | ❌ | ❌ | ❌ |
| DeepSeek | ✅ | ❌ | ❌ | ❌ |
| And more... | | | | |

Configure providers using environment variables. See `.env.example` for all options.

## API Reference

### Core Classes

#### `Notebook`

Represents a research notebook containing sources and notes.

```python
from open_notebook import Notebook, create_notebook, list_notebooks

# Create a notebook
notebook = await create_notebook(name="My Research", description="...")

# Get existing notebook
notebook = await Notebook.get(notebook_id)

# List all notebooks
notebooks = await list_notebooks()

# Get sources in notebook
sources = await notebook.get_sources()

# Archive notebook
notebook.archived = True
await notebook.save()
```

#### `Source`

Represents a research source (document, URL, file, etc.).

```python
from open_notebook import Source
from open_notebook.domain.notebook import Asset

# Create from text
source = Source(title="Title", full_text="Content...")
await source.save()
await source.add_to_notebook(notebook_id)

# Create from URL
asset = Asset(url="https://example.com")
source = Source(title="Article", asset=asset)
await source.save()
await source.add_to_notebook(notebook_id)
```

#### `Note`

AI-generated or manual notes from your sources.

```python
from open_notebook import Note

# Create a note
note = Note(
    notebook_id=notebook_id,
    content="Summary of findings..."
)
await note.save()
```

### Convenience Functions

```python
from open_notebook import create_notebook, get_notebook, list_notebooks

# Create notebook
notebook = await create_notebook(name="Research", description="...")

# Get specific notebook
notebook = await get_notebook(notebook_id)

# List all notebooks
notebooks = await list_notebooks(archived=False)
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/lfnovo/open-notebook
cd open-notebook

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=open_notebook
```

### Project Structure

```
open_notebook/
├── __init__.py           # Public API
├── cli.py                # Command-line interface
├── config.py             # Configuration
├── database/             # Database connection and operations
├── domain/               # Domain models (Notebook, Source, Note, etc.)
├── graphs/               # AI workflows (chat, notes, etc.)
├── plugins/              # Content processing plugins
└── utils/                # Utility functions
```

## Roadmap

- [ ] Enhanced documentation and API reference
- [ ] More examples and tutorials
- [ ] Performance optimizations
- [ ] Additional content transformations
- [ ] Enhanced podcast generation features

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

Open Notebook is MIT licensed. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

Built on top of amazing open-source projects:

- **[Podcast Creator](https://github.com/lfnovo/podcast-creator)** - Advanced podcast generation
- **[Surreal Commands](https://github.com/lfnovo/surreal-commands)** - Background job processing
- **[Content Core](https://github.com/lfnovo/content-core)** - Content processing
- **[Esperanto](https://github.com/lfnovo/esperanto)** - Multi-provider AI abstraction
- **[Docling](https://github.com/docling-project/docling)** - Document parsing

## Contact

- **Luis Novo** - [@lfnovo](https://twitter.com/lfnovo)
- **GitHub Issues** - Report bugs and request features

---

<p align="right"><a href="#readme-top">back to top</a></p>
