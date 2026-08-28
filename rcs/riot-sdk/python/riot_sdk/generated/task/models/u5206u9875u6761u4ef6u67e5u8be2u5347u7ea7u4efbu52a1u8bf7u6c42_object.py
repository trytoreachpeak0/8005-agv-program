from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class U5206u9875u6761u4ef6u67e5u8be2u5347u7ea7u4efbu52a1u8bf7u6c42Object(AdditionalDataHolder, Parsable):
    """
    分页条件查询升级任务请求对象
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 结束时间(yyyy-MM-dd HH:mm:ss)
    end_time: Optional[str] = None
    # 升级版本
    file_name: Optional[str] = None
    # 页码
    page_num: Optional[int] = None
    # 页尺寸(page:1,size:-1查询所有)
    page_size: Optional[int] = None
    # 开始时间(yyyy-MM-dd HH:mm:ss)
    start_time: Optional[str] = None
    # success:成功，failed：失败 ;不传默认查所有
    status: Optional[str] = None
    # 任务类型(SROS_SYNC，SRC_SYNC)
    vehicle_sync_task_type: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> U5206u9875u6761u4ef6u67e5u8be2u5347u7ea7u4efbu52a1u8bf7u6c42Object:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: U5206u9875u6761u4ef6u67e5u8be2u5347u7ea7u4efbu52a1u8bf7u6c42Object
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return U5206u9875u6761u4ef6u67e5u8be2u5347u7ea7u4efbu52a1u8bf7u6c42Object()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "endTime": lambda n : setattr(self, 'end_time', n.get_str_value()),
            "fileName": lambda n : setattr(self, 'file_name', n.get_str_value()),
            "pageNum": lambda n : setattr(self, 'page_num', n.get_int_value()),
            "pageSize": lambda n : setattr(self, 'page_size', n.get_int_value()),
            "startTime": lambda n : setattr(self, 'start_time', n.get_str_value()),
            "status": lambda n : setattr(self, 'status', n.get_str_value()),
            "vehicleSyncTaskType": lambda n : setattr(self, 'vehicle_sync_task_type', n.get_str_value()),
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
        writer.write_str_value("endTime", self.end_time)
        writer.write_str_value("fileName", self.file_name)
        writer.write_int_value("pageNum", self.page_num)
        writer.write_int_value("pageSize", self.page_size)
        writer.write_str_value("startTime", self.start_time)
        writer.write_str_value("status", self.status)
        writer.write_str_value("vehicleSyncTaskType", self.vehicle_sync_task_type)
        writer.write_additional_data_value(self.additional_data)
    

