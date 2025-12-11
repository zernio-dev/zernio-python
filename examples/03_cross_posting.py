"""
Cross-posting content across multiple platforms.

This example demonstrates:
- Using the CrossPosterPipeline
- Automatic content adaptation
- Staggered posting
"""

import asyncio
import os

from late import Late
from late.pipelines import CrossPosterPipeline, PlatformConfig


async def main() -> None:
    api_key = os.getenv("LATE_API_KEY")
    if not api_key:
        print("Set LATE_API_KEY environment variable")
        return

    client = Late(api_key=api_key)

    # Get available accounts
    accounts = client.accounts.list()
    account_list = accounts.get("accounts", [])

    if len(account_list) < 2:
        print("Need at least 2 connected accounts for cross-posting")
        return

    # Build platform configs from available accounts
    platforms = [
        PlatformConfig(
            platform=acc["platform"],
            account_id=acc["_id"],
            delay_minutes=i * 5,  # 5 minutes apart
        )
        for i, acc in enumerate(account_list[:3])
    ]

    print(f"Cross-posting to {len(platforms)} platforms:")
    for p in platforms:
        print(f"  - {p.platform} (delay: {p.delay_minutes}min)")

    # Cross-post
    cross_poster = CrossPosterPipeline(client)

    # Example content
    content = """
Excited to announce our latest feature!

This is going to change how you work with social media.

Check it out and let us know what you think!
    """.strip()

    # Uncomment to actually post:
    # results = await cross_poster.post(
    #     content=content,
    #     platforms=platforms,
    #     tags=["announcement", "newfeature"],
    # )
    #
    # for r in results:
    #     status = "OK" if r.success else f"FAILED: {r.error}"
    #     print(f"  {r.platform}: {status}")

    print("\n(Uncomment the code to actually create posts)")


if __name__ == "__main__":
    asyncio.run(main())
