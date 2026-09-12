# Architecture

## Execution Flow
1. **Compilation**: The `App` and capabilities are compiled into a `FrozenCapabilityRegistry`.
2. **Dependency Injection**: A `DIRegistry` is created and providers are bound to it.
3. **Planning**: An `ExecutionPlan` is compiled from the capability definition and DI registry.
4. **Context Building**: An `Invocation` and `DIContainer` form the `ExecutionContext`.
5. **Execution**: `invoke_result(plan, context)` executes the capability, evaluating scopes, risks, and confirmations, returning a `CanonicalResult` (`Success` or `Failure`).
