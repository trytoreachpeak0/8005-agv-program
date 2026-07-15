from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .template_order_mission_v_o_object import TemplateOrderMissionVOObject

@dataclass
class TemplateOrderVOObject(AdditionalDataHolder, Parsable):
    """
    订单模板参数接收类
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 关联的子账户id集合
    account_ids: Optional[list[int]] = None
    # 预约车辆组Id(与appointVehicleId互斥,不可同时存在)
    appoint_vehicle_group_id: Optional[int] = None
    # 预约车辆id(与appointVehicleGroupId互斥,不可同时存在)
    appoint_vehicle_key: Optional[str] = None
    # 订单模板Id(编辑时必填)
    id: Optional[int] = None
    # 订单任务集合
    missions: Optional[list[TemplateOrderMissionVOObject]] = None
    # 订单优先级:0:低优先级,10:中优先级,20:高优先级,30:最高优先级
    priority: Optional[int] = None
    # 模板名称
    template_name: Optional[str] = None
    # 订单模板标签Id集合
    template_order_tag_ids: Optional[list[int]] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> TemplateOrderVOObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: TemplateOrderVOObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return TemplateOrderVOObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .template_order_mission_v_o_object import TemplateOrderMissionVOObject

        from .template_order_mission_v_o_object import TemplateOrderMissionVOObject

        fields: dict[str, Callable[[Any], None]] = {
            "accountIds": lambda n : setattr(self, 'account_ids', n.get_collection_of_primitive_values(int)),
            "appointVehicleGroupId": lambda n : setattr(self, 'appoint_vehicle_group_id', n.get_int_value()),
            "appointVehicleKey": lambda n : setattr(self, 'appoint_vehicle_key', n.get_str_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "missions": lambda n : setattr(self, 'missions', n.get_collection_of_object_values(TemplateOrderMissionVOObject)),
            "priority": lambda n : setattr(self, 'priority', n.get_int_value()),
            "templateName": lambda n : setattr(self, 'template_name', n.get_str_value()),
            "templateOrderTagIds": lambda n : setattr(self, 'template_order_tag_ids', n.get_collection_of_primitive_values(int)),
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
        writer.write_int_value("appointVehicleGroupId", self.appoint_vehicle_group_id)
        writer.write_str_value("appointVehicleKey", self.appoint_vehicle_key)
        writer.write_int_value("id", self.id)
        writer.write_collection_of_object_values("missions", self.missions)
        writer.write_int_value("priority", self.priority)
        writer.write_str_value("templateName", self.template_name)
        writer.write_collection_of_primitive_values("templateOrderTagIds", self.template_order_tag_ids)
        writer.write_additional_data_value(self.additional_data)
    

