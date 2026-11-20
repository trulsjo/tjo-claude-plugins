import re

_PART = re.compile(r"(\d+)([hms])")
_SECONDS = {"h": 3600, "m": 60, "s": 1}


def parse_duration(text):
    # Parses a duration such as "1h30m" or "45s" and returns the number of seconds.
    # Raises ValueError for anything else, including an empty string.
    parts = _PART.findall(text)
    if not parts or "".join(n + u for n, u in parts) != text:
        raise ValueError(f"bad duration: {text!r}")
    return sum(int(n) * _SECONDS[u] for n, u in parts)


def format_duration(seconds):
    hours, rest = divmod(seconds, 3600)
    minutes, secs = divmod(rest, 60)
    return f"{hours}h{minutes}m{secs}s"
