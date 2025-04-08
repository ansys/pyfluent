"""Launch Fluent through docker compose."""

# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from collections.abc import Iterator
import contextlib
import dataclasses
import enum
import importlib.resources
import math
import os
import pathlib
from pathlib import Path
import subprocess
import uuid

import grpc

from ansys.tools.local_product_launcher.helpers.grpc import check_grpc_health
from ansys.tools.local_product_launcher.interface import (
    METADATA_KEY_DOC,
    METADATA_KEY_NOPROMPT,
    LauncherProtocol,
    ServerType,
)

__all__ = ["DockerComposeLaunchConfig"]


def check_docker_installed():
    """Check if Docker is installed."""
    try:
        result = subprocess.run(  # noqa: F841
            ["docker", "--version"], capture_output=True, text=True, check=True
        )
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False


def check_podman_installed():
    """Check if Podman is installed."""
    try:
        result = subprocess.run(  # noqa: F841
            ["podman", "--version"], capture_output=True, text=True, check=True
        )
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False


class ServerKey(str, enum.Enum):
    """Keys for the servers launched through docker compose."""

    MAIN = "main"


@dataclasses.dataclass
class DockerComposeLaunchConfig:
    """Configuration options for launching Fluent through docker compose."""

    image_name_fluent: str = dataclasses.field(
        default="ghcr.io/ansys/pyfluent:latest",
        metadata={METADATA_KEY_DOC: "Docker image running the Fluent gRPC server."},
    )
    keep_volume: bool = dataclasses.field(
        default=False,
        metadata={
            METADATA_KEY_DOC: "If true, keep the volume after docker compose is stopped."
        },
    )
    compose_file: str | None = dataclasses.field(
        default=None,
        metadata={
            METADATA_KEY_DOC: (
                "Docker compose file used to start the services. Uses the "
                "'docker-compose.yaml' shipped with PyFluent by default."
            ),
            METADATA_KEY_NOPROMPT: True,
        },
    )


def _write_yaml_config(compose_name, container_dict, cmd_str):
    """
    Writes a YAML configuration file for a Docker Compose setup.

    Parameters
    ----------
    compose_name: str
        The name of the compose file (without extension).
    container_dict: dict
        A dictionary containing container configuration.
    cmd_str: str
        The command to run in the container.
    """
    yaml_file_path = Path(__file__).parents[0] / f"{compose_name}.yaml"

    with open(yaml_file_path, "w") as comp_file:
        comp_file.write("networks:\n")
        comp_file.write(f"  {compose_name}_network:\n")
        comp_file.write("    external: true\n\n")
        comp_file.write("services:\n")
        comp_file.write("  fluent:\n")
        comp_file.write(
            f"    image: {container_dict.get('fluent_image', 'default_image_name')}\n"
        )
        comp_file.write("    networks:\n")
        comp_file.write(f"      - {compose_name}_network\n")
        comp_file.write("    environment:\n")
        for env_var, value in container_dict["environment"].items():
            comp_file.write(f"      - {env_var}={value}\n")
        comp_file.write(f"    command: {cmd_str}\n")
        comp_file.write("    ports:\n")
        if not container_dict.get("ports"):
            comp_file.write(
                f"      - {container_dict['fluent_port']}:{container_dict['fluent_port']}\n"
            )
        else:
            for _, port in container_dict["ports"].items():
                comp_file.write(f"      - {port}:{port}\n")
        comp_file.write(f"    working_dir: {container_dict['mount_target']}\n")
        comp_file.write("    volumes:\n")
        comp_file.write(
            f"      - {container_dict['mount_source']}:{container_dict['mount_target']}\n"
        )


def _extract_ports(port_string):
    """
    Extracts ports from a string containing port mappings.

    Parameters
    ----------
    port_string: str
        A string containing port mappings.

    Returns
    -------
    ports: list
        A list of extracted ports.
    """
    ports = []
    for line in port_string.split("\n"):
        if line:
            _, target = line.split("->")
            port = target.split(":")[1]
            ports.append(port)
    return [port for port in ports if port.isdigit()]


