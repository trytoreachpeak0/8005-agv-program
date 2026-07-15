from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .traffic_cache_manager_dump import TrafficCacheManagerDump

@dataclass
class TrafficSubSystemDump(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The trafficCacheManagerDump property
    traffic_cache_manager_dump: Optional[TrafficCacheManagerDump] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> TrafficSubSystemDump:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: TrafficSubSystemDump
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return TrafficSubSystemDump()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .traffic_cache_manager_dump import TrafficCacheManagerDump

        from .traffic_cache_manager_dump import TrafficCacheManagerDump

        fields: dict[str, Callable[[Any], None]] = {
            "trafficCacheManagerDump": lambda n : setattr(self, 'traffic_cache_manager_dump', n.get_object_value(TrafficCacheManagerDump)),
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
        writer.write_object_value("trafficCacheManagerDump", self.traffic_cache_manager_dump)
        writer.write_additional_data_value(self.additional_data)
    

