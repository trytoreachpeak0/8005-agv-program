from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .parameter import Parameter

@dataclass
class Event(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The identifier property
    identifier: Optional[str] = None
    # The name property
    name: Optional[str] = None
    # The outputData property
    output_data: Optional[list[Parameter]] = None
    # The required property
    required: Optional[bool] = None
    # The type property
    type: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> Event:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: Event
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return Event()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .parameter import Parameter

        from .parameter import Parameter

        fields: dict[str, Callable[[Any], None]] = {
            "identifier": lambda n : setattr(self, 'identifier', n.get_str_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "outputData": lambda n : setattr(self, 'output_data', n.get_collection_of_object_values(Parameter)),
            "required": lambda n : setattr(self, 'required', n.get_bool_value()),
            "type": lambda n : setattr(self, 'type', n.get_str_value()),
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
        writer.write_str_value("identifier", self.identifier)
        writer.write_str_value("name", self.name)
        writer.write_collection_of_object_values("outputData", self.output_data)
        writer.write_bool_value("required", self.required)
        writer.write_str_value("type", self.type)
        writer.write_additional_data_value(self.additional_data)
    

