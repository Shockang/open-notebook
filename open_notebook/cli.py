#!/usr/bin/env python3
"""
Open Notebook CLI - Command-line interface for Open Notebook

Usage:
    python -m open_notebook.cli notebooks list
    python -m open_notebook.cli chat <notebook_id>
"""

import asyncio
import sys
from typing import Optional

import click


@click.group()
@click.version_option(version="2.0.0-alpha")
def cli():
    """Open Notebook - Privacy-focused AI Research Assistant"""
    pass


@cli.group()
def notebooks():
    """Manage notebooks"""
    pass


@notebooks.command("create")
@click.argument("name")
@click.option("--description", "-d", default="", help="Notebook description")
def create_notebook(name: str, description: str):
    """Create a new notebook"""

    async def _create():
        from open_notebook import create_notebook

        nb = await create_notebook(name, description)
        click.echo(f"✓ Created notebook: {nb.name}")
        click.echo(f"  ID: {nb.id}")

    asyncio.run(_create())


@notebooks.command("list")
@click.option("--archived", "-a", is_flag=True, help="Include archived notebooks")
def list_notebooks_cmd(archived: bool):
    """List all notebooks"""

    async def _list():
        from open_notebook import list_notebooks, Notebook

        notebooks = await Notebook.get_all()
        if not notebooks:
            click.echo("No notebooks found.")
            return

        click.echo(f"\nFound {len(notebooks)} notebook(s):\n")
        for nb in notebooks:
            if archived or not nb.archived:
                archive_flag = " [ARCHIVED]" if nb.archived else ""
                click.echo(f"  • {nb.name}{archive_flag}")
                click.echo(f"    ID: {nb.id}")
                if nb.description:
                    click.echo(f"    Description: {nb.description}")
                click.echo()

    asyncio.run(_list())


@notebooks.command("archive")
@click.argument("notebook_id")
def archive_notebook(notebook_id: str):
    """Archive a notebook"""

    async def _archive():
        from open_notebook import Notebook

        nb = await Notebook.get(notebook_id)
        nb.archived = True
        await nb.save()
        click.echo(f"✓ Archived notebook: {nb.name}")

    asyncio.run(_archive())


@cli.group()
def sources():
    """Manage sources in notebooks"""
    pass


@sources.command("add")
@click.argument("notebook_id")
@click.option("--url", "-u", help="URL to add as source")
@click.option("--file", "-f", type=click.Path(exists=True), help="File path to add as source")
@click.option("--text", "-t", help="Text content to add as source")
@click.option("--title", "-h", help="Title for the source")
def add_source(notebook_id: str, url: Optional[str], file: Optional[str], text: Optional[str], title: Optional[str]):
    """Add a source to a notebook"""

    if not any([url, file, text]):
        click.echo("Error: Must provide one of: --url, --file, or --text")
        sys.exit(1)

    async def _add():
        from open_notebook import Source
        from open_notebook.domain.notebook import Asset

        # Determine source content and asset
        if url:
            # For URL, create an Asset with the URL
            asset = Asset(url=url)
            source_text = f"URL: {url}"
            source_title = title or f"URL: {url}"
        elif file:
            # Read file content
            with open(file, 'r') as f:
                file_content = f.read()
            asset = Asset(file_path=file)
            source_text = file_content
            source_title = title or file
        else:  # text
            asset = None
            source_text = text
            source_title = title or "Manual Text Entry"

        # Create and save source
        source = Source(
            title=source_title,
            full_text=source_text,
            asset=asset
        )
        await source.save()
        await source.add_to_notebook(notebook_id)

        click.echo(f"✓ Added source to notebook")
        click.echo(f"  Source ID: {source.id}")
        click.echo(f"  Title: {source.title}")

    asyncio.run(_add())


@sources.command("list")
@click.argument("notebook_id")
def list_sources(notebook_id: str):
    """List sources in a notebook"""

    async def _list():
        from open_notebook import Notebook

        nb = await Notebook.get(notebook_id)
        sources = await nb.get_sources()

        if not sources:
            click.echo(f"No sources found in notebook: {nb.name}")
            return

        click.echo(f"\nSources in '{nb.name}' ({len(sources)} total):\n")
        for source in sources:
            click.echo(f"  • {source.title}")
            click.echo(f"    ID: {source.id}")
            if source.asset and source.asset.url:
                click.echo(f"    URL: {source.asset.url}")
            click.echo()

    asyncio.run(_list())


@cli.command()
@click.argument("notebook_id")
@click.argument("question")
@click.option("--model", "-m", help="Override AI model")
def chat(notebook_id: str, question: str, model: Optional[str]):
    """Chat with a notebook using AI"""

    async def _chat():
        from open_notebook import Notebook
        from open_notebook.graphs.chat import ThreadState
        from langchain_core.messages import HumanMessage

        nb = await Notebook.get(notebook_id)

        click.echo(f"\n📓 Chatting with: {nb.name}")
        click.echo(f"📝 Question: {question}\n")

        # Create chat state
        state = ThreadState(
            messages=[HumanMessage(content=question)],
            notebook=nb,
            context=None,
            context_config=None,
            model_override=model,
        )

        # Get AI response (simplified - actual implementation would use the graph)
        from open_notebook.graphs.chat import call_model_with_messages
        from langgraph.checkpoint.sqlite import SqliteSaver

        response = await call_model_with_messages(state, None)
        ai_message = response["messages"][-1]

        click.echo(f"\n🤖 Answer:\n{ai_message.content}\n")

    asyncio.run(_chat())


# Podcast command commented out - requires more complex setup
# Use the Python API directly for podcast generation
# @cli.group()
# def podcasts():
#     """Manage podcasts (coming soon)"""
#     pass
#
#
# @podcasts.command("generate")
# @click.argument("notebook_id")
# @click.option("--speakers", "-s", default=2, type=int, help="Number of speakers (1-4)")
# @click.option("--model", "-m", help="AI model to use")
# def generate_podcast(notebook_id: str, speakers: int, model: Optional[str]):
#     """Generate a podcast from notebook sources"""
#     click.echo("Podcast generation via CLI is under development.")
#     click.echo("Please use the Python API for podcast functionality.")


if __name__ == "__main__":
    cli()
