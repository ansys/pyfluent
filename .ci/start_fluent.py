import os
import subprocess
import sys
import tempfile
import time

from ansys.fluent.core import EXAMPLES_PATH


def start_fluent_container(args):
    fd, sifile = tempfile.mkstemp(
        suffix=".txt", prefix="serverinfo-", dir=EXAMPLES_PATH
    )
    os.close(fd)
    timeout = 100
    license_server = os.environ["ANSYSLMD_LICENSE_FILE"]
    port = os.environ["PYFLUENT_FLUENT_PORT"]

    subprocess.run(["docker", "run", "--name", "fluent_server", "-d", "--rm",
                    "-p", f"{port}:{port}",
                    "-v", f"{EXAMPLES_PATH}:{EXAMPLES_PATH}",
                    "-e", f"ANSYSLMD_LICENSE_FILE={license_server}",
                    "-e", f"REMOTING_PORTS={port}/portspan=2",
                    "-e", "FLUENT_LAUNCHED_FROM_PYFLUENT=1",
                    "ghcr.io/pyansys/pyfluent",
                    "-g", f"-sifile={sifile}"] + args)

    sifile_last_mtime = os.stat(sifile).st_mtime
    while True:
        if os.stat(sifile).st_mtime > sifile_last_mtime:
            time.sleep(1)
            break
        if timeout == 0:
            break
        time.sleep(1)
        timeout -= 1
    if os.path.exists(sifile):
        os.remove(sifile)


if __name__ == "__main__":
    start_fluent_container(sys.argv[1:])
