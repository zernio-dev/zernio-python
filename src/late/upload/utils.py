"""
Utility functions for upload module.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator

    from .protocols import UploadFile


def read_file_content(file: UploadFile) -> bytes:
    """
    Read content bytes from an UploadFile.

    Handles bytes, Path, and file handle content types.
    """
    content = file.content

    if isinstance(content, bytes):
        return content

    if isinstance(content, Path):
        return content.read_bytes()

    # File handle - read and optionally reset position
    data = content.read()
    if hasattr(content, "seek"):
        content.seek(0)
    return data


def iter_file_chunks(
    file: UploadFile, chunk_size: int
) -> Generator[tuple[int, bytes], None, None]:
    """
    Iterate over file content in chunks.

    Yields:
        Tuple of (part_number, chunk_bytes) starting from 1
    """
    content = file.content
    part_number = 1

    if isinstance(content, bytes):
        for i in range(0, len(content), chunk_size):
            yield part_number, content[i : i + chunk_size]
            part_number += 1

    elif isinstance(content, Path):
        with content.open("rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                yield part_number, chunk
                part_number += 1

    else:
        # File handle
        while True:
            chunk = content.read(chunk_size)
            if not chunk:
                break
            yield part_number, chunk
            part_number += 1
