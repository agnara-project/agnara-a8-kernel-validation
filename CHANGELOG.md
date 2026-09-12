# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - Agnara 0.1.0a8 Historical Validation
### Added
- Refund service simulated capability.
- Execution plan and context generation.
- Policy and scope validation tests.
- Introspection snapshot testing.
- `examples/refund_demo.py` smoke scenario.

### Verified
- Direct kernel capability execution.
- Dependency injection (with internal APIs).
- Scopes, risk, effects, confirmation barriers.
- Canonical Success/Failure outcomes.

### Known historical gaps
- `StandardEffect.FINANCIAL` -> `StandardEffect.FINANCIAL_WRITE`.
- `agnara.core.di.*` private imports required.
- `@provider` required for DI bindings.
- `invoke_result` required for canonical outcomes without throwing exceptions.
- `ConfirmationVerifier.verify` is async.

### Repository status
Historical / Frozen

