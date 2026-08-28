from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .agvu72b6u6001u65f6u957f_agv_statistics_state import Agvu72b6u6001u65f6u957f_agvStatisticsState

@dataclass
class Agvu72b6u6001u65f6u957f(AdditionalDataHolder, Parsable):
    """
    agv状态时长-小时切片
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 车辆状态
    agv_statistics_state: Optional[Agvu72b6u6001u65f6u957f_agvStatisticsState] = None
    # 创建人
    create_by: Optional[int] = None
    # 当前小时
    curr_hour: Optional[datetime.datetime] = None
    # 是否删除
    deleted: Optional[bool] = None
    # 车辆唯一标识
    device_key: Optional[str] = None
    # 车辆名称
    device_name: Optional[str] = None
    # 时长：s
    durations: Optional[int] = None
    # 记录生成时间
    gmt_create: Optional[datetime.datetime] = None
    # 更新时间
    gmt_modified: Optional[datetime.datetime] = None
    # 自增id
    id: Optional[int] = None
    # 更新人
    update_by: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> Agvu72b6u6001u65f6u957f:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: Agvu72b6u6001u65f6u957f
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return Agvu72b6u6001u65f6u957f()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .agvu72b6u6001u65f6u957f_agv_statistics_state import Agvu72b6u6001u65f6u957f_agvStatisticsState

        from .agvu72b6u6001u65f6u957f_agv_statistics_state import Agvu72b6u6001u65f6u957f_agvStatisticsState

        fields: dict[str, Callable[[Any], None]] = {
            "agvStatisticsState": lambda n : setattr(self, 'agv_statistics_state', n.get_enum_value(Agvu72b6u6001u65f6u957f_agvStatisticsState)),
            "createBy": lambda n : setattr(self, 'create_by', n.get_int_value()),
            "currHour": lambda n : setattr(self, 'curr_hour', n.get_datetime_value()),
            "deleted": lambda n : setattr(self, 'deleted', n.get_bool_value()),
            "deviceKey": lambda n : setattr(self, 'device_key', n.get_str_value()),
            "deviceName": lambda n : setattr(self, 'device_name', n.get_str_value()),
            "durations": lambda n : setattr(self, 'durations', n.get_int_value()),
            "gmtCreate": lambda n : setattr(self, 'gmt_create', n.get_datetime_value()),
            "gmtModified": lambda n : setattr(self, 'gmt_modified', n.get_datetime_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
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
        writer.write_enum_value("agvStatisticsState", self.agv_statistics_state)
        writer.write_int_value("createBy", self.create_by)
        writer.write_datetime_value("currHour", self.curr_hour)
        writer.write_bool_value("deleted", self.deleted)
        writer.write_str_value("deviceKey", self.device_key)
        writer.write_str_value("deviceName", self.device_name)
        writer.write_int_value("durations", self.durations)
        writer.write_datetime_value("gmtCreate", self.gmt_create)
        writer.write_datetime_value("gmtModified", self.gmt_modified)
        writer.write_int_value("id", self.id)
        writer.write_int_value("updateBy", self.update_by)
        writer.write_additional_data_value(self.additional_data)
    

