# usage
# 1. edit any env vars below
# 2. in python run
#    >>> exec(open("hackathon.py").read())

import os

import ansys.fluent.core as pyfluent

os.environ["PYFLUENT_LAUNCH_CONTAINER"] = "1"
os.environ["FLUENT_IMAGE_TAG"] = "latest"
os.environ["ANSYSLMD_LICENSE_FILE"] = "1055@leblnxlic64.ansys.com"
os.environ["PYFLUENT_CONTAINER_MOUNT_PATH"] = "/testing"

solver = pyfluent.launch_fluent(start_instance=False)
