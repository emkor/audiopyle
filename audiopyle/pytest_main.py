#!/usr/bin/env python3

import pytest

from audiopyle.lib.utils.logger import setup_logger


def main():
    setup_logger()
    pytest.main(["--pyargs", "audiopyle.testcases"])


if __name__ == "__main__":
    main()
