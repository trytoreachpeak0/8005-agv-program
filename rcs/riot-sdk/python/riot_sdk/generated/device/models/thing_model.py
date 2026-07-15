from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .event import Event
    from .extend_config import ExtendConfig
    from .function_block import FunctionBlock
    from .profile import Profile
    from .property_ import Property_
    from .service import Service

@dataclass
class ThingModel(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The description property
    description: Optional[str] = None
    # The events property
    events: Optional[list[Event]] = None
    # The extendConfig property
    extend_config: Optional[ExtendConfig] = None
    # The functionBlockId property
    function_block_id: Optional[str] = None
    # The functionBlockName property
    function_block_name: Optional[str] = None
    # The functionBlocks property
    function_blocks: Optional[list[FunctionBlock]] = None
    # The profile property
    profile: Optional[Profile] = None
    # The properties property
    properties: Optional[list[Property_]] = None
    # The services property
    services: Optional[list[Service]] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ThingModel:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ThingModel
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return ThingModel()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .event import Event
        from .extend_config import ExtendConfig
        from .function_block import FunctionBlock
        from .profile import Profile
        from .property_ import Property_
        from .service import Service

        from .event import Event
        from .extend_config import ExtendConfig
        from .function_block import FunctionBlock
        from .profile import Profile
        from .property_ import Property_
        from .service import Service

        fields: dict[str, Callable[[Any], None]] = {
            "description": lambda n : setattr(self, 'description', n.get_str_value()),
            "events": lambda n : setattr(self, 'events', n.get_collection_of_object_values(Event)),
            "extendConfig": lambda n : setattr(self, 'extend_config', n.get_object_value(ExtendConfig)),
            "functionBlockId": lambda n : setattr(self, 'function_block_id', n.get_str_value()),
            "functionBlockName": lambda n : setattr(self, 'function_block_name', n.get_str_value()),
            "functionBlocks": lambda n : setattr(self, 'function_blocks', n.get_collection_of_object_values(FunctionBlock)),
            "profile": lambda n : setattr(self, 'profile', n.get_object_value(Profile)),
            "properties": lambda n : setattr(self, 'properties', n.get_collection_of_object_values(Property_)),
            "services": lambda n : setattr(self, 'services', n.get_collection_of_object_values(Service)),
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
        writer.write_str_value("description", self.description)
        writer.write_collection_of_object_values("events", self.events)
        writer.write_object_value("extendConfig", self.extend_config)
        writer.write_str_value("functionBlockId", self.function_block_id)
        writer.write_str_value("functionBlockName", self.function_block_name)
        writer.write_collection_of_object_values("functionBlocks", self.function_blocks)
        writer.write_object_value("profile", self.profile)
        writer.write_collection_of_object_values("properties", self.properties)
        writer.write_collection_of_object_values("services", self.services)
        writer.write_additional_data_value(self.additional_data)
    

