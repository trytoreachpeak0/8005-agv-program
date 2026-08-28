from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class StaticTemplateDTOObject(AdditionalDataHolder, Parsable):
    """
    根据静态模板添加订单类
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 是否锁定车辆:1.锁定,0.解锁
    lock_status: Optional[int] = None
    # 锁定车辆的key
    lock_vehicle_key: Optional[str] = None
    # 订单来源 1 FMS, 2 WMS, 3 CALLS, 4 UI
    source: Optional[int] = None
    # 订单模板id
    template_order_id: Optional[int] = None
    # 上层系统订单唯一ID
    upper_id: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> StaticTemplateDTOObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: StaticTemplateDTOObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return StaticTemplateDTOObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "lockStatus": lambda n : setattr(self, 'lock_status', n.get_int_value()),
            "lockVehicleKey": lambda n : setattr(self, 'lock_vehicle_key', n.get_str_value()),
            "source": lambda n : setattr(self, 'source', n.get_int_value()),
            "templateOrderId": lambda n : setattr(self, 'template_order_id', n.get_int_value()),
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
        writer.write_int_value("lockStatus", self.lock_status)
        writer.write_str_value("lockVehicleKey", self.lock_vehicle_key)
        writer.write_int_value("source", self.source)
        writer.write_int_value("templateOrderId", self.template_order_id)
        writer.write_str_value("upperId", self.upper_id)
        writer.write_additional_data_value(self.additional_data)
    

