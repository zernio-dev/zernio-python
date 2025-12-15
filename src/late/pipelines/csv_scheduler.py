"""
Pipeline for scheduling posts from CSV files.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from late.enums import MediaType

if TYPE_CHECKING:
    from collections.abc import Iterator

    from ..client.late_client import Late


@dataclass
class ScheduleResult:
    """Result of scheduling a single post."""

    row: int
    success: bool
    post_id: str | None = None
    error: str | None = None


class CSVSchedulerPipeline:
    """
    Pipeline for scheduling posts from a CSV file.

    CSV columns:
    - content (required): Post content
    - platform (required): Platform name
    - account_id (required): Account ID
    - scheduled_for (required): ISO datetime or custom format
    - title (optional): Post title
    - media_url (optional): Media URL
    - tags (optional): Comma-separated tags

    Example:
        >>> client = Late(api_key="...")
        >>> pipeline = CSVSchedulerPipeline(client)
        >>>
        >>> # Schedule all posts from CSV
        >>> results = pipeline.schedule("posts.csv")
        >>> for r in results:
        ...     print(f"Row {r.row}: {'OK' if r.success else r.error}")
        >>>
        >>> # Dry run (validate without creating)
        >>> results = pipeline.schedule("posts.csv", dry_run=True)
    """

    def __init__(
        self,
        client: Late,
        *,
        date_format: str = "%Y-%m-%d %H:%M:%S",
        default_timezone: str = "UTC",
    ) -> None:
        self._client = client
        self.date_format = date_format
        self.default_timezone = default_timezone

    def _parse_csv(self, file_path: Path) -> Iterator[tuple[int, dict[str, str]]]:
        """Parse CSV and yield (row_number, row_data)."""
        with file_path.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            yield from enumerate(reader, start=2)

    def _parse_datetime(self, value: str) -> datetime:
        """Parse datetime from string."""
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return datetime.strptime(value, self.date_format)

    def _build_payload(self, row: dict[str, str]) -> dict[str, Any]:
        """Build post payload from CSV row."""
        payload: dict[str, Any] = {
            "content": row["content"],
            "platforms": [
                {
                    "platform": row["platform"],
                    "accountId": row["account_id"],
                }
            ],
            "scheduledFor": self._parse_datetime(row["scheduled_for"]).isoformat(),
            "timezone": row.get("timezone", self.default_timezone),
        }

        if row.get("title"):
            payload["title"] = row["title"]

        if row.get("media_url"):
            payload["mediaItems"] = [
                {
                    "type": row.get("media_type", MediaType.IMAGE),
                    "url": row["media_url"],
                }
            ]

        if row.get("tags"):
            payload["tags"] = [t.strip() for t in row["tags"].split(",")]

        return payload

    def schedule(
        self,
        file_path: str | Path,
        *,
        dry_run: bool = False,
    ) -> list[ScheduleResult]:
        """
        Schedule posts from a CSV file.

        Args:
            file_path: Path to CSV file
            dry_run: Validate without creating posts

        Returns:
            List of ScheduleResult for each row
        """
        path = Path(file_path)
        results: list[ScheduleResult] = []

        for row_num, row in self._parse_csv(path):
            try:
                payload = self._build_payload(row)

                if dry_run:
                    results.append(ScheduleResult(row=row_num, success=True))
                else:
                    response = self._client.posts.create(**payload)
                    post_id = response.get("post", {}).get("_id")
                    results.append(
                        ScheduleResult(row=row_num, success=True, post_id=post_id)
                    )

            except Exception as e:
                results.append(ScheduleResult(row=row_num, success=False, error=str(e)))

        return results

    async def aschedule(
        self,
        file_path: str | Path,
        *,
        dry_run: bool = False,
    ) -> list[ScheduleResult]:
        """Schedule posts asynchronously."""
        path = Path(file_path)
        results: list[ScheduleResult] = []

        for row_num, row in self._parse_csv(path):
            try:
                payload = self._build_payload(row)

                if dry_run:
                    results.append(ScheduleResult(row=row_num, success=True))
                else:
                    response = await self._client.posts.acreate(**payload)
                    post_id = response.get("post", {}).get("_id")
                    results.append(
                        ScheduleResult(row=row_num, success=True, post_id=post_id)
                    )

            except Exception as e:
                results.append(ScheduleResult(row=row_num, success=False, error=str(e)))

        return results
