from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class HardwareState(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The batteryCurrent property
    battery_current: Optional[int] = None
    # The batteryPercentage property
    battery_percentage: Optional[int] = None
    # The batteryState property
    battery_state: Optional[int] = None
    # The batteryTemperature property
    battery_temperature: Optional[int] = None
    # The batteryUseCycles property
    battery_use_cycles: Optional[int] = None
    # The batteryVoltage property
    battery_voltage: Optional[int] = None
    # The boxTemperature property
    box_temperature: Optional[int] = None
    # The breakSwState property
    break_sw_state: Optional[int] = None
    # The cpuTemperature property
    cpu_temperature: Optional[int] = None
    # The cpuUsage property
    cpu_usage: Optional[int] = None
    # The desc property
    desc: Optional[str] = None
    # The deviceId property
    device_id: Optional[int] = None
    # The diskUsage property
    disk_usage: Optional[int] = None
    # The hardwareErrorCode property
    hardware_error_code: Optional[int] = None
    # The hostPort property
    host_port: Optional[str] = None
    # The hstate property
    hstate: Optional[int] = None
    # The m1StatusCode property
    m1_status_code: Optional[int] = None
    # The m2StatusCode property
    m2_status_code: Optional[int] = None
    # The m3StatusCode property
    m3_status_code: Optional[int] = None
    # The m4StatusCode property
    m4_status_code: Optional[int] = None
    # The memoryUsage property
    memory_usage: Optional[int] = None
    # The modelVersion property
    model_version: Optional[str] = None
    # The nodeType property
    node_type: Optional[int] = None
    # The powerState property
    power_state: Optional[int] = None
    # The remainDiskSpace property
    remain_disk_space: Optional[int] = None
    # The totalMileage property
    total_mileage: Optional[int] = None
    # The totalPowerCycle property
    total_power_cycle: Optional[int] = None
    # The totalPoweronTime property
    total_poweron_time: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> HardwareState:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: HardwareState
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return HardwareState()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "batteryCurrent": lambda n : setattr(self, 'battery_current', n.get_int_value()),
            "batteryPercentage": lambda n : setattr(self, 'battery_percentage', n.get_int_value()),
            "batteryState": lambda n : setattr(self, 'battery_state', n.get_int_value()),
            "batteryTemperature": lambda n : setattr(self, 'battery_temperature', n.get_int_value()),
            "batteryUseCycles": lambda n : setattr(self, 'battery_use_cycles', n.get_int_value()),
            "batteryVoltage": lambda n : setattr(self, 'battery_voltage', n.get_int_value()),
            "boxTemperature": lambda n : setattr(self, 'box_temperature', n.get_int_value()),
            "breakSwState": lambda n : setattr(self, 'break_sw_state', n.get_int_value()),
            "cpuTemperature": lambda n : setattr(self, 'cpu_temperature', n.get_int_value()),
            "cpuUsage": lambda n : setattr(self, 'cpu_usage', n.get_int_value()),
            "desc": lambda n : setattr(self, 'desc', n.get_str_value()),
            "deviceId": lambda n : setattr(self, 'device_id', n.get_int_value()),
            "diskUsage": lambda n : setattr(self, 'disk_usage', n.get_int_value()),
            "hardwareErrorCode": lambda n : setattr(self, 'hardware_error_code', n.get_int_value()),
            "hostPort": lambda n : setattr(self, 'host_port', n.get_str_value()),
            "hstate": lambda n : setattr(self, 'hstate', n.get_int_value()),
            "m1StatusCode": lambda n : setattr(self, 'm1_status_code', n.get_int_value()),
            "m2StatusCode": lambda n : setattr(self, 'm2_status_code', n.get_int_value()),
            "m3StatusCode": lambda n : setattr(self, 'm3_status_code', n.get_int_value()),
            "m4StatusCode": lambda n : setattr(self, 'm4_status_code', n.get_int_value()),
            "memoryUsage": lambda n : setattr(self, 'memory_usage', n.get_int_value()),
            "modelVersion": lambda n : setattr(self, 'model_version', n.get_str_value()),
            "nodeType": lambda n : setattr(self, 'node_type', n.get_int_value()),
            "powerState": lambda n : setattr(self, 'power_state', n.get_int_value()),
            "remainDiskSpace": lambda n : setattr(self, 'remain_disk_space', n.get_int_value()),
            "totalMileage": lambda n : setattr(self, 'total_mileage', n.get_int_value()),
            "totalPowerCycle": lambda n : setattr(self, 'total_power_cycle', n.get_int_value()),
            "totalPoweronTime": lambda n : setattr(self, 'total_poweron_time', n.get_int_value()),
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
        writer.write_int_value("batteryCurrent", self.battery_current)
        writer.write_int_value("batteryPercentage", self.battery_percentage)
        writer.write_int_value("batteryState", self.battery_state)
        writer.write_int_value("batteryTemperature", self.battery_temperature)
        writer.write_int_value("batteryUseCycles", self.battery_use_cycles)
        writer.write_int_value("batteryVoltage", self.battery_voltage)
        writer.write_int_value("boxTemperature", self.box_temperature)
        writer.write_int_value("breakSwState", self.break_sw_state)
        writer.write_int_value("cpuTemperature", self.cpu_temperature)
        writer.write_int_value("cpuUsage", self.cpu_usage)
        writer.write_str_value("desc", self.desc)
        writer.write_int_value("deviceId", self.device_id)
        writer.write_int_value("diskUsage", self.disk_usage)
        writer.write_int_value("hardwareErrorCode", self.hardware_error_code)
        writer.write_str_value("hostPort", self.host_port)
        writer.write_int_value("hstate", self.hstate)
        writer.write_int_value("m1StatusCode", self.m1_status_code)
        writer.write_int_value("m2StatusCode", self.m2_status_code)
        writer.write_int_value("m3StatusCode", self.m3_status_code)
        writer.write_int_value("m4StatusCode", self.m4_status_code)
        writer.write_int_value("memoryUsage", self.memory_usage)
        writer.write_str_value("modelVersion", self.model_version)
        writer.write_int_value("nodeType", self.node_type)
        writer.write_int_value("powerState", self.power_state)
        writer.write_int_value("remainDiskSpace", self.remain_disk_space)
        writer.write_int_value("totalMileage", self.total_mileage)
        writer.write_int_value("totalPowerCycle", self.total_power_cycle)
        writer.write_int_value("totalPoweronTime", self.total_poweron_time)
        writer.write_additional_data_value(self.additional_data)
    

