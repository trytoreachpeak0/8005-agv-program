from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class OrderGroupVoObject(AdditionalDataHolder, Parsable):
    """
    订单组合参数接收类
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 预约指定车型组id
    appoint_vehicle_group_id: Optional[int] = None
    # 预约指定车辆id
    appoint_vehicle_key: Optional[str] = None
    # 订单组合Id
    id: Optional[int] = None
    # 订单组合名称
    order_group_name: Optional[str] = None
    # 原始的订单模板id集合,给前端回显使用
    original_template_order_id: Optional[str] = None
    # 订单组合优先级
    priority: Optional[int] = None
    # 订单模板id集合
    template_order_ids: Optional[list[int]] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> OrderGroupVoObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: OrderGroupVoObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return OrderGroupVoObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "appointVehicleGroupId": lambda n : setattr(self, 'appoint_vehicle_group_id', n.get_int_value()),
            "appointVehicleKey": lambda n : setattr(self, 'appoint_vehicle_key', n.get_str_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "orderGroupName": lambda n : setattr(self, 'order_group_name', n.get_str_value()),
            "originalTemplateOrderId": lambda n : setattr(self, 'original_template_order_id', n.get_str_value()),
            "priority": lambda n : setattr(self, 'priority', n.get_int_value()),
            "templateOrderIds": lambda n : setattr(self, 'template_order_ids', n.get_collection_of_primitive_values(int)),
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
        writer.write_int_value("id", self.id)
        writer.write_str_value("orderGroupName", self.order_group_name)
        writer.write_str_value("originalTemplateOrderId", self.original_template_order_id)
        writer.write_int_value("priority", self.priority)
        writer.write_collection_of_primitive_values("templateOrderIds", self.template_order_ids)
        writer.write_additional_data_value(self.additional_data)
    

