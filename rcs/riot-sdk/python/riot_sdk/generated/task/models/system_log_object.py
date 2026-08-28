from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class SystemLogObject(AdditionalDataHolder, Parsable):
    """
    系统日志
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 发送时间
    create_time: Optional[datetime.datetime] = None
    # 告警描述
    desc: Optional[str] = None
    # 告警详情,如何处理
    detail: Optional[str] = None
    # 车辆的key
    device_key: Optional[str] = None
    # 车辆的名称
    device_name: Optional[str] = None
    # 错误编码
    error_code: Optional[str] = None
    # 额外参数
    ext_param: Optional[str] = None
    # 处理事件时间
    handler_time: Optional[datetime.datetime] = None
    # 处理用户
    handler_user_id: Optional[int] = None
    # The id property
    id: Optional[int] = None
    # 警告级别:1.严重,2.警告,3.一般,4.致命
    log_level: Optional[int] = None
    # 订单id
    order_id: Optional[str] = None
    # 告警来源:0:机器人,1:订单,2:设备,3:服务器
    source: Optional[int] = None
    # 告警来源:机器人,订单,设备
    source_name: Optional[str] = None
    # 处理状态:0:已读,1:未读
    status: Optional[int] = None
    # 处理状态:已读,未读
    status_name: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> SystemLogObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: SystemLogObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return SystemLogObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "createTime": lambda n : setattr(self, 'create_time', n.get_datetime_value()),
            "desc": lambda n : setattr(self, 'desc', n.get_str_value()),
            "detail": lambda n : setattr(self, 'detail', n.get_str_value()),
            "deviceKey": lambda n : setattr(self, 'device_key', n.get_str_value()),
            "deviceName": lambda n : setattr(self, 'device_name', n.get_str_value()),
            "errorCode": lambda n : setattr(self, 'error_code', n.get_str_value()),
            "extParam": lambda n : setattr(self, 'ext_param', n.get_str_value()),
            "handlerTime": lambda n : setattr(self, 'handler_time', n.get_datetime_value()),
            "handlerUserId": lambda n : setattr(self, 'handler_user_id', n.get_int_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "logLevel": lambda n : setattr(self, 'log_level', n.get_int_value()),
            "orderId": lambda n : setattr(self, 'order_id', n.get_str_value()),
            "source": lambda n : setattr(self, 'source', n.get_int_value()),
            "sourceName": lambda n : setattr(self, 'source_name', n.get_str_value()),
            "status": lambda n : setattr(self, 'status', n.get_int_value()),
            "statusName": lambda n : setattr(self, 'status_name', n.get_str_value()),
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
        writer.write_datetime_value("createTime", self.create_time)
        writer.write_str_value("desc", self.desc)
        writer.write_str_value("detail", self.detail)
        writer.write_str_value("deviceKey", self.device_key)
        writer.write_str_value("deviceName", self.device_name)
        writer.write_str_value("errorCode", self.error_code)
        writer.write_str_value("extParam", self.ext_param)
        writer.write_datetime_value("handlerTime", self.handler_time)
        writer.write_int_value("handlerUserId", self.handler_user_id)
        writer.write_int_value("id", self.id)
        writer.write_int_value("logLevel", self.log_level)
        writer.write_str_value("orderId", self.order_id)
        writer.write_int_value("source", self.source)
        writer.write_str_value("sourceName", self.source_name)
        writer.write_int_value("status", self.status)
        writer.write_str_value("statusName", self.status_name)
        writer.write_additional_data_value(self.additional_data)
    

