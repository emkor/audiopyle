import unittest

from persister.model.db_access_data import DbAccessData
from persister.service.db_connector import DbConnector
from testcases.docker.container import Container
from testcases.docker.utils import IMAGE_MYSQL
import MySQLdb

REDIS_QUEUE_NAME = 'xtracter_tasks'


class DbConnectorIntegrationTest(unittest.TestCase):
    MYSQL_CONTAINER = None
    MYSQL_ROOT_PASSWORD = "arthur"
    MYSQL_DB_NAME = "audiopyle"

    @classmethod
    def setUpClass(cls):
        cls.MYSQL_CONTAINER = Container(IMAGE_MYSQL, 'MySQLTestInstance', default_boot_time=10)
        cls.MYSQL_CONTAINER.run(extra_args=["-p", "127.0.0.1:3306:3306",
                                            "-e", "MYSQL_ROOT_PASSWORD={}".format(cls.MYSQL_ROOT_PASSWORD)
                                            ])

    @classmethod
    def tearDownClass(cls):
        cls.MYSQL_CONTAINER.destroy()

    def setUp(self):
        self.access_data = DbAccessData("root", self.MYSQL_ROOT_PASSWORD)
        self.connector = DbConnector(self.access_data, self.MYSQL_DB_NAME)

    def tearDown(self):
        self.connector.drop_db()

    def test_db_should_not_be_initialized(self):
        db_exists_query = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{}'".format(
            self.MYSQL_DB_NAME)
        result_rows = self._execute_simple_query(db_exists_query)
        self.assertNotIn(self.MYSQL_DB_NAME, self._flatten(result_rows))

    def test_db_should_be_initialized_properly(self):
        self.connector.initialize_db()
        db_exists_query = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{}'".format(
            self.MYSQL_DB_NAME)
        all_tables_query = "SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='{}';".format(self.MYSQL_DB_NAME)

        dbs_list = self._execute_simple_query(db_exists_query)
        self.assertIn(self.MYSQL_DB_NAME, self._flatten(dbs_list))

        table_names = self._execute_simple_query(all_tables_query)
        self.assertIn("plugin", self._flatten(table_names))
        self.assertIn("feature", self._flatten(table_names))
        self.assertIn("track", self._flatten(table_names))

    def test_db_should_be_dropped_properly(self):
        self.connector.initialize_db()
        self.connector.drop_db()
        db_exists_query = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{}'".format(
            self.MYSQL_DB_NAME)
        result_rows = self._execute_simple_query(db_exists_query)
        self.assertNotIn(self.MYSQL_DB_NAME, self._flatten(result_rows))

    def _execute_simple_query(self, query):
        cnx = MySQLdb.connect(host='127.0.0.1', user='root', passwd=self.MYSQL_ROOT_PASSWORD)
        cursor = cnx.cursor()
        cursor.execute(query)
        rows_list = [list(row_values) for row_values in cursor]
        cursor.close()
        cnx.close()
        return rows_list

    def _flatten(self, list_with_sublists):
        return [item for sublist in list_with_sublists for item in sublist]
