from enum import Enum

class MapSyncRecordObject_mapSyncType(str, Enum):
    Pull = "pull",
    Push = "push",
    Upload = "upload",

