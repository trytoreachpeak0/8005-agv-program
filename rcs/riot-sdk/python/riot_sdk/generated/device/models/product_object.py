from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .product_object_data_format import ProductObject_dataFormat
    from .product_object_net_type import ProductObject_netType
    from .product_object_node_type import ProductObject_nodeType
    from .product_object_status import ProductObject_status
    from .product_object_validate_type import ProductObject_validateType
    from .product_types_object import ProductTypesObject

@dataclass
class ProductObject(AdditionalDataHolder, Parsable):
    """
    产品表
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # 产品下的设备接入物联网平台的认证方式: DeviceSecret
    auth_type: Optional[str] = None
    # 产品品类的标识符。如果传入此参数，创建的产品将使用指定品类的物模型；不传入，则不使用任何品类的标准物模型
    category_key: Optional[str] = None
    # 创建用户
    created_by: Optional[str] = None
    # 数据格式 0:custom_format; 1:srlink_format
    data_format: Optional[ProductObject_dataFormat] = None
    # The deleted property
    deleted: Optional[bool] = None
    # 产品描述
    description: Optional[str] = None
    # 创建时间
    gmt_create: Optional[datetime.datetime] = None
    # 更新时间
    gmt_modified: Optional[datetime.datetime] = None
    # 该版产品发布的时间
    gmt_release: Optional[datetime.datetime] = None
    # 主键ID
    id: Optional[int] = None
    # 产品图片
    image_url: Optional[str] = None
    # 入网凭证ID
    join_permission_id: Optional[str] = None
    # 更新用户
    modified_by: Optional[str] = None
    # 连网方式 可选值: 2:Wi-Fi 6:CELLULAR 蜂窝网 7:ETHERNET 以太网 8:LORA(LoRaWAN)
    net_type: Optional[ProductObject_netType] = None
    # 节点类型: 1-直连设备 2-网关设备 3-网关子设备
    node_type: Optional[ProductObject_nodeType] = None
    # 物联网平台为新建产品颁发的产品Key，作为该产品的全局唯一标识
    product_key: Optional[str] = None
    # 产品名称
    product_name: Optional[str] = None
    # 产品密钥
    product_secret: Optional[str] = None
    # 设备接入网关的协议类型 modbus opc-ua customize(自定义协议) ble(BLE协议) zigbee
    protocol_type: Optional[str] = None
    # 注册状态 未上线(1)/已上线(2)/撤销(3)
    status: Optional[ProductObject_status] = None
    # 是否标准品类
    templates: Optional[bool] = None
    # 租户ID
    tenant_id: Optional[str] = None
    # 产品类型
    types_list: Optional[list[ProductTypesObject]] = None
    # 数据校验级别: 1,强校验；2,弱校验；3,免校验
    validate_type: Optional[ProductObject_validateType] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ProductObject:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ProductObject
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return ProductObject()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .product_object_data_format import ProductObject_dataFormat
        from .product_object_net_type import ProductObject_netType
        from .product_object_node_type import ProductObject_nodeType
        from .product_object_status import ProductObject_status
        from .product_object_validate_type import ProductObject_validateType
        from .product_types_object import ProductTypesObject

        from .product_object_data_format import ProductObject_dataFormat
        from .product_object_net_type import ProductObject_netType
        from .product_object_node_type import ProductObject_nodeType
        from .product_object_status import ProductObject_status
        from .product_object_validate_type import ProductObject_validateType
        from .product_types_object import ProductTypesObject

        fields: dict[str, Callable[[Any], None]] = {
            "authType": lambda n : setattr(self, 'auth_type', n.get_str_value()),
            "categoryKey": lambda n : setattr(self, 'category_key', n.get_str_value()),
            "createdBy": lambda n : setattr(self, 'created_by', n.get_str_value()),
            "dataFormat": lambda n : setattr(self, 'data_format', n.get_enum_value(ProductObject_dataFormat)),
            "deleted": lambda n : setattr(self, 'deleted', n.get_bool_value()),
            "description": lambda n : setattr(self, 'description', n.get_str_value()),
            "gmtCreate": lambda n : setattr(self, 'gmt_create', n.get_datetime_value()),
            "gmtModified": lambda n : setattr(self, 'gmt_modified', n.get_datetime_value()),
            "gmtRelease": lambda n : setattr(self, 'gmt_release', n.get_datetime_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "imageUrl": lambda n : setattr(self, 'image_url', n.get_str_value()),
            "joinPermissionId": lambda n : setattr(self, 'join_permission_id', n.get_str_value()),
            "modifiedBy": lambda n : setattr(self, 'modified_by', n.get_str_value()),
            "netType": lambda n : setattr(self, 'net_type', n.get_enum_value(ProductObject_netType)),
            "nodeType": lambda n : setattr(self, 'node_type', n.get_enum_value(ProductObject_nodeType)),
            "productKey": lambda n : setattr(self, 'product_key', n.get_str_value()),
            "productName": lambda n : setattr(self, 'product_name', n.get_str_value()),
            "productSecret": lambda n : setattr(self, 'product_secret', n.get_str_value()),
            "protocolType": lambda n : setattr(self, 'protocol_type', n.get_str_value()),
            "status": lambda n : setattr(self, 'status', n.get_enum_value(ProductObject_status)),
            "templates": lambda n : setattr(self, 'templates', n.get_bool_value()),
            "tenantId": lambda n : setattr(self, 'tenant_id', n.get_str_value()),
            "typesList": lambda n : setattr(self, 'types_list', n.get_collection_of_object_values(ProductTypesObject)),
            "validateType": lambda n : setattr(self, 'validate_type', n.get_enum_value(ProductObject_validateType)),
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
        writer.write_str_value("authType", self.auth_type)
        writer.write_str_value("categoryKey", self.category_key)
        writer.write_str_value("createdBy", self.created_by)
        writer.write_enum_value("dataFormat", self.data_format)
        writer.write_bool_value("deleted", self.deleted)
        writer.write_str_value("description", self.description)
        writer.write_datetime_value("gmtCreate", self.gmt_create)
        writer.write_datetime_value("gmtModified", self.gmt_modified)
        writer.write_datetime_value("gmtRelease", self.gmt_release)
        writer.write_int_value("id", self.id)
        writer.write_str_value("imageUrl", self.image_url)
        writer.write_str_value("joinPermissionId", self.join_permission_id)
        writer.write_str_value("modifiedBy", self.modified_by)
        writer.write_enum_value("netType", self.net_type)
        writer.write_enum_value("nodeType", self.node_type)
        writer.write_str_value("productKey", self.product_key)
        writer.write_str_value("productName", self.product_name)
        writer.write_str_value("productSecret", self.product_secret)
        writer.write_str_value("protocolType", self.protocol_type)
        writer.write_enum_value("status", self.status)
        writer.write_bool_value("templates", self.templates)
        writer.write_str_value("tenantId", self.tenant_id)
        writer.write_collection_of_object_values("typesList", self.types_list)
        writer.write_enum_value("validateType", self.validate_type)
        writer.write_additional_data_value(self.additional_data)
    

