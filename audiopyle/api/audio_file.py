from flask import request

from audiopyle.lib.abstractions.api import AbstractRestApi
from audiopyle.lib.abstractions.api_model import ApiResponse, HttpStatusCode
from audiopyle.api.utils import build_request, log_api_call, build_response
from audiopyle.lib.services.store_provider import FileStore


class AudioFileListApi(AbstractRestApi):
    def __init__(self, file_store: FileStore) -> None:
        self.file_store = file_store

    def get(self, **kwargs) -> str:
        """Returns list of available audio file names
        ---
        responses:
            200:
                description: A list of file names
                schema:
                    type: array
                    items:
                        type: string
        """
        api_request = build_request(request, **kwargs)
        api_response = ApiResponse(HttpStatusCode.ok, self.file_store.list())
        log_api_call(api_request, api_response)
        return build_response(api_response)


class AudioFileDetailApi(AbstractRestApi):
    def __init__(self, file_store: FileStore) -> None:
        self.file_store = file_store

    def get(self, **kwargs) -> str:
        """Returns audio file details
        ---
        definitions:
            FileDetail:
                type: object
                properties:
                    file_name:
                        type: "string"
                    size:
                        description: "File size in bytes"
                        type: "integer"
                    created_on:
                        description: "Unix creation date (UTC) in format: %Y-%m-%d %H:%M:%S"
                        type: "string"
                    last_modification:
                        description: "Unix last modification date (UTC) in format: %Y-%m-%d %H:%M:%S"
                        type: "string"
                    last_access:
                        description: "Unix last access date (UTC) in format: %Y-%m-%d %H:%M:%S"
                        type: "string"
        parameters:
            -   name: "file_name"
                in: path
                required: "true"
                type: "string"
        responses:
            200:
                description: Details of given audio file
                schema:
                    $ref: '#/definitions/FileDetail'
                examples:
                    application/json: |-
                        {
                            created_on: "2018-08-16 08:58:49",
                            file_name: "102bpm_drum_loop.flac",
                            last_access: "2018-08-16 08:58:49",
                            last_modification: "2018-08-16 08:58:49",
                            size: 111690
                        }
            400:
                description: file_name parameter was not provided in URL
            404:
                description: Can not find a file with given name
        """
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
