from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RiotOptions:
    """Connection options for a RIoT instance."""

    base_url: str
    username: str
    password: str
    timeout: float = 30.0