class DockerComposeLauncher(LauncherProtocol[DockerComposeLaunchConfig]):
    """Launch Fluent through docker compose."""

    CONFIG_MODEL = DockerComposeLaunchConfig
    SERVER_SPEC = {ServerKey.MAIN: ServerType.GRPC}

    def __init__(self, *, container_dict, config: DockerComposeLaunchConfig):
        self._compose_name = f"pyfluent_compose_{uuid.uuid4().hex}"
        self._urls: dict[str, str]
        self._docker_available = check_docker_installed()
        self._podman_available = check_podman_installed()
        self._container_dict = container_dict
        self._keep_volume = config.keep_volume

        cmd_str = " ".join(self._container_dict["command"])
        self._container_source = self._set_compose_cmds()
        self._container_source.remove("compose")

        network = subprocess.check_call(  # noqa: F841
            self._container_source
            + ["network", "create", f"{self._compose_name}_network"],
        )

        _write_yaml_config(self._compose_name, self._container_dict, cmd_str)

        if config.compose_file is not None:
            self._compose_file: pathlib.Path | None = pathlib.Path(config.compose_file)
        else:
            self._compose_file = None

    def _set_compose_cmds(self):
        """Sets the compose commands based on available tools and permissions."""

        # Determine the compose command
        if self._docker_available and self._podman_available:
            self._compose_cmds = ["docker", "compose"]
        elif self._docker_available:
            self._compose_cmds = ["docker", "compose"]
        elif self._podman_available:
            self._compose_cmds = ["podman", "compose"]
        else:
            self._compose_cmds = []

        return self._compose_cmds

    @contextlib.contextmanager
    def _get_compose_file(self) -> Iterator[pathlib.Path]:
        if self._compose_file is not None:
            yield self._compose_file
        else:
            with importlib.resources.path(
                "ansys.fluent.core.docker", f"{self._compose_name}.yaml"
            ) as compose_file:
                yield compose_file

    def check_image_exists(self, image_name: str | None = None) -> bool:
        """Check if a Docker image exists locally."""
        image_name = (
            image_name
            if image_name
            else f"ghcr.io/ansys/pyfluent:{os.getenv('FLUENT_IMAGE_TAG')}"
        )
        try:
            output = subprocess.check_output(["docker", "images", "-q", image_name])
            return output.decode("utf-8").strip() != ""
        except subprocess.CalledProcessError as e:  # noqa: F841
            return False

    def pull_image(self, image_name: str | None = None) -> None:
        """Pull a Docker image if it does not exist locally."""
        image_name = (
            image_name
            if image_name
            else f"ghcr.io/ansys/pyfluent:{os.getenv('FLUENT_IMAGE_TAG')}"
        )
        try:
            output = subprocess.check_call(["docker", "pull", image_name])  # noqa: F841
        except subprocess.CalledProcessError as e:
            print(f"Failed to pull image: {e}")

    def start(self) -> None:
        """Start the services."""

        with self._get_compose_file() as compose_file:
            self._urls = {
                ServerKey.MAIN: f"localhost:{self._container_dict['fluent_port']}",
            }

            cmd = [
                "-f",
                str(compose_file.resolve()),
                "--project-name",
                self._compose_name,
                "up",
                "--detach",
            ]

            output = subprocess.check_call(  # noqa: F841
                self._set_compose_cmds() + cmd,
            )

    def stop(self, *, timeout: float | None = None) -> None:
        """Stop the services."""
        # The compose file needs to be passed for all commands with docker-compose 1.X.
        # With docker-compose 2.X, this no longer seems to be necessary.
        with self._get_compose_file() as compose_file:
            cmd = [
                "-f",
                str(compose_file),
                "--project-name",
                self._compose_name,
                "down",
            ]
            if timeout is not None:
                # --timeout must be an integer, so we round up.
                cmd.extend(["--timeout", str(math.ceil(timeout))])
            if not self._keep_volume:
                cmd.append("--volumes")

            output = subprocess.check_call(  # noqa: F841
                self._set_compose_cmds() + cmd,
            )

    def remove_network(self) -> None:
        """Remove the services."""

        cmd = ["network", "rm", "-f", f"{self._compose_name}_network"]

        try:
            output = subprocess.check_call(  # noqa: F841
                self._container_source + cmd,
            )
        except subprocess.CalledProcessError as e:  # noqa: F841
            pass

    def remove_compose_file(self) -> None:
        """Remove the compose file."""
        file_path = Path(__file__).parents[0] / f"{self._compose_name}.yaml"
        file_path.unlink(missing_ok=True)

    def exit(self) -> None:
        """Exit the container launcher."""
        self.stop()
        self.remove_network()
        # self.remove_compose_file()

    def check(self, timeout: float | None = None) -> bool:
        """Check if the services are running."""
        for url in self.urls.values():
            channel = grpc.insecure_channel(url)
            if not check_grpc_health(channel=channel, timeout=timeout):
                return False
        return True

    @property
    def urls(self) -> dict[str, str]:
        """Return the URLs of the launched services."""
        return self._urls

    @property
    def ports(self) -> list[str]:
        """Return the URLs of the launched services."""
        output = subprocess.check_output(
            self._container_source + ["port", f"{self._compose_name}-fluent-1"],
        )
        return _extract_ports(output.decode("utf-8").strip())
