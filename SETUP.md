# Development Setup Guide

This guide explains how to set up a development environment for Open Notebook.

## Prerequisites

- Python 3.11 or 3.12
- SurrealDB
- Git

## Installation Steps

### 1. Create a Virtual Environment

It's highly recommended to use a project-specific virtual environment to avoid dependency conflicts:

```bash
# Using venv (built into Python)
python3.11 -m venv .venv
source .venv/bin/activate  # On Linux/macOS
# OR
.venv\Scripts\activate  # On Windows

# OR using uv (recommended for faster dependency resolution)
uv venv
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
# Install in development mode
pip install -e ".[dev]"

# OR using uv
uv pip install -e ".[dev]"
```

### 3. Start SurrealDB

```bash
# Start SurrealDB with file storage
surreal start --user root --pass root file:test.db

# OR start with Docker
docker run -d --name surrealdb \
  -p 8000:8000 \
  surrealdb/surrealdb:latest \
  start --user root --pass root memory
```

### 4. Configure Environment Variables

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` and set at minimum:

```bash
# Database configuration
SURREAL_URL="ws://localhost:8000/rpc"
SURREAL_USER="root"
SURREAL_PASSWORD="root"
SURREAL_NAMESPACE="open_notebook"
SURREAL_DATABASE="production"

# AI provider (choose one or more)
OPENAI_API_KEY="your-key-here"
# OR
ANTHROPIC_API_KEY="your-key-here"
```

### 5. Load Environment Variables

```bash
# Load from .env file
source .env  # On Linux/macOS
# OR
export $(cat .env | xargs)  # Alternative

# On Windows PowerShell
Get-Content .env | ForEach-Object {
    $var = $_.Split('=')
    [Environment]::SetEnvironmentVariable($var[0], $var[1])
}
```

### 6. Initialize the Database

Run the migration script to create database tables:

```bash
python -m open_notebook.database.migrate
```

### 7. Configure Default AI Models

After the first migration, you need to configure default AI models:

```bash
python -c "
import asyncio
from open_notebook.domain.models import DefaultModels

async def setup_models():
    defaults = DefaultModels(
        default_chat_model='model:openai-gpt-4o-mini',
        default_transformation_model='model:openai-gpt-4o-mini',
        large_context_model='model:anthropic-claude-3-5-sonnet-20241022',
        default_embedding_model='model:openai-text-embedding-3-small',
    )
    await defaults.save()
    print('✓ Default models configured')

asyncio.run(setup_models())
"
```

## Common Issues

### NumPy Compatibility Issue

**Error**: `A module that was compiled using NumPy 1.x cannot be run in NumPy 2.4.0`

**Solution**: The project is using a virtual environment from another project with incompatible NumPy version. Create a project-specific virtual environment:

```bash
# Create new venv
python3.11 -m venv .venv
source .venv/bin/activate

# Reinstall dependencies
pip install -e ".[dev]"
```

### Database Authentication Error

**Error**: `There was a problem with authentication`

**Solution**: Ensure SurrealDB is running and credentials match:

```bash
# Check SurrealDB is running
ps aux | grep surreal

# Test connection
surreal sql --conn ws://localhost:8000 --user root --pass root \
  --ns open_notebook --db production \
  --query "SELECT * FROM model;"
```

### No module named 'open_notebook'

**Solution**: Install the package in development mode:

```bash
pip install -e .
```

## Testing Your Setup

Run the basic usage example to verify everything is working:

```bash
python examples/basic_usage.py
```

Run the chat example to test AI functionality:

```bash
python examples/chat_example.py
```

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=open_notebook

# Run specific test file
pytest tests/test_domain.py
```

### Code Quality

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Type checking
mypy open_notebook/
```

## Next Steps

- Read the [README.md](README.md) for usage examples
- Explore the [examples/](examples/) directory
- Check [CLAUDE.md](CLAUDE.md) for project-specific instructions

## Getting Help

- Check existing [GitHub Issues](https://github.com/lfnovo/open-notebook/issues)
- Create a new issue with error details and environment information
