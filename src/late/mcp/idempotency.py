from __future__ import annotations

import hashlib
import json
from typing import Any


def same_arguments_key(scope: str, arguments: dict[str, Any]) -> str:
    digest = hashlib.sha256(
        json.dumps(arguments, sort_keys=True, default=str).encode()
    ).hexdigest()
    return f"mcp-{scope}-{digest[:40]}"
