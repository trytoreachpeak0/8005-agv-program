from enum import Enum

class Vehicle_actionState(str, Enum):
    AT_FINISHED = "AT_FINISHED",
    AT_IN_CANCEL = "AT_IN_CANCEL",
    AT_NA = "AT_NA",
    AT_PAUSED = "AT_PAUSED",
    AT_RUNNING = "AT_RUNNING",
    AT_WAIT_FOR_ACK = "AT_WAIT_FOR_ACK",
    AT_WAIT_FOR_START = "AT_WAIT_FOR_START",

