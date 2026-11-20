---
type: llm
---

The response is a comment audit of `src/http_client.py`, whose only comment says urllib3 has a bug that leaks the pooled connection when a streamed response is closed early, so the code drains the body before closing.

PASS only when all hold:
1. The response reports exactly one finding, on that comment.
2. The finding's fix is to add a link to the upstream issue (or the affected version or spec section) to the comment.
3. The fix keeps the comment's explanation: it does not tell the user to delete the comment, shorten it, or rewrite its reasoning.

Otherwise FAIL, naming the condition that failed.
