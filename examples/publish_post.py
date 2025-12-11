"""
Example: Publish a post with Late SDK.
"""

import os
from datetime import datetime, timedelta

from late import Late


def main() -> None:
    client = Late(api_key=os.getenv("LATE_API_KEY", ""))

    # 1. Get your connected accounts
    print("Fetching accounts...")
    accounts_response = client.accounts.list()
    accounts = accounts_response.get("accounts", [])

    if not accounts:
        print("No accounts connected. Connect an account at https://getlate.dev")
        return

    print(f"Found {len(accounts)} account(s):")
    for i, acc in enumerate(accounts):
        print(f"  [{i}] {acc['platform']}: {acc.get('username', acc['_id'])}")

    # 2. Select first account
    account = accounts[0]
    print(f"\nUsing: {account['platform']} ({account.get('username', '')})")

    # 3. Create post - scheduled for 1 hour from now
    scheduled_time = datetime.now() + timedelta(hours=1)

    post = client.posts.create(
        content="Hello from Late Python SDK! 🚀",
        platforms=[
            {
                "platform": account["platform"],
                "accountId": account["_id"],
            }
        ],
        scheduled_for=scheduled_time,
    )

    print(f"\n✅ Post created!")
    print(f"   ID: {post['post']['_id']}")
    print(f"   Status: {post['post']['status']}")
    print(f"   Scheduled: {scheduled_time.strftime('%Y-%m-%d %H:%M')}")


if __name__ == "__main__":
    main()
