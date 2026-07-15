from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .coordinate import Coordinate
    from .hardware_state import HardwareState
    from .info_state import InfoState
    from .load_handling_device import LoadHandlingDevice
    from .system_state import SystemState
    from .s_r_object_reference_of_vehicle import SRObjectReference_Of_Vehicle
    from .vehicle_action_state import Vehicle_actionState
    from .vehicle_agv_info_state import Vehicle_agvInfoState
    from .vehicle_battery_state import Vehicle_batteryState
    from .vehicle_break_switch_state import Vehicle_breakSwitchState
    from .vehicle_control_state import Vehicle_controlState
    from .vehicle_emergency_state import Vehicle_emergencyState
    from .vehicle_fleet_mode import Vehicle_fleetMode
    from .vehicle_hardware_state import Vehicle_hardwareState
    from .vehicle_location_state import Vehicle_locationState
    from .vehicle_mode import Vehicle_mode
    from .vehicle_motor_exception_state import Vehicle_motorExceptionState
    from .vehicle_movement_state import Vehicle_movementState
    from .vehicle_power_mode import Vehicle_powerMode
    from .vehicle_routing_group import Vehicle_routingGroup
    from .vehicle_state import Vehicle_state

@dataclass
class Vehicle(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The actionState property
    action_state: Optional[Vehicle_actionState] = None
    # The actionTaskNo property
    action_task_no: Optional[int] = None
    # The agvInfoState property
    agv_info_state: Optional[Vehicle_agvInfoState] = None
    # The aliveState property
    alive_state: Optional[bool] = None
    # The battery property
    battery: Optional[int] = None
    # The batteryState property
    battery_state: Optional[Vehicle_batteryState] = None
    # The breakSwitchState property
    break_switch_state: Optional[Vehicle_breakSwitchState] = None
    # The confidence property
    confidence: Optional[int] = None
    # The connected property
    connected: Optional[bool] = None
    # The connectedTimestamp property
    connected_timestamp: Optional[int] = None
    # The controlState property
    control_state: Optional[Vehicle_controlState] = None
    # The curCheckPointNo property
    cur_check_point_no: Optional[int] = None
    # The curPathNo property
    cur_path_no: Optional[int] = None
    # The currentNode property
    current_node: Optional[int] = None
    # The currentStation property
    current_station: Optional[int] = None
    # The emergencyState property
    emergency_state: Optional[Vehicle_emergencyState] = None
    # The faultCodes property
    fault_codes: Optional[str] = None
    # The faultCodesList property
    fault_codes_list: Optional[list[int]] = None
    # The firstReportData property
    first_report_data: Optional[bool] = None
    # The fleetMode property
    fleet_mode: Optional[Vehicle_fleetMode] = None
    # The freshState property
    fresh_state: Optional[int] = None
    # The hardWareErrorCode property
    hard_ware_error_code: Optional[int] = None
    # The hardwareState property
    hardware_state: Optional[Vehicle_hardwareState] = None
    # The infoState property
    info_state: Optional[InfoState] = None
    # The key property
    key: Optional[str] = None
    # The lastErrorCode property
    last_error_code: Optional[int] = None
    # The lastReportTime property
    last_report_time: Optional[int] = None
    # The length property
    length: Optional[int] = None
    # The loadHandlingDevices property
    load_handling_devices: Optional[list[LoadHandlingDevice]] = None
    # The loadState property
    load_state: Optional[int] = None
    # The locationState property
    location_state: Optional[Vehicle_locationState] = None
    # The mode property
    mode: Optional[Vehicle_mode] = None
    # The motorExceptionState property
    motor_exception_state: Optional[Vehicle_motorExceptionState] = None
    # The moveTaskNo property
    move_task_no: Optional[int] = None
    # The movementState property
    movement_state: Optional[Vehicle_movementState] = None
    # The name property
    name: Optional[str] = None
    # The noNode property
    no_node: Optional[bool] = None
    # The noStation property
    no_station: Optional[bool] = None
    # The orientationAngle property
    orientation_angle: Optional[float] = None
    # The originalLength property
    original_length: Optional[int] = None
    # The originalWidth property
    original_width: Optional[int] = None
    # The pausePosition property
    pause_position: Optional[Coordinate] = None
    # The paused property
    paused: Optional[bool] = None
    # The plantModel property
    plant_model: Optional[str] = None
    # The powerMode property
    power_mode: Optional[Vehicle_powerMode] = None
    # The precisePosition property
    precise_position: Optional[Coordinate] = None
    # The previousState property
    previous_state: Optional[SystemState] = None
    # The productKey property
    product_key: Optional[str] = None
    # The reference property
    reference: Optional[SRObjectReference_Of_Vehicle] = None
    # The routingGroup property
    routing_group: Optional[Vehicle_routingGroup] = None
    # The running property
    running: Optional[bool] = None
    # The speed property
    speed: Optional[float] = None
    # The startPauseTime property
    start_pause_time: Optional[int] = None
    # The state property
    state: Optional[Vehicle_state] = None
    # The status property
    status: Optional[int] = None
    # The vehicleHardware property
    vehicle_hardware: Optional[HardwareState] = None
    # The vehicleId property
    vehicle_id: Optional[int] = None
    # The width property
    width: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> Vehicle:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: Vehicle
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return Vehicle()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .coordinate import Coordinate
        from .hardware_state import HardwareState
        from .info_state import InfoState
        from .load_handling_device import LoadHandlingDevice
        from .system_state import SystemState
        from .s_r_object_reference_of_vehicle import SRObjectReference_Of_Vehicle
        from .vehicle_action_state import Vehicle_actionState
        from .vehicle_agv_info_state import Vehicle_agvInfoState
        from .vehicle_battery_state import Vehicle_batteryState
        from .vehicle_break_switch_state import Vehicle_breakSwitchState
        from .vehicle_control_state import Vehicle_controlState
        from .vehicle_emergency_state import Vehicle_emergencyState
        from .vehicle_fleet_mode import Vehicle_fleetMode
        from .vehicle_hardware_state import Vehicle_hardwareState
        from .vehicle_location_state import Vehicle_locationState
        from .vehicle_mode import Vehicle_mode
        from .vehicle_motor_exception_state import Vehicle_motorExceptionState
        from .vehicle_movement_state import Vehicle_movementState
        from .vehicle_power_mode import Vehicle_powerMode
        from .vehicle_routing_group import Vehicle_routingGroup
        from .vehicle_state import Vehicle_state

        from .coordinate import Coordinate
        from .hardware_state import HardwareState
        from .info_state import InfoState
        from .load_handling_device import LoadHandlingDevice
        from .system_state import SystemState
        from .s_r_object_reference_of_vehicle import SRObjectReference_Of_Vehicle
        from .vehicle_action_state import Vehicle_actionState
        from .vehicle_agv_info_state import Vehicle_agvInfoState
        from .vehicle_battery_state import Vehicle_batteryState
        from .vehicle_break_switch_state import Vehicle_breakSwitchState
        from .vehicle_control_state import Vehicle_controlState
        from .vehicle_emergency_state import Vehicle_emergencyState
        from .vehicle_fleet_mode import Vehicle_fleetMode
        from .vehicle_hardware_state import Vehicle_hardwareState
        from .vehicle_location_state import Vehicle_locationState
        from .vehicle_mode import Vehicle_mode
        from .vehicle_motor_exception_state import Vehicle_motorExceptionState
        from .vehicle_movement_state import Vehicle_movementState
        from .vehicle_power_mode import Vehicle_powerMode
        from .vehicle_routing_group import Vehicle_routingGroup
        from .vehicle_state import Vehicle_state

        fields: dict[str, Callable[[Any], None]] = {
            "actionState": lambda n : setattr(self, 'action_state', n.get_enum_value(Vehicle_actionState)),
            "actionTaskNo": lambda n : setattr(self, 'action_task_no', n.get_int_value()),
            "agvInfoState": lambda n : setattr(self, 'agv_info_state', n.get_enum_value(Vehicle_agvInfoState)),
            "aliveState": lambda n : setattr(self, 'alive_state', n.get_bool_value()),
            "battery": lambda n : setattr(self, 'battery', n.get_int_value()),
            "batteryState": lambda n : setattr(self, 'battery_state', n.get_enum_value(Vehicle_batteryState)),
            "breakSwitchState": lambda n : setattr(self, 'break_switch_state', n.get_enum_value(Vehicle_breakSwitchState)),
            "confidence": lambda n : setattr(self, 'confidence', n.get_int_value()),
            "connected": lambda n : setattr(self, 'connected', n.get_bool_value()),
            "connectedTimestamp": lambda n : setattr(self, 'connected_timestamp', n.get_int_value()),
            "controlState": lambda n : setattr(self, 'control_state', n.get_enum_value(Vehicle_controlState)),
            "curCheckPointNo": lambda n : setattr(self, 'cur_check_point_no', n.get_int_value()),
            "curPathNo": lambda n : setattr(self, 'cur_path_no', n.get_int_value()),
            "currentNode": lambda n : setattr(self, 'current_node', n.get_int_value()),
            "currentStation": lambda n : setattr(self, 'current_station', n.get_int_value()),
            "emergencyState": lambda n : setattr(self, 'emergency_state', n.get_enum_value(Vehicle_emergencyState)),
            "faultCodes": lambda n : setattr(self, 'fault_codes', n.get_str_value()),
            "faultCodesList": lambda n : setattr(self, 'fault_codes_list', n.get_collection_of_primitive_values(int)),
            "firstReportData": lambda n : setattr(self, 'first_report_data', n.get_bool_value()),
            "fleetMode": lambda n : setattr(self, 'fleet_mode', n.get_enum_value(Vehicle_fleetMode)),
            "freshState": lambda n : setattr(self, 'fresh_state', n.get_int_value()),
            "hardWareErrorCode": lambda n : setattr(self, 'hard_ware_error_code', n.get_int_value()),
            "hardwareState": lambda n : setattr(self, 'hardware_state', n.get_enum_value(Vehicle_hardwareState)),
            "infoState": lambda n : setattr(self, 'info_state', n.get_object_value(InfoState)),
            "key": lambda n : setattr(self, 'key', n.get_str_value()),
            "lastErrorCode": lambda n : setattr(self, 'last_error_code', n.get_int_value()),
            "lastReportTime": lambda n : setattr(self, 'last_report_time', n.get_int_value()),
            "length": lambda n : setattr(self, 'length', n.get_int_value()),
            "loadHandlingDevices": lambda n : setattr(self, 'load_handling_devices', n.get_collection_of_object_values(LoadHandlingDevice)),
            "loadState": lambda n : setattr(self, 'load_state', n.get_int_value()),
            "locationState": lambda n : setattr(self, 'location_state', n.get_enum_value(Vehicle_locationState)),
            "mode": lambda n : setattr(self, 'mode', n.get_enum_value(Vehicle_mode)),
            "motorExceptionState": lambda n : setattr(self, 'motor_exception_state', n.get_enum_value(Vehicle_motorExceptionState)),
            "moveTaskNo": lambda n : setattr(self, 'move_task_no', n.get_int_value()),
            "movementState": lambda n : setattr(self, 'movement_state', n.get_enum_value(Vehicle_movementState)),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "noNode": lambda n : setattr(self, 'no_node', n.get_bool_value()),
            "noStation": lambda n : setattr(self, 'no_station', n.get_bool_value()),
            "orientationAngle": lambda n : setattr(self, 'orientation_angle', n.get_float_value()),
            "originalLength": lambda n : setattr(self, 'original_length', n.get_int_value()),
            "originalWidth": lambda n : setattr(self, 'original_width', n.get_int_value()),
            "pausePosition": lambda n : setattr(self, 'pause_position', n.get_object_value(Coordinate)),
            "paused": lambda n : setattr(self, 'paused', n.get_bool_value()),
            "plantModel": lambda n : setattr(self, 'plant_model', n.get_str_value()),
            "powerMode": lambda n : setattr(self, 'power_mode', n.get_enum_value(Vehicle_powerMode)),
            "precisePosition": lambda n : setattr(self, 'precise_position', n.get_object_value(Coordinate)),
            "previousState": lambda n : setattr(self, 'previous_state', n.get_object_value(SystemState)),
            "productKey": lambda n : setattr(self, 'product_key', n.get_str_value()),
            "reference": lambda n : setattr(self, 'reference', n.get_object_value(SRObjectReference_Of_Vehicle)),
            "routingGroup": lambda n : setattr(self, 'routing_group', n.get_enum_value(Vehicle_routingGroup)),
            "running": lambda n : setattr(self, 'running', n.get_bool_value()),
            "speed": lambda n : setattr(self, 'speed', n.get_float_value()),
            "startPauseTime": lambda n : setattr(self, 'start_pause_time', n.get_int_value()),
            "state": lambda n : setattr(self, 'state', n.get_enum_value(Vehicle_state)),
            "status": lambda n : setattr(self, 'status', n.get_int_value()),
            "vehicleHardware": lambda n : setattr(self, 'vehicle_hardware', n.get_object_value(HardwareState)),
            "vehicleId": lambda n : setattr(self, 'vehicle_id', n.get_int_value()),
            "width": lambda n : setattr(self, 'width', n.get_int_value()),
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
        writer.write_enum_value("actionState", self.action_state)
        writer.write_int_value("actionTaskNo", self.action_task_no)
        writer.write_enum_value("agvInfoState", self.agv_info_state)
        writer.write_bool_value("aliveState", self.alive_state)
        writer.write_int_value("battery", self.battery)
        writer.write_enum_value("batteryState", self.battery_state)
        writer.write_enum_value("breakSwitchState", self.break_switch_state)
        writer.write_int_value("confidence", self.confidence)
        writer.write_bool_value("connected", self.connected)
        writer.write_int_value("connectedTimestamp", self.connected_timestamp)
        writer.write_enum_value("controlState", self.control_state)
        writer.write_int_value("curCheckPointNo", self.cur_check_point_no)
        writer.write_int_value("curPathNo", self.cur_path_no)
        writer.write_int_value("currentNode", self.current_node)
        writer.write_int_value("currentStation", self.current_station)
        writer.write_enum_value("emergencyState", self.emergency_state)
        writer.write_str_value("faultCodes", self.fault_codes)
        writer.write_collection_of_primitive_values("faultCodesList", self.fault_codes_list)
        writer.write_bool_value("firstReportData", self.first_report_data)
        writer.write_enum_value("fleetMode", self.fleet_mode)
        writer.write_int_value("freshState", self.fresh_state)
        writer.write_int_value("hardWareErrorCode", self.hard_ware_error_code)
        writer.write_enum_value("hardwareState", self.hardware_state)
        writer.write_object_value("infoState", self.info_state)
        writer.write_str_value("key", self.key)
        writer.write_int_value("lastErrorCode", self.last_error_code)
        writer.write_int_value("lastReportTime", self.last_report_time)
        writer.write_int_value("length", self.length)
        writer.write_collection_of_object_values("loadHandlingDevices", self.load_handling_devices)
        writer.write_int_value("loadState", self.load_state)
        writer.write_enum_value("locationState", self.location_state)
        writer.write_enum_value("mode", self.mode)
        writer.write_enum_value("motorExceptionState", self.motor_exception_state)
        writer.write_int_value("moveTaskNo", self.move_task_no)
        writer.write_enum_value("movementState", self.movement_state)
        writer.write_str_value("name", self.name)
        writer.write_bool_value("noNode", self.no_node)
        writer.write_bool_value("noStation", self.no_station)
        writer.write_float_value("orientationAngle", self.orientation_angle)
        writer.write_int_value("originalLength", self.original_length)
        writer.write_int_value("originalWidth", self.original_width)
        writer.write_object_value("pausePosition", self.pause_position)
        writer.write_bool_value("paused", self.paused)
        writer.write_str_value("plantModel", self.plant_model)
        writer.write_enum_value("powerMode", self.power_mode)
        writer.write_object_value("precisePosition", self.precise_position)
        writer.write_object_value("previousState", self.previous_state)
        writer.write_str_value("productKey", self.product_key)
        writer.write_object_value("reference", self.reference)
        writer.write_enum_value("routingGroup", self.routing_group)
        writer.write_bool_value("running", self.running)
        writer.write_float_value("speed", self.speed)
        writer.write_int_value("startPauseTime", self.start_pause_time)
        writer.write_enum_value("state", self.state)
        writer.write_int_value("status", self.status)
        writer.write_object_value("vehicleHardware", self.vehicle_hardware)
        writer.write_int_value("vehicleId", self.vehicle_id)
        writer.write_int_value("width", self.width)
        writer.write_additional_data_value(self.additional_data)
    

