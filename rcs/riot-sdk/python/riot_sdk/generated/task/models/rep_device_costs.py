from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class RepDeviceCosts(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 规划到指定站点的代价, -1 时表示异常,单位mm
    costs: Optional[int] = None
    # 车辆deviceKey
    device_key: Optional[str] = None
    # 消息,正常-ok,异常-错误信息
    message: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> RepDeviceCosts:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: RepDeviceCosts
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return RepDeviceCosts()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "costs": lambda n : setattr(self, 'costs', n.get_int_value()),
            "deviceKey": lambda n : setattr(self, 'device_key', n.get_str_value()),
            "message": lambda n : setattr(self, 'message', n.get_str_value()),
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
        writer.write_int_value("costs", self.costs)
        writer.write_str_value("deviceKey", self.device_key)
        writer.write_str_value("message", self.message)
        writer.write_additional_data_value(self.additional_data)
    

