from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .order_group_object_template_order_maps import OrderGroupObject_templateOrderMaps

@dataclass
class OrderGroupObject(AdditionalDataHolder, Parsable):
    """
    订单组合关系表
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 预约指定执行时间
    appoint_execute_time: Optional[datetime.datetime] = None
    # 预约指定车型组id
    appoint_vehicle_group_id: Optional[int] = None
    # 预约指定车辆id
    appoint_vehicle_key: Optional[str] = None
    # 创建用户
    created_by: Optional[str] = None
    # 创建时间
    gmt_create: Optional[datetime.datetime] = None
    # 最后更新时间
    gmt_modified: Optional[datetime.datetime] = None
    # The id property
    id: Optional[int] = None
    # 是否支持预约
    is_appoint_enable: Optional[int] = None
    # The isDeleted property
    is_deleted: Optional[int] = None
    # 编辑用户
    modified_by: Optional[str] = None
    # 订单组合名称
    order_group_name: Optional[str] = None
    # 原始的订单模板id
    original_template_order_id: Optional[str] = None
    # 订单组合优先级:0:低优先级,1:中优先级,2:高优先级,3:最高优先级
    priority: Optional[int] = None
    # 订单模板Id集合
    template_order_ids: Optional[list[int]] = None
    # 订单模板map
    template_order_maps: Optional[OrderGroupObject_templateOrderMaps] = None
    # 创建用户
    user_id: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> OrderGroupObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: OrderGroupObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return OrderGroupObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .order_group_object_template_order_maps import OrderGroupObject_templateOrderMaps

        from .order_group_object_template_order_maps import OrderGroupObject_templateOrderMaps

        fields: dict[str, Callable[[Any], None]] = {
            "appointExecuteTime": lambda n : setattr(self, 'appoint_execute_time', n.get_datetime_value()),
            "appointVehicleGroupId": lambda n : setattr(self, 'appoint_vehicle_group_id', n.get_int_value()),
            "appointVehicleKey": lambda n : setattr(self, 'appoint_vehicle_key', n.get_str_value()),
            "createdBy": lambda n : setattr(self, 'created_by', n.get_str_value()),
            "gmtCreate": lambda n : setattr(self, 'gmt_create', n.get_datetime_value()),
            "gmtModified": lambda n : setattr(self, 'gmt_modified', n.get_datetime_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "isAppointEnable": lambda n : setattr(self, 'is_appoint_enable', n.get_int_value()),
            "isDeleted": lambda n : setattr(self, 'is_deleted', n.get_int_value()),
            "modifiedBy": lambda n : setattr(self, 'modified_by', n.get_str_value()),
            "orderGroupName": lambda n : setattr(self, 'order_group_name', n.get_str_value()),
            "originalTemplateOrderId": lambda n : setattr(self, 'original_template_order_id', n.get_str_value()),
            "priority": lambda n : setattr(self, 'priority', n.get_int_value()),
            "templateOrderIds": lambda n : setattr(self, 'template_order_ids', n.get_collection_of_primitive_values(int)),
            "templateOrderMaps": lambda n : setattr(self, 'template_order_maps', n.get_object_value(OrderGroupObject_templateOrderMaps)),
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
        writer.write_int_value("appointVehicleGroupId", self.appoint_vehicle_group_id)
        writer.write_str_value("appointVehicleKey", self.appoint_vehicle_key)
        writer.write_str_value("createdBy", self.created_by)
        writer.write_datetime_value("gmtCreate", self.gmt_create)
        writer.write_datetime_value("gmtModified", self.gmt_modified)
        writer.write_int_value("id", self.id)
        writer.write_int_value("isAppointEnable", self.is_appoint_enable)
        writer.write_int_value("isDeleted", self.is_deleted)
        writer.write_str_value("modifiedBy", self.modified_by)
        writer.write_str_value("orderGroupName", self.order_group_name)
        writer.write_str_value("originalTemplateOrderId", self.original_template_order_id)
        writer.write_int_value("priority", self.priority)
        writer.write_collection_of_primitive_values("templateOrderIds", self.template_order_ids)
        writer.write_object_value("templateOrderMaps", self.template_order_maps)
        writer.write_int_value("userId", self.user_id)
        writer.write_additional_data_value(self.additional_data)
    

