from enum import Enum

class OrderDTO_orderType(str, Enum):
    BATTERY_MAINTAIN = "BATTERY_MAINTAIN",
    CHARGE = "CHARGE",
    NORMAL = "NORMAL",
    PARKING = "PARKING",

