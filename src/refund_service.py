import asyncio
from typing import Any

from agnara import (
    Agnara,
    AnonymousPrincipal,
    App,
    CapabilityId,
    Confirmation,
    ConfirmationEvidence,
    ConfirmationVerdict,
    ConfirmationVerifier,
    Principal,
    Risk,
    StandardEffect,
)
from agnara.core.di.registry import DIRegistry
from agnara.core.di.resolver import DIContainer
from agnara.execution import (
    ExecutionContext,
    ExecutionPlan,
    Invocation,
    InvocationStartEvent,
    InvocationTerminalEvent,
    TelemetryHook,
)


# 1. Dependency
class PaymentGateway:
    async def refund(self, amount: float, user_id: str) -> bool:
        if amount == 999.0:
            await asyncio.sleep(6.0)
        if amount <= 0:
            return False
        return True


# 2. App & Capability
app = App("refund_service")


@app.capability(
    risk=Risk.HIGH,
    confirmation=Confirmation.REQUIRED,
    scopes=["refund:execute"],
    effects=[StandardEffect.FINANCIAL_WRITE],
)
async def process_refund(amount: float, user_id: str, gateway: PaymentGateway) -> bool:
    if amount <= 0:
        return False
    success = await gateway.refund(amount, user_id)
    return success


# 3. Telemetry Hook
class RefundTelemetryHook(TelemetryHook):
    def __init__(self):
        self.starts = []
        self.terminals = []

    def on_invocation_start(self, event: InvocationStartEvent) -> None:
        self.starts.append(event)

    def on_invocation_terminal(self, event: InvocationTerminalEvent) -> None:
        self.terminals.append(event)


# 4. Confirmation Verifier
class RefundConfirmationVerifier(ConfirmationVerifier):
    async def verify(
        self,
        evidence: ConfirmationEvidence,
        *,
        capability_id: CapabilityId,
        invocation: Invocation,
        principal: Principal,
    ) -> ConfirmationVerdict:
        if evidence.value == "CONFIRM_REFUND":
            return ConfirmationVerdict.VALID
        return ConfirmationVerdict.INVALID


# 5. Core execution logic
async def run_refund(
    amount: float,
    user_id: str,
    principal: Principal | None = None,
    evidence: ConfirmationEvidence | None = None,
    gateway_override: PaymentGateway | None = None,
) -> Any:
    # Compile kernel
    kernel = Agnara("refund_kernel")
    kernel.include(app)
    frozen_reg = kernel.compile()

    cap_id = CapabilityId(namespace="refund_service", name="process_refund")
    cap_def = frozen_reg.get(cap_id)

    # DI Registry
    from agnara.core.di.provider import Scope, provider

    @provider(scope=Scope.INVOCATION)
    def provide_gateway() -> PaymentGateway:
        return gateway_override or PaymentGateway()

    di_registry = DIRegistry()
    di_registry.bind(PaymentGateway, provide_gateway)

    # Telemetry and Verifier
    telemetry = RefundTelemetryHook()
    verifier = RefundConfirmationVerifier()

    # Execution Plan
    plan = ExecutionPlan.compile(
        cap_def, registry=di_registry, hooks=[telemetry], confirmation_verifier=verifier
    )

    # Invocation & Context
    invocation = Invocation(
        capability_id=cap_id,
        payload={"amount": amount, "user_id": user_id},
        metadata={"client": "test"},
        deadline=5.0,  # seconds
    )

    di_container = DIContainer(di_registry)
    context = ExecutionContext(
        invocation=invocation,
        di_container=di_container,
        principal=principal or AnonymousPrincipal(),
        confirmation_evidence=evidence,
    )

    # Run
    from agnara.execution.runtime import invoke_result
    from agnara.introspection import describe_app, snapshot

    app_descriptor = describe_app(kernel, [plan], dependencies=di_registry)
    intro_snap = snapshot([app_descriptor])

    try:
        result = await invoke_result(plan, context)
        return {"result": result, "telemetry": telemetry, "introspection": intro_snap}
    except Exception as e:
        return {"error": e, "telemetry": telemetry, "introspection": intro_snap}
