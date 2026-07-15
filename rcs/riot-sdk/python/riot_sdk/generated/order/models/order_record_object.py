from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .order_mission_object import OrderMissionObject

@dataclass
class OrderRecordObject(AdditionalDataHolder, Parsable):
    """
    订单表
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 预约指定执行时间
    appoint_execute_time: Optional[datetime.datetime] = None
    # 预约指定指定地图id
    appoint_map_id: Optional[int] = None
    # 预约指定指定地图站点id
    appoint_station_id: Optional[int] = None
    # 预约指定车型组id
    appoint_vehicle_group_id: Optional[int] = None
    # 预约指定车型组名
    appoint_vehicle_group_name: Optional[str] = None
    # 预约指定车辆id
    appoint_vehicle_key: Optional[str] = None
    # 预计到达下一站时间(s)
    arrive_time: Optional[int] = None
    # 预计到达下一站时间
    arrive_time_msg: Optional[str] = None
    # 订单是否处于换车中:0:否,1:是
    change_vehicle: Optional[int] = None
    # 订单切换车辆原因
    change_vehicle_reason: Optional[str] = None
    # 订单切换车辆记录
    change_vehicle_record: Optional[str] = None
    # 创建时间
    create_time: Optional[datetime.datetime] = None
    # 创建用户
    created_by: Optional[str] = None
    # 实时距离mm
    distance: Optional[int] = None
    # 完成时间
    done_time: Optional[datetime.datetime] = None
    # 终站点名
    end_station_name: Optional[str] = None
    # 结束站点编号
    end_station_no: Optional[int] = None
    # 剩余时间s
    eta: Optional[int] = None
    # 执行时间
    execute_time: Optional[datetime.datetime] = None
    # 执行车辆id
    execute_vehicle_key: Optional[str] = None
    # 执行车辆名
    execute_vehicle_name: Optional[str] = None
    # 任务执行序号
    executing_index: Optional[int] = None
    # 任务失败原因
    fail_reason: Optional[str] = None
    # The id property
    id: Optional[int] = None
    # 是否支持预约
    is_appoint_enable: Optional[int] = None
    # 是否删除
    is_deleted: Optional[int] = None
    # The lockStatus property
    lock_status: Optional[int] = None
    # The lockVehicleKey property
    lock_vehicle_key: Optional[str] = None
    # 订单子任务
    missions: Optional[list[OrderMissionObject]] = None
    # 编辑用户
    modified_by: Optional[str] = None
    # 订单id,riot全局唯一
    order_id: Optional[str] = None
    # 订单名称
    order_name: Optional[str] = None
    # 订单状态 1 QUEUEING 队列中 , 2 CANCELLED 已取消, 3 EXECUTING 执行中, 4 FAILED 已失败, 5 SUCCESS 已完成, 6 DELETED  已删除, 7 PAUSED已暂停 ,8 SUSPENDED 已移除, 9 HANG 已挂起, 10 队列优先执行
    order_state: Optional[int] = None
    # 订单标签
    order_tag: Optional[str] = None
    # 订单类型 1 NORMAL 工作订单, 2 CHARGE 充电订单 , 3 CMD 停靠订单 4 MAINTAIN 电池保养
    order_type: Optional[int] = None
    # 优先级 0 低优先级 1 中优先级 2 高优先级 3 最高优先级
    priority: Optional[int] = None
    # 是否是队列中优先级:0:否,1:是
    priority_queue: Optional[int] = None
    # 进度
    progress: Optional[int] = None
    # 订单来源 1 FMS, 2 WMS, 3 CALLS, 4 UI
    source: Optional[str] = None
    # 起点>终点
    start_end_station_name: Optional[str] = None
    # 起点>终点详情
    start_end_station_name_detail: Optional[str] = None
    # 起站点名
    start_station_name: Optional[str] = None
    # 起始站点编号
    start_station_no: Optional[int] = None
    # 任务状态
    task_state: Optional[str] = None
    # 总消耗
    total_costs: Optional[int] = None
    # 最后更新时间
    update_time: Optional[datetime.datetime] = None
    # 上层系统订单唯一ID
    upper_id: Optional[str] = None
    # 操作用户id
    user_id: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> OrderRecordObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: OrderRecordObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return OrderRecordObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .order_mission_object import OrderMissionObject

        from .order_mission_object import OrderMissionObject

        fields: dict[str, Callable[[Any], None]] = {
            "appointExecuteTime": lambda n : setattr(self, 'appoint_execute_time', n.get_datetime_value()),
            "appointMapId": lambda n : setattr(self, 'appoint_map_id', n.get_int_value()),
            "appointStationId": lambda n : setattr(self, 'appoint_station_id', n.get_int_value()),
            "appointVehicleGroupId": lambda n : setattr(self, 'appoint_vehicle_group_id', n.get_int_value()),
            "appointVehicleGroupName": lambda n : setattr(self, 'appoint_vehicle_group_name', n.get_str_value()),
            "appointVehicleKey": lambda n : setattr(self, 'appoint_vehicle_key', n.get_str_value()),
            "arriveTime": lambda n : setattr(self, 'arrive_time', n.get_int_value()),
            "arriveTimeMsg": lambda n : setattr(self, 'arrive_time_msg', n.get_str_value()),
            "changeVehicle": lambda n : setattr(self, 'change_vehicle', n.get_int_value()),
            "changeVehicleReason": lambda n : setattr(self, 'change_vehicle_reason', n.get_str_value()),
            "changeVehicleRecord": lambda n : setattr(self, 'change_vehicle_record', n.get_str_value()),
            "createTime": lambda n : setattr(self, 'create_time', n.get_datetime_value()),
            "createdBy": lambda n : setattr(self, 'created_by', n.get_str_value()),
            "distance": lambda n : setattr(self, 'distance', n.get_int_value()),
            "doneTime": lambda n : setattr(self, 'done_time', n.get_datetime_value()),
            "endStationName": lambda n : setattr(self, 'end_station_name', n.get_str_value()),
            "endStationNo": lambda n : setattr(self, 'end_station_no', n.get_int_value()),
            "eta": lambda n : setattr(self, 'eta', n.get_int_value()),
            "executeTime": lambda n : setattr(self, 'execute_time', n.get_datetime_value()),
            "executeVehicleKey": lambda n : setattr(self, 'execute_vehicle_key', n.get_str_value()),
            "executeVehicleName": lambda n : setattr(self, 'execute_vehicle_name', n.get_str_value()),
            "executingIndex": lambda n : setattr(self, 'executing_index', n.get_int_value()),
            "failReason": lambda n : setattr(self, 'fail_reason', n.get_str_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "isAppointEnable": lambda n : setattr(self, 'is_appoint_enable', n.get_int_value()),
            "isDeleted": lambda n : setattr(self, 'is_deleted', n.get_int_value()),
            "lockStatus": lambda n : setattr(self, 'lock_status', n.get_int_value()),
            "lockVehicleKey": lambda n : setattr(self, 'lock_vehicle_key', n.get_str_value()),
            "missions": lambda n : setattr(self, 'missions', n.get_collection_of_object_values(OrderMissionObject)),
            "modifiedBy": lambda n : setattr(self, 'modified_by', n.get_str_value()),
            "orderId": lambda n : setattr(self, 'order_id', n.get_str_value()),
            "orderName": lambda n : setattr(self, 'order_name', n.get_str_value()),
            "orderState": lambda n : setattr(self, 'order_state', n.get_int_value()),
            "orderTag": lambda n : setattr(self, 'order_tag', n.get_str_value()),
            "orderType": lambda n : setattr(self, 'order_type', n.get_int_value()),
            "priority": lambda n : setattr(self, 'priority', n.get_int_value()),
            "priorityQueue": lambda n : setattr(self, 'priority_queue', n.get_int_value()),
            "progress": lambda n : setattr(self, 'progress', n.get_int_value()),
            "source": lambda n : setattr(self, 'source', n.get_str_value()),
            "startEndStationName": lambda n : setattr(self, 'start_end_station_name', n.get_str_value()),
            "startEndStationNameDetail": lambda n : setattr(self, 'start_end_station_name_detail', n.get_str_value()),
            "startStationName": lambda n : setattr(self, 'start_station_name', n.get_str_value()),
            "startStationNo": lambda n : setattr(self, 'start_station_no', n.get_int_value()),
            "taskState": lambda n : setattr(self, 'task_state', n.get_str_value()),
            "totalCosts": lambda n : setattr(self, 'total_costs', n.get_int_value()),
            "updateTime": lambda n : setattr(self, 'update_time', n.get_datetime_value()),
            "upperId": lambda n : setattr(self, 'upper_id', n.get_str_value()),
            "userId": lambda n : setattr(self, 'user_id', n.get_int_value()),
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
        writer.write_datetime_value("appointExecuteTime", self.appoint_execute_time)
        writer.write_int_value("appointMapId", self.appoint_map_id)
        writer.write_int_value("appointStationId", self.appoint_station_id)
        writer.write_int_value("appointVehicleGroupId", self.appoint_vehicle_group_id)
        writer.write_str_value("appointVehicleGroupName", self.appoint_vehicle_group_name)
        writer.write_str_value("appointVehicleKey", self.appoint_vehicle_key)
        writer.write_int_value("arriveTime", self.arrive_time)
        writer.write_str_value("arriveTimeMsg", self.arrive_time_msg)
        writer.write_int_value("changeVehicle", self.change_vehicle)
        writer.write_str_value("changeVehicleReason", self.change_vehicle_reason)
        writer.write_str_value("changeVehicleRecord", self.change_vehicle_record)
        writer.write_datetime_value("createTime", self.create_time)
        writer.write_str_value("createdBy", self.created_by)
        writer.write_int_value("distance", self.distance)
        writer.write_datetime_value("doneTime", self.done_time)
        writer.write_str_value("endStationName", self.end_station_name)
        writer.write_int_value("endStationNo", self.end_station_no)
        writer.write_int_value("eta", self.eta)
        writer.write_datetime_value("executeTime", self.execute_time)
        writer.write_str_value("executeVehicleKey", self.execute_vehicle_key)
        writer.write_str_value("executeVehicleName", self.execute_vehicle_name)
        writer.write_int_value("executingIndex", self.executing_index)
        writer.write_str_value("failReason", self.fail_reason)
        writer.write_int_value("id", self.id)
        writer.write_int_value("isAppointEnable", self.is_appoint_enable)
        writer.write_int_value("isDeleted", self.is_deleted)
        writer.write_int_value("lockStatus", self.lock_status)
        writer.write_str_value("lockVehicleKey", self.lock_vehicle_key)
        writer.write_collection_of_object_values("missions", self.missions)
        writer.write_str_value("modifiedBy", self.modified_by)
        writer.write_str_value("orderId", self.order_id)
        writer.write_str_value("orderName", self.order_name)
        writer.write_int_value("orderState", self.order_state)
        writer.write_str_value("orderTag", self.order_tag)
        writer.write_int_value("orderType", self.order_type)
        writer.write_int_value("priority", self.priority)
        writer.write_int_value("priorityQueue", self.priority_queue)
        writer.write_int_value("progress", self.progress)
        writer.write_str_value("source", self.source)
        writer.write_str_value("startEndStationName", self.start_end_station_name)
        writer.write_str_value("startEndStationNameDetail", self.start_end_station_name_detail)
        writer.write_str_value("startStationName", self.start_station_name)
        writer.write_int_value("startStationNo", self.start_station_no)
        writer.write_str_value("taskState", self.task_state)
        writer.write_int_value("totalCosts", self.total_costs)
        writer.write_datetime_value("updateTime", self.update_time)
        writer.write_str_value("upperId", self.upper_id)
        writer.write_int_value("userId", self.user_id)
        writer.write_additional_data_value(self.additional_data)
    

