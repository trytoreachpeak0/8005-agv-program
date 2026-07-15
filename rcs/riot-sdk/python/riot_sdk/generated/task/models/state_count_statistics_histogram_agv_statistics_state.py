from enum import Enum

class StateCountStatisticsHistogram_agvStatisticsState(str, Enum):
    BREAK_SWITCH_STATE = "BREAK_SWITCH_STATE",
    CHARGING = "CHARGING",
    EXCEPTION = "EXCEPTION",
    EXECUTING = "EXECUTING",
    IDLE = "IDLE",
    LOCATION_EXC_STATE = "LOCATION_EXC_STATE",
    MONITOR_EXC_STATE = "MONITOR_EXC_STATE",
    OFF_LINE = "OFF_LINE",
    PAUSE = "PAUSE",

