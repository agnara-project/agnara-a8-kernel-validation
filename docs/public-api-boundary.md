# Public API Boundary

This document records the verified public API surface of Agnara `0.1.0a8`.

## Public Verified
These APIs are safely exposed at the root `agnara` namespace or documented core structures:
- `agnara.Agnara`
- `agnara.AnonymousPrincipal`
- `agnara.App`
- `agnara.CapabilityId`
- `agnara.Confirmation`
- `agnara.ConfirmationEvidence`
- `agnara.ConfirmationVerdict`
- `agnara.ConfirmationVerifier`
- `agnara.Principal`
- `agnara.Risk`
- `agnara.StandardEffect`

## Public Submodule Verified
These APIs live safely in expected submodules and were successfully validated:
- `agnara.execution.ExecutionContext`
- `agnara.execution.ExecutionPlan`
- `agnara.execution.Invocation`
- `agnara.execution.InvocationStartEvent`
- `agnara.execution.InvocationTerminalEvent`
- `agnara.execution.TelemetryHook`
- `agnara.execution.Success`
- `agnara.execution.Failure`
- `agnara.execution.FailureCode`
- `agnara.execution.PolicyDeniedError`
- `agnara.execution.runtime.invoke_result`
- `agnara.introspection.snapshot`
- `agnara.introspection.describe_app`

## Internal/Private Historical Gaps
These components were found hidden, requiring internal imports, or absent under expected names:
- `agnara.core.di.registry.DIRegistry`
- `agnara.core.di.resolver.DIContainer`
- `agnara.core.di.provider.provider`
- `agnara.core.di.provider.Scope`
- `StandardEffect.FINANCIAL_WRITE` (Used instead of the undocumented `FINANCIAL` effect).
