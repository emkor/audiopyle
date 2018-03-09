from datetime import datetime
from enum import Enum
from typing import Text, Any, Dict, Optional

from commons.abstractions.model import Model


class HttpStatusCode(Enum):
    ok = 200
    created = 201
    accepted = 202
    no_content = 204
    bad_request = 400
    not_found = 404
    method_not_allowed = 405
    request_timeout = 408
    internal_server_error = 500


class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class _ApiError(Exception):
    def __init__(self, message: Text, status_code: HttpStatusCode) -> None:
        self.status_code = status_code
        self.message = message


class ClientError(_ApiError):
    def __init__(self, message: Text, status_code: HttpStatusCode = HttpStatusCode.bad_request) -> None:
        self.status_code = status_code
        self.message = message


class ServerError(_ApiError):
    def __init__(self, message: Text, status_code: HttpStatusCode = HttpStatusCode.internal_server_error) -> None:
        self.status_code = status_code
        self.message = message


class ApiRequest(Model):
    def __init__(self, url: Text, method: HttpMethod, query_params: Dict[Text, Any],
                 headers: Dict[Text, Any], payload: Dict[Text, Any]) -> None:
        self.method = method
        self.url = url
        self.query_params = query_params
        self.headers = headers
        self.payload = payload
        self.creation_time = datetime.utcnow()


class ApiResponse(Model):
    def __init__(self, status_code: HttpStatusCode, payload: Optional[Any],
                 headers: Optional[Dict[Text, Any]] = None) -> None:
        self.status_code = status_code
        self.payload = payload
        self.headers = headers
        self.creation_time = datetime.utcnow()
