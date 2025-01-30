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

"""Miscellaneous utility functions."""

import importlib.util
import logging
from pathlib import Path
import sys

from ansys.fluent.core.search import search  # noqa: F401

logger = logging.getLogger("pyfluent.general")


def load_module(module_name, file_path):
    """Load a module from a file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    logger.info(f"Loaded module {module_name} from {file_path}")
    return module


def get_examples_download_dir():
    """Return the path to the examples download directory."""
    parent_path = Path.home() / "Downloads"
    parent_path.mkdir(exist_ok=True)
    return parent_path / "ansys_fluent_core_examples"


def get_user_data_dir():
    """Return the path to the user data directory."""
    if sys.platform == "win32":
        return Path.home() / "AppData" / "Local" / "Ansys" / "ansys_fluent_core"
    else:
        return Path.home() / ".local" / "share" / "Ansys" / "ansys_fluent_core"
