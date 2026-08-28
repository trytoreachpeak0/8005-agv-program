from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .s_r_object_reference_of_order_sequence import SRObjectReference_Of_OrderSequence
    from .s_r_object_reference_of_order_task import SRObjectReference_Of_OrderTask
    from .s_r_object_reference_of_vehicle_task_info import SRObjectReference_Of_VehicleTaskInfo
    from .vehicle_task_info_integration_level import VehicleTaskInfo_integrationLevel
    from .vehicle_task_info_proc_state import VehicleTaskInfo_procState

@dataclass
class VehicleTaskInfo(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The batteryMaintenanceTime property
    battery_maintenance_time: Optional[int] = None
    # The enable property
    enable: Optional[bool] = None
    # The handlePauseTime property
    handle_pause_time: Optional[int] = None
    # The integrationLevel property
    integration_level: Optional[VehicleTaskInfo_integrationLevel] = None
    # The integrationLevelTime property
    integration_level_time: Optional[int] = None
    # The key property
    key: Optional[str] = None
    # The lastExecuteOrderTimestamp property
    last_execute_order_timestamp: Optional[int] = None
    # The name property
    name: Optional[str] = None
    # The orderSequence property
    order_sequence: Optional[SRObjectReference_Of_OrderSequence] = None
    # The orderTask property
    order_task: Optional[SRObjectReference_Of_OrderTask] = None
    # The procState property
    proc_state: Optional[VehicleTaskInfo_procState] = None
    # The processingOrder property
    processing_order: Optional[bool] = None
    # The reason property
    reason: Optional[str] = None
    # The reference property
    reference: Optional[SRObjectReference_Of_VehicleTaskInfo] = None
    # The routeProgressIndex property
    route_progress_index: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> VehicleTaskInfo:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: VehicleTaskInfo
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return VehicleTaskInfo()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .s_r_object_reference_of_order_sequence import SRObjectReference_Of_OrderSequence
        from .s_r_object_reference_of_order_task import SRObjectReference_Of_OrderTask
        from .s_r_object_reference_of_vehicle_task_info import SRObjectReference_Of_VehicleTaskInfo
        from .vehicle_task_info_integration_level import VehicleTaskInfo_integrationLevel
        from .vehicle_task_info_proc_state import VehicleTaskInfo_procState

        from .s_r_object_reference_of_order_sequence import SRObjectReference_Of_OrderSequence
        from .s_r_object_reference_of_order_task import SRObjectReference_Of_OrderTask
        from .s_r_object_reference_of_vehicle_task_info import SRObjectReference_Of_VehicleTaskInfo
        from .vehicle_task_info_integration_level import VehicleTaskInfo_integrationLevel
        from .vehicle_task_info_proc_state import VehicleTaskInfo_procState

        fields: dict[str, Callable[[Any], None]] = {
            "batteryMaintenanceTime": lambda n : setattr(self, 'battery_maintenance_time', n.get_int_value()),
            "enable": lambda n : setattr(self, 'enable', n.get_bool_value()),
            "handlePauseTime": lambda n : setattr(self, 'handle_pause_time', n.get_int_value()),
            "integrationLevel": lambda n : setattr(self, 'integration_level', n.get_enum_value(VehicleTaskInfo_integrationLevel)),
            "integrationLevelTime": lambda n : setattr(self, 'integration_level_time', n.get_int_value()),
            "key": lambda n : setattr(self, 'key', n.get_str_value()),
            "lastExecuteOrderTimestamp": lambda n : setattr(self, 'last_execute_order_timestamp', n.get_int_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "orderSequence": lambda n : setattr(self, 'order_sequence', n.get_object_value(SRObjectReference_Of_OrderSequence)),
            "orderTask": lambda n : setattr(self, 'order_task', n.get_object_value(SRObjectReference_Of_OrderTask)),
            "procState": lambda n : setattr(self, 'proc_state', n.get_enum_value(VehicleTaskInfo_procState)),
            "processingOrder": lambda n : setattr(self, 'processing_order', n.get_bool_value()),
            "reason": lambda n : setattr(self, 'reason', n.get_str_value()),
            "reference": lambda n : setattr(self, 'reference', n.get_object_value(SRObjectReference_Of_VehicleTaskInfo)),
            "routeProgressIndex": lambda n : setattr(self, 'route_progress_index', n.get_int_value()),
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
        writer.write_int_value("batteryMaintenanceTime", self.battery_maintenance_time)
        writer.write_bool_value("enable", self.enable)
        writer.write_int_value("handlePauseTime", self.handle_pause_time)
        writer.write_enum_value("integrationLevel", self.integration_level)
        writer.write_int_value("integrationLevelTime", self.integration_level_time)
        writer.write_str_value("key", self.key)
        writer.write_int_value("lastExecuteOrderTimestamp", self.last_execute_order_timestamp)
        writer.write_str_value("name", self.name)
        writer.write_object_value("orderSequence", self.order_sequence)
        writer.write_object_value("orderTask", self.order_task)
        writer.write_enum_value("procState", self.proc_state)
        writer.write_bool_value("processingOrder", self.processing_order)
        writer.write_str_value("reason", self.reason)
        writer.write_object_value("reference", self.reference)
        writer.write_int_value("routeProgressIndex", self.route_progress_index)
        writer.write_additional_data_value(self.additional_data)
    

