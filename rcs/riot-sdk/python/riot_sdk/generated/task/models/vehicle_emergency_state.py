from enum import Enum

class Vehicle_emergencyState(str, Enum):
    CAN_NOT_RECOVER = "CAN_NOT_RECOVER",
    CAN_RECOVER = "CAN_RECOVER",
    OK = "OK",

