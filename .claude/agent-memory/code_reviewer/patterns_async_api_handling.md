---
name: async_api_client_pattern
description: Best practice for managing async HTTP clients with proper resource cleanup
metadata:
  type: reference
---

## Async API Client Management Pattern

**Location:** `.claude/skills/fetchapi/scripts/fetch_data.py` (lines 111-113)

### Pattern

Use context manager for async HTTP clients to ensure proper resource cleanup:

```python
async with httpx.AsyncClient() as client:
    tasks = [fetch_data_from_api(client, url, logger) for url in urls]
    results = await asyncio.gather(*tasks)
```

### Why

- **Resource cleanup:** Context manager automatically closes connections
- **Connection pooling:** AsyncClient reuses connections across multiple requests
- **Error safety:** Guarantees cleanup even if exception occurs
- **Performance:** Much faster than creating new client for each request

### How to apply

When writing async code that makes multiple API calls:
1. Create AsyncClient once in a context manager
2. Pass the client to worker coroutines
3. Use `asyncio.gather()` to execute tasks concurrently
4. Return tuple (success_flag, message) for result aggregation

### Related pattern

[[logging_setup_pattern]] - Use logging to track API operations
[[summary_stats_reporting]] - Report on batch operation outcomes
