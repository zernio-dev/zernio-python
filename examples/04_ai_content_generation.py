"""
AI Content Generation example.

This example demonstrates:
- Using the ContentGenerator with OpenAI
- Generating platform-specific content
- Combining AI generation with Late scheduling
"""

import asyncio
import os

from late import Late
from late.ai import ContentGenerator, GenerateRequest


async def main() -> None:
    late_key = os.getenv("LATE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if not late_key:
        print("Set LATE_API_KEY environment variable")
        return

    if not openai_key:
        print("Set OPENAI_API_KEY for AI generation")
        print("(Showing Late-only examples instead)\n")

    client = Late(api_key=late_key)

    # If OpenAI key is available, generate content
    if openai_key:
        generator = ContentGenerator(provider="openai", api_key=openai_key)

        print("=== Generating Content ===")

        # Generate for different platforms
        platforms = ["twitter", "linkedin", "instagram"]
        topic = "the benefits of automation for social media managers"

        for platform in platforms:
            request = GenerateRequest(
                prompt=f"Write about {topic}",
                platform=platform,
                tone="professional",
                max_tokens=300,
            )

            response = await generator.agenerate(request)
            print(f"\n--- {platform.upper()} ---")
            print(response.text[:200] + "..." if len(response.text) > 200 else response.text)

        # Using convenience method
        print("\n=== Quick Generation ===")
        post = generator.generate_post(
            topic="productivity tips for remote workers",
            platform="twitter",
            tone="casual",
        )
        print(f"Twitter post: {post}")

    # Show how to combine with Late
    print("\n=== Available Accounts ===")
    accounts = client.accounts.list()
    for acc in accounts.get("accounts", []):
        print(f"  - {acc['platform']}: {acc.get('username', 'N/A')}")

    print("\n(Combine AI generation with client.posts.create() to schedule)")


if __name__ == "__main__":
    asyncio.run(main())
