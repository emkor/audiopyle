import pymysql

from commons.service.file_accessor import FileAccessor
from commons.service.os_env_accessor import OsEnvAccessor

class DbInitializer(object):
    def __init__(self, db_access):
        self.db_access = db_access

    def run(self):
        if self._is_initialized():
            print("Database is already initialized! Doing nothing.")
        else:
            try:
                self._initialize()
            except Exception as e:
                print("Error occured on initialization. Details: {}".format(e))

    def _is_initialized(self):
        with pymysql.connect(charset='utf8', **self.db_access.__dict__) as cursor:
            response = cursor.execute(
                "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'audiopyle'")
            return response == 1

    def _initialize(self):
        ddl_script = self._read_dll_script()
        if ddl_script:
            with pymysql.connect(charset='utf8', **self.db_access.__dict__) as cursor:
                cursor.execute(ddl_script)
        else:
            raise ValueError("Could not read SQL DDL script.")

    def _read_dll_script(self):
        home_dir = OsEnvAccessor.get_env_variable("AUDIOPYLE_HOME")
        sql_ddl_file_path = FileAccessor.join(home_dir, "persister", "devops", "ddl_script.sql")
        if FileAccessor.is_file(sql_ddl_file_path):
            with open(sql_ddl_file_path) as sql_ddl_file:
                output = sql_ddl_file.readlines()
            single_output = ''.join(output)
            prepared_output = single_output.replace("\n", " ").replace("  ", " ")
            return prepared_output
        else:
            print("Could not find SQL DDL script under: {}".format(sql_ddl_file_path))
            return None
