"""Create .env file for docker-compose.yml."""

import os
from pathlib import Path

with open(".env", "w") as f:
    f.write(f"FLUENT_IMAGE={os.getenv('FLUENT_IMAGE')}\n")
    f.write(f"ANSYSLMD_LICENSE_FILE={os.getenv('ANSYSLMD_LICENSE_FILE')}\n")
    f.write(f"MOUNT_SOURCE={os.getenv('MOUNT_SOURCE', Path(os.getcwd()).resolve())}\n")
