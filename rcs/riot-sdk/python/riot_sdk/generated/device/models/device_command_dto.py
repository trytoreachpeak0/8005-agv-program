from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .device_command_dto_things_properties import DeviceCommandDto_thingsProperties
    from .http_callback import HttpCallback
    from .mq_callback import MqCallback

@dataclass
class DeviceCommandDto(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The httpCallback property
    http_callback: Optional[HttpCallback] = None
    # The messageId property
    message_id: Optional[str] = None
    # The mqCallback property
    mq_callback: Optional[MqCallback] = None
    # The thingsProperties property
    things_properties: Optional[DeviceCommandDto_thingsProperties] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> DeviceCommandDto:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: DeviceCommandDto
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return DeviceCommandDto()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .device_command_dto_things_properties import DeviceCommandDto_thingsProperties
        from .http_callback import HttpCallback
        from .mq_callback import MqCallback

        from .device_command_dto_things_properties import DeviceCommandDto_thingsProperties
        from .http_callback import HttpCallback
        from .mq_callback import MqCallback

        fields: dict[str, Callable[[Any], None]] = {
            "httpCallback": lambda n : setattr(self, 'http_callback', n.get_object_value(HttpCallback)),
            "messageId": lambda n : setattr(self, 'message_id', n.get_str_value()),
            "mqCallback": lambda n : setattr(self, 'mq_callback', n.get_object_value(MqCallback)),
            "thingsProperties": lambda n : setattr(self, 'things_properties', n.get_object_value(DeviceCommandDto_thingsProperties)),
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
        writer.write_object_value("httpCallback", self.http_callback)
        writer.write_str_value("messageId", self.message_id)
        writer.write_object_value("mqCallback", self.mq_callback)
        writer.write_object_value("thingsProperties", self.things_properties)
        writer.write_additional_data_value(self.additional_data)
    

