"""
Open Notebook - Chat Example

This example demonstrates how to use Open Notebook's AI chat functionality
to ask questions about your research materials.
"""

import asyncio
from open_notebook import Notebook, create_notebook, Source
from langchain_core.messages import HumanMessage


async def main():
    """Example: Chat with your notebook"""

    print("=" * 60)
    print("Open Notebook - Chat Example")
    print("=" * 60)

    # 1. Create or load a notebook
    print("\n1. Setting up notebook...")
    try:
        # Try to load existing notebook
        notebooks = await Notebook.get_all()
        if notebooks:
            notebook = notebooks[0]
            print(f"   Using existing notebook: {notebook.name}")
        else:
            # Create new one if none exists
            notebook = await create_notebook(
                name="Chat Demo",
                description="Demonstrating chat functionality"
            )
            print(f"   Created new notebook: {notebook.name}")
    except Exception as e:
        print(f"   Error: {e}")
        return

    # 2. Add some research content
    print("\n2. Adding research content...")
    research_text = """
    Climate Change Impact on Biodiversity

    Climate change poses significant threats to global biodiversity.
    Rising temperatures are forcing species to migrate to cooler areas,
    disrupting ecosystems that have developed over thousands of years.

    Key impacts:
    1. Habitat loss - Polar bears, coral reefs, and alpine species are
       losing their habitats as temperatures rise.
    2. Migration patterns - Birds are migrating earlier, and some species
       are moving to higher latitudes or elevations.
    3. Extinction risk - Species with limited ranges or specialized
       habitat requirements face the highest extinction risks.
    4. Ecosystem disruption - Changes in one species affect entire
       food webs and ecosystem services.

    Conservation strategies include:
    - Protecting climate refugia (areas that remain suitable)
    - Creating wildlife corridors for migration
    - Reducing non-climate stressors (pollution, habitat fragmentation)
    - Assisted migration to suitable new habitats
    """

    try:
        # Create source directly
        source = Source(
            title="Climate Change Research",
            full_text=research_text.strip()
        )
        await source.save()
        await source.add_to_notebook(notebook.id)
        print(f"   ✓ Added source: {source.title}")
    except Exception as e:
        print(f"   ⚠ Could not add source: {e}")
        print("   Continuing with existing sources...")

    # 3. Check available sources
    sources = await notebook.get_sources()
    print(f"\n   Notebook has {len(sources)} source(s)")

    # 4. Ask questions using AI chat
    print("\n3. Asking questions using AI chat...")

    questions = [
        "What are the main impacts of climate change on biodiversity?",
        "What conservation strategies are mentioned?",
    ]

    from open_notebook.graphs.chat import ThreadState, call_model_with_messages

    for i, question in enumerate(questions, 1):
        print(f"\n   Question {i}: {question}")
        print("   " + "-" * 50)

        try:
            # Create chat state
            state = ThreadState(
                messages=[HumanMessage(content=question)],
                notebook=notebook,
                context=None,  # Let the system use default context
                context_config=None,
                model_override=None,  # Use default model
            )

            # Get AI response
            response = await call_model_with_messages(state, None)
            ai_message = response["messages"][-1]

            print(f"   Answer: {ai_message.content[:500]}")
            if len(ai_message.content) > 500:
                print("   ...")

        except Exception as e:
            print(f"   ⚠ Error getting response: {e}")
            print("   (Make sure AI provider is configured)")

    # 5. Summary
    print("\n" + "=" * 60)
    print("Chat example completed!")
    print(f"Notebook: {notebook.name} ({notebook.id})")
    print("Sources: {} | Questions asked: {}".format(len(sources), len(questions)))
    print("=" * 60)

    print("\n💡 Tip: Configure your AI provider in environment variables:")
    print("   - OPENAI_API_KEY for OpenAI models")
    print("   - ANTHROPIC_API_KEY for Claude models")
    print("   - Or use local models via Ollama")


if __name__ == "__main__":
    asyncio.run(main())
