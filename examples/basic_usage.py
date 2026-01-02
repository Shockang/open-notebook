"""
Open Notebook - Basic Usage Example

This example demonstrates the core functionality of Open Notebook as a Python library.
"""

import asyncio
from open_notebook import (
    create_notebook,
    list_notebooks,
    Notebook,
    Source,
)


async def main():
    """Example: Basic notebook operations"""

    print("=" * 60)
    print("Open Notebook - Basic Usage Example")
    print("=" * 60)

    # 1. Create a new notebook
    print("\n1. Creating a new notebook...")
    notebook = await create_notebook(
        name="AI Research Project",
        description="Research on latest AI developments"
    )
    print(f"   ✓ Created: {notebook.name} (ID: {notebook.id})")

    # 2. List all notebooks
    print("\n2. Listing all notebooks...")
    notebooks = await list_notebooks()
    print(f"   Found {len(notebooks)} notebook(s):")
    for nb in notebooks[:5]:  # Show first 5
        print(f"   - {nb.name}: {nb.description or 'No description'}")

    # 3. Add sources to the notebook
    print("\n3. Adding sources to notebook...")

    # Example: Add from URL
    try:
        from content_core import Content

        # Add a URL source
        print("   Adding source from URL...")
        content = await Content.from_url("https://example.com/article")
        source = await notebook.add_source(content)
        print(f"   ✓ Added: {source.title}")
    except Exception as e:
        print(f"   ⚠ Skipped URL example (requires network): {e}")

    # Example: Add from text
    print("\n   Adding source from text...")
    text_content = """
    Artificial Intelligence (AI) has revolutionized many industries.
    Machine learning models can now perform complex tasks that were once
    thought to be exclusive to humans. Natural language processing, computer
    vision, and robotics are among the key areas seeing rapid advancement.
    """
    from content_core import Content, ContentType

    content = Content(
        content_type=ContentType.text,
        title="AI Overview",
        content=text_content.strip(),
    )
    source = await notebook.add_source(content)
    print(f"   ✓ Added: {source.title}")

    # 4. List sources in the notebook
    print("\n4. Listing sources in notebook...")
    sources = await notebook.get_sources()
    print(f"   Found {len(sources)} source(s):")
    for src in sources:
        print(f"   - {src.title} (Type: {src.source_type})")

    # 5. Archive notebook (optional)
    print("\n5. Notebook management...")
    print(f"   Notebook '{notebook.name}' is ready for use!")
    print(f"   ID: {notebook.id}")
    print(f"   Created: {notebook.created}")
    print(f"   Sources: {len(sources)}")

    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
