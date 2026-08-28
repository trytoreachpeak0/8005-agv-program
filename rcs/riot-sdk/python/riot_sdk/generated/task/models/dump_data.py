from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .edge_group_processor_dump import EdgeGroupProcessorDump
    from .traffic_sub_system_dump import TrafficSubSystemDump

@dataclass
class DumpData(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The edgeGroupProcessorDump property
    edge_group_processor_dump: Optional[EdgeGroupProcessorDump] = None
    # The trafficSubSystemDumpList property
    traffic_sub_system_dump_list: Optional[list[TrafficSubSystemDump]] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> DumpData:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: DumpData
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return DumpData()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .edge_group_processor_dump import EdgeGroupProcessorDump
        from .traffic_sub_system_dump import TrafficSubSystemDump

        from .edge_group_processor_dump import EdgeGroupProcessorDump
        from .traffic_sub_system_dump import TrafficSubSystemDump

        fields: dict[str, Callable[[Any], None]] = {
            "edgeGroupProcessorDump": lambda n : setattr(self, 'edge_group_processor_dump', n.get_object_value(EdgeGroupProcessorDump)),
            "trafficSubSystemDumpList": lambda n : setattr(self, 'traffic_sub_system_dump_list', n.get_collection_of_object_values(TrafficSubSystemDump)),
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
        writer.write_object_value("edgeGroupProcessorDump", self.edge_group_processor_dump)
        writer.write_collection_of_object_values("trafficSubSystemDumpList", self.traffic_sub_system_dump_list)
        writer.write_additional_data_value(self.additional_data)
    

