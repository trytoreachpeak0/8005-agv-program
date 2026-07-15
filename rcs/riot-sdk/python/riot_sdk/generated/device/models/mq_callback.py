from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class MqCallback(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The expireTime property
    expire_time: Optional[int] = None
    # The nameServer property
    name_server: Optional[str] = None
    # The tag property
    tag: Optional[str] = None
    # The topic property
    topic: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> MqCallback:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: MqCallback
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return MqCallback()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "expireTime": lambda n : setattr(self, 'expire_time', n.get_int_value()),
            "nameServer": lambda n : setattr(self, 'name_server', n.get_str_value()),
            "tag": lambda n : setattr(self, 'tag', n.get_str_value()),
            "topic": lambda n : setattr(self, 'topic', n.get_str_value()),
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
        writer.write_int_value("expireTime", self.expire_time)
        writer.write_str_value("nameServer", self.name_server)
        writer.write_str_value("tag", self.tag)
        writer.write_str_value("topic", self.topic)
        writer.write_additional_data_value(self.additional_data)
    

