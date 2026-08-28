from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .custom_park_config_object_group_names import CustomParkConfigObject_groupNames

@dataclass
class CustomParkConfigObject(AdditionalDataHolder, Parsable):
    """
    自定义停靠配置表
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 启用停靠站点优先级
    consider_parking_position_priorities: Optional[bool] = None
    # 需要充电的车
    device_keys: Optional[list[str]] = None
    # 车型组id集合
    group_id_list: Optional[list[str]] = None
    # 车型组id集合
    group_ids: Optional[str] = None
    # 车型组名称集合
    group_names: Optional[CustomParkConfigObject_groupNames] = None
    # The id property
    id: Optional[int] = None
    # 配置名称
    name: Optional[str] = None
    # 启用空闲车辆停靠(true:启用,false:不启用)
    park_idle_vehicles: Optional[bool] = None
    # 车辆完成任务后分配停靠任务的间隔时间
    park_idle_waiting_interval: Optional[int] = None
    # 停靠点可用距离判断
    parking_near_station_distance: Optional[int] = None
    # 优先级
    priority: Optional[int] = None
    # 是否依据站点优先级重新停靠
    repark_vehicles_to_higher_priority_positions: Optional[bool] = None
    # 充电桩可作停靠站点
    use_charge_location_as_parking_lot: Optional[bool] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> CustomParkConfigObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: CustomParkConfigObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return CustomParkConfigObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .custom_park_config_object_group_names import CustomParkConfigObject_groupNames

        from .custom_park_config_object_group_names import CustomParkConfigObject_groupNames

        fields: dict[str, Callable[[Any], None]] = {
            "considerParkingPositionPriorities": lambda n : setattr(self, 'consider_parking_position_priorities', n.get_bool_value()),
            "deviceKeys": lambda n : setattr(self, 'device_keys', n.get_collection_of_primitive_values(str)),
            "groupIdList": lambda n : setattr(self, 'group_id_list', n.get_collection_of_primitive_values(str)),
            "groupIds": lambda n : setattr(self, 'group_ids', n.get_str_value()),
            "groupNames": lambda n : setattr(self, 'group_names', n.get_object_value(CustomParkConfigObject_groupNames)),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "parkIdleVehicles": lambda n : setattr(self, 'park_idle_vehicles', n.get_bool_value()),
            "parkIdleWaitingInterval": lambda n : setattr(self, 'park_idle_waiting_interval', n.get_int_value()),
            "parkingNearStationDistance": lambda n : setattr(self, 'parking_near_station_distance', n.get_int_value()),
            "priority": lambda n : setattr(self, 'priority', n.get_int_value()),
            "reparkVehiclesToHigherPriorityPositions": lambda n : setattr(self, 'repark_vehicles_to_higher_priority_positions', n.get_bool_value()),
            "useChargeLocationAsParkingLot": lambda n : setattr(self, 'use_charge_location_as_parking_lot', n.get_bool_value()),
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
        writer.write_bool_value("considerParkingPositionPriorities", self.consider_parking_position_priorities)
        writer.write_collection_of_primitive_values("deviceKeys", self.device_keys)
        writer.write_collection_of_primitive_values("groupIdList", self.group_id_list)
        writer.write_str_value("groupIds", self.group_ids)
        writer.write_object_value("groupNames", self.group_names)
        writer.write_int_value("id", self.id)
        writer.write_str_value("name", self.name)
        writer.write_bool_value("parkIdleVehicles", self.park_idle_vehicles)
        writer.write_int_value("parkIdleWaitingInterval", self.park_idle_waiting_interval)
        writer.write_int_value("parkingNearStationDistance", self.parking_near_station_distance)
        writer.write_int_value("priority", self.priority)
        writer.write_bool_value("reparkVehiclesToHigherPriorityPositions", self.repark_vehicles_to_higher_priority_positions)
        writer.write_bool_value("useChargeLocationAsParkingLot", self.use_charge_location_as_parking_lot)
        writer.write_additional_data_value(self.additional_data)
    

