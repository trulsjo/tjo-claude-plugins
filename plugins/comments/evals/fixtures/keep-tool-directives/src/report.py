import os  # noqa: F401
import json
from typing import Any


def load(path: str) -> Any:
    with open(path) as f:
        return json.load(f)  # type: ignore[no-any-return]
