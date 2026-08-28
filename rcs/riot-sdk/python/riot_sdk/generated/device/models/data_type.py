from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .array_specs import ArraySpecs
    from .bool_specs import BoolSpecs
    from .data_type_enum_specs import DataType_enumSpecs
    from .date_specs import DateSpecs
    from .number_specs import NumberSpecs
    from .struct_spec import StructSpec
    from .text_specs import TextSpecs

@dataclass
class DataType(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The arraySpecs property
    array_specs: Optional[ArraySpecs] = None
    # The boolSpecs property
    bool_specs: Optional[BoolSpecs] = None
    # The dateSpecs property
    date_specs: Optional[DateSpecs] = None
    # The enumSpecs property
    enum_specs: Optional[DataType_enumSpecs] = None
    # The numberSpecs property
    number_specs: Optional[NumberSpecs] = None
    # The structSpecs property
    struct_specs: Optional[list[StructSpec]] = None
    # The textSpecs property
    text_specs: Optional[TextSpecs] = None
    # The type property
    type: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> DataType:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: DataType
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return DataType()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .array_specs import ArraySpecs
        from .bool_specs import BoolSpecs
        from .data_type_enum_specs import DataType_enumSpecs
        from .date_specs import DateSpecs
        from .number_specs import NumberSpecs
        from .struct_spec import StructSpec
        from .text_specs import TextSpecs

        from .array_specs import ArraySpecs
        from .bool_specs import BoolSpecs
        from .data_type_enum_specs import DataType_enumSpecs
        from .date_specs import DateSpecs
        from .number_specs import NumberSpecs
        from .struct_spec import StructSpec
        from .text_specs import TextSpecs

        fields: dict[str, Callable[[Any], None]] = {
            "arraySpecs": lambda n : setattr(self, 'array_specs', n.get_object_value(ArraySpecs)),
            "boolSpecs": lambda n : setattr(self, 'bool_specs', n.get_object_value(BoolSpecs)),
            "dateSpecs": lambda n : setattr(self, 'date_specs', n.get_object_value(DateSpecs)),
            "enumSpecs": lambda n : setattr(self, 'enum_specs', n.get_object_value(DataType_enumSpecs)),
            "numberSpecs": lambda n : setattr(self, 'number_specs', n.get_object_value(NumberSpecs)),
            "structSpecs": lambda n : setattr(self, 'struct_specs', n.get_collection_of_object_values(StructSpec)),
            "textSpecs": lambda n : setattr(self, 'text_specs', n.get_object_value(TextSpecs)),
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
        writer.write_object_value("arraySpecs", self.array_specs)
        writer.write_object_value("boolSpecs", self.bool_specs)
        writer.write_object_value("dateSpecs", self.date_specs)
        writer.write_object_value("enumSpecs", self.enum_specs)
        writer.write_object_value("numberSpecs", self.number_specs)
        writer.write_collection_of_object_values("structSpecs", self.struct_specs)
        writer.write_object_value("textSpecs", self.text_specs)
        writer.write_str_value("type", self.type)
        writer.write_additional_data_value(self.additional_data)
    

