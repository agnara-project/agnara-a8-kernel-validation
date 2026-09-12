---
name: repository-maintenance
description: How an agent should safely inspect, modify and verify this repository.
---
# Repository Maintenance

1. **Verify State**: Always run `pytest tests/` and `ruff check .` before starting work.
2. **Environment**: Use `uv venv --python 3.14 .venv` and `uv pip install -e ".[dev,test]" --python .venv`.
3. **Boundaries**: Do not upgrade `agnara` version in `pyproject.toml`. It is frozen at `0.1.0a8`.
