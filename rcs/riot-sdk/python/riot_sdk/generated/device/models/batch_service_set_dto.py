from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .device_command_dto import DeviceCommandDto

@dataclass
class BatchServiceSetDto(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The deviceCommandDto property
    device_command_dto: Optional[DeviceCommandDto] = None
    # The deviceKeys property
    device_keys: Optional[list[str]] = None
    # The serviceId property
    service_id: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> BatchServiceSetDto:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: BatchServiceSetDto
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return BatchServiceSetDto()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .device_command_dto import DeviceCommandDto

        from .device_command_dto import DeviceCommandDto

        fields: dict[str, Callable[[Any], None]] = {
            "deviceCommandDto": lambda n : setattr(self, 'device_command_dto', n.get_object_value(DeviceCommandDto)),
            "deviceKeys": lambda n : setattr(self, 'device_keys', n.get_collection_of_primitive_values(str)),
            "serviceId": lambda n : setattr(self, 'service_id', n.get_str_value()),
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
        writer.write_object_value("deviceCommandDto", self.device_command_dto)
        writer.write_collection_of_primitive_values("deviceKeys", self.device_keys)
        writer.write_str_value("serviceId", self.service_id)
        writer.write_additional_data_value(self.additional_data)
    

