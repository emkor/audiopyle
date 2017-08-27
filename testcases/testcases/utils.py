import os
from datetime import datetime
from time import sleep

import requests

DEFAULT_API_TIMEOUT = 10.
DEFAULT_TICK_TIME = .5
DEFAULT_EXPECTED_STATUS = 200

SERVICE_HOSTS = {
    "coordinator": "coordinator",
    "mysql": "mysql_host",
    "rabbitmq": "rabbitmq_host",
    "extractor": "extractor_host_1",
    "testcases": "testcases"
}


def get_service_host_name(service_name):
    if os.environ.get("CI_BUILD") == "1":
        return SERVICE_HOSTS.get(service_name)
    else:
        return "localhost"


class TimeoutException(Exception):
    pass


def keep_polling_until(url, expected_status=DEFAULT_EXPECTED_STATUS, timeout=DEFAULT_API_TIMEOUT,
                       tick=DEFAULT_TICK_TIME):
    response = None
    start_time = datetime.utcnow()
    while (datetime.utcnow() - start_time).total_seconds() <= timeout:
        response = requests.get(url=url)
        if response.status_code == expected_status:
            return response
        sleep(tick)
    if response:
        message = "URL {} did not return status {} within {}s. Actual response: {} {}".format(url, expected_status,
                                                                                              timeout,
                                                                                              response.status_code,
                                                                                              response.content)
    else:
        message = "URL {} did not return any response within {}s.".format(url, expected_status, timeout)
    raise TimeoutException(message)
