from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .check_fail_detail_type import CheckFailDetail_type

@dataclass
class CheckFailDetail(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The appliedVehicleId property
    applied_vehicle_id: Optional[str] = None
    # The detail property
    detail: Optional[str] = None
    # The lockedVehicleIds property
    locked_vehicle_ids: Optional[list[str]] = None
    # The time property
    time: Optional[str] = None
    # The type property
    type: Optional[CheckFailDetail_type] = None
    # The vehicleNames property
    vehicle_names: Optional[list[str]] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> CheckFailDetail:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: CheckFailDetail
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return CheckFailDetail()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .check_fail_detail_type import CheckFailDetail_type

        from .check_fail_detail_type import CheckFailDetail_type

        fields: dict[str, Callable[[Any], None]] = {
            "appliedVehicleId": lambda n : setattr(self, 'applied_vehicle_id', n.get_str_value()),
            "detail": lambda n : setattr(self, 'detail', n.get_str_value()),
            "lockedVehicleIds": lambda n : setattr(self, 'locked_vehicle_ids', n.get_collection_of_primitive_values(str)),
            "time": lambda n : setattr(self, 'time', n.get_str_value()),
            "type": lambda n : setattr(self, 'type', n.get_enum_value(CheckFailDetail_type)),
            "vehicleNames": lambda n : setattr(self, 'vehicle_names', n.get_collection_of_primitive_values(str)),
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
        writer.write_str_value("appliedVehicleId", self.applied_vehicle_id)
        writer.write_str_value("detail", self.detail)
        writer.write_collection_of_primitive_values("lockedVehicleIds", self.locked_vehicle_ids)
        writer.write_str_value("time", self.time)
        writer.write_enum_value("type", self.type)
        writer.write_collection_of_primitive_values("vehicleNames", self.vehicle_names)
        writer.write_additional_data_value(self.additional_data)
    

