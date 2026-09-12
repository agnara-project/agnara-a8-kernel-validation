# Agnara 0.1.0a8 Kernel Validation

**Project Identity:** agnara-a8-kernel-validation
**Role:** Release validation project for Agnara kernel capabilities.
**Target Release:** Agnara `0.1.0a8` (Historical / Frozen)
**Python Version:** >= 3.14

## Purpose
This repository provides a reproducible, point-in-time conformance validation of the `agnara` package as an external consumer. It specifically tests the real execution runtime using a direct kernel invocation of a simulated `RefundService`. 

## What This Validates
- Capability declaration, compilation, and lookup.
- Dependency injection via DI Registry and Containers.
- Execution plans and execution contexts.
- Principals, scopes, risks, and standard effects.
- Confirmations (evidence/verifiers) correctly blocking side-effects.
- Canonical `Success`/`Failure` outcome extraction.
- Timeout and invalid input handling.
- Telemetry hooks and introspection metadata.

## What This Does NOT Validate
- HTTP, MCP, CLI, or distributed execution.
- Any network operations or persistence mechanisms.
- Event transport and Agent-to-Agent architectures.

## Architecture Summary
The execution flow strictly abides by the framework's boundaries: the app capabilities are compiled into a `FrozenCapabilityRegistry`. An `ExecutionPlan` is generated along with a `DIRegistry` storing necessary dependency providers. `invoke_result` executes the plan passing an `ExecutionContext` populated with the invocation parameters, the authenticated principal, and the provided confirmation evidence. See [ARCHITECTURE.md](ARCHITECTURE.md) for deeper details.

## Private API Warning
> [!WARNING]
> This repository validates `agnara==0.1.0a8` and intentionally uses several internal paths (`agnara.core.di.*`) as they were not exposed publicly in this version. Do not use these imports in modern applications. They are strictly retained as historical evidence.

## Quick Start
```bash
# Clone the repository
git clone https://github.com/agnara-project/agnara-a8-kernel-validation.git
cd agnara-a8-kernel-validation

# Install Python 3.14 and create isolated environment
uv venv --python 3.14 .venv
uv pip install -e ".[dev,test]" --python .venv

# Run the validation smoke scenario
python examples/refund_demo.py
```

## Tested Scenarios
The validation suite enforces strict security boundaries and covers:
- **Successful Refund**: Returns a canonical `Success` object.
- **Invalid Input**: Framework schema validation intercepts execution (`FailureCode.INVALID_INPUT`).
- **Missing Scope**: Kernel denies execution before side-effects (`FailureCode.FORBIDDEN`).
- **Invalid Confirmation**: Evidence verifier denies execution before side-effects (`FailureCode.FORBIDDEN`).
- **Timeout**: Enforced invocation deadline gracefully truncates execution (`FailureCode.TIMEOUT`).
- **Introspection/Telemetry**: Accurate collection of lifecycle events and public schemas.

## Findings and Gaps
1. **Missing `StandardEffect.FINANCIAL`**: The effect expected was absent; it was mapped to `StandardEffect.FINANCIAL_WRITE`.
2. **`DIRegistry`/`DIContainer` Exposure**: DI components require imports from the private-like core module `agnara.core.di.*`.
3. **DI Binding Requires `@provider`**: `DIRegistry.bind` does not accept raw instances. It demands a `ProviderDefinition` function wrapped via `@provider`.
4. **Canonical Outcomes**: Utilizing `invoke_result` is required to gracefully capture canonical `Success`/`Failure` instances (preventing unhandled framework exceptions like `PolicyDeniedError`).
5. **Async Verifier**: `ConfirmationVerifier.verify` is expected to be an asynchronous method to prevent runtime type errors.

## Quality Gates
The following gates must successfully execute to validate the environment:
- `python -m pip check`
- `ruff format --check .`
- `ruff check .`
- `pytest -v tests/`
- `python examples/refund_demo.py`
- `python -m build`

## Project Structure
- `src/refund_service.py`: Execution workflow and direct capability implementation.
- `tests/test_refund.py`: Pytest suite exercising success, failure, and security policies.
- `examples/refund_demo.py`: Executable smoke scenario avoiding Pytest abstractions.
- `docs/`: Public boundaries and kernel validation specific guidelines.
- `ARCHITECTURE.md` & `AGENTS.md`: Operational truth for agents and technical documentation.

## Historical / Frozen Status
**Status: Historical / Frozen / Complete**
This repository is locked to `agnara==0.1.0a8`. Do not submit Pull Requests to update dependencies.