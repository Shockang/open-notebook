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
def add_source(notebook_id: str, url: Optional[str], file: Optional[str], text: Optional[str]):
    """Add a source to a notebook"""

    if not any([url, file, text]):
        click.echo("Error: Must provide one of: --url, --file, or --text")
        sys.exit(1)

    async def _add():
        from open_notebook import Notebook
        from content_core import Content, ContentType

        nb = await Notebook.get(notebook_id)

        # Create content based on input type
        if url:
            content = await Content.from_url(url)
        elif file:
            content = await Content.from_file(file)
        else:  # text
            content = Content(
                content_type=ContentType.text,
                title="Manual Text Entry",
                content=text,
            )

        # Add source to notebook
        source = await nb.add_source(content)
        click.echo(f"✓ Added source to notebook: {nb.name}")
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
            click.echo(f"    Type: {source.source_type}")
            if source.url:
                click.echo(f"    URL: {source.url}")
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


@cli.group()
def podcasts():
    """Manage podcasts"""
    pass


@podcasts.command("generate")
@click.argument("notebook_id")
@click.option("--speakers", "-s", default=2, type=int, help="Number of speakers (1-4)")
@click.option("--model", "-m", help="AI model to use")
def generate_podcast(notebook_id: str, speakers: int, model: Optional[str]):
    """Generate a podcast from notebook sources"""

    if not 1 <= speakers <= 4:
        click.echo("Error: Number of speakers must be between 1 and 4")
        sys.exit(1)

    async def _generate():
        from open_notebook import Notebook, Podcast
        from open_notebook.domain.podcast import SpeakerProfile

        nb = await Notebook.get(notebook_id)
        sources = await nb.get_sources()

        if not sources:
            click.echo(f"Error: No sources found in notebook: {nb.name}")
            sys.exit(1)

        click.echo(f"\n🎙️ Generating podcast for: {nb.name}")
        click.echo(f"📚 Using {len(sources)} source(s)")
        click.echo(f"🗣️ Speakers: {speakers}\n")

        # Create podcast
        podcast = await Podcast.create(
            notebook_id=nb.id,
            speaker_count=speakers,
            model_override=model,
        )

        click.echo(f"\n✓ Podcast generated!")
        click.echo(f"  ID: {podcast.id}")
        click.echo(f"  Status: {podcast.status}")

        if podcast.transcript:
            click.echo(f"\n📝 Transcript Preview:")
            click.echo(podcast.transcript[:500] + "..." if len(podcast.transcript) > 500 else podcast.transcript)

    asyncio.run(_generate())


if __name__ == "__main__":
    cli()
