"""
Schedule posts from a CSV file.

This example demonstrates:
- Using the CSVSchedulerPipeline
- Dry run validation
- Error handling
"""

import os
from pathlib import Path

from late import Late
from late.pipelines import CSVSchedulerPipeline


def main() -> None:
    api_key = os.getenv("LATE_API_KEY")
    if not api_key:
        print("Set LATE_API_KEY environment variable")
        return

    client = Late(api_key=api_key)
    pipeline = CSVSchedulerPipeline(client)

    csv_path = Path(__file__).parent / "data" / "sample_posts.csv"

    # First, do a dry run to validate
    print("=== Dry Run ===")
    results = pipeline.schedule(csv_path, dry_run=True)

    success = sum(1 for r in results if r.success)
    failed = sum(1 for r in results if not r.success)
    print(f"Valid: {success}, Invalid: {failed}")

    for r in results:
        if not r.success:
            print(f"  Row {r.row}: {r.error}")

    # If all valid, schedule for real
    # if failed == 0:
    #     print("\n=== Scheduling Posts ===")
    #     results = pipeline.schedule(csv_path)
    #     for r in results:
    #         if r.success:
    #             print(f"  Row {r.row}: Created post {r.post_id}")
    #         else:
    #             print(f"  Row {r.row}: Failed - {r.error}")


if __name__ == "__main__":
    main()
