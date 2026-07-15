from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .mission_d_t_o import MissionDTO

@dataclass
class OrderRecordDTOObject(AdditionalDataHolder, Parsable):
    """
    OrderRecordDTO对象
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 预约指定指定地图id
    appoint_map_id: Optional[int] = None
    # 预约指定指定地图站点id
    appoint_station_id: Optional[int] = None
    # 预约指定车型组id
    appoint_vehicle_group_id: Optional[int] = None
    # 预约指定车型组名
    appoint_vehicle_group_name: Optional[str] = None
    # 预约指定车辆id
    appoint_vehicle_key: Optional[str] = None
    # 是否支持预约:1.支持,0.不支持
    is_appoint_enable: Optional[int] = None
    # 是否锁定车辆:1.锁定,0.解锁
    lock_status: Optional[int] = None
    # 锁定车辆的key
    lock_vehicle_key: Optional[str] = None
    # 默认mission
    mission: Optional[list[MissionDTO]] = None
    # 订单名称
    order_name: Optional[str] = None
    # 优先级:0:低优先级,1:中优先级,2:高优先级,3:最高优先级
    priority: Optional[int] = None
    # 订单来源:1 FMS, 2 WMS, 3 CALLS, 4 UI
    source: Optional[int] = None
    # 中控系统订单唯一ID
    upper_id: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> OrderRecordDTOObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: OrderRecordDTOObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return OrderRecordDTOObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .mission_d_t_o import MissionDTO

        from .mission_d_t_o import MissionDTO

        fields: dict[str, Callable[[Any], None]] = {
            "appointMapId": lambda n : setattr(self, 'appoint_map_id', n.get_int_value()),
            "appointStationId": lambda n : setattr(self, 'appoint_station_id', n.get_int_value()),
            "appointVehicleGroupId": lambda n : setattr(self, 'appoint_vehicle_group_id', n.get_int_value()),
            "appointVehicleGroupName": lambda n : setattr(self, 'appoint_vehicle_group_name', n.get_str_value()),
            "appointVehicleKey": lambda n : setattr(self, 'appoint_vehicle_key', n.get_str_value()),
            "isAppointEnable": lambda n : setattr(self, 'is_appoint_enable', n.get_int_value()),
            "lockStatus": lambda n : setattr(self, 'lock_status', n.get_int_value()),
            "lockVehicleKey": lambda n : setattr(self, 'lock_vehicle_key', n.get_str_value()),
            "mission": lambda n : setattr(self, 'mission', n.get_collection_of_object_values(MissionDTO)),
            "orderName": lambda n : setattr(self, 'order_name', n.get_str_value()),
            "priority": lambda n : setattr(self, 'priority', n.get_int_value()),
            "source": lambda n : setattr(self, 'source', n.get_int_value()),
            "upperId": lambda n : setattr(self, 'upper_id', n.get_str_value()),
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
        writer.write_int_value("appointMapId", self.appoint_map_id)
        writer.write_int_value("appointStationId", self.appoint_station_id)
        writer.write_int_value("appointVehicleGroupId", self.appoint_vehicle_group_id)
        writer.write_str_value("appointVehicleGroupName", self.appoint_vehicle_group_name)
        writer.write_str_value("appointVehicleKey", self.appoint_vehicle_key)
        writer.write_int_value("isAppointEnable", self.is_appoint_enable)
        writer.write_int_value("lockStatus", self.lock_status)
        writer.write_str_value("lockVehicleKey", self.lock_vehicle_key)
        writer.write_collection_of_object_values("mission", self.mission)
        writer.write_str_value("orderName", self.order_name)
        writer.write_int_value("priority", self.priority)
        writer.write_int_value("source", self.source)
        writer.write_str_value("upperId", self.upper_id)
        writer.write_additional_data_value(self.additional_data)
    

