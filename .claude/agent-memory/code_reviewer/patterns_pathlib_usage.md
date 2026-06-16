---
name: pathlib_pattern
description: Prefer pathlib.Path over string path operations for cross-platform compatibility
metadata:
  type: reference
---

## Pathlib Pattern for Cross-Platform Path Handling

**Location:** Multiple files in .claude/skills

### Pattern (GOOD)

Use pathlib.Path for all file system operations:

```python
from pathlib import Path

# Create directory structure
output_dir = Path(".claude/skills/fetchapi/data") / timestamp
output_dir.mkdir(parents=True, exist_ok=True)

# Save file
file_path = output_dir / filename
file_path.write_text(response.text)

# Iterate files
csv_files = list(source.glob("*.csv"))
```

### Anti-pattern (AVOID)

Raw strings with backslashes (Windows-only):

```python
# WRONG - breaks on Unix/Linux
source_base = r".\.claude\skills\fetchapi\data"

# String concatenation
file_path = os.path.join(base, folder, filename)
```

### Why

- **Cross-platform:** Works on Windows (\\), Unix (/), macOS without modification
- **Readability:** `/` operator is more intuitive than `os.path.join()`
- **Type safety:** Path object has methods (mkdir, glob, etc.)
- **CLAUDE.md aligned:** Project uses pathlib consistently elsewhere

### Location of anti-pattern

**convert_to_parquet.py (Line 92-93):**
```python
source_base = r".\.claude\skills\fetchapi\data"
output_base = r".\.claude\skills\migrate\data"
```

Should be:
```python
source_base = Path(".claude") / "skills" / "fetchapi" / "data"
output_base = Path(".claude") / "skills" / "migrate" / "data"
```

### How to apply

1. Use Path for all directory/file operations
2. Use `/` operator to join path segments
3. Call `.mkdir(parents=True, exist_ok=True)` instead of os.makedirs()
4. Use `.glob()` for pattern matching instead of os.listdir()
5. Use `.exists()`, `.is_dir()`, `.is_file()` for checks

### Related patterns

[[logging_setup_pattern]] - Logging setup also uses pathlib correctly
