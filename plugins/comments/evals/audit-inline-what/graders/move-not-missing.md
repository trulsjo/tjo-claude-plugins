---
type: llm
---

The response is a comment audit of `src/duration.py`. It has two public functions: `parse_duration`, whose body opens with an inline comment saying what it parses, what it returns and when it raises ValueError, and `format_duration`, which has no comments and no docstring.

PASS only when all hold:
1. The inline comment in `parse_duration` is reported, and its fix moves the text into `parse_duration`'s docstring (API doc) rather than deleting it.
2. No finding says that `format_duration`, or any other function, is missing a docstring or doc comment, and the response does not suggest adding one to `format_duration`.

Otherwise FAIL, naming the condition that failed.
