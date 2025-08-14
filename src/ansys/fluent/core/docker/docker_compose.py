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

import subprocess
import uuid

from .utils import get_ghcr_fluent_image_name


class ComposeBasedLauncher:
    """Launch Fluent through docker or Podman compose."""

    def __init__(self, compose_config, container_dict):
        from ansys.fluent.core import config

        self._compose_config = compose_config
        self._compose_name = f"pyfluent_compose_{uuid.uuid4().hex}"
        self._container_dict = container_dict
        image_tag = config.fluent_image_tag
        self._image_name = (
            container_dict.get("fluent_image")
            or f"{get_ghcr_fluent_image_name(image_tag)}:{image_tag}"
        )
        self._container_source = self._set_compose_cmds()
        self._container_source.remove("compose")

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
            If neither Docker nor Podman is specified.
        """

        # Determine the compose command
        if self._compose_config.use_podman_compose:
            self._compose_cmds = (
                ["sudo", "podman", "compose"]
                if hasattr(self, "_container_source")
                and "sudo" in self._container_source
                else ["podman", "compose"]
            )
        elif self._compose_config.use_docker_compose:
            self._compose_cmds = ["docker", "compose"]
        else:
            raise RuntimeError("Neither Docker nor Podman is specified.")

        return self._compose_cmds

    def check_image_exists(self) -> bool:
        """Check if the image exists locally."""
        try:
            cmd = self._container_source + ["images", "-q", self._image_name]
            # Podman users do not always configure rootless mode in /etc/subuids and /etc/subgids
            if self._compose_config.use_podman_compose:
                sudo_cmd = ["sudo"] + cmd
                output_1 = subprocess.check_output(cmd)
                output_2 = subprocess.check_output(sudo_cmd)
                output_1_result = output_1.decode("utf-8").strip() != ""
                output_2_result = output_2.decode("utf-8").strip() != ""
                if output_2_result and not output_1_result:
                    self._container_source.insert(0, "sudo")
                return output_1_result or output_2_result
            else:
                output = subprocess.check_output(cmd)
                return output.decode("utf-8").strip() != ""
        except subprocess.CalledProcessError as e:  # noqa: F841
            return False

    def pull_image(self) -> None:
        """Pull a Docker image if it does not exist locally."""

        cmd = self._container_source + ["pull", self._image_name]

        subprocess.check_call(cmd)

    def _start_stop_helper(
        self, compose_cmd: list[str], cmd: list[str], timeout: float
    ) -> None:
        """Helper function to start or stop the services.
        Parameters
        ----------
        compose_cmd: list[str]
            The command to run.
        cmd: list[str]
            The command to run.
        timeout: float
            The timeout for the command.
        """
        process = subprocess.Popen(
            compose_cmd + cmd,
            stdin=subprocess.PIPE,
            text=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        process.communicate(input=self._compose_file, timeout=timeout)
        return_code = process.wait(timeout=timeout)

        if return_code != 0:
            raise subprocess.CalledProcessError(return_code, compose_cmd + cmd)

    def start(self) -> None:
        """Start the services.

        Raises
        ------
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

        self._start_stop_helper(self._set_compose_cmds(), cmd, 60)

    def stop(self) -> None:
        """Stop the services.

        Raises
        ------
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

        self._start_stop_helper(self._set_compose_cmds(), cmd, 30)

    @property
    def ports(self) -> list[str]:
        """Return the ports of the launched services."""
        output = subprocess.check_output(
            self._container_source + ["port", f"{self._compose_name}-fluent-1"],
        )
        return self._extract_ports(output.decode("utf-8").strip())
