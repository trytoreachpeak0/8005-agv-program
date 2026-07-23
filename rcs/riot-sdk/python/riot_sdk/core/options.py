from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RiotOptions:
    """Connection options for a RIoT instance.

    Default auth is ``call_api_key`` (ADR-0001); AdminLogin username/password are optional backup.
    """

    base_url: str
    call_api_key: str | None = None
    username: str | None = None
    password: str | None = None
    timeout: float = 30.0
