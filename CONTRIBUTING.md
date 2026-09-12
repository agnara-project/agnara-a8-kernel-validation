# Contributing

This repository is frozen to validate Agnara `0.1.0a8`. Contributions are generally not accepted unless they fix severe testing errors in the validation itself, without altering the target version.

## Immutability Rules
- `agnara==0.1.0a8` is strictly immutable.
- Upgrades to `a9` or later are not accepted.
- No local dependencies of Agnara are allowed.
- Any new use of an internal API must be documented.
- This repository only accepts historical validation fixes.

## Quality Gates
Any exceptional correction must use Conventional Commits and pass the full quality suite:
```bash
python -m pip check
ruff format --check .
ruff check .
pytest -v tests/
python examples/refund_demo.py
python -m build
```
