from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .system_log_object import SystemLogObject

@dataclass
class SystemLogStatusDTO(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The deadly property
    deadly: Optional[int] = None
    # The deadlyList property
    deadly_list: Optional[list[SystemLogObject]] = None
    # The error property
    error: Optional[int] = None
    # The normal property
    normal: Optional[int] = None
    # The total property
    total: Optional[int] = None
    # The warmList property
    warm_list: Optional[list[SystemLogObject]] = None
    # The warn property
    warn: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> SystemLogStatusDTO:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: SystemLogStatusDTO
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return SystemLogStatusDTO()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .system_log_object import SystemLogObject

        from .system_log_object import SystemLogObject

        fields: dict[str, Callable[[Any], None]] = {
            "deadly": lambda n : setattr(self, 'deadly', n.get_int_value()),
            "deadlyList": lambda n : setattr(self, 'deadly_list', n.get_collection_of_object_values(SystemLogObject)),
            "error": lambda n : setattr(self, 'error', n.get_int_value()),
            "normal": lambda n : setattr(self, 'normal', n.get_int_value()),
            "total": lambda n : setattr(self, 'total', n.get_int_value()),
            "warmList": lambda n : setattr(self, 'warm_list', n.get_collection_of_object_values(SystemLogObject)),
            "warn": lambda n : setattr(self, 'warn', n.get_int_value()),
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
        writer.write_int_value("deadly", self.deadly)
        writer.write_collection_of_object_values("deadlyList", self.deadly_list)
        writer.write_int_value("error", self.error)
        writer.write_int_value("normal", self.normal)
        writer.write_int_value("total", self.total)
        writer.write_collection_of_object_values("warmList", self.warm_list)
        writer.write_int_value("warn", self.warn)
        writer.write_additional_data_value(self.additional_data)
    

