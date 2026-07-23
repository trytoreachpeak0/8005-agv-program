from enum import Enum

class GetStateQueryParameterType(str, Enum):
    Activated = "activated",
    Inactivated = "inactivated",

