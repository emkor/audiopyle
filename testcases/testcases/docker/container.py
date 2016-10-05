import os
import subprocess
from datetime import datetime
from time import sleep

from commons.utils.conversion import utc_datetime_to_timestamp
from testcases.docker.utils import ContainerException, IMAGE_XTRACTER, IMAGE_REDIS, build_commands_string


class Container(object):
    BOOT_TIMEOUT = 60
    FNULL = open(os.devnull, 'w')

    def __init__(self, image_name, container_name):
        """
        :type image_name: str
        :type container_name: str
        """
        self.image_name = image_name
        self.container_name = container_name

    def run(self, wait_until_ready=True, extra_args=None):
        """
        :type wait_until_ready: bool
        :type extra_args: list
        """
        try:
            if self._container_already_exists():
                self.destroy()
            commands_list = ["docker", "run"] + (extra_args or []) + ["--name", self.container_name, self.image_name]
            print("Running container: {} based on image: {} using command: {}...".format(self.container_name,
                                                                                         self.image_name,
                                                                                         build_commands_string(
                                                                                             commands_list)))
            subprocess.Popen(commands_list, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            raise ContainerException(e,
                                     "Could not run container: {} from image {}.".format(self.container_name,
                                                                                         self.image_name))
        if wait_until_ready:
            self._wait_until_ready()

    def logs(self):
        """
        :rtype: str
        """
        try:
            return subprocess.check_output(["docker", "logs", self.container_name], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            raise ContainerException(e, "Could not check logs of a container named {}.".format(self.container_name))

    def stop(self):
        try:
            print("Stopping container: {}...".format(self.container_name))
            subprocess.call(["docker", "stop", self.container_name], stdout=self.FNULL, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            raise ContainerException(e, "Could not stop container named {}".format(self.container_name))

    def destroy(self):
        try:
            print("Destroying container: {}...".format(self.container_name))
            if self.is_running():
                self.stop()
            subprocess.call(
                ["docker", "rm", self.container_name],
                stdout=self.FNULL,
                stderr=subprocess.STDOUT
            )
        except subprocess.CalledProcessError as e:
            raise ContainerException(e, "Could not destroy container: {}".format(self.container_name, e))

    def status(self):
        """
        :rtype: str
        """
        try:
            return self._run_status_command()
        except subprocess.CalledProcessError as e:
            raise ContainerException(e, "Could not check status of a container: {}".format(self.container_name))

    def is_running(self):
        status = self.status().lower().strip()
        return status == "running"

    def _wait_until_ready(self):
        start_timestamp = utc_datetime_to_timestamp(datetime.now())
        is_container_running = False
        while not is_container_running and utc_datetime_to_timestamp(
                datetime.now()) - start_timestamp < self.BOOT_TIMEOUT:
            sleep(1)
            is_container_running = self.is_running()
        if not is_container_running:
            raise Exception("Container was not ready after {} seconds.".format(self.BOOT_TIMEOUT))

    def _container_already_exists(self):
        try:
            self._run_status_command()
        except subprocess.CalledProcessError as e:
            exception_message = e.output.lower()
            already_exists = "no such" not in exception_message
            return already_exists

    def _run_status_command(self):
        return subprocess.check_output(
            ["docker", "inspect", "-f", "{{.State.Status}}", self.container_name],
            stderr=subprocess.STDOUT
        )

xtracter_container = Container(IMAGE_XTRACTER, "test-xtracter")
xtracter_container.run(wait_until_ready=True, extra_args=["--net=host"])
print("AAA")
print(xtracter_container.logs())
redis_container = Container(IMAGE_REDIS, "test-redis")
redis_container.run(extra_args=["-p", "127.0.0.1:6379:6379"])
print("BBB")
print(xtracter_container.logs())
print("CCC")
xtracter_container.destroy()
print("DDD")
redis_container.destroy()
print("EEE")
