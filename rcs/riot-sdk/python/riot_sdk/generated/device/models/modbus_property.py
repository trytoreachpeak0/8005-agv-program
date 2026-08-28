from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .original_data_type import OriginalDataType

@dataclass
class ModbusProperty(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The bitMask property
    bit_mask: Optional[int] = None
    # The identifier property
    identifier: Optional[str] = None
    # The operateType property
    operate_type: Optional[str] = None
    # The originalDataType property
    original_data_type: Optional[OriginalDataType] = None
    # The pollingTime property
    polling_time: Optional[int] = None
    # The registerAddress property
    register_address: Optional[str] = None
    # The scaling property
    scaling: Optional[float] = None
    # The trigger property
    trigger: Optional[int] = None
    # The writeFunctionCode property
    write_function_code: Optional[int] = None
    # The writeOnly property
    write_only: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ModbusProperty:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ModbusProperty
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return ModbusProperty()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .original_data_type import OriginalDataType

        from .original_data_type import OriginalDataType

        fields: dict[str, Callable[[Any], None]] = {
            "bitMask": lambda n : setattr(self, 'bit_mask', n.get_int_value()),
            "identifier": lambda n : setattr(self, 'identifier', n.get_str_value()),
            "operateType": lambda n : setattr(self, 'operate_type', n.get_str_value()),
            "originalDataType": lambda n : setattr(self, 'original_data_type', n.get_object_value(OriginalDataType)),
            "pollingTime": lambda n : setattr(self, 'polling_time', n.get_int_value()),
            "registerAddress": lambda n : setattr(self, 'register_address', n.get_str_value()),
            "scaling": lambda n : setattr(self, 'scaling', n.get_float_value()),
            "trigger": lambda n : setattr(self, 'trigger', n.get_int_value()),
            "writeFunctionCode": lambda n : setattr(self, 'write_function_code', n.get_int_value()),
            "writeOnly": lambda n : setattr(self, 'write_only', n.get_int_value()),
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
        writer.write_int_value("bitMask", self.bit_mask)
        writer.write_str_value("identifier", self.identifier)
        writer.write_str_value("operateType", self.operate_type)
        writer.write_object_value("originalDataType", self.original_data_type)
        writer.write_int_value("pollingTime", self.polling_time)
        writer.write_str_value("registerAddress", self.register_address)
        writer.write_float_value("scaling", self.scaling)
        writer.write_int_value("trigger", self.trigger)
        writer.write_int_value("writeFunctionCode", self.write_function_code)
        writer.write_int_value("writeOnly", self.write_only)
        writer.write_additional_data_value(self.additional_data)
    

