from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .edge_group_processor_dump_edge_group_vehicle_resource_id_map import EdgeGroupProcessorDump_edgeGroupVehicleResourceIdMap
    from .edge_group_processor_dump_vehicle_applied_resource_order_map import EdgeGroupProcessorDump_vehicleAppliedResourceOrderMap

@dataclass
class EdgeGroupProcessorDump(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The edgeGroupVehicleResourceIdMap property
    edge_group_vehicle_resource_id_map: Optional[EdgeGroupProcessorDump_edgeGroupVehicleResourceIdMap] = None
    # The vehicleAppliedResourceOrderMap property
    vehicle_applied_resource_order_map: Optional[EdgeGroupProcessorDump_vehicleAppliedResourceOrderMap] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> EdgeGroupProcessorDump:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: EdgeGroupProcessorDump
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return EdgeGroupProcessorDump()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .edge_group_processor_dump_edge_group_vehicle_resource_id_map import EdgeGroupProcessorDump_edgeGroupVehicleResourceIdMap
        from .edge_group_processor_dump_vehicle_applied_resource_order_map import EdgeGroupProcessorDump_vehicleAppliedResourceOrderMap

        from .edge_group_processor_dump_edge_group_vehicle_resource_id_map import EdgeGroupProcessorDump_edgeGroupVehicleResourceIdMap
        from .edge_group_processor_dump_vehicle_applied_resource_order_map import EdgeGroupProcessorDump_vehicleAppliedResourceOrderMap

        fields: dict[str, Callable[[Any], None]] = {
            "edgeGroupVehicleResourceIdMap": lambda n : setattr(self, 'edge_group_vehicle_resource_id_map', n.get_object_value(EdgeGroupProcessorDump_edgeGroupVehicleResourceIdMap)),
            "vehicleAppliedResourceOrderMap": lambda n : setattr(self, 'vehicle_applied_resource_order_map', n.get_object_value(EdgeGroupProcessorDump_vehicleAppliedResourceOrderMap)),
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
        writer.write_object_value("edgeGroupVehicleResourceIdMap", self.edge_group_vehicle_resource_id_map)
        writer.write_object_value("vehicleAppliedResourceOrderMap", self.vehicle_applied_resource_order_map)
        writer.write_additional_data_value(self.additional_data)
    

