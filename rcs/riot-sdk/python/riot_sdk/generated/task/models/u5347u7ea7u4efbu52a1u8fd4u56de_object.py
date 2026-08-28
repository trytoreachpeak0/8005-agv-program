from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class U5347u7ea7u4efbu52a1u8fd4u56deObject(AdditionalDataHolder, Parsable):
    """
    升级任务返回对象
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 完成所用时间
    cost_time: Optional[int] = None
    # 操作用户
    create_by: Optional[int] = None
    # 车辆名称
    device_name: Optional[str] = None
    # 完成时间
    end_time: Optional[str] = None
    # 文件名
    file_name: Optional[str] = None
    # 进度
    progress: Optional[int] = None
    # 升级结果
    result: Optional[str] = None
    # 说明
    result_detail: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> U5347u7ea7u4efbu52a1u8fd4u56deObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: U5347u7ea7u4efbu52a1u8fd4u56deObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return U5347u7ea7u4efbu52a1u8fd4u56deObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "costTime": lambda n : setattr(self, 'cost_time', n.get_int_value()),
            "createBy": lambda n : setattr(self, 'create_by', n.get_int_value()),
            "deviceName": lambda n : setattr(self, 'device_name', n.get_str_value()),
            "endTime": lambda n : setattr(self, 'end_time', n.get_str_value()),
            "fileName": lambda n : setattr(self, 'file_name', n.get_str_value()),
            "progress": lambda n : setattr(self, 'progress', n.get_int_value()),
            "result": lambda n : setattr(self, 'result', n.get_str_value()),
            "resultDetail": lambda n : setattr(self, 'result_detail', n.get_str_value()),
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
        writer.write_int_value("costTime", self.cost_time)
        writer.write_int_value("createBy", self.create_by)
        writer.write_str_value("deviceName", self.device_name)
        writer.write_str_value("endTime", self.end_time)
        writer.write_str_value("fileName", self.file_name)
        writer.write_int_value("progress", self.progress)
        writer.write_str_value("result", self.result)
        writer.write_str_value("resultDetail", self.result_detail)
        writer.write_additional_data_value(self.additional_data)
    

