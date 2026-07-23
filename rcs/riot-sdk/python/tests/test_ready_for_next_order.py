from __future__ import annotations

from riot_sdk.core.ready_for_next_order import is_ready_for_next_order


def test_is_ready_success_and_idle_returns_true() -> None:
    # Round8 E2: orderState=5 SUCCESS, procState=IDLE → 可再派
    assert is_ready_for_next_order(order_state=5, proc_state="IDLE", processing_order=False)


def test_is_ready_awaiting_order_before_success_returns_false() -> None:
    # BC-STATE-003: 物理到站时 proc=AWAITING_ORDER，order 仍可能为 EXECUTING(3)
    assert not is_ready_for_next_order(
        order_state=3,
        proc_state="AWAITING_ORDER",
        processing_order=True,
    )
