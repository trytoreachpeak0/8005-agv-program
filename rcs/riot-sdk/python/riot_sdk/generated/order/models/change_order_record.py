from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .mission_d_t_o import MissionDTO

@dataclass
class ChangeOrderRecord(AdditionalDataHolder, Parsable):
    """
    换订单对象
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 预约的车型组id
    appoint_vehicle_group_id: Optional[int] = None
    # 预约的车辆key
    appoint_vehicle_key: Optional[str] = None
    # 换车理由
    change_reason: Optional[str] = None
    # 新插入的子任务
    missions: Optional[list[MissionDTO]] = None
    # 被换的订单key
    order_task_key: Optional[str] = None
    # 执行的车辆key
    process_vehicle_key: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ChangeOrderRecord:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ChangeOrderRecord
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return ChangeOrderRecord()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .mission_d_t_o import MissionDTO

        from .mission_d_t_o import MissionDTO

        fields: dict[str, Callable[[Any], None]] = {
            "appointVehicleGroupId": lambda n : setattr(self, 'appoint_vehicle_group_id', n.get_int_value()),
            "appointVehicleKey": lambda n : setattr(self, 'appoint_vehicle_key', n.get_str_value()),
            "changeReason": lambda n : setattr(self, 'change_reason', n.get_str_value()),
            "missions": lambda n : setattr(self, 'missions', n.get_collection_of_object_values(MissionDTO)),
            "orderTaskKey": lambda n : setattr(self, 'order_task_key', n.get_str_value()),
            "processVehicleKey": lambda n : setattr(self, 'process_vehicle_key', n.get_str_value()),
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
        writer.write_int_value("appointVehicleGroupId", self.appoint_vehicle_group_id)
        writer.write_str_value("appointVehicleKey", self.appoint_vehicle_key)
        writer.write_str_value("changeReason", self.change_reason)
        writer.write_collection_of_object_values("missions", self.missions)
        writer.write_str_value("orderTaskKey", self.order_task_key)
        writer.write_str_value("processVehicleKey", self.process_vehicle_key)
        writer.write_additional_data_value(self.additional_data)
    

