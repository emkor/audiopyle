from datetime import datetime
import requests

DEFAULT_API_TIMEOUT = 10.
DEFAULT_EXPECTED_STATUS = 200


class TimeoutException(Exception):
    pass


def keep_polling_until(url, expected_status=DEFAULT_EXPECTED_STATUS, timeout=DEFAULT_API_TIMEOUT):
    response = None
    start_time = datetime.utcnow()
    while (datetime.utcnow() - start_time).total_seconds() <= timeout:
        response = requests.get(url=url)
        if response.status_code == expected_status:
            return response
    if response:
        message = "URL {} did not return status {} within {}s. Actual response: {} {}".format(url, expected_status,
                                                                                              timeout,
                                                                                              response.status_code,
                                                                                              response.content)
    else:
        message = "URL {} did not return any response within {}s.".format(url, expected_status, timeout)
    raise TimeoutException(message)
