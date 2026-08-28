from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .order_mission_object_extend_params import OrderMissionObject_extendParams

@dataclass
class OrderMissionObject(AdditionalDataHolder, Parsable):
    """
    订单任务表
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 动作类型id
    action_id: Optional[int] = None
    # 动作名称
    action_name: Optional[str] = None
    # 动作参数字符串
    action_param_str: Optional[str] = None
    # 动作参数1
    action_param1: Optional[int] = None
    # 动作参数2
    action_param2: Optional[int] = None
    # 创建时间
    create_time: Optional[datetime.datetime] = None
    # 子任务创建方式:0(外部创建),1(系统自动创建)
    create_type: Optional[int] = None
    # 目的地
    destination: Optional[int] = None
    # 目的地
    destination_name: Optional[str] = None
    # 子任务执行时间
    execute_time: Optional[datetime.datetime] = None
    # 当前任务系列号
    executing_index: Optional[int] = None
    # 拓展参数
    extend_params: Optional[OrderMissionObject_extendParams] = None
    # 子任务执行失败的策略
    fail_strategy: Optional[str] = None
    # 失败策略对应的参数
    fail_value: Optional[str] = None
    # 子任务完成时间
    finish_time: Optional[datetime.datetime] = None
    # 关联物模型定义的动作服务key
    function_key: Optional[str] = None
    # The id property
    id: Optional[int] = None
    # 操作子任务的索引
    index: Optional[int] = None
    # 是否删除
    is_deleted: Optional[int] = None
    # 当前任务车长mm
    length: Optional[int] = None
    # 地图id
    map_id: Optional[int] = None
    # 地图名称
    map_name: Optional[str] = None
    # 0:na，1:执行中，2:完成，3:失败，4:取消
    mission_state: Optional[int] = None
    # 订单id
    order_id: Optional[int] = None
    # 上层系统给每一个子任务定义的唯一id
    order_uuid: Optional[str] = None
    # 子任务执行结果状态
    result_code: Optional[int] = None
    # 子任务执行结果
    result_str: Optional[str] = None
    # 当前任务指定速度m/s
    speed: Optional[float] = None
    # 子任务执行成功的策略
    success_strategy: Optional[str] = None
    # 任务类型
    type: Optional[str] = None
    # 最后更新时间
    update_time: Optional[datetime.datetime] = None
    # 当前任务车宽mm
    width: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> OrderMissionObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: OrderMissionObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return OrderMissionObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .order_mission_object_extend_params import OrderMissionObject_extendParams

        from .order_mission_object_extend_params import OrderMissionObject_extendParams

        fields: dict[str, Callable[[Any], None]] = {
            "actionId": lambda n : setattr(self, 'action_id', n.get_int_value()),
            "actionName": lambda n : setattr(self, 'action_name', n.get_str_value()),
            "actionParamStr": lambda n : setattr(self, 'action_param_str', n.get_str_value()),
            "actionParam1": lambda n : setattr(self, 'action_param1', n.get_int_value()),
            "actionParam2": lambda n : setattr(self, 'action_param2', n.get_int_value()),
            "createTime": lambda n : setattr(self, 'create_time', n.get_datetime_value()),
            "createType": lambda n : setattr(self, 'create_type', n.get_int_value()),
            "destination": lambda n : setattr(self, 'destination', n.get_int_value()),
            "destinationName": lambda n : setattr(self, 'destination_name', n.get_str_value()),
            "executeTime": lambda n : setattr(self, 'execute_time', n.get_datetime_value()),
            "executingIndex": lambda n : setattr(self, 'executing_index', n.get_int_value()),
            "extendParams": lambda n : setattr(self, 'extend_params', n.get_object_value(OrderMissionObject_extendParams)),
            "failStrategy": lambda n : setattr(self, 'fail_strategy', n.get_str_value()),
            "failValue": lambda n : setattr(self, 'fail_value', n.get_str_value()),
            "finishTime": lambda n : setattr(self, 'finish_time', n.get_datetime_value()),
            "functionKey": lambda n : setattr(self, 'function_key', n.get_str_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "index": lambda n : setattr(self, 'index', n.get_int_value()),
            "isDeleted": lambda n : setattr(self, 'is_deleted', n.get_int_value()),
            "length": lambda n : setattr(self, 'length', n.get_int_value()),
            "mapId": lambda n : setattr(self, 'map_id', n.get_int_value()),
            "mapName": lambda n : setattr(self, 'map_name', n.get_str_value()),
            "missionState": lambda n : setattr(self, 'mission_state', n.get_int_value()),
            "orderId": lambda n : setattr(self, 'order_id', n.get_int_value()),
            "orderUuid": lambda n : setattr(self, 'order_uuid', n.get_str_value()),
            "resultCode": lambda n : setattr(self, 'result_code', n.get_int_value()),
            "resultStr": lambda n : setattr(self, 'result_str', n.get_str_value()),
            "speed": lambda n : setattr(self, 'speed', n.get_float_value()),
            "successStrategy": lambda n : setattr(self, 'success_strategy', n.get_str_value()),
            "type": lambda n : setattr(self, 'type', n.get_str_value()),
            "updateTime": lambda n : setattr(self, 'update_time', n.get_datetime_value()),
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
        writer.write_int_value("actionId", self.action_id)
        writer.write_str_value("actionName", self.action_name)
        writer.write_str_value("actionParamStr", self.action_param_str)
        writer.write_int_value("actionParam1", self.action_param1)
        writer.write_int_value("actionParam2", self.action_param2)
        writer.write_datetime_value("createTime", self.create_time)
        writer.write_int_value("createType", self.create_type)
        writer.write_int_value("destination", self.destination)
        writer.write_str_value("destinationName", self.destination_name)
        writer.write_datetime_value("executeTime", self.execute_time)
        writer.write_int_value("executingIndex", self.executing_index)
        writer.write_object_value("extendParams", self.extend_params)
        writer.write_str_value("failStrategy", self.fail_strategy)
        writer.write_str_value("failValue", self.fail_value)
        writer.write_datetime_value("finishTime", self.finish_time)
        writer.write_str_value("functionKey", self.function_key)
        writer.write_int_value("id", self.id)
        writer.write_int_value("index", self.index)
        writer.write_int_value("isDeleted", self.is_deleted)
        writer.write_int_value("length", self.length)
        writer.write_int_value("mapId", self.map_id)
        writer.write_str_value("mapName", self.map_name)
        writer.write_int_value("missionState", self.mission_state)
        writer.write_int_value("orderId", self.order_id)
        writer.write_str_value("orderUuid", self.order_uuid)
        writer.write_int_value("resultCode", self.result_code)
        writer.write_str_value("resultStr", self.result_str)
        writer.write_float_value("speed", self.speed)
        writer.write_str_value("successStrategy", self.success_strategy)
        writer.write_str_value("type", self.type)
        writer.write_datetime_value("updateTime", self.update_time)
        writer.write_int_value("width", self.width)
        writer.write_additional_data_value(self.additional_data)
    

