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

import collections
from collections.abc import Iterator
import contextlib
import dataclasses
import enum
import importlib.resources
import math
import os
import pathlib
import platform
import subprocess
import uuid

import grpc

from ansys.tools.local_product_launcher.helpers.grpc import check_grpc_health
from ansys.tools.local_product_launcher.helpers.ports import find_free_ports
from ansys.tools.local_product_launcher.interface import (
    METADATA_KEY_DOC,
    METADATA_KEY_NOPROMPT,
    LauncherProtocol,
    ServerType,
)


def has_sudo_permissions():
    """Check if the user has sudo permissions."""
    if platform.system() == "Windows":
        return False
    try:
        # Run 'sudo -l' to list user's sudo privileges
        result = subprocess.run(  # noqa: F841
            ["sudo", "-l"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:  # noqa: F841
        return False


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


def check_docker_compose_installed():
    """Check if Docker Compose is installed."""
    try:
        result = subprocess.run(  # noqa: F841
            ["docker-compose", "--version"], capture_output=True, text=True, check=True
        )
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False


def check_podman_compose_installed():
    """Check if Podman Compose is installed."""
    try:
        result = subprocess.run(  # noqa: F841
            ["podman-compose", "--version"], capture_output=True, text=True, check=True
        )
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False


class ServerKey(str, enum.Enum):
    """Keys for the servers launched through docker compose."""

    MAIN = "main"
    FILE_TRANSFER = "file_transfer"


__all__ = ["DockerComposeLaunchConfig"]


def _get_default_license_server() -> str:
    try:
        return os.environ["ANSYSLMD_LICENSE_FILE"]
    except KeyError:
        return ""


@dataclasses.dataclass
class DockerComposeLaunchConfig:
    """Configuration options for launching Fluent through docker compose."""

    image_name_fluent: str = dataclasses.field(
        default="ghcr.io/ansys/pyfluent:latest",
        metadata={METADATA_KEY_DOC: "Docker image running the Fluent gRPC server."},
    )
    image_name_filetransfer: str = dataclasses.field(
        default="ghcr.io/ansys/tools-filetransfer:latest",
        metadata={METADATA_KEY_DOC: "Docker image running the file transfer service."},
    )
    license_server: str = dataclasses.field(
        default=_get_default_license_server(),
        metadata={
            METADATA_KEY_DOC: (
                "License server passed to the container as "
                "'ANSYSLMD_LICENSE_FILE' environment variable."
            )
        },
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
    environment_variables: dict[str, str] = dataclasses.field(
        default_factory=dict,
        metadata={
            METADATA_KEY_DOC: (
                "Additional environment variables passed to docker compose. These take "
                "precedence over environment variables defined through another configuration "
                "option (for example 'license_server' which defines 'ANSYSLMD_LICENSE_FILE') "
                "or the pre-existing environment variables."
            ),
            METADATA_KEY_NOPROMPT: True,
        },
    )


class DockerComposeLauncher(LauncherProtocol[DockerComposeLaunchConfig]):
    """Launch Fluent through docker compose."""

    CONFIG_MODEL = DockerComposeLaunchConfig
    SERVER_SPEC = {
        ServerKey.MAIN: ServerType.GRPC,
        ServerKey.FILE_TRANSFER: ServerType.GRPC,
    }

    def __init__(self, *, container_dict, config: DockerComposeLaunchConfig):
        self._compose_name = f"pyfluent_compose_{uuid.uuid4().hex}"
        self._urls: dict[str, str]
        self._docker_available = check_docker_installed()
        self._podman_available = check_podman_installed()
        self._docker_compose_available = check_docker_compose_installed()
        self._podman_compose_available = check_podman_compose_installed()
        self._container_dict = container_dict

        try:
            import ansys.tools.filetransfer  # noqa
        except ImportError as err:
            raise ImportError(
                "The 'ansys.tools.filetransfer' module is needed to launch Fluent via docker-compose."
            ) from err

        cmd_str = " ".join(self._container_dict["command"])
        self._env = {}
        self._env.update(
            IMAGE_NAME_FLUENT=self._container_dict["fluent_image"],
            IMAGE_NAME_FILETRANSFER=config.image_name_filetransfer,
            MOUNT_SOURCE=self._container_dict["mount_source"],
            FLUENT_COMMAND=cmd_str,
            FLUENT_PORT=str(self._container_dict["fluent_port"]),
        )
        self._env.update(self._container_dict["environment"])
        self._env.update(config.environment_variables)
        self._keep_volume = config.keep_volume

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

        if has_sudo_permissions():
            self._compose_cmds.insert(0, "sudo")

        return self._compose_cmds

    def _set_compose_cmd(self):
        """Sets the specific compose command based on available tools and permissions."""

        if self._docker_compose_available and self._podman_compose_available:
            self._compose_cmd = ["docker-compose"]
        elif self._docker_compose_available:
            self._compose_cmd = ["docker-compose"]
        elif self._podman_compose_available:
            self._compose_cmd = ["podman-compose"]
        else:
            self._compose_cmd = []  # No available commands

        if has_sudo_permissions():
            self._compose_cmd.insert(0, "sudo")

        return self._compose_cmd

    @contextlib.contextmanager
    def _get_compose_file(self) -> Iterator[pathlib.Path]:
        if self._compose_file is not None:
            yield self._compose_file
        else:
            with importlib.resources.path(
                "ansys.fluent.core.docker", "docker-compose.yaml"
            ) as compose_file:
                yield compose_file

    def start(self) -> None:
        """Start the services."""
        with self._get_compose_file() as compose_file:
            port_ft = find_free_ports(1)
            self._urls = {
                ServerKey.MAIN: f"localhost:{self._container_dict['fluent_port']}",
                ServerKey.FILE_TRANSFER: f"localhost:{port_ft[0]}",
            }

            env = collections.ChainMap(
                {"PORT_FILETRANSFER": str(port_ft[0])},
                self._env,
            )

            # The compose_file may be temporary, in particular if the package is a zipfile.
            # To avoid it being deleted before docker compose has read it, we use the '--wait'
            # flag for 'docker compose'.
            cmd = [
                "-f",
                str(compose_file.resolve()),
                "--project-name",
                self._compose_name,
                "up",
                "--detach",
                "--wait",
            ]

            try:
                # Prefer docker-compose or podman-compose
                output = subprocess.Popen(  # noqa: F841
                    self._set_compose_cmd() + cmd,
                    env=env,
                    stderr=subprocess.STDOUT,
                )
            except subprocess.CalledProcessError as e:  # noqa: F841
                output = subprocess.Popen(  # noqa: F841
                    self._set_compose_cmds() + cmd,
                    env=env,
                    stderr=subprocess.STDOUT,
                )
                # print(f"Command failed with exit code {e.returncode}")
                # print(f"Output: {e.output.decode()}")

    def stop(self, *, timeout: float | None = None) -> None:
        """Stop the services."""
        # The compose file needs to be passed for all commands with docker-compose 1.X.
        # With docker-compose 2.X, this no longer seems to be necessary.
        with self._get_compose_file() as compose_file:
            cmd = self._compose_cmds + [
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
            subprocess.check_call(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

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
