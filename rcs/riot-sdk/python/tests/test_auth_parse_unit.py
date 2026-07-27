from __future__ import annotations

from riot_sdk.core.auth import _find_token, _strip_bearer
from riot_sdk.core.business_response import is_success_code


def test_strip_bearer() -> None:
    assert _strip_bearer("Bearer abc") == "abc"
    assert _strip_bearer("token") == "token"


def test_success_codes() -> None:
    assert is_success_code("0")
    assert is_success_code("200")
    assert not is_success_code("401")


def test_find_token_prefers_known_keys() -> None:
    raw = {"foo": "x", "accessToken": "the-token-value-1234567890"}
    assert _find_token(raw, "token", "accessToken") == "the-token-value-1234567890"
