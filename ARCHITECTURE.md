# Architecture

## Mission
This repository demonstrates and validates the real execution semantics of the `agnara` kernel version `0.1.0a8` acting as an external consumer. The goal is to provide a reproducible, frozen baseline of capabilities, dependency injection, policies, scopes, risk levels, and confirmation boundaries executing entirely within a local kernel environment without transport layers.

## Execution Lifecycle
The execution flow rigorously validates the following steps:
1. **App ↓ Capability declaration**: Constructing a local application with typed capabilities.
2. **Kernel include ↓ FrozenCapabilityRegistry**: Including the app into an `Agnara` kernel and compiling it into an immutable registry.
3. **Capability lookup**: Retrieving the raw `CapabilityDefinition`.
4. **DIRegistry**: Establishing dependency injection rules (requires `@provider` mappings).
5. **ExecutionPlan**: Compiling an optimized execution plan incorporating dependencies, telemetry hooks, and confirmation verifiers.
6. **Invocation ↓ ExecutionContext**: Creating the runtime context carrying the principal and confirmation evidence.
7. **invoke_result()**: Dispatching the plan securely to evaluate scopes, risk, and confirmations before executing the capability.
8. **Success / Failure**: Receiving canonical outcome instances natively from the framework.
9. **Telemetry + Introspection**: Collecting terminal events and exporting introspection metadata via `ApplicationDescriptor`.

## Trust and Policy Boundaries
The following boundaries are fully enforced by the kernel and verified by this repository's test suite:
- **Scope enforcement**: The principal must hold `refund:execute`. Otherwise, a `PolicyDeniedError` is generated and cleanly returned as `FailureCode.FORBIDDEN`.
- **Risk metadata & Effects**: `Risk.HIGH` and `StandardEffect.FINANCIAL_WRITE` are accurately declared.
- **Confirmation requirement**: Execution mandates `Confirmation.REQUIRED`.
- **Confirmation verifier**: A custom `RefundConfirmationVerifier` explicitly checks the provided `ConfirmationEvidence`. Rejection correctly halts execution *before* any side effect (the mocked gateway is strictly proven untouched).
- **Deadline / Timeout semantics**: Simulated long-running tasks exceed the `Invocation` deadline, correctly returning a `FailureCode.TIMEOUT` without corrupting state.

## Dependency Injection Boundary
As a verified historical private/internal dependency gap for `0.1.0a8`, the framework's direct dependency injection components are not cleanly exposed at the root level.
This repository strictly documents and uses:
- `agnara.core.di.registry.DIRegistry`
- `agnara.core.di.resolver.DIContainer`
- `agnara.core.di.provider.Scope`
- `agnara.core.di.provider.provider`

These are classified as **verified historical internal dependencies** and should not be considered a recommended public API pattern for newer versions of the framework. Furthermore, `DIRegistry.bind` strictly rejects raw instances, demanding the use of `ProviderDefinition` functions decorated with `@provider`.

## Out of Scope
This repository provides isolated *kernel validation*. It **does not** validate or mock:
- HTTP endpoints or REST APIs
- Model Context Protocol (MCP) integrations
- CLI generation
- Distributed execution / remote RPC
- Persistence or external queues
- Agent-to-Agent (A2A) flows
- Event transport and asynchronous pub/sub systems
