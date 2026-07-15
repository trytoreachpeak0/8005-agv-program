from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .action_task import ActionTask
    from .motion_control_state import MotionControlState
    from .movement_state import MovementState
    from .pose import Pose

@dataclass
class SystemState(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The actionTask property
    action_task: Optional[ActionTask] = None
    # The currentPosition property
    current_position: Optional[Pose] = None
    # The emergencyState property
    emergency_state: Optional[int] = None
    # The faultCodesList property
    fault_codes_list: Optional[list[int]] = None
    # The fleetMode property
    fleet_mode: Optional[int] = None
    # The freshState property
    fresh_state: Optional[int] = None
    # The lastErrorCode property
    last_error_code: Optional[int] = None
    # The locationState property
    location_state: Optional[int] = None
    # The mapName property
    map_name: Optional[str] = None
    # The motionControlState property
    motion_control_state: Optional[MotionControlState] = None
    # The movementState property
    movement_state: Optional[MovementState] = None
    # The multiLoadState property
    multi_load_state: Optional[int] = None
    # The newMovementTaskState property
    new_movement_task_state: Optional[int] = None
    # The operationState property
    operation_state: Optional[int] = None
    # The stationNo property
    station_no: Optional[int] = None
    # The sysState property
    sys_state: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> SystemState:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: SystemState
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return SystemState()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .action_task import ActionTask
        from .motion_control_state import MotionControlState
        from .movement_state import MovementState
        from .pose import Pose

        from .action_task import ActionTask
        from .motion_control_state import MotionControlState
        from .movement_state import MovementState
        from .pose import Pose

        fields: dict[str, Callable[[Any], None]] = {
            "actionTask": lambda n : setattr(self, 'action_task', n.get_object_value(ActionTask)),
            "currentPosition": lambda n : setattr(self, 'current_position', n.get_object_value(Pose)),
            "emergencyState": lambda n : setattr(self, 'emergency_state', n.get_int_value()),
            "faultCodesList": lambda n : setattr(self, 'fault_codes_list', n.get_collection_of_primitive_values(int)),
            "fleetMode": lambda n : setattr(self, 'fleet_mode', n.get_int_value()),
            "freshState": lambda n : setattr(self, 'fresh_state', n.get_int_value()),
            "lastErrorCode": lambda n : setattr(self, 'last_error_code', n.get_int_value()),
            "locationState": lambda n : setattr(self, 'location_state', n.get_int_value()),
            "mapName": lambda n : setattr(self, 'map_name', n.get_str_value()),
            "motionControlState": lambda n : setattr(self, 'motion_control_state', n.get_object_value(MotionControlState)),
            "movementState": lambda n : setattr(self, 'movement_state', n.get_object_value(MovementState)),
            "multiLoadState": lambda n : setattr(self, 'multi_load_state', n.get_int_value()),
            "newMovementTaskState": lambda n : setattr(self, 'new_movement_task_state', n.get_int_value()),
            "operationState": lambda n : setattr(self, 'operation_state', n.get_int_value()),
            "stationNo": lambda n : setattr(self, 'station_no', n.get_int_value()),
            "sysState": lambda n : setattr(self, 'sys_state', n.get_int_value()),
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
        writer.write_object_value("actionTask", self.action_task)
        writer.write_object_value("currentPosition", self.current_position)
        writer.write_int_value("emergencyState", self.emergency_state)
        writer.write_collection_of_primitive_values("faultCodesList", self.fault_codes_list)
        writer.write_int_value("fleetMode", self.fleet_mode)
        writer.write_int_value("freshState", self.fresh_state)
        writer.write_int_value("lastErrorCode", self.last_error_code)
        writer.write_int_value("locationState", self.location_state)
        writer.write_str_value("mapName", self.map_name)
        writer.write_object_value("motionControlState", self.motion_control_state)
        writer.write_object_value("movementState", self.movement_state)
        writer.write_int_value("multiLoadState", self.multi_load_state)
        writer.write_int_value("newMovementTaskState", self.new_movement_task_state)
        writer.write_int_value("operationState", self.operation_state)
        writer.write_int_value("stationNo", self.station_no)
        writer.write_int_value("sysState", self.sys_state)
        writer.write_additional_data_value(self.additional_data)
    

