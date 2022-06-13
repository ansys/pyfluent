import os

import docker

_IMAGE_TAG = os.getenv("FLUENT_IMAGE_TAG", "latest")
_IMAGE_NAME = f"ghcr.io/pyansys/pyfluent:{_IMAGE_TAG}"


def _is_newer_version_available(client: docker.DockerClient):
    try:
        local_image = client.images.get(name=_IMAGE_NAME)
    except docker.errors.ImageNotFound:
        return True

    local_image_digest = local_image.attrs.get("RepoDigests")[0].split("@")[-1]
    remote_image_digest = client.images.get_registry_data(name=_IMAGE_NAME).id
    return remote_image_digest != local_image_digest


def _pull_image(client: docker.DockerClient):
    if _is_newer_version_available(client=client):
        try:
            client.images.remove(image=_IMAGE_NAME, force=True)
        except docker.errors.ImageNotFound:
            pass
        client.images.pull(repository=_IMAGE_NAME)


if __name__ == "__main__":
    client = docker.from_env()
    _pull_image(client=client)
