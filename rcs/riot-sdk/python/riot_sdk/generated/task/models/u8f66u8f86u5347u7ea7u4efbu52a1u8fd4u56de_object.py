from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class U8f66u8f86u5347u7ea7u4efbu52a1u8fd4u56deObject(AdditionalDataHolder, Parsable):
    """
    车辆升级任务返回对象
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 当前版本
    cur_file_name: Optional[str] = None
    # 车辆唯一标识
    device_key: Optional[str] = None
    # 车辆名称
    device_name: Optional[str] = None
    # 上一个版本
    last_file_name: Optional[str] = None
    # 车辆型号
    model: Optional[str] = None
    # 车辆系列
    series: Optional[str] = None
    # 更新时间
    update_time: Optional[datetime.datetime] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> U8f66u8f86u5347u7ea7u4efbu52a1u8fd4u56deObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: U8f66u8f86u5347u7ea7u4efbu52a1u8fd4u56deObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return U8f66u8f86u5347u7ea7u4efbu52a1u8fd4u56deObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "curFileName": lambda n : setattr(self, 'cur_file_name', n.get_str_value()),
            "deviceKey": lambda n : setattr(self, 'device_key', n.get_str_value()),
            "deviceName": lambda n : setattr(self, 'device_name', n.get_str_value()),
            "lastFileName": lambda n : setattr(self, 'last_file_name', n.get_str_value()),
            "model": lambda n : setattr(self, 'model', n.get_str_value()),
            "series": lambda n : setattr(self, 'series', n.get_str_value()),
            "updateTime": lambda n : setattr(self, 'update_time', n.get_datetime_value()),
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
        writer.write_str_value("curFileName", self.cur_file_name)
        writer.write_str_value("deviceKey", self.device_key)
        writer.write_str_value("deviceName", self.device_name)
        writer.write_str_value("lastFileName", self.last_file_name)
        writer.write_str_value("model", self.model)
        writer.write_str_value("series", self.series)
        writer.write_datetime_value("updateTime", self.update_time)
        writer.write_additional_data_value(self.additional_data)
    

