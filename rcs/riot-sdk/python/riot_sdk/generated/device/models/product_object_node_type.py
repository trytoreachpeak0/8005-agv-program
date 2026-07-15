from enum import Enum

class ProductObject_nodeType(str, Enum):
    CONNECTED_DEVICE = "CONNECTED_DEVICE",
    GATEWAY_DEVICE = "GATEWAY_DEVICE",
    SUB_DEVICE = "SUB_DEVICE",

