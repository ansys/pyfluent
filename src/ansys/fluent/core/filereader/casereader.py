"""Provides a module for Case Reader."""

import warnings

from ansys.fluent.core.warnings import PyFluentDeprecationWarning

# Compatibility aliases
warnings.warn(
    "Use case_file.CaseFile instead of casereader.CaseReader",
    PyFluentDeprecationWarning,
)
from .case_file import CaseFile as CaseReader  # noqa: F401
