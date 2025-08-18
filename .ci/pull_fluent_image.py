"""
Pull a Fluent Docker image based on the FLUENT_IMAGE_TAG environment variable.
"""

import subprocess

from ansys.fluent.core import config
from ansys.fluent.core.docker.utils import get_ghcr_fluent_image_name


def pull_fluent_image():
    """Pull Fluent Docker image and clean up dangling images."""
    fluent_image_tag = config.fluent_image_tag
    image_name = get_ghcr_fluent_image_name(fluent_image_tag)
    separator = "@" if fluent_image_tag.startswith("sha256") else ":"
    full_image_name = f"{image_name}{separator}{fluent_image_tag}"
    subprocess.run(["docker", "pull", full_image_name], check=True)
    subprocess.run(["docker", "image", "prune", "-f"], check=True)


if __name__ == "__main__":
    pull_fluent_image()
