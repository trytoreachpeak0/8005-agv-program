from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .download.download_request_builder import DownloadRequestBuilder
    from .map_image.map_image_request_builder import MapImageRequestBuilder
    from .pull.pull_request_builder import PullRequestBuilder
    from .push.push_request_builder import PushRequestBuilder
    from .re_push.re_push_request_builder import RePushRequestBuilder
    from .save.save_request_builder import SaveRequestBuilder
    from .upload.upload_request_builder import UploadRequestBuilder

class FileRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/imap/v1/mapInfo/file
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new FileRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/imap/v1/mapInfo/file", path_parameters)
    
    @property
    def download(self) -> DownloadRequestBuilder:
        """
        The download property
        """
        from .download.download_request_builder import DownloadRequestBuilder

        return DownloadRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def map_image(self) -> MapImageRequestBuilder:
        """
        The mapImage property
        """
        from .map_image.map_image_request_builder import MapImageRequestBuilder

        return MapImageRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def pull(self) -> PullRequestBuilder:
        """
        The pull property
        """
        from .pull.pull_request_builder import PullRequestBuilder

        return PullRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def push(self) -> PushRequestBuilder:
        """
        The push property
        """
        from .push.push_request_builder import PushRequestBuilder

        return PushRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def re_push(self) -> RePushRequestBuilder:
        """
        The rePush property
        """
        from .re_push.re_push_request_builder import RePushRequestBuilder

        return RePushRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def save(self) -> SaveRequestBuilder:
        """
        The save property
        """
        from .save.save_request_builder import SaveRequestBuilder

        return SaveRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def upload(self) -> UploadRequestBuilder:
        """
        The upload property
        """
        from .upload.upload_request_builder import UploadRequestBuilder

        return UploadRequestBuilder(self.request_adapter, self.path_parameters)
    

