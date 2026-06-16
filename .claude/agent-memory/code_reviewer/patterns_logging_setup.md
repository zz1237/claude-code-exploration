---
name: logging_setup_pattern
description: Standard logging configuration with file and console handlers
metadata:
  type: reference
---

## Proper Logging Setup Pattern

**Location:** `.claude/skills/fetchapi/scripts/fetch_data.py` (lines 18-45)

### Pattern

Configure logging with both file and console handlers at module startup:

```python
def setup_logging():
    """Set up logging configuration with timestamp-based directory."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_dir = Path(".claude/skills/fetchapi/logs") / timestamp
    log_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_dir / "fetchapi.log")
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
```

### Why

- **Dual output:** Users see important messages on console, full details in file
- **Timestamp-based:** Log files organized by execution time (easier to find related logs)
- **Configurable levels:** File captures DEBUG, console shows INFO+ (less noise)
- **Consistent format:** Both handlers use same timestamp format for correlation
- **Observability:** Enables audit trails and debugging post-execution

### How to apply

1. Call `setup_logging()` early in main function
2. Pass logger to functions needing to log
3. Use appropriate levels: DEBUG for detailed flow, INFO for milestones, ERROR for problems
4. Replace print() statements with logger calls (logger.info(), logger.error(), etc.)

### Contrast with anti-pattern

**Do NOT use print() statements** in production code. This project has mixed approaches:
- fetch_data.py: Uses logging (GOOD)
- convert_to_parquet.py: Uses print (should convert to logging)
- visualize.py: Uses print (should convert to logging)

### Related patterns

[[summary_stats_reporting]] - Use logging to report batch outcomes
