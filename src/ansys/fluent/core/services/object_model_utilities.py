# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
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

"""Contains utilities for object model."""

from collections.abc import Sequence
from enum import Enum
import os
from typing import Any, Iterable

from ansys.fluent.core.solver.error_message import allowed_name_error_message
from ansys.fluent.core.utils.get_completer_info import (
    get_completer_info as _completer_info_method,
)

ValueT = None | bool | int | float | str | Sequence["ValueT"] | dict[str, "ValueT"]
Path = list[tuple[str, str]]


class Attribute(Enum):
    """Contains the standard names of data model attributes associated with the data
    model service."""

    IS_ACTIVE: str = "isActive"
    EXPOSURE_LEVEL: str = "exposureLevel"
    IS_READ_ONLY: str = "isReadOnly"
    DEFAULT: str = "default"
    FORCE_DEFAULT: str = "forceDefault"
    MIN: str = "min"
    MAX: str = "max"
    ALLOWED_VALUES: str = "allowedValues"
    EXCLUDED_VALUES: str = "excludedValues"
    MIN_LENGTH: str = "minLength"
    MAX_LENGTH: str = "maxLength"
    ERROR_STATUS: str = "errorStatus"
    USER_ERROR_STATUS: str = "userErrorStatus"
    MEMBERS: str = "members"
    DISPLAY_TEXT: str = "displayText"
    NAMES: str = "__names__"
    INTERNAL_NAMES: str = "__ids__"
    PATHS: str = "__paths__"
    ROOT_ID: str = "__root__"
    NAME: str = "_name_"
    REFERENCE_PATH: str = "referencePath"
    ARGUMENTS: str = "arguments"
    TOOL_TIP: str = "toolTip"
    SHOW_AT_PARENT_NODE: str = "showAtParentNode"
    WIDGET_TYPE: str = "widgetType"
    ECHO_MODE: str = "echoMode"
    IS_TREE_NODE: str = "isTreeNode"
    MIGRATION: str = "migration"
    DEPRECATED_VERSION: str = "deprecatedVersion"


class ReadOnlyObjectError(RuntimeError):
    """Raised on an attempt to mutate a read-only object."""

    def __init__(self, obj_name):
        """Initialize ReadOnlyObjectError."""
        super().__init__(f"{obj_name} is readonly!")


class InvalidNamedObject(RuntimeError):
    """Raised when the object is not a named object."""

    def __init__(self, class_name):
        """Initialize InvalidNamedObject."""
        super().__init__(f"{class_name} is not a named object class.")


class DisallowedFilePurpose(ValueError):
    """Is raised when the specified file purpose is not in the allowed values."""

    def __init__(
        self,
        context: Any | None = None,
        name: Any | None = None,
        allowed_values: Any | None = None,
    ):
        """Initialize DisallowedFilePurpose."""
        super().__init__(
            allowed_name_error_message(
                context=context, trial_name=name, allowed_values=allowed_values
            )
        )


def convert_path_to_se_path(path: Path) -> str:
    """Convert a path structure to a StateEngine path.

    Parameters
    ----------
    path : Path
        Path structure.

    Returns
    -------
    str
        stateengine path
    """
    se_path = ""
    for comp in path:
        se_path += "/" + comp[0]
        if comp[1]:
            se_path += ":" + comp[1]
    return se_path


def convert_se_path_to_path(se_path: str) -> Path:
    """Convert a StateEngine path to a path structure.

    Parameters
    ----------
    se_path : str
        StateEngine path.

    Returns
    -------
    Path
        path structure
    """
    path = []
    for comp in se_path.split("/"):
        if comp:
            if ":" in comp:
                name, value = comp.split(":")
            else:
                name, value = comp, ""
            path.append((name, value))
    return path


def _bool_value_if_none(val: bool | None, default: bool) -> bool:
    if isinstance(val, bool) or val is None:
        return default if val is None else val
    raise TypeError(f"{val} should be a bool or None")


def true_if_none(val: bool | None) -> bool:
    """Returns true if 'val' is true or None, else returns false."""
    return _bool_value_if_none(val, default=True)


def false_if_none(val: bool | None) -> bool:
    """Returns false if 'val' is false or None, else returns true."""
    return _bool_value_if_none(val, default=False)


def _get_completer_info(
    obj, base_class: type, prefix: str, excluded: Iterable
) -> list[list[str]]:
    _type_name_map = {
        _InputFile: "InputFilename",
        _OutputFile: "OutputFilename",
        _InOutFile: "InOutFilename",
    }
    return _completer_info_method(
        obj=obj,
        base_class=base_class,
        prefix=prefix,
        excluded=excluded,
        type_name_map=_type_name_map,
    )


class _InputFile:
    def _do_before_execute(self, value):
        try:
            file_names = value if isinstance(value, list) else [value]
            base_names = []
            for file_name in file_names:
                self.service.file_transfer_service.upload(file_name=file_name)
                base_names.append(os.path.basename(file_name))
            return base_names if isinstance(value, list) else base_names[0]
        except AttributeError:
            return value


class _OutputFile:
    def _do_after_execute(self, value):
        try:
            file_names = value if isinstance(value, list) else [value]
            for file_name in file_names:
                self.service.file_transfer_service.download(file_name=file_name)
        except AttributeError:
            pass


class _InOutFile(_InputFile, _OutputFile):
    pass
