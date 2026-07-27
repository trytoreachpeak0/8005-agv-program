from __future__ import annotations

from typing import TypeVar

from riot_sdk.core.exceptions import RiotApiException

T = TypeVar("T")

_SUCCESS_CODES = frozenset({"0", "200", "OK", "ok", "success", "SUCCESS"})


def is_success_code(code: str | None) -> bool:
    """True when RIoT business code is empty/whitespace or a known success token (ADR-sdk-0005)."""
    if code is None:
        return True
    stripped = code.strip()
    return not stripped or stripped in _SUCCESS_CODES


def require_response(response: T | None, operation: str) -> T:
    if response is None:
        raise RiotApiException(f"{operation} returned empty response.")
    return response


def require_result(result: T | None, operation: str, business_code: str) -> T:
    if result is None:
        raise RiotApiException(
            f"{operation} returned null result.",
            business_code=business_code,
        )
    return result


def ensure_success(code: str | None, message: str | None) -> None:
    if is_success_code(code):
        return
    raise RiotApiException(
        f"RIoT business failure code={code} message={message}",
        status_code=200,
        business_code=code,
    )
