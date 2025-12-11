"""
Basic usage example for Late Python SDK.

This example demonstrates:
- Initializing the client
- Listing profiles and accounts
- Creating a scheduled post
"""

import os
from datetime import datetime, timedelta

from late import Late


def main() -> None:
    # Initialize client
    api_key = os.getenv("LATE_API_KEY")
    if not api_key:
        print("Set LATE_API_KEY environment variable")
        return

    client = Late(api_key=api_key)

    # List profiles
    print("=== Profiles ===")
    profiles = client.profiles.list()
    for profile in profiles.get("profiles", []):
        print(f"  - {profile['name']} (ID: {profile['_id']})")

    # List connected accounts
    print("\n=== Connected Accounts ===")
    accounts = client.accounts.list()
    for account in accounts.get("accounts", []):
        print(f"  - {account['platform']}: {account.get('username', 'N/A')}")

    # List scheduled posts
    print("\n=== Scheduled Posts ===")
    posts = client.posts.list(status="scheduled", limit=5)
    for post in posts.get("posts", []):
        print(f"  - {post['content'][:50]}... ({post['status']})")

    # Create a new post (example - uncomment to use)
    # if accounts.get("accounts"):
    #     account = accounts["accounts"][0]
    #     scheduled_time = datetime.now() + timedelta(hours=1)
    #
    #     post = client.posts.create(
    #         content="Hello from Late Python SDK!",
    #         platforms=[{
    #             "platform": account["platform"],
    #             "accountId": account["_id"],
    #         }],
    #         scheduled_for=scheduled_time,
    #         tags=["test", "late-sdk"],
    #     )
    #     print(f"\nCreated post: {post['post']['_id']}")


if __name__ == "__main__":
    main()
