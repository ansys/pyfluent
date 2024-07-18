"""Miscellaneous utility functions."""

import importlib.util
import logging
import sys

logger = logging.getLogger("pyfluent.general")

from ansys.fluent.core.search import _search  # noqa: F401


def load_module(module_name, file_path):
    """Load a module from a file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    logger.info(f"Loaded module {module_name} from {file_path}")
    return module
