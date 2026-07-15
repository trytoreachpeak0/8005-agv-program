from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .all_file_names.all_file_names_request_builder import AllFileNamesRequestBuilder
    from .batch_add.batch_add_request_builder import BatchAddRequestBuilder
    from .query_cur_sync_tasks.query_cur_sync_tasks_request_builder import QueryCurSyncTasksRequestBuilder
    from .query_device_by_type.query_device_by_type_request_builder import QueryDeviceByTypeRequestBuilder
    from .query_sync_tasks_by_condition.query_sync_tasks_by_condition_request_builder import QuerySyncTasksByConditionRequestBuilder
    from .sync_tasks_export.sync_tasks_export_request_builder import SyncTasksExportRequestBuilder

class VehicleSyncTaskRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/task/v1/vehicleSyncTask
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new VehicleSyncTaskRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/task/v1/vehicleSyncTask", path_parameters)
    
    @property
    def all_file_names(self) -> AllFileNamesRequestBuilder:
        """
        The allFileNames property
        """
        from .all_file_names.all_file_names_request_builder import AllFileNamesRequestBuilder

        return AllFileNamesRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def batch_add(self) -> BatchAddRequestBuilder:
        """
        The batchAdd property
        """
        from .batch_add.batch_add_request_builder import BatchAddRequestBuilder

        return BatchAddRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def query_cur_sync_tasks(self) -> QueryCurSyncTasksRequestBuilder:
        """
        The queryCurSyncTasks property
        """
        from .query_cur_sync_tasks.query_cur_sync_tasks_request_builder import QueryCurSyncTasksRequestBuilder

        return QueryCurSyncTasksRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def query_device_by_type(self) -> QueryDeviceByTypeRequestBuilder:
        """
        The queryDeviceByType property
        """
        from .query_device_by_type.query_device_by_type_request_builder import QueryDeviceByTypeRequestBuilder

        return QueryDeviceByTypeRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def query_sync_tasks_by_condition(self) -> QuerySyncTasksByConditionRequestBuilder:
        """
        The querySyncTasksByCondition property
        """
        from .query_sync_tasks_by_condition.query_sync_tasks_by_condition_request_builder import QuerySyncTasksByConditionRequestBuilder

        return QuerySyncTasksByConditionRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def sync_tasks_export(self) -> SyncTasksExportRequestBuilder:
        """
        The SyncTasksExport property
        """
        from .sync_tasks_export.sync_tasks_export_request_builder import SyncTasksExportRequestBuilder

        return SyncTasksExportRequestBuilder(self.request_adapter, self.path_parameters)
    

