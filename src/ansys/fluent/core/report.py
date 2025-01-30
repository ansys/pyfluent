# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""ansys-tools-report."""

import ansys.tools.report as pyansys_report

ANSYS_ENV_VARS = [
    "ANSYSLMD_LICENSE_FILE",
    "AWP_ROOT<NNN>",
    "FLUENT_CONTAINER_IMAGE",
    "FLUENT_IMAGE_NAME",
    "FLUENT_IMAGE_TAG",
    "PYFLUENT_CODEGEN_OUTDIR",
    "PYFLUENT_CODEGEN_SKIP_BUILTIN_SETTINGS",
    "PYFLUENT_CONTAINER_MOUNT_SOURCE",
    "PYFLUENT_CONTAINER_MOUNT_TARGET",
    "PYFLUENT_FLUENT_DEBUG",
    "PYFLUENT_DOC_SKIP_CHEATSHEET:",
    "PYFLUENT_DOC_SKIP_EXAMPLES",
    "PYFLUENT_FLUENT_IP",
    "PYFLUENT_FLUENT_PORT",
    "PYFLUENT_FLUENT_ROOT",
    "PYFLUENT_GRPC_LOG_BYTES_LIMIT",
    "PYFLUENT_LAUNCH_CONTAINER",
    "PYFLUENT_LOGGING",
    "PYFLUENT_NO_FIX_PARAMETER_LIST_RETURN",
    "PYFLUENT_SHOW_SERVER_GUI",
    "PYFLUENT_SKIP_API_UPGRADE_ADVICE",
    "PYFLUENT_TIMEOUT_FORCE_EXIT",
    "PYFLUENT_WATCHDOG_DEBUG",
    "PYFLUENT_WATCHDOG_EXCEPTION_ON_ERROR",
    "REMOTING_PORTS",
    "REMOTING_SERVER_ADDRESS",
    "SERVER_INFO_DIR",
]

dependencies = {
    "ansys-api-fluent": "0.3.34",
    "ansys-platform-instancemanagement": "1.1",
    "ansys-tools-filetransfer": "0.1,<0.3",
    "ansys-units": "0.3.3,<0.5",
    "docker": "7.1.0",
    "grpcio": "1.30.0",
    "grpcio-health-checking": "1.30.0",
    "grpcio-status": "1.30.0",
    "h5py": "3.12.1",
    "lxml": "4.9.2",
    "nltk": "3.9.1",
    "numpy": "1.14.0,<3.0.0",
    "pandas": "1.1.0,<2.3",
    "pyansys-tools-report": "0.8.1",
    "pyyaml": "6.0",
}

if __name__ == "__main__":
    rep = pyansys_report.Report(ansys_libs=dependencies, ansys_vars=ANSYS_ENV_VARS)
    print(rep)
