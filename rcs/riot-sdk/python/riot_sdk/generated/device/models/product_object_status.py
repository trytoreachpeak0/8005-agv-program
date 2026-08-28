from enum import Enum

class ProductObject_status(str, Enum):
    NOT_ONLINE = "NOT_ONLINE",
    ONLINE = "ONLINE",
    REVERSED = "REVERSED",

