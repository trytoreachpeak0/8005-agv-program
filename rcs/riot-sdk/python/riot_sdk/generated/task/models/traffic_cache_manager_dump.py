from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .traffic_cache_manager_dump_vehicle_applied_resource_shape_map import TrafficCacheManagerDump_vehicleAppliedResourceShapeMap
    from .traffic_cache_manager_dump_vehicle_locked_resource_shape_map import TrafficCacheManagerDump_vehicleLockedResourceShapeMap

@dataclass
class TrafficCacheManagerDump(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The mapId property
    map_id: Optional[int] = None
    # The vehicleAppliedResourceShapeMap property
    vehicle_applied_resource_shape_map: Optional[TrafficCacheManagerDump_vehicleAppliedResourceShapeMap] = None
    # The vehicleLockedResourceShapeMap property
    vehicle_locked_resource_shape_map: Optional[TrafficCacheManagerDump_vehicleLockedResourceShapeMap] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> TrafficCacheManagerDump:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: TrafficCacheManagerDump
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return TrafficCacheManagerDump()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .traffic_cache_manager_dump_vehicle_applied_resource_shape_map import TrafficCacheManagerDump_vehicleAppliedResourceShapeMap
        from .traffic_cache_manager_dump_vehicle_locked_resource_shape_map import TrafficCacheManagerDump_vehicleLockedResourceShapeMap

        from .traffic_cache_manager_dump_vehicle_applied_resource_shape_map import TrafficCacheManagerDump_vehicleAppliedResourceShapeMap
        from .traffic_cache_manager_dump_vehicle_locked_resource_shape_map import TrafficCacheManagerDump_vehicleLockedResourceShapeMap

        fields: dict[str, Callable[[Any], None]] = {
            "mapId": lambda n : setattr(self, 'map_id', n.get_int_value()),
            "vehicleAppliedResourceShapeMap": lambda n : setattr(self, 'vehicle_applied_resource_shape_map', n.get_object_value(TrafficCacheManagerDump_vehicleAppliedResourceShapeMap)),
            "vehicleLockedResourceShapeMap": lambda n : setattr(self, 'vehicle_locked_resource_shape_map', n.get_object_value(TrafficCacheManagerDump_vehicleLockedResourceShapeMap)),
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
        writer.write_int_value("mapId", self.map_id)
        writer.write_object_value("vehicleAppliedResourceShapeMap", self.vehicle_applied_resource_shape_map)
        writer.write_object_value("vehicleLockedResourceShapeMap", self.vehicle_locked_resource_shape_map)
        writer.write_additional_data_value(self.additional_data)
    

