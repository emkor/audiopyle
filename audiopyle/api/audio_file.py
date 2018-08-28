from flask import request

from audiopyle.lib.abstractions.api import AbstractRestApi
from audiopyle.lib.abstractions.api_model import ApiResponse, HttpStatusCode
from audiopyle.api.utils import build_request, log_api_call, build_response
from audiopyle.lib.services.store_provider import FileStore


class AudioFileListApi(AbstractRestApi):
    def __init__(self, file_store: FileStore) -> None:
        self.file_store = file_store

    def get(self, **kwargs) -> str:
        api_request = build_request(request, **kwargs)
        api_response = ApiResponse(HttpStatusCode.ok, self.file_store.list())
        log_api_call(api_request, api_response)
        return build_response(api_response)


class AudioFileDetailApi(AbstractRestApi):
    def __init__(self, file_store: FileStore) -> None:
        self.file_store = file_store

    def get(self, **kwargs) -> str:
        api_request = build_request(request, **kwargs)
        file_name = api_request.query_params.get("file_name")
        if file_name is None:
            api_response = ApiResponse(HttpStatusCode.bad_request,
                                       {"error": "Parameter file_name was not provided"})
        elif self.file_store.exists(file_name):
            api_response = ApiResponse(HttpStatusCode.ok, self.file_store.meta(file_name).to_serializable())
        else:
            api_response = ApiResponse(HttpStatusCode.not_found,
                                       {"error": "Can't find file with name: {}".format(file_name)})
        log_api_call(api_request, api_response)
        return build_response(api_response)
