from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class TemplateOrderMissionObject(AdditionalDataHolder, Parsable):
    """
    模板管理-订单任务表
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 动作模板Id
    action_template_id: Optional[int] = None
    # 目的地
    destination: Optional[int] = None
    # 子任务执行失败的策略(动作任务)
    fail_strategy: Optional[str] = None
    # 策略对应的参数
    fail_value: Optional[str] = None
    # 自增id
    id: Optional[int] = None
    # 删除标识:0未删除,1:已删除
    is_deleted: Optional[int] = None
    # 地图id
    map_id: Optional[int] = None
    # fixed:固定任务,dynamic:动态任务
    mission_type: Optional[str] = None
    # 订单模板id
    template_id: Optional[int] = None
    # 任务类型(act:动作任务,move:移动任务)
    type: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> TemplateOrderMissionObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: TemplateOrderMissionObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return TemplateOrderMissionObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "actionTemplateId": lambda n : setattr(self, 'action_template_id', n.get_int_value()),
            "destination": lambda n : setattr(self, 'destination', n.get_int_value()),
            "failStrategy": lambda n : setattr(self, 'fail_strategy', n.get_str_value()),
            "failValue": lambda n : setattr(self, 'fail_value', n.get_str_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "isDeleted": lambda n : setattr(self, 'is_deleted', n.get_int_value()),
            "mapId": lambda n : setattr(self, 'map_id', n.get_int_value()),
            "missionType": lambda n : setattr(self, 'mission_type', n.get_str_value()),
            "templateId": lambda n : setattr(self, 'template_id', n.get_int_value()),
            "type": lambda n : setattr(self, 'type', n.get_str_value()),
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
        writer.write_int_value("actionTemplateId", self.action_template_id)
        writer.write_int_value("destination", self.destination)
        writer.write_str_value("failStrategy", self.fail_strategy)
        writer.write_str_value("failValue", self.fail_value)
        writer.write_int_value("id", self.id)
        writer.write_int_value("isDeleted", self.is_deleted)
        writer.write_int_value("mapId", self.map_id)
        writer.write_str_value("missionType", self.mission_type)
        writer.write_int_value("templateId", self.template_id)
        writer.write_str_value("type", self.type)
        writer.write_additional_data_value(self.additional_data)
    

