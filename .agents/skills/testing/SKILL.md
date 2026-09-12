---
name: testing
description: How to run the project's validation gates and how to interpret failures.
---
# Testing

Run `PYTHONPATH=. pytest tests/` to execute validation suite.
All tests must pass. If a test fails, it might be an actual gap in the `agnara` kernel behavior. Do not mock it; document it.
