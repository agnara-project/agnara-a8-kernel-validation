# Autonomous Agent Operations

This file is the single operational source of truth for autonomous coding agents (Codex, Claude Code, Antigravity, etc.).

## 1. Project Identity
- **Repository**: agnara-a8-kernel-validation
- **Purpose**: Release validation project for Agnara 0.1.0a8 execution kernel.
- **Target Agnara version**: `0.1.0a8`
- **Python version**: `>= 3.14`
- **Status**: Frozen validation state.

## 2. Inviolable Architectural Constraints
- Dependency on `agnara` must remain exactly `0.1.0a8`.
- Do not use private internals of `agnara` unless absolutely necessary (and if so, document as a gap).
- Do not suppress test failures.

## 3. Codebase Structure and Ownership
- `src/refund_service.py`: Execution workflow and dummy capability.
- `tests/test_refund.py`: Pytest suite validating behaviors.
- `docs/`: Expanded boundaries and guides.

## 4. Environment and Command Palette
- Install: `uv venv --python 3.14 .venv && uv pip install -e ".[dev,test]" --python .venv`
- Format: `ruff format .`
- Lint: `ruff check .`
- Test: `PYTHONPATH=. pytest tests/`

## 5. Public API / Integration Boundary
This project verifies public APIs of Agnara 0.1.0a8. Any undocumented requirement (like `DIRegistry` not being exposed publicly) is treated as a gap and documented.

## 6. Negative Constraints
- **DO NOT** upgrade `agnara`.
- **DO NOT** replace PyPI dependencies with local paths.
- **DO NOT** weaken assertions.

## 7. Git and Contribution Protocol
Conventional Commits required (`feat:`, `fix:`, `docs:`, etc.).
Branching: `feature/` -> `main`.

## 8. Documentation Synchronization Contract
Changes to `src/refund_service.py` must be reflected in `README.md` gaps and `docs/public-api-boundary.md`.

## 9. Definition of Done
Passes all gates: `ruff format --check .`, `ruff check .`, `pytest tests/`.
