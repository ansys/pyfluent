# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
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
"""Configuration variables for PyFluent."""
import os

from ansys.fluent.core.utils import get_examples_download_dir


class Config:
    """Set the global configuration variables for PyFluent."""

    def __init__(self):
        """__init__ method of Config class."""
        # Read the environment variable once when pyfluent is imported
        # and reuse it throughout process lifetime.
        self._env = os.environ.copy()

        # Variables which has some additional logic in getter/setter methods
        # are implemented as properties. Rest of the variables are public attributes.
        # All properties and public attributes returns a valid value.

        # Backend variables of the properties
        self._examples_path = None

        #: Host path which is mounted to the container
        self.container_mount_source = None

        #: Path inside the container where the host path is mounted
        self.container_mount_target = "/home/container/workdir"

    @property
    def examples_path(self) -> str:
        """Path to the example input/data files are downloaded."""
        if self._examples_path is None:
            self._examples_path = str(get_examples_download_dir())
        return self._examples_path

    @examples_path.setter
    def examples_path(self, val: str) -> None:
        """Set the path to the example input/data files are downloaded."""
        self._examples_path = val

    @property
    def interactive(self) -> bool:
        """Boolean flag to access mode (interactive or non-interactive)."""
        return self._interactive

    @interactive.setter
    def interactive(self, val: bool) -> None:
        """Set mode (interactive or non-interactive)."""
        if self._single_window and val == False:
            warnings.warn(
                "Single window is only available for interactive mode."
                "\nReverting 'interactive' to 'True'."
            )
        else:
            self._interactive = bool(val)

    @property
    def single_window(self) -> bool:
        """Whether single Qt window is activated."""
        return self._single_window

    @single_window.setter
    def single_window(self, val: bool) -> None:
        """Activate (or Deactivate) single Qt window."""
        if val and not self._interactive:
            warnings.warn(
                "Single window is only available for interactive mode."
                "\nReverting 'single_window' to 'False'."
            )
        else:
            self._single_window = bool(val)

    @property
    def view(self) -> View:
        """Returns the view set for displaying graphics."""
        return self._view

    @view.setter
    def view(self, val: str | View) -> None:
        """Sets the view for displaying graphics."""
        self._view = View(val)

    @property
    def two_dimensional_renderer(self) -> str:
        """Returns the default renderer name for displaying 2D plots."""
        return self._two_dimensional_renderer

    @two_dimensional_renderer.setter
    def two_dimensional_renderer(self, val: str) -> None:
        """Sets the default renderer for displaying 2D plots."""
        if isinstance(val, str):
            if val in _renderer:
                self._two_dimensional_renderer = val
            else:
                raise ValueError(
                    f"{val} is not a valid renderer. "
                    f"Valid renderers are {list(_renderer)}."
                )

    @property
    def three_dimensional_renderer(self) -> str:
        """Returns the default renderer name for displaying 3D graphics."""
        return self._three_dimensional_renderer

    @three_dimensional_renderer.setter
    def three_dimensional_renderer(self, val: str) -> None:
        """Sets the default renderer for displaying 3D graphics."""
        if isinstance(val, str):
            if val in _renderer:
                self._three_dimensional_renderer = val
            else:
                raise ValueError(
                    f"{val} is not a valid renderer. "
                    f"Valid renderers are {list(_renderer)}."
                )


config = Config()


def set_config(blocking: bool = False, set_view_on_display: str = "isometric"):
    """Set visualization configuration."""
    warnings.warn(
        "Please use the module level 'config' instead.", PyFluentDeprecationWarning
    )
    config.interactive = not blocking
    config.view = set_view_on_display


def get_config():
    """Get visualization configuration."""
    warnings.warn(
        "Please use the module level 'config' instead.", PyFluentDeprecationWarning
    )
    return {"blocking": not config.interactive, "set_view_on_display": config.view}
