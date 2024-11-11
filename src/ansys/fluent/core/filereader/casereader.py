"""Provides a module for Case Reader."""

import warnings

from ansys.fluent.core.warnings import PyFluentDeprecationWarning

from .case_file import CaseFile as CaseReader  # noqa: F401

# Compatibility aliases
warnings.warn(
    "Use case_file.CaseFile instead of casereader.CaseReader",
    PyFluentDeprecationWarning,
)
