from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class DynamicOrderMissionDTO(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 动作类型id
    action_id: Optional[int] = None
    # 动作参数3,str
    action_param_str: Optional[str] = None
    # 动作参数1
    action_param1: Optional[int] = None
    # 动作参数2
    action_param2: Optional[int] = None
    # 目的地id
    destination: Optional[int] = None
    # 子任务执行失败的策略
    fail_strategy: Optional[str] = None
    # 策略对应的参数
    fail_value: Optional[str] = None
    # 关联物模型定义的动作服务key
    function_key: Optional[str] = None
    # 当前任务车长mm
    length: Optional[int] = None
    # 地图id
    map_id: Optional[int] = None
    # 替换的序列号
    replace_index: Optional[int] = None
    # 当前任务指定速度m/s
    speed: Optional[float] = None
    # 任务类型move,act
    type: Optional[str] = None
    # 当前任务车宽mm
    width: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> DynamicOrderMissionDTO:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: DynamicOrderMissionDTO
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return DynamicOrderMissionDTO()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "actionId": lambda n : setattr(self, 'action_id', n.get_int_value()),
            "actionParamStr": lambda n : setattr(self, 'action_param_str', n.get_str_value()),
            "actionParam1": lambda n : setattr(self, 'action_param1', n.get_int_value()),
            "actionParam2": lambda n : setattr(self, 'action_param2', n.get_int_value()),
            "destination": lambda n : setattr(self, 'destination', n.get_int_value()),
            "failStrategy": lambda n : setattr(self, 'fail_strategy', n.get_str_value()),
            "failValue": lambda n : setattr(self, 'fail_value', n.get_str_value()),
            "functionKey": lambda n : setattr(self, 'function_key', n.get_str_value()),
            "length": lambda n : setattr(self, 'length', n.get_int_value()),
            "mapId": lambda n : setattr(self, 'map_id', n.get_int_value()),
            "replaceIndex": lambda n : setattr(self, 'replace_index', n.get_int_value()),
            "speed": lambda n : setattr(self, 'speed', n.get_float_value()),
            "type": lambda n : setattr(self, 'type', n.get_str_value()),
            "width": lambda n : setattr(self, 'width', n.get_int_value()),
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
        writer.write_str_value("actionParamStr", self.action_param_str)
        writer.write_int_value("actionParam1", self.action_param1)
        writer.write_int_value("actionParam2", self.action_param2)
        writer.write_int_value("destination", self.destination)
        writer.write_str_value("failStrategy", self.fail_strategy)
        writer.write_str_value("failValue", self.fail_value)
        writer.write_str_value("functionKey", self.function_key)
        writer.write_int_value("length", self.length)
        writer.write_int_value("mapId", self.map_id)
        writer.write_int_value("replaceIndex", self.replace_index)
        writer.write_float_value("speed", self.speed)
        writer.write_str_value("type", self.type)
        writer.write_int_value("width", self.width)
        writer.write_additional_data_value(self.additional_data)
    

