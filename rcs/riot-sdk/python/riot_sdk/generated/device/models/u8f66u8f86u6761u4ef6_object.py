from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class U8f66u8f86u6761u4ef6Object(AdditionalDataHolder, Parsable):
    """
    车辆条件对象
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 车辆名称
    device_name: Optional[str] = None
    # 车辆型号
    model: Optional[str] = None
    # 车辆系列
    series: Optional[str] = None
    # 车辆型号(0:初始值; 1:上线, 2:下线)
    status: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> U8f66u8f86u6761u4ef6Object:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: U8f66u8f86u6761u4ef6Object
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return U8f66u8f86u6761u4ef6Object()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "deviceName": lambda n : setattr(self, 'device_name', n.get_str_value()),
            "model": lambda n : setattr(self, 'model', n.get_str_value()),
            "series": lambda n : setattr(self, 'series', n.get_str_value()),
            "status": lambda n : setattr(self, 'status', n.get_int_value()),
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
        writer.write_str_value("deviceName", self.device_name)
        writer.write_str_value("model", self.model)
        writer.write_str_value("series", self.series)
        writer.write_int_value("status", self.status)
        writer.write_additional_data_value(self.additional_data)
    

