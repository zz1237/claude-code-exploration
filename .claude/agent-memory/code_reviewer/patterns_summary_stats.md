---
name: summary_stats_reporting
description: Pattern for reporting aggregate statistics from batch operations
metadata:
  type: reference
---

## Summary Statistics Reporting Pattern

**Location:** `.claude/skills/fetchapi/scripts/fetch_data.py` (lines 115-124)

### Pattern

Collect operation results and report summary statistics at end of batch work:

```python
async def main():
    # ... perform operations, collect results ...
    results = await asyncio.gather(*tasks)
    
    # Count successes/failures
    successful = sum(1 for success, _ in results if success)
    failed = len(results) - successful
    
    # Report summary
    logger.info("=" * 60)
    logger.info("API Fetch Operation Summary")
    logger.info(f"Total requests: {len(results)}")
    logger.info(f"Successful: {successful}")
    logger.info(f"Failed: {failed}")
    logger.info("=" * 60)
    
    # Return exit code
    return failed == 0
```

### Why

- **Visibility:** Users immediately see overall success/failure status
- **Debugging:** Helps identify systemic problems (all failed = network issue vs some failed = specific data issue)
- **Automation-friendly:** Exit code (0=success, 1=failure) works with scripts/CI
- **Complete picture:** Summary + individual logs give full context

### How to apply

For any batch operation (fetching multiple URLs, processing multiple files, etc.):

1. Collect results as tuples: (success: bool, message: str)
2. Use generator expression to count: `sum(1 for success, _ in results if success)`
3. Print separator lines for readability
4. Log all metrics (total, successful, failed)
5. Return boolean success flag for exit code

### Example in context

In this project's fetch_data.py:
- Each API call returns (True, msg) or (False, error_msg)
- Main collects results from asyncio.gather()
- Counts successes and failures
- Logs summary with clear formatting
- Returns success flag to exit() call

### Related patterns

[[logging_setup_pattern]] - Use logging module for reporting
[[async_api_client_pattern]] - Collecting results from async operations
