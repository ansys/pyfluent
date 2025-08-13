"""
Pull a Fluent Docker image based on the FLUENT_IMAGE_TAG environment variable.
"""

import os
import subprocess

from ansys.fluent.core.docker.utils import get_ghcr_fluent_image_name


def pull_fluent_image():
    """Pull Fluent Docker image and clean up dangling images."""
    fluent_image_tag = os.getenv("FLUENT_IMAGE_TAG", "latest")
    image_name = (
        f"ghcr.io/ansys/pyfluent@{fluent_image_tag}"
        if fluent_image_tag.startswith("sha256")
        else f"{get_ghcr_fluent_image_name(fluent_image_tag)}:{fluent_image_tag}"
    )
    subprocess.run(["docker", "pull", image_name], check=True)
    subprocess.run(["docker", "image", "prune", "-f"], check=True)


if __name__ == "__main__":
    pull_fluent_image()
