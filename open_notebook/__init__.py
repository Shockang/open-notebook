"""
Open Notebook - Privacy-focused AI Research Assistant

A Python library for managing notebooks, sources, and AI-powered research.
"""

__version__ = "2.0.0-alpha"

# Core domain models
from open_notebook.domain.notebook import Notebook, Source, Note, SourceInsight
from open_notebook.domain.models import Model, ModelManager
from open_notebook.domain.podcast import PodcastEpisode, SpeakerProfile, EpisodeProfile
from open_notebook.domain.transformation import Transformation

# Exceptions
from open_notebook.exceptions import (
    OpenNotebookError,
    DatabaseOperationError,
    ExternalServiceError,
    InvalidInputError,
    NotFoundError,
)

# Configuration
from open_notebook.config import LANGGRAPH_CHECKPOINT_FILE

# Export main classes
__all__ = [
    # Version
    "__version__",
    # Domain Models
    "Notebook",
    "Source",
    "Note",
    "SourceInsight",
    "Model",
    "ModelManager",
    "PodcastEpisode",
    "SpeakerProfile",
    "EpisodeProfile",
    "Transformation",
    # Exceptions
    "OpenNotebookError",
    "DatabaseOperationError",
    "ExternalServiceError",
    "InvalidInputError",
    "NotFoundError",
    # Config
    "LANGGRAPH_CHECKPOINT_FILE",
]

# Convenience functions for common operations
async def create_notebook(name: str, description: str = "") -> Notebook:
    """
    Create a new notebook.

    Args:
        name: Name of the notebook
        description: Optional description

    Returns:
        Created Notebook instance

    Example:
        >>> from open_notebook import create_notebook
        >>> nb = await create_notebook("My Research", "AI research project")
    """
    notebook = Notebook(name=name, description=description)
    await notebook.save()
    return notebook


async def get_notebook(notebook_id: str) -> Notebook:
    """
    Retrieve a notebook by ID.

    Args:
        notebook_id: The notebook ID

    Returns:
        Notebook instance

    Example:
        >>> from open_notebook import get_notebook
        >>> nb = await get_notebook("notebook:abc123")
    """
    return await Notebook.get(notebook_id)


async def list_notebooks(archived: bool = False) -> list[Notebook]:
    """
    List all notebooks.

    Args:
        archived: Include archived notebooks

    Returns:
        List of Notebook instances

    Example:
        >>> from open_notebook import list_notebooks
        >>> notebooks = await list_notebooks()
        >>> for nb in notebooks:
        ...     print(f"{nb.name}: {nb.source_count} sources")
    """
    return await Notebook.get_all(archived=archived)


# Add convenience functions to exports
__all__.extend(["create_notebook", "get_notebook", "list_notebooks"])
