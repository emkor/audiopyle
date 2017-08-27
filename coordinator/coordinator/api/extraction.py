import cherrypy

from commons.abstractions.api import AudiopyleRestApi
from commons.services.extraction import ExtractionRequest
from commons.services.uuid_generation import generate_uuid
from extractor.service import run_task, retrieve_result, delete_result
from extractor.tasks import extract_feature


class ExtractionApi(AudiopyleRestApi):
    def get(self, request_url, query_params):
        task_id = str(query_params.get("id"))
        self.logger.info("Querying result of {}...".format(task_id))
        extraction_result = retrieve_result(task_id)
        self.logger.info("Returning result of {}: {}".format(task_id, extraction_result.status))
        return extraction_result

    def post(self, request_url, query_params, request_payload):
        execution_request = ExtractionRequest.deserialize(request_payload)
        self.logger.info("Sending feature extraction task: {}...".format(execution_request))
        serialized_request = execution_request.serialize()
        async_result = run_task(task=extract_feature,
                                task_id=generate_uuid(serialized_request),
                                extraction_request=serialized_request)
        self.logger.info("Sent feature extraction task! ID: {}.".format(async_result.task_id))
        return async_result.task_id

    def delete(self, request_url, query_params):
        task_id = str(query_params.get("id"))
        was_successful = delete_result(task_id)
        if was_successful:
            return task_id
        else:
            raise cherrypy.HTTPError(status=410, message="Did not find result with given task id: {}".format(task_id))
