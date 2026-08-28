from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class TemplateOrderMissionVOObject(AdditionalDataHolder, Parsable):
    """
    订单模板子任务参数接收类
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 动作id
    action_id: Optional[int] = None
    # 动作名称
    action_name: Optional[str] = None
    # 动作参数3
    action_param_str: Optional[str] = None
    # 动作参数1
    action_param1: Optional[int] = None
    # 动作参数2
    action_param2: Optional[int] = None
    # 动作模板Id
    action_template_id: Optional[int] = None
    # 目的地
    destination: Optional[int] = None
    # 子任务执行失败的策略(动作任务)
    fail_strategy: Optional[str] = None
    # 策略对应的参数
    fail_value: Optional[str] = None
    # 地图id
    map_id: Optional[int] = None
    # fixed:固定任务,dynamic:动态任务
    mission_type: Optional[str] = None
    # 任务类型(act:动作任务,move:移动任务)
    type: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> TemplateOrderMissionVOObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: TemplateOrderMissionVOObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return TemplateOrderMissionVOObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "actionId": lambda n : setattr(self, 'action_id', n.get_int_value()),
            "actionName": lambda n : setattr(self, 'action_name', n.get_str_value()),
            "actionParamStr": lambda n : setattr(self, 'action_param_str', n.get_str_value()),
            "actionParam1": lambda n : setattr(self, 'action_param1', n.get_int_value()),
            "actionParam2": lambda n : setattr(self, 'action_param2', n.get_int_value()),
            "actionTemplateId": lambda n : setattr(self, 'action_template_id', n.get_int_value()),
            "destination": lambda n : setattr(self, 'destination', n.get_int_value()),
            "failStrategy": lambda n : setattr(self, 'fail_strategy', n.get_str_value()),
            "failValue": lambda n : setattr(self, 'fail_value', n.get_str_value()),
            "mapId": lambda n : setattr(self, 'map_id', n.get_int_value()),
            "missionType": lambda n : setattr(self, 'mission_type', n.get_str_value()),
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
        writer.write_int_value("actionId", self.action_id)
        writer.write_str_value("actionName", self.action_name)
        writer.write_str_value("actionParamStr", self.action_param_str)
        writer.write_int_value("actionParam1", self.action_param1)
        writer.write_int_value("actionParam2", self.action_param2)
        writer.write_int_value("actionTemplateId", self.action_template_id)
        writer.write_int_value("destination", self.destination)
        writer.write_str_value("failStrategy", self.fail_strategy)
        writer.write_str_value("failValue", self.fail_value)
        writer.write_int_value("mapId", self.map_id)
        writer.write_str_value("missionType", self.mission_type)
        writer.write_str_value("type", self.type)
        writer.write_additional_data_value(self.additional_data)
    

