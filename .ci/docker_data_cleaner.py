"""
Script to clean up all docker data except for specified images.
Run this script before and after each job that starts the Fluent docker container.
Must set the FLUENT_STABLE_IMAGE_DEV environment variable to the dev image sha256 value.
"""

import os
import subprocess

IMAGE_TAGS_TO_RETAIN = ["v24.2.5", "v25.1.4", "v25.2.3", "v26.1.latest"]


def clean_docker_data():
    """Cleans up all docker data except for specified images.

    Raises
    ------
    OSError
        If FLUENT_STABLE_IMAGE_DEV environment variable is not set.
    """
    # Stop and remove all containers
    container_ids = subprocess.check_output(["docker", "ps", "-aq"]).decode().split()
    for container_id in container_ids:
        subprocess.run(["docker", "rm", "-f", container_id], check=True)

    # Remove all images except those in IMAGE_TAGS_TO_RETAIN and the dev image
    images_to_retain = [f"ghcr.io/ansys/fluent:{tag}" for tag in IMAGE_TAGS_TO_RETAIN]
    dev_image_sha = os.getenv("FLUENT_STABLE_IMAGE_DEV")
    if not dev_image_sha:
        raise OSError("FLUENT_STABLE_IMAGE_DEV environment variable is not set.")

    images_output = subprocess.check_output(
        [
            "docker",
            "images",
            "--format",
            "{{.Repository}}:{{.Tag}} {{.ID}}",
            "--no-trunc",
        ]
    ).decode()
    for line in images_output.splitlines():
        image, image_id = line.strip().split()
        if image not in images_to_retain and image_id != dev_image_sha:
            subprocess.run(["docker", "rmi", "-f", image_id], check=True)

    # Remove everything else (networks, volumes)
    subprocess.run(["docker", "system", "prune", "-f", "--volumes"], check=True)


if __name__ == "__main__":
    clean_docker_data()
