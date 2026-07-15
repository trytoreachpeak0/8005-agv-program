from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .customize_func import CustomizeFunc

@dataclass
class CustomizeConfig(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The events property
    events: Optional[list[CustomizeFunc]] = None
    # The properties property
    properties: Optional[list[CustomizeFunc]] = None
    # The services property
    services: Optional[list[CustomizeFunc]] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> CustomizeConfig:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: CustomizeConfig
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return CustomizeConfig()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .customize_func import CustomizeFunc

        from .customize_func import CustomizeFunc

        fields: dict[str, Callable[[Any], None]] = {
            "events": lambda n : setattr(self, 'events', n.get_collection_of_object_values(CustomizeFunc)),
            "properties": lambda n : setattr(self, 'properties', n.get_collection_of_object_values(CustomizeFunc)),
            "services": lambda n : setattr(self, 'services', n.get_collection_of_object_values(CustomizeFunc)),
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
        writer.write_collection_of_object_values("events", self.events)
        writer.write_collection_of_object_values("properties", self.properties)
        writer.write_collection_of_object_values("services", self.services)
        writer.write_additional_data_value(self.additional_data)
    

