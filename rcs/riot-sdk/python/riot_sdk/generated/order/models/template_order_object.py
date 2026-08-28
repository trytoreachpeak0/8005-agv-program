from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .template_order_mission_object import TemplateOrderMissionObject

@dataclass
class TemplateOrderObject(AdditionalDataHolder, Parsable):
    """
    模板管理-订单模板表
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 子用户Id集合
    account_ids: Optional[list[int]] = None
    # 预约指定执行时间
    appoint_execute_time: Optional[datetime.datetime] = None
    # 预约车辆组Id
    appoint_vehicle_group_id: Optional[int] = None
    # 预约车辆id
    appoint_vehicle_key: Optional[str] = None
    # 创建用户
    created_by: Optional[str] = None
    # 创建时间
    gmt_create: Optional[datetime.datetime] = None
    # 最后更新时间
    gmt_modified: Optional[datetime.datetime] = None
    # 自增id
    id: Optional[int] = None
    # 是否支持预约
    is_appoint_enable: Optional[int] = None
    # 删除标识:0:未删除,1:已删除
    is_deleted: Optional[int] = None
    # 订单模板子任务
    missions: Optional[list[TemplateOrderMissionObject]] = None
    # 编辑用户
    modified_by: Optional[str] = None
    # 订单优先级:0:低优先级,1:中优先级,2:高优先级,3:最高优先级
    priority: Optional[int] = None
    # 模板名称
    template_name: Optional[str] = None
    # 订单模板标签Id集合
    template_order_tag_ids: Optional[list[int]] = None
    # 创建用户id
    user_id: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> TemplateOrderObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: TemplateOrderObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return TemplateOrderObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .template_order_mission_object import TemplateOrderMissionObject

        from .template_order_mission_object import TemplateOrderMissionObject

        fields: dict[str, Callable[[Any], None]] = {
            "accountIds": lambda n : setattr(self, 'account_ids', n.get_collection_of_primitive_values(int)),
            "appointExecuteTime": lambda n : setattr(self, 'appoint_execute_time', n.get_datetime_value()),
            "appointVehicleGroupId": lambda n : setattr(self, 'appoint_vehicle_group_id', n.get_int_value()),
            "appointVehicleKey": lambda n : setattr(self, 'appoint_vehicle_key', n.get_str_value()),
            "createdBy": lambda n : setattr(self, 'created_by', n.get_str_value()),
            "gmtCreate": lambda n : setattr(self, 'gmt_create', n.get_datetime_value()),
            "gmtModified": lambda n : setattr(self, 'gmt_modified', n.get_datetime_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "isAppointEnable": lambda n : setattr(self, 'is_appoint_enable', n.get_int_value()),
            "isDeleted": lambda n : setattr(self, 'is_deleted', n.get_int_value()),
            "missions": lambda n : setattr(self, 'missions', n.get_collection_of_object_values(TemplateOrderMissionObject)),
            "modifiedBy": lambda n : setattr(self, 'modified_by', n.get_str_value()),
            "priority": lambda n : setattr(self, 'priority', n.get_int_value()),
            "templateName": lambda n : setattr(self, 'template_name', n.get_str_value()),
            "templateOrderTagIds": lambda n : setattr(self, 'template_order_tag_ids', n.get_collection_of_primitive_values(int)),
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
        writer.write_collection_of_primitive_values("accountIds", self.account_ids)
        writer.write_datetime_value("appointExecuteTime", self.appoint_execute_time)
        writer.write_int_value("appointVehicleGroupId", self.appoint_vehicle_group_id)
        writer.write_str_value("appointVehicleKey", self.appoint_vehicle_key)
        writer.write_str_value("createdBy", self.created_by)
        writer.write_datetime_value("gmtCreate", self.gmt_create)
        writer.write_datetime_value("gmtModified", self.gmt_modified)
        writer.write_int_value("id", self.id)
        writer.write_int_value("isAppointEnable", self.is_appoint_enable)
        writer.write_int_value("isDeleted", self.is_deleted)
        writer.write_collection_of_object_values("missions", self.missions)
        writer.write_str_value("modifiedBy", self.modified_by)
        writer.write_int_value("priority", self.priority)
        writer.write_str_value("templateName", self.template_name)
        writer.write_collection_of_primitive_values("templateOrderTagIds", self.template_order_tag_ids)
        writer.write_int_value("userId", self.user_id)
        writer.write_additional_data_value(self.additional_data)
    

