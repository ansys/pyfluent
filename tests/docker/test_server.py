import os
import subprocess
from time import sleep


def test_fluent_server():
    license_server = os.getenv("LICENSE_SERVER", "leblnxlic64.ansys.com")
    subprocess.run(["docker", "run", "-d", "--rm", "-p", "63084:63084",
                    "-e", f"ANSYSLMD_LICENSE_FILE=1055@{license_server}",
                    "-e", "REMOTING_PORTS=63084/portspan=2",
                    "-e", "FLUENT_LAUNCHED_FROM_PYFLUENT=1",
                    "ghcr.io/pyansys/pyfluent", "3ddp", "-g",
                    "-sifile=server.txt"])
    sleep(60)
    from ansys.fluent.core.session import Session
    session = Session("localhost", 63084)
    assert session.check_health() == "SERVING"
    session.exit()
