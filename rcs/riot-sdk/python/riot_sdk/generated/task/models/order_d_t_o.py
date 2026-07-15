from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .mission_d_t_o import MissionDTO
    from .order_d_t_o_order_type import OrderDTO_orderType

@dataclass
class OrderDTO(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The appointMapId property
    appoint_map_id: Optional[int] = None
    # The appointStationId property
    appoint_station_id: Optional[int] = None
    # The appointVehicleGroup property
    appoint_vehicle_group: Optional[int] = None
    # The appointVehicleKey property
    appoint_vehicle_key: Optional[str] = None
    # The createTime property
    create_time: Optional[str] = None
    # The deadline property
    deadline: Optional[str] = None
    # The executeVehicleKey property
    execute_vehicle_key: Optional[str] = None
    # The lockStatus property
    lock_status: Optional[int] = None
    # The lockVehicleKey property
    lock_vehicle_key: Optional[str] = None
    # The mission property
    mission: Optional[list[MissionDTO]] = None
    # The orderId property
    order_id: Optional[str] = None
    # The orderName property
    order_name: Optional[str] = None
    # The orderType property
    order_type: Optional[OrderDTO_orderType] = None
    # The priority property
    priority: Optional[int] = None
    # The upperId property
    upper_id: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> OrderDTO:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: OrderDTO
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return OrderDTO()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .mission_d_t_o import MissionDTO
        from .order_d_t_o_order_type import OrderDTO_orderType

        from .mission_d_t_o import MissionDTO
        from .order_d_t_o_order_type import OrderDTO_orderType

        fields: dict[str, Callable[[Any], None]] = {
            "appointMapId": lambda n : setattr(self, 'appoint_map_id', n.get_int_value()),
            "appointStationId": lambda n : setattr(self, 'appoint_station_id', n.get_int_value()),
            "appointVehicleGroup": lambda n : setattr(self, 'appoint_vehicle_group', n.get_int_value()),
            "appointVehicleKey": lambda n : setattr(self, 'appoint_vehicle_key', n.get_str_value()),
            "createTime": lambda n : setattr(self, 'create_time', n.get_str_value()),
            "deadline": lambda n : setattr(self, 'deadline', n.get_str_value()),
            "executeVehicleKey": lambda n : setattr(self, 'execute_vehicle_key', n.get_str_value()),
            "lockStatus": lambda n : setattr(self, 'lock_status', n.get_int_value()),
            "lockVehicleKey": lambda n : setattr(self, 'lock_vehicle_key', n.get_str_value()),
            "mission": lambda n : setattr(self, 'mission', n.get_collection_of_object_values(MissionDTO)),
            "orderId": lambda n : setattr(self, 'order_id', n.get_str_value()),
            "orderName": lambda n : setattr(self, 'order_name', n.get_str_value()),
            "orderType": lambda n : setattr(self, 'order_type', n.get_enum_value(OrderDTO_orderType)),
            "priority": lambda n : setattr(self, 'priority', n.get_int_value()),
            "upperId": lambda n : setattr(self, 'upper_id', n.get_str_value()),
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
        writer.write_int_value("appointMapId", self.appoint_map_id)
        writer.write_int_value("appointStationId", self.appoint_station_id)
        writer.write_int_value("appointVehicleGroup", self.appoint_vehicle_group)
        writer.write_str_value("appointVehicleKey", self.appoint_vehicle_key)
        writer.write_str_value("createTime", self.create_time)
        writer.write_str_value("deadline", self.deadline)
        writer.write_str_value("executeVehicleKey", self.execute_vehicle_key)
        writer.write_int_value("lockStatus", self.lock_status)
        writer.write_str_value("lockVehicleKey", self.lock_vehicle_key)
        writer.write_collection_of_object_values("mission", self.mission)
        writer.write_str_value("orderId", self.order_id)
        writer.write_str_value("orderName", self.order_name)
        writer.write_enum_value("orderType", self.order_type)
        writer.write_int_value("priority", self.priority)
        writer.write_str_value("upperId", self.upper_id)
        writer.write_additional_data_value(self.additional_data)
    

