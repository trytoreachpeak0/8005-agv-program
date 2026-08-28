from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class U8f66u8f86u7535u6c60_u91ccu7a0b(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 设备名称
    device_name: Optional[str] = None
    # 当前车IP
    host_port: Optional[str] = None
    # 当前车里程
    total_mileage: Optional[int] = None
    # 当前车电池周期
    total_power_cycle: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> U8f66u8f86u7535u6c60_u91ccu7a0b:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: U8f66u8f86u7535u6c60_u91ccu7a0b
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return U8f66u8f86u7535u6c60_u91ccu7a0b()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "deviceName": lambda n : setattr(self, 'device_name', n.get_str_value()),
            "hostPort": lambda n : setattr(self, 'host_port', n.get_str_value()),
            "totalMileage": lambda n : setattr(self, 'total_mileage', n.get_int_value()),
            "totalPowerCycle": lambda n : setattr(self, 'total_power_cycle', n.get_int_value()),
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
        writer.write_str_value("hostPort", self.host_port)
        writer.write_int_value("totalMileage", self.total_mileage)
        writer.write_int_value("totalPowerCycle", self.total_power_cycle)
        writer.write_additional_data_value(self.additional_data)
    

