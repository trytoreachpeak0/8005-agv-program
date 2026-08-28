from __future__ import annotations

import pytest

from riot_sdk.core.dispatchable_vehicles import DispatchableVehicle, resolve_device_key
from riot_sdk.core.exceptions import RiotApiException


_SAMPLE = [
    DispatchableVehicle("BROKERX-8ffb2294db594d7480125d379b39cfd6", "新基测试300c顶升2"),
    DispatchableVehicle("BROKERX-aee2f93d717546cf9510c98c854fe83e", "新基测试300c协作1"),
    DispatchableVehicle("BROKERX-757de62710d84cec9fe9907691672cbc", "尊阳-多仓位1"),
]


def test_resolve_device_key_exact_name_returns_unique_key() -> None:
    key = resolve_device_key(_SAMPLE, "新基测试300c协作1")
    assert key == "BROKERX-aee2f93d717546cf9510c98c854fe83e"


def test_resolve_device_key_unknown_name_throws_not_found() -> None:
    # Fixture B1-name-to-deviceKey.unknownNameLookup
    with pytest.raises(RiotApiException) as caught:
        resolve_device_key(_SAMPLE, "不存在的车辆名-riot-behavior-lab")
    assert caught.value.business_code == "vehicle-name-not-found"


def test_resolve_device_key_duplicate_name_throws_ambiguous() -> None:
    # BC-VEH-002: 重名必须失败而不是任选一台（现场本轮无重名，用合成样例）
    duplicates = [
        DispatchableVehicle("BROKERX-key-a", "重名车"),
        DispatchableVehicle("BROKERX-key-b", "重名车"),
    ]
    with pytest.raises(RiotApiException) as caught:
        resolve_device_key(duplicates, "重名车")
    assert caught.value.business_code == "vehicle-name-ambiguous"
