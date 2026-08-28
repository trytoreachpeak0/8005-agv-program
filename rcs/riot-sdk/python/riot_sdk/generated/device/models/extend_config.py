from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .customize_config import CustomizeConfig
    from .mc_config import McConfig
    from .modbus_config import ModbusConfig
    from .opc_config import OpcConfig

@dataclass
class ExtendConfig(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The customizeConfig property
    customize_config: Optional[CustomizeConfig] = None
    # The mcConfig property
    mc_config: Optional[McConfig] = None
    # The modbusConfig property
    modbus_config: Optional[ModbusConfig] = None
    # The opcConfig property
    opc_config: Optional[OpcConfig] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ExtendConfig:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ExtendConfig
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return ExtendConfig()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .customize_config import CustomizeConfig
        from .mc_config import McConfig
        from .modbus_config import ModbusConfig
        from .opc_config import OpcConfig

        from .customize_config import CustomizeConfig
        from .mc_config import McConfig
        from .modbus_config import ModbusConfig
        from .opc_config import OpcConfig

        fields: dict[str, Callable[[Any], None]] = {
            "customizeConfig": lambda n : setattr(self, 'customize_config', n.get_object_value(CustomizeConfig)),
            "mcConfig": lambda n : setattr(self, 'mc_config', n.get_object_value(McConfig)),
            "modbusConfig": lambda n : setattr(self, 'modbus_config', n.get_object_value(ModbusConfig)),
            "opcConfig": lambda n : setattr(self, 'opc_config', n.get_object_value(OpcConfig)),
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
        writer.write_object_value("customizeConfig", self.customize_config)
        writer.write_object_value("mcConfig", self.mc_config)
        writer.write_object_value("modbusConfig", self.modbus_config)
        writer.write_object_value("opcConfig", self.opc_config)
        writer.write_additional_data_value(self.additional_data)
    

