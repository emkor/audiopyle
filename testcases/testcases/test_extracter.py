# import unittest
# from time import sleep
#
# from assertpy import assert_that
#
# from commons.model.analysis_task import AnalysisTask
# from commons.model.remote_file_meta import RemoteFileMeta
# from commons.model.remote_file_source import create_b2_source_config
# from commons.provider.redis_queue_client import RedisQueueClient
# from commons.utils.constant import B2_TEST_FILE_PATH, B2_ACCOUNT_ID, B2_APPLICATION_KEY, \
#     B2_RESOURCES_BUCKET
#
# from testcases.docker.container import Container
# from testcases.docker.utils import IMAGE_REDIS, IMAGE_XTRACTER
#
# REDIS_TASK_QUEUE_NAME = 'xtracter_tasks'
# REDIS_RESULT_QUEUE_NAME = 'xtracter_results'
# TASK_TAKE_TIME = 4
# ANALYSIS_TIMEOUT = 90
#
#
# class XtracterIntegrationTest(unittest.TestCase):
#     REDIS_CONTAINER = None
#     XTRACTER_CONTAINER = None
#
#     @classmethod
#     def setUpClass(cls):
#         cls.REDIS_CONTAINER = Container(IMAGE_REDIS, 'RedisTestInstance')
#         cls.XTRACTER_CONTAINER = Container(IMAGE_XTRACTER, 'XtracterTestInstance')
#         cls.REDIS_CONTAINER.run(extra_args=["-p", "127.0.0.1:6379:6379"])
#         cls.XTRACTER_CONTAINER.run(extra_args=["--net=host"])
#
#     @classmethod
#     def tearDownClass(cls):
#         cls.XTRACTER_CONTAINER.destroy()
#         cls.REDIS_CONTAINER.destroy()
#
#     def setUp(self):
#         self.redis_task_client = RedisQueueClient(REDIS_TASK_QUEUE_NAME)
#         self.redis_results_client = RedisQueueClient(REDIS_RESULT_QUEUE_NAME)
#         assert_that(self.redis_task_client.length()).is_equal_to(0)
#         assert_that(self.redis_results_client.length()).is_equal_to(0)
#
#     def tearDown(self):
#         self.redis_task_client.clear()
#         self.redis_results_client.clear()
#
#     def test_should_take_task_and_extract_features_from_test_file(self):
#         self._add_test_file_task()
#         assert_that(self.redis_task_client.length()).is_equal_to(1)
#         sleep(TASK_TAKE_TIME)
#         assert_that(self.redis_task_client.length()).is_equal_to(0)
#         assert_that(self._keep_polling_for_results_until_timeout()).is_true()
#
#     def _add_test_file_task(self):
#         remote_file_meta = RemoteFileMeta(B2_TEST_FILE_PATH, 0, 0)
#         remote_file_source = create_b2_source_config(B2_ACCOUNT_ID, B2_APPLICATION_KEY, B2_RESOURCES_BUCKET)
#         task = AnalysisTask(remote_file_meta, remote_file_source)
#         self.redis_task_client.add(task.to_dict())
#
#     def _keep_polling_for_results_until_timeout(self):
#         analysis_time = 0
#         interval_time = 3
#         while analysis_time < ANALYSIS_TIMEOUT:
#             if self.redis_results_client.length() > 0:
#                 print("Results appeared after {} seconds!".format(analysis_time))
#                 print("Xtracter logs: {}".format(self.XTRACTER_CONTAINER.logs()))
#                 return True
#             else:
#                 analysis_time += interval_time
#                 sleep(interval_time)
#                 print("Waiting for results next {} seconds...".format(interval_time))
#         print("Results did not come up within {} seconds!".format(ANALYSIS_TIMEOUT))
#         print("Xtracter log: {}".format(self.XTRACTER_CONTAINER.logs()))
#         print("Redis log: {}".format(self.REDIS_CONTAINER.logs()))
#         return False
