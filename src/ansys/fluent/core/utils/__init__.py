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
