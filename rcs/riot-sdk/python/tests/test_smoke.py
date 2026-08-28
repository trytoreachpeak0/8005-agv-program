from __future__ import annotations

import os

import pytest

from riot_sdk import RiotOptions, RiotSession


def _load_options() -> RiotOptions | None:
    enabled = os.getenv("RIOT_SMOKE", "")
    if enabled not in ("1", "true", "True", "YES", "yes"):
        return None
    return RiotOptions(
        base_url=os.getenv("RIOT_BASE_URL", "http://172.19.206.222:8888"),
        username=os.getenv("RIOT_USERNAME", "admin"),
        password=os.getenv("RIOT_PASSWORD", "admin"),
    )


@pytest.mark.asyncio
async def test_login_and_list_devices_smoke() -> None:
    options = _load_options()
    if options is None:
        pytest.skip("Set RIOT_SMOKE=1 to run live smoke against RIoT")

    async with RiotSession(options) as session:
        tokens = await session.login()
        assert tokens.access_token
        devices = await session.device.list_devices(page_num=1, page_size=10)
        assert devices is not None
        print(f"devices.total={devices.total} records={len(devices.records or [])}")
