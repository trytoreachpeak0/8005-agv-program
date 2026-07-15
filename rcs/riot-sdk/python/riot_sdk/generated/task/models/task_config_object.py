from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class TaskConfigObject(AdditionalDataHolder, Parsable):
    """
    任务管理配置表
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The categoryName property
    category_name: Optional[str] = None
    # The configKey property
    config_key: Optional[str] = None
    # The defaultValue property
    default_value: Optional[str] = None
    # The displayDescription property
    display_description: Optional[str] = None
    # The displayName property
    display_name: Optional[str] = None
    # The id property
    id: Optional[int] = None
    # The isDeleted property
    is_deleted: Optional[int] = None
    # The name property
    name: Optional[str] = None
    # The permission property
    permission: Optional[int] = None
    # The value property
    value: Optional[str] = None
    # The valueRange property
    value_range: Optional[str] = None
    # The valueType property
    value_type: Optional[str] = None
    # The valueUnit property
    value_unit: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> TaskConfigObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: TaskConfigObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return TaskConfigObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "categoryName": lambda n : setattr(self, 'category_name', n.get_str_value()),
            "configKey": lambda n : setattr(self, 'config_key', n.get_str_value()),
            "defaultValue": lambda n : setattr(self, 'default_value', n.get_str_value()),
            "displayDescription": lambda n : setattr(self, 'display_description', n.get_str_value()),
            "displayName": lambda n : setattr(self, 'display_name', n.get_str_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "isDeleted": lambda n : setattr(self, 'is_deleted', n.get_int_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "permission": lambda n : setattr(self, 'permission', n.get_int_value()),
            "value": lambda n : setattr(self, 'value', n.get_str_value()),
            "valueRange": lambda n : setattr(self, 'value_range', n.get_str_value()),
            "valueType": lambda n : setattr(self, 'value_type', n.get_str_value()),
            "valueUnit": lambda n : setattr(self, 'value_unit', n.get_str_value()),
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
        writer.write_str_value("categoryName", self.category_name)
        writer.write_str_value("configKey", self.config_key)
        writer.write_str_value("defaultValue", self.default_value)
        writer.write_str_value("displayDescription", self.display_description)
        writer.write_str_value("displayName", self.display_name)
        writer.write_int_value("id", self.id)
        writer.write_int_value("isDeleted", self.is_deleted)
        writer.write_str_value("name", self.name)
        writer.write_int_value("permission", self.permission)
        writer.write_str_value("value", self.value)
        writer.write_str_value("valueRange", self.value_range)
        writer.write_str_value("valueType", self.value_type)
        writer.write_str_value("valueUnit", self.value_unit)
        writer.write_additional_data_value(self.additional_data)
    

