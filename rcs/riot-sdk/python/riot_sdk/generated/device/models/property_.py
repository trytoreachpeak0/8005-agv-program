from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .data_type import DataType

@dataclass
class Property_(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The accessMode property
    access_mode: Optional[str] = None
    # The dataType property
    data_type: Optional[DataType] = None
    # The desc property
    desc: Optional[str] = None
    # The identifier property
    identifier: Optional[str] = None
    # The name property
    name: Optional[str] = None
    # The required property
    required: Optional[bool] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> Property_:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: Property_
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return Property_()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .data_type import DataType

        from .data_type import DataType

        fields: dict[str, Callable[[Any], None]] = {
            "accessMode": lambda n : setattr(self, 'access_mode', n.get_str_value()),
            "dataType": lambda n : setattr(self, 'data_type', n.get_object_value(DataType)),
            "desc": lambda n : setattr(self, 'desc', n.get_str_value()),
            "identifier": lambda n : setattr(self, 'identifier', n.get_str_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "required": lambda n : setattr(self, 'required', n.get_bool_value()),
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
        writer.write_str_value("accessMode", self.access_mode)
        writer.write_object_value("dataType", self.data_type)
        writer.write_str_value("desc", self.desc)
        writer.write_str_value("identifier", self.identifier)
        writer.write_str_value("name", self.name)
        writer.write_bool_value("required", self.required)
        writer.write_additional_data_value(self.additional_data)
    

