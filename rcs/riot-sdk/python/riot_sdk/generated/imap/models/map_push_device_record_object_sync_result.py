from enum import Enum

class MapPushDeviceRecordObject_syncResult(str, Enum):
    Failed = "failed",
    PartitionSuccess = "partitionSuccess",
    Success = "success",
    Syncing = "syncing",

