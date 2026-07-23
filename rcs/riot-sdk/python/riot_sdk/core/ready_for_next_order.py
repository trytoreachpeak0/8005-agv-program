from __future__ import annotations

SUCCESS_ORDER_STATE = 5
IDLE_PROC_STATE = "IDLE"


def is_ready_for_next_order(
    order_state: int,
    proc_state: str | None,
    processing_order: bool = False,
) -> bool:
    """Pure ReadyForNextOrder check (BC-STATE-003 / ADR-0008).

    True only when previous order is SUCCESS and vehicle is IDLE.
    AWAITING_ORDER alone is not sufficient.
    """
    return (
        order_state == SUCCESS_ORDER_STATE
        and proc_state == IDLE_PROC_STATE
        and not processing_order
    )
