from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class FunctionBlock(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The description property
    description: Optional[str] = None
    # The functionBlockId property
    function_block_id: Optional[str] = None
    # The functionBlockName property
    function_block_name: Optional[str] = None
    # The productKey property
    product_key: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> FunctionBlock:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: FunctionBlock
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return FunctionBlock()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "description": lambda n : setattr(self, 'description', n.get_str_value()),
            "functionBlockId": lambda n : setattr(self, 'function_block_id', n.get_str_value()),
            "functionBlockName": lambda n : setattr(self, 'function_block_name', n.get_str_value()),
            "productKey": lambda n : setattr(self, 'product_key', n.get_str_value()),
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
        writer.write_str_value("description", self.description)
        writer.write_str_value("functionBlockId", self.function_block_id)
        writer.write_str_value("functionBlockName", self.function_block_name)
        writer.write_str_value("productKey", self.product_key)
        writer.write_additional_data_value(self.additional_data)
    

