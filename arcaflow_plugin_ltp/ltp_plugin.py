#!/usr/bin/env python3

import sys
import typing
import sys
import typing
import tempfile
import subprocess
import os
import yaml
from arcaflow_plugin_sdk import plugin
from ltp_schema import (
    TestArguments
    LtpGlobalParams
    TestError
    testslist_schemas
    TestResults
)

@plugin.step(
    id="run-ltp-realtime",
    name="LTP realtime tests",
    description="Run LTP realtime test with the arguments provided",
    outputs={"success": TestResults, "error": TestError},
)
def run_ltp_realtime(
    params: LtpGlobalParams,
) -> typing.Tuple[str, typing.Union[TestResults, TestError]]:
    """The function is the implementation for the step. It needs the decorator
    above to make it into a step. The type hints for the params are required.

    :param params:

    :return: the string identifying which output it is, as well the output
        structure
    """
    # print("===>> Generating job file ...")
    # result = params.to_jobfile()
    ltp_realtime_cmd = ["/opt/ltp/testcases/run.sh",
                        "-t"
                        params.test_argument,
                        "-l",
                        params.loop,
    ]

    print("==>> Running stress-ng with the temporary jobfile...")
    # Check if logs directory exists
    path.mkdir("/root/ltp/testcases/realtime/logs/", exist_ok=True)
    logdir = "/root/ltp/testcases/realtime/logs/"
    try:
        print(
            subprocess.check_output(
                ltp_realtime_cmd,
                cwd=logdir,
                text=True,
                stderr=subprocess.STDOUT,
            )
        )
    except subprocess.CalledProcessError as error:
        return "error", TestError(
            f"""{error.cmd[0]} failed with return code
                {error.returncode}:\n{error.output}"""
        )

    """ Process log files here, depending on test selected there might be multiple files 
        Test with pi-tests testcases """

    return "success", TestOutput("Need to get this to work!!!")


if __name__ == "__main__":
    sys.exit(
        plugin.run(
            plugin.build_schema(
                # List your step functions here:
                run_ltp_realtime,
            )
        )
    )
