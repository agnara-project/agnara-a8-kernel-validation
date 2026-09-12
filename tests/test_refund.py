import asyncio

import pytest
from agnara import ConfirmationEvidence, Principal
from agnara.execution import Failure, FailureCode, Success

from src.refund_service import PaymentGateway, run_refund


class MockGateway(PaymentGateway):
    def __init__(self):
        self.called = False
        self.amount = 0.0

    async def refund(self, amount: float, user_id: str) -> bool:
        self.called = True
        self.amount = amount
        # Simulate delay for timeout tests
        if amount == 999.0:
            await asyncio.sleep(10.0)
        return amount > 0


@pytest.mark.asyncio
async def test_successful_refund():
    gateway = MockGateway()
    principal = Principal("user1", scopes=["refund:execute"])
    evidence = ConfirmationEvidence("CONFIRM_REFUND")

    res = await run_refund(
        amount=100.0,
        user_id="user123",
        principal=principal,
        evidence=evidence,
        gateway_override=gateway,
    )

    assert "error" not in res
    result = res["result"]
    assert isinstance(result, Success)
    assert result.value is True

    assert gateway.called is True
    assert gateway.amount == 100.0

    # Verify telemetry
    assert len(res["telemetry"].terminals) == 1
    assert res["telemetry"].terminals[0].outcome == "success"


@pytest.mark.asyncio
async def test_failure_invalid_input():
    gateway = MockGateway()
    principal = Principal("user1", scopes=["refund:execute"])
    evidence = ConfirmationEvidence("CONFIRM_REFUND")

    res = await run_refund(
        amount="not_a_float",  # type: ignore
        user_id="user123",
        principal=principal,
        evidence=evidence,
        gateway_override=gateway,
    )

    assert "error" not in res
    result = res["result"]
    assert isinstance(result, Failure)
    assert result.code == FailureCode.INVALID_INPUT

    assert gateway.called is False


@pytest.mark.asyncio
async def test_failure_missing_scope():
    gateway = MockGateway()
    principal = Principal("user1", scopes=["other:scope"])  # missing refund:execute
    evidence = ConfirmationEvidence("CONFIRM_REFUND")

    res = await run_refund(
        amount=100.0,
        user_id="user123",
        principal=principal,
        evidence=evidence,
        gateway_override=gateway,
    )

    assert "error" not in res
    result = res["result"]
    assert isinstance(result, Failure)
    assert result.code == FailureCode.FORBIDDEN
    assert "missing required scopes: refund:execute" in result.message
    assert gateway.called is False


@pytest.mark.asyncio
async def test_failure_invalid_confirmation():
    gateway = MockGateway()
    principal = Principal("user1", scopes=["refund:execute"])
    evidence = ConfirmationEvidence("CONFIRM_NO")  # Invalid evidence

    res = await run_refund(
        amount=100.0,
        user_id="user123",
        principal=principal,
        evidence=evidence,
        gateway_override=gateway,
    )

    assert "error" not in res
    result = res["result"]
    assert isinstance(result, Failure)
    assert result.code == FailureCode.FORBIDDEN

    assert gateway.called is False  # Confirmation before effects


@pytest.mark.asyncio
async def test_failure_timeout():
    gateway = MockGateway()
    principal = Principal("user1", scopes=["refund:execute"])
    evidence = ConfirmationEvidence("CONFIRM_REFUND")

    res = await run_refund(
        amount=999.0,  # Triggers sleep in mock
        user_id="user123",
        principal=principal,
        evidence=evidence,
        gateway_override=gateway,
    )

    assert "error" not in res
    result = res["result"]
    assert isinstance(result, Failure)
    assert result.code == FailureCode.TIMEOUT

    # Telemetry should record the timeout
    assert len(res["telemetry"].terminals) == 1
    assert res["telemetry"].terminals[0].outcome == "timeout"


@pytest.mark.asyncio
async def test_introspection_snapshot():
    res = await run_refund(
        amount=100.0,
        user_id="user123",
        principal=Principal("u", scopes=["refund:execute"]),
        evidence=ConfirmationEvidence("CONFIRM_REFUND"),
    )
    intro = res["introspection"]
    assert len(intro.apps) == 1
    assert intro.apps[0].name == "refund_kernel"
    assert len(intro.apps[0].capabilities) == 1

    cap = intro.apps[0].capabilities[0]
    assert cap.id == "refund_service.process_refund"
    assert cap.risk == "high"
    assert cap.confirmation == "required"
