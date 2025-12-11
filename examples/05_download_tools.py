"""
Media download tools example.

This example demonstrates:
- Downloading content from various platforms
- Getting YouTube transcripts
- Using the caption generator
"""

import os

from late import Late


def main() -> None:
    api_key = os.getenv("LATE_API_KEY")
    if not api_key:
        print("Set LATE_API_KEY environment variable")
        return

    client = Late(api_key=api_key)

    print("=== Late Tools API ===")
    print("Rate limits: Build (50/day), Accelerate (500/day), Unlimited (unlimited)\n")

    # Check usage
    usage = client.analytics.get_usage()
    stats = usage.get("usage", {})
    print(f"Tools used today: {stats.get('toolsUsedToday', 0)}/{stats.get('toolsLimit', 'unlimited')}")

    # Example: YouTube download
    # result = client.tools.youtube_download("https://youtube.com/watch?v=...")
    # print(f"Download URL: {result.get('downloadUrl')}")

    # Example: YouTube transcript
    # result = client.tools.youtube_transcript("https://youtube.com/watch?v=...")
    # for segment in result.get("transcript", []):
    #     print(f"[{segment['start']:.1f}s] {segment['text']}")

    # Example: Instagram download
    # result = client.tools.instagram_download("https://instagram.com/p/...")

    # Example: TikTok download
    # result = client.tools.tiktok_download("https://tiktok.com/@user/video/...")

    # Example: Caption generator
    # result = client.tools.generate_caption(
    #     image_url="https://example.com/image.jpg",
    #     tone="professional",
    # )
    # for caption in result.get("captions", []):
    #     print(f"  - {caption}")

    print("\n(Uncomment examples to use - each call counts against rate limits)")


if __name__ == "__main__":
    main()
