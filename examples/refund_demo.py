import asyncio
from importlib.metadata import version

from agnara import ConfirmationEvidence, Principal
from agnara.execution import Success

from src.refund_service import run_refund


async def main():
    # 1. Version constraint check
    assert version("agnara") == "0.1.0a8", "This demo is strictly for agnara 0.1.0a8"

    # 2. Setup inputs
    principal = Principal("admin", scopes=["refund:execute"])
    evidence = ConfirmationEvidence("CONFIRM_REFUND")
    amount = 50.0
    user_id = "user_42"

    print(f"Executing direct kernel refund for user '{user_id}' with amount {amount}...")

    # 3. Execution
    res = await run_refund(amount=amount, user_id=user_id, principal=principal, evidence=evidence)

    # 4. Result validation
    result = res["result"]
    assert isinstance(result, Success), f"Expected Success, got {result}"
    assert result.value is True, "Refund was expected to succeed"
    print("Execution Result: Success (refund applied)")

    # 5. Telemetry / Introspection validation
    telemetry = res["telemetry"]
    assert len(telemetry.terminals) == 1
    print(f"Telemetry Status: {telemetry.terminals[0].outcome}")

    intro = res["introspection"]
    app_desc = intro.apps[0]
    cap_desc = app_desc.capabilities[0]

    print("\nIntrospection Summary:")
    print(f"App: {app_desc.name}")
    print(f"Capability: {cap_desc.id}")
    print(f"Risk: {cap_desc.risk}")
    print(f"Confirmation: {cap_desc.confirmation}")
    print(f"Scopes: {cap_desc.scopes}")


if __name__ == "__main__":
    asyncio.run(main())
