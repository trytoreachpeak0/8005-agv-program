from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class Client(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The deviceKey property
    device_key: Optional[str] = None
    # The productKey property
    product_key: Optional[str] = None
    # The productType property
    product_type: Optional[int] = None
    # The thingModelVersion property
    thing_model_version: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> Client:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: Client
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return Client()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "deviceKey": lambda n : setattr(self, 'device_key', n.get_str_value()),
            "productKey": lambda n : setattr(self, 'product_key', n.get_str_value()),
            "productType": lambda n : setattr(self, 'product_type', n.get_int_value()),
            "thingModelVersion": lambda n : setattr(self, 'thing_model_version', n.get_str_value()),
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
        writer.write_str_value("deviceKey", self.device_key)
        writer.write_str_value("productKey", self.product_key)
        writer.write_int_value("productType", self.product_type)
        writer.write_str_value("thingModelVersion", self.thing_model_version)
        writer.write_additional_data_value(self.additional_data)
    

