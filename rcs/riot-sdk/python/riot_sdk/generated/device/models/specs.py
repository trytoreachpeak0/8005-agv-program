from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class Specs(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The registerCount property
    register_count: Optional[int] = None
    # The reverseRegister property
    reverse_register: Optional[int] = None
    # The swap16 property
    swap16: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> Specs:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: Specs
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return Specs()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "registerCount": lambda n : setattr(self, 'register_count', n.get_int_value()),
            "reverseRegister": lambda n : setattr(self, 'reverse_register', n.get_int_value()),
            "swap16": lambda n : setattr(self, 'swap16', n.get_int_value()),
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
        writer.write_int_value("registerCount", self.register_count)
        writer.write_int_value("reverseRegister", self.reverse_register)
        writer.write_int_value("swap16", self.swap16)
        writer.write_additional_data_value(self.additional_data)
    

