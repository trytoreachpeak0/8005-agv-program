from __future__ import annotations


class RiotApiException(Exception):
    """Raised when a RIoT HTTP call fails or returns a non-success business code."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        business_code: str | None = None,
        response_body: str | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.business_code = business_code
        self.response_body = response_body
