from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .vehicle import Vehicle
    from .vehicle_task_info import VehicleTaskInfo

@dataclass
class VehicleAllInfo(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The vehicle property
    vehicle: Optional[Vehicle] = None
    # The vehicleTaskInfo property
    vehicle_task_info: Optional[VehicleTaskInfo] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> VehicleAllInfo:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: VehicleAllInfo
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return VehicleAllInfo()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .vehicle import Vehicle
        from .vehicle_task_info import VehicleTaskInfo

        from .vehicle import Vehicle
        from .vehicle_task_info import VehicleTaskInfo

        fields: dict[str, Callable[[Any], None]] = {
            "vehicle": lambda n : setattr(self, 'vehicle', n.get_object_value(Vehicle)),
            "vehicleTaskInfo": lambda n : setattr(self, 'vehicle_task_info', n.get_object_value(VehicleTaskInfo)),
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
        writer.write_object_value("vehicle", self.vehicle)
        writer.write_object_value("vehicleTaskInfo", self.vehicle_task_info)
        writer.write_additional_data_value(self.additional_data)
    

