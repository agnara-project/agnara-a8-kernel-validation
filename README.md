# Agnara 0.1.0a8 Kernel Validation

Validation project for Agnara kernel capabilities in a simulated direct execution context, targeting specifically the `0.1.0a8` release from PyPI.

This repository demonstrates the execution of a `RefundService` capability acting as an external consumer of the `agnara` package. It utilizes capabilities, dependency injection (DI), policies, scopes, risk levels, confirmation evidence, invocation lifecycles, and introspection.

## Project Structure

- `src/refund_service.py`: Contains the definition of the `PaymentGateway` dependency, the `refund_service` app, its `process_refund` capability, telemetry hooks, confirmation verifiers, and the `run_refund` workflow which sets up the `ExecutionContext`.
- `tests/test_refund.py`: Contains `pytest` cases to validate success paths, policy failures (missing scopes), forbidden executions (rejected confirmations), invalid input validations, timeouts, and introspection snapshots.
- `pyproject.toml`: Dependency specification fixing `agnara==0.1.0a8`.

## Release Validation

**Target Version:** `agnara==0.1.0a8` (PyPI)
**Python Version:** >= 3.14

### Environment and Installed Packages

```text
agnara==0.1.0a8
colorama==0.4.6
iniconfig==2.3.0
packaging==26.3
pluggy==1.6.0
pygments==2.21.0
pytest==9.1.1
pytest-asyncio==1.4.0
```

### Reproducible Commands

To run the validation suite:

```bash
uv venv --python 3.14 .venv
uv pip install -e ".[test]" --python .venv
$env:PYTHONPATH="."  # (Windows)
# or export PYTHONPATH="." (Unix)
.\.venv\Scripts\pytest tests/
```

### Findings and Gaps

During the validation of `0.1.0a8`, several differences from the expected interfaces were found. These have been documented and adapted inside this minimal reproducible example without modifying the framework itself:

1. **Missing `StandardEffect.FINANCIAL`**: The effect expected was absent. We mapped it to `StandardEffect.FINANCIAL_WRITE` which was found in the enumeration.
2. **`DIRegistry` and `DIContainer` Exposure**: The DI components are not exposed directly in `agnara`. We had to import them from the private-like core modules: `from agnara.core.di.registry import DIRegistry` and `from agnara.core.di.resolver import DIContainer`.
3. **DI Binding Requires `@provider`**: `DIRegistry.bind` does not accept raw instances. It mandates a `ProviderDefinition`, requiring developers to wrap instances inside a `@provider` decorated factory function.
4. **Outcome Extraction**: Using `invoke(plan, context)` raw does not return `Success` or `Failure` objects, instead, it returns the unwrapped value or raises an exception. To receive the canonical `Success`/`Failure` types and handle `PolicyDeniedError` gracefully as `FailureCode.FORBIDDEN`, one must use `from agnara.execution.runtime import invoke_result`.

### Limitations

- **Async ConfirmationVerifier**: `ConfirmationVerifier.verify` is required to be an `async def` function, otherwise it causes an awaitable TypeError during execution.
- No HTTP or external adapters (MCP) are used. Execution simulates direct kernel usage.

This repository serves as a frozen point-in-time validation for `agnara==0.1.0a8`.