"""
Pull a Fluent Docker image based on the FLUENT_IMAGE_TAG environment variable.
"""

import subprocess
import time

from ansys.fluent.core import config
from ansys.fluent.core.docker.utils import get_ghcr_fluent_image_name


def pull_fluent_image():
    """Pull Fluent Docker image and clean up dangling images.

    Raises
    ------
    subprocess.CalledProcessError
        If the cleanup script fails to execute.
    """
    max_retries = 3
    fluent_image_tag = config.fluent_image_tag
    image_name = get_ghcr_fluent_image_name(fluent_image_tag)
    separator = "@" if fluent_image_tag.startswith("sha256") else ":"
    full_image_name = f"{image_name}{separator}{fluent_image_tag}"
    for attempt in range(max_retries):
        try:
            subprocess.run(["docker", "pull", full_image_name], check=True)
            break  # Success! Exit the loop.
        except subprocess.CalledProcessError as e:
            if attempt < max_retries - 1:
                print(
                    f"Pull failed due to rate limits. Retrying in 2 seconds... (Attempt {attempt + 1}/{max_retries})"
                )
                time.sleep(2)
            else:
                raise e
    subprocess.run(["docker", "pull", full_image_name], check=True)
    subprocess.run(["docker", "image", "prune", "-f"], check=True)


if __name__ == "__main__":
    pull_fluent_image()
