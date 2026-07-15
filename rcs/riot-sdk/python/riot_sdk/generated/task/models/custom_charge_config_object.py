from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .custom_charge_config_object_group_names import CustomChargeConfigObject_groupNames

@dataclass
class CustomChargeConfigObject(AdditionalDataHolder, Parsable):
    """
    自定义配置表
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 保护电量阈值(%)
    battery_level_critical: Optional[int] = None
    # 充满电量阈值(%)
    battery_level_fully_recharged: Optional[int] = None
    # 可工作电量阈值(%)
    battery_level_sufficiently_recharged: Optional[int] = None
    # 需要充电的车
    device_keys: Optional[list[str]] = None
    # 启动电池保养(1:是,0:否)
    enable_battery_maintenance: Optional[bool] = None
    # 启用空闲车辆充电(true:启用,false:不启用)
    enable_idle_charge: Optional[bool] = None
    # 车型组id集合
    group_id_list: Optional[list[str]] = None
    # 车型组id集合
    group_ids: Optional[str] = None
    # 车型组名称集合
    group_names: Optional[CustomChargeConfigObject_groupNames] = None
    # The id property
    id: Optional[int] = None
    # 车辆空闲充电判定时间阈值(min)
    idle_charge_frequency: Optional[int] = None
    # 当低电量车充电时达到可工作电量后仍然需要充电的增量
    increment_battery: Optional[int] = None
    # 自动充电必须充满(1:是,0:否)
    keep_recharging_until_fully_charged: Optional[bool] = None
    # 配置名称
    name: Optional[str] = None
    # 优先级
    priority: Optional[int] = None
    # 停止充电后的等待时间(s)
    stop_charge_wait_time: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> CustomChargeConfigObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: CustomChargeConfigObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return CustomChargeConfigObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .custom_charge_config_object_group_names import CustomChargeConfigObject_groupNames

        from .custom_charge_config_object_group_names import CustomChargeConfigObject_groupNames

        fields: dict[str, Callable[[Any], None]] = {
            "batteryLevelCritical": lambda n : setattr(self, 'battery_level_critical', n.get_int_value()),
            "batteryLevelFullyRecharged": lambda n : setattr(self, 'battery_level_fully_recharged', n.get_int_value()),
            "batteryLevelSufficientlyRecharged": lambda n : setattr(self, 'battery_level_sufficiently_recharged', n.get_int_value()),
            "deviceKeys": lambda n : setattr(self, 'device_keys', n.get_collection_of_primitive_values(str)),
            "enableBatteryMaintenance": lambda n : setattr(self, 'enable_battery_maintenance', n.get_bool_value()),
            "enableIdleCharge": lambda n : setattr(self, 'enable_idle_charge', n.get_bool_value()),
            "groupIdList": lambda n : setattr(self, 'group_id_list', n.get_collection_of_primitive_values(str)),
            "groupIds": lambda n : setattr(self, 'group_ids', n.get_str_value()),
            "groupNames": lambda n : setattr(self, 'group_names', n.get_object_value(CustomChargeConfigObject_groupNames)),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "idleChargeFrequency": lambda n : setattr(self, 'idle_charge_frequency', n.get_int_value()),
            "incrementBattery": lambda n : setattr(self, 'increment_battery', n.get_int_value()),
            "keepRechargingUntilFullyCharged": lambda n : setattr(self, 'keep_recharging_until_fully_charged', n.get_bool_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "priority": lambda n : setattr(self, 'priority', n.get_int_value()),
            "stopChargeWaitTime": lambda n : setattr(self, 'stop_charge_wait_time', n.get_int_value()),
        }
        return fields
    
    def serialize(self,writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        param writer: Serialization writer to use to serialize this model
        Returns: None
        """
        if writer is None:
            raise TypeError("writer cannot be null.")
        writer.write_int_value("batteryLevelCritical", self.battery_level_critical)
        writer.write_int_value("batteryLevelFullyRecharged", self.battery_level_fully_recharged)
        writer.write_int_value("batteryLevelSufficientlyRecharged", self.battery_level_sufficiently_recharged)
        writer.write_collection_of_primitive_values("deviceKeys", self.device_keys)
        writer.write_bool_value("enableBatteryMaintenance", self.enable_battery_maintenance)
        writer.write_bool_value("enableIdleCharge", self.enable_idle_charge)
        writer.write_collection_of_primitive_values("groupIdList", self.group_id_list)
        writer.write_str_value("groupIds", self.group_ids)
        writer.write_object_value("groupNames", self.group_names)
        writer.write_int_value("id", self.id)
        writer.write_int_value("idleChargeFrequency", self.idle_charge_frequency)
        writer.write_int_value("incrementBattery", self.increment_battery)
        writer.write_bool_value("keepRechargingUntilFullyCharged", self.keep_recharging_until_fully_charged)
        writer.write_str_value("name", self.name)
        writer.write_int_value("priority", self.priority)
        writer.write_int_value("stopChargeWaitTime", self.stop_charge_wait_time)
        writer.write_additional_data_value(self.additional_data)
    

