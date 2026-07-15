from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .u8f66u8f86u540cu6b65u4efbu52a1_status import U8f66u8f86u540cu6b65u4efbu52a1_status
    from .u8f66u8f86u540cu6b65u4efbu52a1_type import U8f66u8f86u540cu6b65u4efbu52a1_type

@dataclass
class U8f66u8f86u540cu6b65u4efbu52a1(AdditionalDataHolder, Parsable):
    """
    车辆同步任务
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 创建人
    create_by: Optional[int] = None
    # 是否删除
    deleted: Optional[bool] = None
    # 车辆唯一标识
    device_key: Optional[str] = None
    # 车辆名称
    device_name: Optional[str] = None
    # 任务结束时间
    end_time: Optional[datetime.datetime] = None
    # 文件名
    file_name: Optional[str] = None
    # 记录生成时间
    gmt_create: Optional[datetime.datetime] = None
    # 更新时间
    gmt_modified: Optional[datetime.datetime] = None
    # 自增id
    id: Optional[int] = None
    # 上一次文件名
    last_file_name: Optional[str] = None
    # 进度
    progress: Optional[int] = None
    # 任务执行结果描述
    result_detail: Optional[str] = None
    # 任务开始时间
    start_time: Optional[datetime.datetime] = None
    # 任务状态
    status: Optional[U8f66u8f86u540cu6b65u4efbu52a1_status] = None
    # 任务类型
    type: Optional[U8f66u8f86u540cu6b65u4efbu52a1_type] = None
    # 更新人
    update_by: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> U8f66u8f86u540cu6b65u4efbu52a1:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: U8f66u8f86u540cu6b65u4efbu52a1
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return U8f66u8f86u540cu6b65u4efbu52a1()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .u8f66u8f86u540cu6b65u4efbu52a1_status import U8f66u8f86u540cu6b65u4efbu52a1_status
        from .u8f66u8f86u540cu6b65u4efbu52a1_type import U8f66u8f86u540cu6b65u4efbu52a1_type

        from .u8f66u8f86u540cu6b65u4efbu52a1_status import U8f66u8f86u540cu6b65u4efbu52a1_status
        from .u8f66u8f86u540cu6b65u4efbu52a1_type import U8f66u8f86u540cu6b65u4efbu52a1_type

        fields: dict[str, Callable[[Any], None]] = {
            "createBy": lambda n : setattr(self, 'create_by', n.get_int_value()),
            "deleted": lambda n : setattr(self, 'deleted', n.get_bool_value()),
            "deviceKey": lambda n : setattr(self, 'device_key', n.get_str_value()),
            "deviceName": lambda n : setattr(self, 'device_name', n.get_str_value()),
            "endTime": lambda n : setattr(self, 'end_time', n.get_datetime_value()),
            "fileName": lambda n : setattr(self, 'file_name', n.get_str_value()),
            "gmtCreate": lambda n : setattr(self, 'gmt_create', n.get_datetime_value()),
            "gmtModified": lambda n : setattr(self, 'gmt_modified', n.get_datetime_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "lastFileName": lambda n : setattr(self, 'last_file_name', n.get_str_value()),
            "progress": lambda n : setattr(self, 'progress', n.get_int_value()),
            "resultDetail": lambda n : setattr(self, 'result_detail', n.get_str_value()),
            "startTime": lambda n : setattr(self, 'start_time', n.get_datetime_value()),
            "status": lambda n : setattr(self, 'status', n.get_enum_value(U8f66u8f86u540cu6b65u4efbu52a1_status)),
            "type": lambda n : setattr(self, 'type', n.get_enum_value(U8f66u8f86u540cu6b65u4efbu52a1_type)),
            "updateBy": lambda n : setattr(self, 'update_by', n.get_int_value()),
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
        writer.write_int_value("createBy", self.create_by)
        writer.write_bool_value("deleted", self.deleted)
        writer.write_str_value("deviceKey", self.device_key)
        writer.write_str_value("deviceName", self.device_name)
        writer.write_datetime_value("endTime", self.end_time)
        writer.write_str_value("fileName", self.file_name)
        writer.write_datetime_value("gmtCreate", self.gmt_create)
        writer.write_datetime_value("gmtModified", self.gmt_modified)
        writer.write_int_value("id", self.id)
        writer.write_str_value("lastFileName", self.last_file_name)
        writer.write_int_value("progress", self.progress)
        writer.write_str_value("resultDetail", self.result_detail)
        writer.write_datetime_value("startTime", self.start_time)
        writer.write_enum_value("status", self.status)
        writer.write_enum_value("type", self.type)
        writer.write_int_value("updateBy", self.update_by)
        writer.write_additional_data_value(self.additional_data)
    

