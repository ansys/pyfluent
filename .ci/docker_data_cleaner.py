"""
Script to clean up all docker data except for specified images.
Run this script before and after each job that starts the Fluent docker container.
Must set the FLUENT_STABLE_IMAGE_DEV environment variable to the dev image sha256 value.
"""

import os
import subprocess

IMAGE_TAGS_TO_RETAIN = ["v24.2.5", "v25.1.4", "v25.2.3"]


def clean_docker_data():
    """Cleans up all docker data except for specified images."""
    # Stop and remove all containers
    subprocess.run("docker ps -aq | xargs -r docker rm -f", shell=True, check=True)

    # Remove all images except those in IMAGE_TAGS_TO_RETAIN
    images_to_retain = [f"ghcr.io/ansys/fluent:{tag}" for tag in IMAGE_TAGS_TO_RETAIN]
    dev_image_sha = os.environ["FLUENT_STABLE_IMAGE_DEV"]
    images_output = subprocess.check_output(
        "docker images --format '{{.Repository}}:{{.Tag}} {{.ID}}' --no-trunc",
        shell=True,
    ).decode()
    for line in images_output.splitlines():
        image, image_id = line.split()
        if image not in images_to_retain and image_id != dev_image_sha:
            subprocess.run(f"docker rmi -f {image_id}", shell=True, check=True)

    # Remove dangling images
    subprocess.run("docker image prune -f", shell=True, check=True)

    # Remove everything else (networks, volumes)
    subprocess.run("docker system prune -f --volumes", shell=True, check=True)


if __name__ == "__main__":
    clean_docker_data()
