from logging import Logger
from typing import Any, Dict, Optional

import requests


class ResultApiClient(object):
    def __init__(self, host: str, port: int, logger: Logger) -> None:
        self.host = host
        self.port = port
        self.logger = logger

    def store_data(self, task_id: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self._send_post(payload, "http://{}:{}/result/{}/data".format(self.host, self.port, task_id))

    def store_meta(self, task_id: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self._send_post(payload, "http://{}:{}/result/{}/meta".format(self.host, self.port, task_id))

    def store_stats(self, task_id: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self._send_post(payload, "http://{}:{}/result/{}/stats".format(self.host, self.port, task_id))

    def _send_post(self, payload: Dict[str, Any], url: str) -> Optional[Dict[str, Any]]:
        resp = requests.post(url=url, json=payload)
        if resp.ok:
            return resp.json()
        else:
            self.logger.warning("Could not store data under URL {}: {}".format(url, resp.content))
            return None
