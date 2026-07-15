from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class NumberSpecs(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The max property
    max: Optional[str] = None
    # The min property
    min: Optional[str] = None
    # The step property
    step: Optional[str] = None
    # The unit property
    unit: Optional[str] = None
    # The unitName property
    unit_name: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> NumberSpecs:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: NumberSpecs
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return NumberSpecs()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "max": lambda n : setattr(self, 'max', n.get_str_value()),
            "min": lambda n : setattr(self, 'min', n.get_str_value()),
            "step": lambda n : setattr(self, 'step', n.get_str_value()),
            "unit": lambda n : setattr(self, 'unit', n.get_str_value()),
            "unitName": lambda n : setattr(self, 'unit_name', n.get_str_value()),
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
        writer.write_str_value("max", self.max)
        writer.write_str_value("min", self.min)
        writer.write_str_value("step", self.step)
        writer.write_str_value("unit", self.unit)
        writer.write_str_value("unitName", self.unit_name)
        writer.write_additional_data_value(self.additional_data)
    

