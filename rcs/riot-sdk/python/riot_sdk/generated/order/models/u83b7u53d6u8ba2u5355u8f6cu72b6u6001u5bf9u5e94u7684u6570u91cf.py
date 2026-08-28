from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class U83b7u53d6u8ba2u5355u8f6cu72b6u6001u5bf9u5e94u7684u6570u91cf(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 已取消数量
    cancel_num: Optional[int] = None
    # 正在执行数量
    executing_num: Optional[int] = None
    # 已失败数量
    failed_num: Optional[int] = None
    # 已挂起数量
    hang_num: Optional[int] = None
    # 订单状态下的订单数量
    num: Optional[int] = None
    # 订单状态
    order_state: Optional[int] = None
    # 队列中(换车)数量
    queueing_change_car_num: Optional[int] = None
    # 队列中数量
    queueing_num: Optional[int] = None
    # 队列中(优先执行)数量
    queueing_priority_num: Optional[int] = None
    # 已完成数量
    success_num: Optional[int] = None
    # 订单总数
    total: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> U83b7u53d6u8ba2u5355u8f6cu72b6u6001u5bf9u5e94u7684u6570u91cf:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: U83b7u53d6u8ba2u5355u8f6cu72b6u6001u5bf9u5e94u7684u6570u91cf
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return U83b7u53d6u8ba2u5355u8f6cu72b6u6001u5bf9u5e94u7684u6570u91cf()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "cancelNum": lambda n : setattr(self, 'cancel_num', n.get_int_value()),
            "executingNum": lambda n : setattr(self, 'executing_num', n.get_int_value()),
            "failedNum": lambda n : setattr(self, 'failed_num', n.get_int_value()),
            "hangNum": lambda n : setattr(self, 'hang_num', n.get_int_value()),
            "num": lambda n : setattr(self, 'num', n.get_int_value()),
            "orderState": lambda n : setattr(self, 'order_state', n.get_int_value()),
            "queueingChangeCarNum": lambda n : setattr(self, 'queueing_change_car_num', n.get_int_value()),
            "queueingNum": lambda n : setattr(self, 'queueing_num', n.get_int_value()),
            "queueingPriorityNum": lambda n : setattr(self, 'queueing_priority_num', n.get_int_value()),
            "successNum": lambda n : setattr(self, 'success_num', n.get_int_value()),
            "total": lambda n : setattr(self, 'total', n.get_int_value()),
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
        writer.write_int_value("cancelNum", self.cancel_num)
        writer.write_int_value("executingNum", self.executing_num)
        writer.write_int_value("failedNum", self.failed_num)
        writer.write_int_value("hangNum", self.hang_num)
        writer.write_int_value("num", self.num)
        writer.write_int_value("orderState", self.order_state)
        writer.write_int_value("queueingChangeCarNum", self.queueing_change_car_num)
        writer.write_int_value("queueingNum", self.queueing_num)
        writer.write_int_value("queueingPriorityNum", self.queueing_priority_num)
        writer.write_int_value("successNum", self.success_num)
        writer.write_int_value("total", self.total)
        writer.write_additional_data_value(self.additional_data)
    

