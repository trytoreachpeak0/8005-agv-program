from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class TemplateActionVOObject(AdditionalDataHolder, Parsable):
    """
    动作模板参数接收类
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 动作类型id,在定义自定义服务时,需要录入
    action_id: Optional[int] = None
    # 动作名称
    action_name: Optional[str] = None
    # 动作参数3
    action_param_str: Optional[str] = None
    # 动作参数1
    action_param1: Optional[int] = None
    # 动作参数2
    action_param2: Optional[int] = None
    # 关联物模型定义的动作服务key
    function_key: Optional[str] = None
    # 关联物模型定义的动作服务名称
    function_name: Optional[str] = None
    # 自增id,编辑时必填
    id: Optional[int] = None
    # 产品Key，作为该产品的全局唯一标识
    product_key: Optional[str] = None
    # 模板类型:1:机器人服务,2:自定义
    template_type: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> TemplateActionVOObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: TemplateActionVOObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return TemplateActionVOObject()
    
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
            "functionKey": lambda n : setattr(self, 'function_key', n.get_str_value()),
            "functionName": lambda n : setattr(self, 'function_name', n.get_str_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "productKey": lambda n : setattr(self, 'product_key', n.get_str_value()),
            "templateType": lambda n : setattr(self, 'template_type', n.get_str_value()),
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
        writer.write_str_value("functionKey", self.function_key)
        writer.write_str_value("functionName", self.function_name)
        writer.write_int_value("id", self.id)
        writer.write_str_value("productKey", self.product_key)
        writer.write_str_value("templateType", self.template_type)
        writer.write_additional_data_value(self.additional_data)
    

