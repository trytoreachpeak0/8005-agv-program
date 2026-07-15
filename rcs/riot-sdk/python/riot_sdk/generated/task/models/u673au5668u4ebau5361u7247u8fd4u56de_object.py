from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .pose import Pose
    from .traffic_vehicle import TrafficVehicle
    from .u673au5668u4ebau5361u7247u8fd4u56de_object_mode import U673au5668u4ebau5361u7247u8fd4u56deObject_mode
    from .u673au5668u4ebau5361u7247u8fd4u56de_object_power_mode import U673au5668u4ebau5361u7247u8fd4u56deObject_powerMode
    from .u673au5668u4ebau5361u7247u8fd4u56de_object_task_type import U673au5668u4ebau5361u7247u8fd4u56deObject_taskType

@dataclass
class U673au5668u4ebau5361u7247u8fd4u56deObject(AdditionalDataHolder, Parsable):
    """
    机器人卡片返回对象
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 动作任务名称
    action_name: Optional[str] = None
    # 系统状态上报的动作状态:AT_NA, AT_WAIT_FOR_START, AT_RUNNING, AT_PAUSED, AT_FINISHED, AT_IN_CANCEL, AT_WAIT_FOR_ACK
    action_state: Optional[str] = None
    # 当前电量
    battery: Optional[int] = None
    # 电池充电状态
    battery_state: Optional[str] = None
    # 解抱闸状态
    break_switch_state: Optional[str] = None
    # 定位精度
    confidence: Optional[str] = None
    # 当前地图
    current_map: Optional[str] = None
    # 当前站点
    current_position: Optional[int] = None
    # 机器人描述
    desc: Optional[str] = None
    # id
    device_id: Optional[int] = None
    # 设备 key
    device_key: Optional[str] = None
    # 设备名称
    device_name: Optional[str] = None
    # 急停状态
    emergency_state: Optional[str] = None
    # 车辆启用/禁用
    enable: Optional[bool] = None
    # 车辆启用时间
    enable_time: Optional[str] = None
    # 终站点名
    end_station_name: Optional[str] = None
    # 结束站点编号
    end_station_no: Optional[int] = None
    # 所在车辆组
    existed_in_group: Optional[list[str]] = None
    # IP地址
    host_port: Optional[str] = None
    # 载货状态
    load_state: Optional[int] = None
    # 定位状态
    location_state: Optional[str] = None
    # 车辆是否被订单锁定，1锁定 0未锁定
    lock_status: Optional[int] = None
    # 小车规划的路径资源
    map_resource_ids: Optional[list[str]] = None
    # agv控制模式:自动,手动
    mode: Optional[U673au5668u4ebau5361u7247u8fd4u56deObject_mode] = None
    # 物模型版本
    model_version: Optional[str] = None
    # 机构高度
    module_height: Optional[float] = None
    # 系统状态上报的移动状态
    movement_state: Optional[str] = None
    # 节点类型
    node_type: Optional[int] = None
    # 被交管的车辆
    occupy_devices: Optional[list[TrafficVehicle]] = None
    # 当前任务名字
    order_name: Optional[str] = None
    # 当前任务id
    order_task_id: Optional[str] = None
    # The position property
    position: Optional[Pose] = None
    # 功耗状态
    power_mode: Optional[U673au5668u4ebau5361u7247u8fd4u56deObject_powerMode] = None
    # 运行状态
    proc_state: Optional[str] = None
    # 产品名称
    product_key: Optional[str] = None
    # 订单完成进度
    progress: Optional[int] = None
    # 机器人型号：产品系列.型号
    robot_model: Optional[str] = None
    # 行驶速度
    speed: Optional[float] = None
    # 起站点名
    start_station_name: Optional[str] = None
    # 起始站点编号
    start_station_no: Optional[int] = None
    # 设备上下线状态(对应vehicle中online)
    status: Optional[int] = None
    # The sysState property
    sys_state: Optional[str] = None
    # 订单类型
    task_type: Optional[U673au5668u4ebau5361u7247u8fd4u56deObject_taskType] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> U673au5668u4ebau5361u7247u8fd4u56deObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: U673au5668u4ebau5361u7247u8fd4u56deObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return U673au5668u4ebau5361u7247u8fd4u56deObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .pose import Pose
        from .traffic_vehicle import TrafficVehicle
        from .u673au5668u4ebau5361u7247u8fd4u56de_object_mode import U673au5668u4ebau5361u7247u8fd4u56deObject_mode
        from .u673au5668u4ebau5361u7247u8fd4u56de_object_power_mode import U673au5668u4ebau5361u7247u8fd4u56deObject_powerMode
        from .u673au5668u4ebau5361u7247u8fd4u56de_object_task_type import U673au5668u4ebau5361u7247u8fd4u56deObject_taskType

        from .pose import Pose
        from .traffic_vehicle import TrafficVehicle
        from .u673au5668u4ebau5361u7247u8fd4u56de_object_mode import U673au5668u4ebau5361u7247u8fd4u56deObject_mode
        from .u673au5668u4ebau5361u7247u8fd4u56de_object_power_mode import U673au5668u4ebau5361u7247u8fd4u56deObject_powerMode
        from .u673au5668u4ebau5361u7247u8fd4u56de_object_task_type import U673au5668u4ebau5361u7247u8fd4u56deObject_taskType

        fields: dict[str, Callable[[Any], None]] = {
            "actionName": lambda n : setattr(self, 'action_name', n.get_str_value()),
            "actionState": lambda n : setattr(self, 'action_state', n.get_str_value()),
            "battery": lambda n : setattr(self, 'battery', n.get_int_value()),
            "batteryState": lambda n : setattr(self, 'battery_state', n.get_str_value()),
            "breakSwitchState": lambda n : setattr(self, 'break_switch_state', n.get_str_value()),
            "confidence": lambda n : setattr(self, 'confidence', n.get_str_value()),
            "currentMap": lambda n : setattr(self, 'current_map', n.get_str_value()),
            "currentPosition": lambda n : setattr(self, 'current_position', n.get_int_value()),
            "desc": lambda n : setattr(self, 'desc', n.get_str_value()),
            "deviceId": lambda n : setattr(self, 'device_id', n.get_int_value()),
            "deviceKey": lambda n : setattr(self, 'device_key', n.get_str_value()),
            "deviceName": lambda n : setattr(self, 'device_name', n.get_str_value()),
            "emergencyState": lambda n : setattr(self, 'emergency_state', n.get_str_value()),
            "enable": lambda n : setattr(self, 'enable', n.get_bool_value()),
            "enableTime": lambda n : setattr(self, 'enable_time', n.get_str_value()),
            "endStationName": lambda n : setattr(self, 'end_station_name', n.get_str_value()),
            "endStationNo": lambda n : setattr(self, 'end_station_no', n.get_int_value()),
            "existedInGroup": lambda n : setattr(self, 'existed_in_group', n.get_collection_of_primitive_values(str)),
            "hostPort": lambda n : setattr(self, 'host_port', n.get_str_value()),
            "loadState": lambda n : setattr(self, 'load_state', n.get_int_value()),
            "locationState": lambda n : setattr(self, 'location_state', n.get_str_value()),
            "lockStatus": lambda n : setattr(self, 'lock_status', n.get_int_value()),
            "mapResourceIds": lambda n : setattr(self, 'map_resource_ids', n.get_collection_of_primitive_values(str)),
            "mode": lambda n : setattr(self, 'mode', n.get_enum_value(U673au5668u4ebau5361u7247u8fd4u56deObject_mode)),
            "modelVersion": lambda n : setattr(self, 'model_version', n.get_str_value()),
            "moduleHeight": lambda n : setattr(self, 'module_height', n.get_float_value()),
            "movementState": lambda n : setattr(self, 'movement_state', n.get_str_value()),
            "nodeType": lambda n : setattr(self, 'node_type', n.get_int_value()),
            "occupyDevices": lambda n : setattr(self, 'occupy_devices', n.get_collection_of_object_values(TrafficVehicle)),
            "orderName": lambda n : setattr(self, 'order_name', n.get_str_value()),
            "orderTaskId": lambda n : setattr(self, 'order_task_id', n.get_str_value()),
            "position": lambda n : setattr(self, 'position', n.get_object_value(Pose)),
            "powerMode": lambda n : setattr(self, 'power_mode', n.get_enum_value(U673au5668u4ebau5361u7247u8fd4u56deObject_powerMode)),
            "procState": lambda n : setattr(self, 'proc_state', n.get_str_value()),
            "productKey": lambda n : setattr(self, 'product_key', n.get_str_value()),
            "progress": lambda n : setattr(self, 'progress', n.get_int_value()),
            "robotModel": lambda n : setattr(self, 'robot_model', n.get_str_value()),
            "speed": lambda n : setattr(self, 'speed', n.get_float_value()),
            "startStationName": lambda n : setattr(self, 'start_station_name', n.get_str_value()),
            "startStationNo": lambda n : setattr(self, 'start_station_no', n.get_int_value()),
            "status": lambda n : setattr(self, 'status', n.get_int_value()),
            "sysState": lambda n : setattr(self, 'sys_state', n.get_str_value()),
            "taskType": lambda n : setattr(self, 'task_type', n.get_enum_value(U673au5668u4ebau5361u7247u8fd4u56deObject_taskType)),
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
        writer.write_str_value("actionName", self.action_name)
        writer.write_str_value("actionState", self.action_state)
        writer.write_int_value("battery", self.battery)
        writer.write_str_value("batteryState", self.battery_state)
        writer.write_str_value("breakSwitchState", self.break_switch_state)
        writer.write_str_value("confidence", self.confidence)
        writer.write_str_value("currentMap", self.current_map)
        writer.write_int_value("currentPosition", self.current_position)
        writer.write_str_value("desc", self.desc)
        writer.write_int_value("deviceId", self.device_id)
        writer.write_str_value("deviceKey", self.device_key)
        writer.write_str_value("deviceName", self.device_name)
        writer.write_str_value("emergencyState", self.emergency_state)
        writer.write_bool_value("enable", self.enable)
        writer.write_str_value("enableTime", self.enable_time)
        writer.write_str_value("endStationName", self.end_station_name)
        writer.write_int_value("endStationNo", self.end_station_no)
        writer.write_collection_of_primitive_values("existedInGroup", self.existed_in_group)
        writer.write_str_value("hostPort", self.host_port)
        writer.write_int_value("loadState", self.load_state)
        writer.write_str_value("locationState", self.location_state)
        writer.write_int_value("lockStatus", self.lock_status)
        writer.write_collection_of_primitive_values("mapResourceIds", self.map_resource_ids)
        writer.write_enum_value("mode", self.mode)
        writer.write_str_value("modelVersion", self.model_version)
        writer.write_float_value("moduleHeight", self.module_height)
        writer.write_str_value("movementState", self.movement_state)
        writer.write_int_value("nodeType", self.node_type)
        writer.write_collection_of_object_values("occupyDevices", self.occupy_devices)
        writer.write_str_value("orderName", self.order_name)
        writer.write_str_value("orderTaskId", self.order_task_id)
        writer.write_object_value("position", self.position)
        writer.write_enum_value("powerMode", self.power_mode)
        writer.write_str_value("procState", self.proc_state)
        writer.write_str_value("productKey", self.product_key)
        writer.write_int_value("progress", self.progress)
        writer.write_str_value("robotModel", self.robot_model)
        writer.write_float_value("speed", self.speed)
        writer.write_str_value("startStationName", self.start_station_name)
        writer.write_int_value("startStationNo", self.start_station_no)
        writer.write_int_value("status", self.status)
        writer.write_str_value("sysState", self.sys_state)
        writer.write_enum_value("taskType", self.task_type)
        writer.write_additional_data_value(self.additional_data)
    

