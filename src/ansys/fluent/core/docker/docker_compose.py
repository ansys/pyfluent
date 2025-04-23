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

import os
import subprocess
import uuid


class ComposeBasedLauncher:
    """Launch Fluent through docker or Podman compose."""

    def __init__(self, *, container_dict):
        self._compose_name = f"pyfluent_compose_{uuid.uuid4().hex}"
        self._container_dict = container_dict
        self._container_source = self._set_compose_cmds()
        self._container_source.remove("compose")

        # Sudo is required for Podman on Linux
        if self._container_source[0] == "podman" and self._has_sudo_access():
            self._container_source.insert(0, "sudo")
            self._compose_cmds = self._set_compose_cmds()
            self._compose_cmds.insert(0, "sudo")
        else:
            self._compose_cmds = self._set_compose_cmds()

        if "docker" in self._container_source:
            self._compose_cmd = ["docker-compose"]
        elif "podman" in self._container_source:
            self._compose_cmd = ["podman-compose"]

        self._compose_file = self._get_compose_file(container_dict)

    def _get_compose_file(self, container_dict):
        """Generates compose file for the Docker Compose setup.

        Parameters
        ----------
        container_dict: dict
            A dictionary containing container configuration.
        """

        indent = "  "

        if container_dict.get("ports"):
            ports = list(container_dict.get("ports").values())
        else:
            ports = [container_dict.get("fluent_port", "")]

        compose_file = f"""
        services:
          fluent:
            image: {container_dict.get("fluent_image")}
            command: {" ".join(container_dict["command"])}
            working_dir: {container_dict.get("mount_target")}
            volumes:
            {indent}- {container_dict.get("mount_source")}:{container_dict.get("mount_target")}
            ports:
        """

        for port in ports:
            if len(ports) == 1:
                compose_file += f"{indent * 3}- {port}:{port}"
            else:
                if port == ports[0]:
                    compose_file += f"{indent * 3}- {port}:{port}\n"
                elif port == ports[-1]:
                    compose_file += f"{indent * 7}- {port}:{port}"
                else:
                    compose_file += f"{indent * 7}- {port}:{port}\n"

        compose_file_env = f"""
        {indent * 2}environment:
        """

        for key, value in container_dict["environment"].items():
            if key == "ANSYSLMD_LICENSE_FILE":
                compose_file_env += f"""{indent * 3}- {key}={value}\n"""
            else:
                compose_file_env += f"""{indent * 7}- {key}={value}\n"""

        compose_file += compose_file_env

        return compose_file

    def _has_sudo_access(self):
        result = subprocess.run(
            ["sudo", "-n", "true"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return result.returncode == 0

    def _extract_ports(self, port_string):
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

    def _set_compose_cmds(self):
        """Sets the compose commands based on available tools and permissions.

        Raises
        ------
        RuntimeError
            If neither Docker nor Podman is installed.
        """

        # Determine the compose command
        if os.getenv("USE_PODMAN_COMPOSE") == "1":
            self._compose_cmds = ["podman", "compose"]
        elif os.getenv("USE_DOCKER_COMPOSE") == "1":
            self._compose_cmds = ["docker", "compose"]
        else:
            raise RuntimeError("Neither Docker nor Podman is installed.")

        return self._compose_cmds

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
        if len(self._container_source) == 1:
            subprocess.check_call([f"{self._container_source[0]}", "pull", image_name])
        else:
            subprocess.check_call(
                [
                    f"{self._container_source[0]}",
                    f"{self._container_source[1]}",
                    "pull",
                    image_name,
                ]
            )

    def start(self) -> None:
        """Start the services.

        Raises
        -------
        subprocess.CalledProcessError
            If the command fails.
        """

        cmd = [
            "-f",
            "-",
            "--project-name",
            self._compose_name,
            "up",
            "--detach",
        ]

        try:
            # Some Docker and Podman versions support compose
            # So use docker compose or podman compose
            process = subprocess.Popen(
                self._compose_cmds + cmd,
                stdin=subprocess.PIPE,
                text=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            process.communicate(input=self._compose_file, timeout=10)
            return_code = process.wait(timeout=10)

            if return_code != 0:
                raise subprocess.CalledProcessError(
                    return_code, self._compose_cmds + cmd
                )
        except subprocess.CalledProcessError:
            # Some Docker and Podman versions do not support compose
            # So use docker-compose or podman-compose
            process = subprocess.Popen(
                self._compose_cmd + cmd,
                stdin=subprocess.PIPE,
                text=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            process.communicate(input=self._compose_file, timeout=10)
            return_code = process.wait(timeout=10)

            if return_code != 0:
                raise subprocess.CalledProcessError(
                    return_code, self._compose_cmd + cmd
                )

    def stop(self) -> None:
        """Stop the services.

        Raises
        -------
        subprocess.CalledProcessError
            If the command fails.
        """
        cmd = [
            "-f",
            "-",
            "--project-name",
            self._compose_name,
            "down",
        ]

        try:
            process = subprocess.Popen(
                self._compose_cmds + cmd,
                stdin=subprocess.PIPE,
                text=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            process.communicate(input=self._compose_file, timeout=20)
            return_code = process.wait(timeout=20)

            if return_code != 0:
                raise subprocess.CalledProcessError(
                    return_code, self._compose_cmds + cmd
                )
        except subprocess.CalledProcessError:
            process = subprocess.Popen(
                self._compose_cmd + cmd,
                stdin=subprocess.PIPE,
                text=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            process.communicate(input=self._compose_file, timeout=20)
            return_code = process.wait(timeout=20)

            if return_code != 0:
                raise subprocess.CalledProcessError(
                    return_code, self._compose_cmd + cmd
                )

    @property
    def ports(self) -> list[str]:
        """Return the ports of the launched services."""
        output = subprocess.check_output(
            self._container_source + ["port", f"{self._compose_name}-fluent-1"],
        )
        return self._extract_ports(output.decode("utf-8").strip())
