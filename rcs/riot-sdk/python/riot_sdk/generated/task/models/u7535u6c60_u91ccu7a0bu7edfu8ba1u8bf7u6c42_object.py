from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class U7535u6c60_u91ccu7a0bu7edfu8ba1u8bf7u6c42Object(AdditionalDataHolder, Parsable):
    """
    电池、里程统计请求对象
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 车辆名称
    vehicle_name: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> U7535u6c60_u91ccu7a0bu7edfu8ba1u8bf7u6c42Object:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: U7535u6c60_u91ccu7a0bu7edfu8ba1u8bf7u6c42Object
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return U7535u6c60_u91ccu7a0bu7edfu8ba1u8bf7u6c42Object()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "vehicleName": lambda n : setattr(self, 'vehicle_name', n.get_str_value()),
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
        writer.write_str_value("vehicleName", self.vehicle_name)
        writer.write_additional_data_value(self.additional_data)
    

