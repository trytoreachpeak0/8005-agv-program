from enum import Enum

class MapSyncRecordObject_mapSyncResult(str, Enum):
    Failed = "failed",
    PartitionSuccess = "partitionSuccess",
    Success = "success",
    Syncing = "syncing",

