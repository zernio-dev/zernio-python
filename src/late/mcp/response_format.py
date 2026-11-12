from __future__ import annotations

import json
from contextvars import ContextVar
from enum import Enum
from typing import Any

MAX_RESULT_CHARS = 80_000
_NOTE_RESERVE_CHARS = 2_000
_MIN_STRING_CHARS = 1_000
_MAX_FITTING_ROUNDS = 50
_CUT_MARK = "…[cut]"

format_stats: ContextVar[dict[str, Any] | None] = ContextVar(
    "format_stats", default=None
)

Path = tuple[str | int, ...]


def format_payload(value: Any) -> str:
    document = _without_nulls(value)
    text = to_compact_json(document)
    stats = format_stats.get()
    if stats is not None:
        stats["raw_chars"] = len(text)
    if len(text) <= MAX_RESULT_CHARS:
        return text
    if stats is not None:
        stats["truncated"] = True
    return fit_to_size(document, MAX_RESULT_CHARS)


def to_compact_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), default=str)


def fit_to_size(document: Any, max_chars: int) -> str:
    root = document if isinstance(document, dict) else {"items": document}
    trims = _Trims(root)
    budget = max_chars - _NOTE_RESERVE_CHARS
    for _ in range(_MAX_FITTING_ROUNDS):
        excess = len(to_compact_json(root)) - budget
        if excess <= 0:
            break
        if not _trim_largest_list(root, excess, trims) and not _trim_longest_string(
            root, excess, trims
        ):
            break
    text = to_compact_json({"_truncated": trims.notes(root), **root})
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 60] + f"…[cut at {max_chars} characters, not valid JSON]"


def _without_nulls(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        value = value.model_dump(mode="json", by_alias=True, exclude_none=True)
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {
            key: _without_nulls(item) for key, item in value.items() if item is not None
        }
    if isinstance(value, (list, tuple)):
        return [_without_nulls(item) for item in value]
    return value


class _Trims:
    def __init__(self, root: dict[str, Any]) -> None:
        pagination = root.get("pagination")
        self.page_key = _main_list_key(root)
        self.pages_by_cursor = (
            isinstance(pagination, dict) and pagination.get("nextCursor") is not None
        )
        self.list_totals: dict[Path, int] = {}
        self.string_totals: dict[Path, int] = {}

    def notes(self, root: dict[str, Any]) -> list[str]:
        lists = [
            self._list_note(root, path, total)
            for path, total in self.list_totals.items()
        ]
        strings = [
            f"`{_path_label(path)}` keeps its first {_kept_chars(root, path)} of {total} characters."
            for path, total in self.string_totals.items()
        ]
        return lists + strings

    def _list_note(self, root: dict[str, Any], path: Path, total: int) -> str:
        keep = len(_value_at(root, path))
        if path == (self.page_key,):
            return _page_note(
                root, path[0], keep, total, pages_by_cursor=self.pages_by_cursor
            )
        return (
            f"`{_path_label(path)}` shows {keep} of {total} items; the response was too large. "
            "Narrow the request (filters, a shorter date range or a smaller limit) to see the rest."
        )


def _trim_largest_list(root: dict[str, Any], excess: int, trims: _Trims) -> bool:
    found = _largest_list(root)
    if found is None:
        return False
    path, items = found
    keep = _items_that_fit(items, excess)
    if path == (trims.page_key,):
        keep = _aligned_to_page_size(keep, root["pagination"])
        _drop_stale_page_counts(root["pagination"])
    trims.list_totals.setdefault(path, len(items))
    _assign(root, path, items[:keep])
    return True


def _largest_list(root: dict[str, Any]) -> tuple[Path, list[Any]] | None:
    best: tuple[int, Path, list[Any]] | None = None
    for path, items in _lists(root, ()):
        size = len(to_compact_json(items))
        if best is None or size > best[0]:
            best = (size, path, items)
    return None if best is None else (best[1], best[2])


def _lists(value: Any, path: Path):
    if isinstance(value, dict):
        for key, item in value.items():
            yield from _lists(item, (*path, key))
    elif isinstance(value, list):
        if len(value) > 1:
            yield path, value
        for index, item in enumerate(value):
            yield from _lists(item, (*path, index))


def _items_that_fit(items: list[Any], excess: int) -> int:
    removed = 0
    keep = len(items)
    while keep > 1 and removed < excess:
        keep -= 1
        removed += len(to_compact_json(items[keep])) + 1
    return keep


def _main_list_key(root: dict[str, Any]) -> str | None:
    if not isinstance(root.get("pagination"), dict):
        return None
    return next((key for key, value in root.items() if isinstance(value, list)), None)


def _aligned_to_page_size(keep: int, pagination: dict[str, Any]) -> int:
    page_size = pagination.get("limit")
    if (
        not isinstance(page_size, int)
        or not isinstance(pagination.get("page"), int)
        or page_size <= 0
    ):
        return keep
    return max(
        divisor
        for divisor in range(1, min(keep, page_size) + 1)
        if page_size % divisor == 0
    )


def _drop_stale_page_counts(pagination: dict[str, Any]) -> None:
    for stale in ("pages", "nextCursor", "hasMore"):
        pagination.pop(stale, None)


def _page_note(
    root: dict[str, Any], key: str, keep: int, total: int, *, pages_by_cursor: bool
) -> str:
    pagination = root["pagination"]
    shown = f"`{key}` shows {keep} of the {total} items of this page; the full page was too large."
    steps = []
    page, page_size = pagination.get("page"), pagination.get("limit")
    if isinstance(page, int) and isinstance(page_size, int) and page_size % keep == 0:
        steps.append(
            f"if you page with `page`, continue with limit={keep} and page={(page - 1) * page_size // keep + 2}"
        )
    if pages_by_cursor:
        steps.append(
            f"if you page with `cursor`, call again with the same cursor and limit={keep}: "
            f"its first {keep} items repeat these and its nextCursor then continues without gaps"
        )
    if not steps:
        return (
            f"{shown} Narrow the request (filters or a smaller limit) to see the rest."
        )
    return f"{shown} To read the rest, {'; '.join(steps)}."


def _trim_longest_string(root: dict[str, Any], excess: int, trims: _Trims) -> bool:
    found = max(_strings(root, ()), key=lambda entry: len(entry[1]), default=None)
    if found is None or len(found[1]) <= _MIN_STRING_CHARS:
        return False
    path, text = found
    keep = max(_MIN_STRING_CHARS, len(text) - excess)
    trims.string_totals.setdefault(path, len(text))
    _assign(root, path, f"{text[:keep]}{_CUT_MARK}")
    return True


def _strings(value: Any, path: Path):
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from _strings(item, (*path, key))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from _strings(item, (*path, index))


def _kept_chars(root: dict[str, Any], path: Path) -> int:
    return len(_value_at(root, path)) - len(_CUT_MARK)


def _value_at(root: dict[str, Any], path: Path) -> Any:
    value: Any = root
    for step in path:
        value = value[step]
    return value


def _assign(root: dict[str, Any], path: Path, value: Any) -> None:
    parent: Any = root
    for step in path[:-1]:
        parent = parent[step]
    parent[path[-1]] = value


def _path_label(path: Path) -> str:
    label = ""
    for step in path:
        label += f"[{step}]" if isinstance(step, int) else f".{step}" if label else step
    return label
