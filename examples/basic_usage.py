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

    # Example: Add from text
    print("   Adding source from text...")
    text_content = """
    Artificial Intelligence (AI) has revolutionized many industries.
    Machine learning models can now perform complex tasks that were once
    thought to be exclusive to humans. Natural language processing, computer
    vision, and robotics are among the key areas seeing rapid advancement.
    """

    # Create a source object directly
    from open_notebook import Source

    source = Source(
        title="AI Overview",
        full_text=text_content.strip()
    )
    await source.save()
    await source.add_to_notebook(notebook.id)
    print(f"   ✓ Added: {source.title}")

    # 4. List sources in the notebook
    print("\n4. Listing sources in notebook...")
    sources = await notebook.get_sources()
    print(f"   Found {len(sources)} source(s):")
    for src in sources:
        print(f"   - {src.title}")

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
