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

"""Module that provides a method to handle deprecated arguments."""

import functools
import logging
import warnings

from ansys.fluent.core.pyfluent_warnings import PyFluentDeprecationWarning

logger = logging.getLogger("pyfluent.general")


def deprecate_argument(
    old_arg,
    new_arg,
    converter=lambda x: x,
    warning_cls=PyFluentDeprecationWarning,
    **kwds,
):
    """Warns that the argument provided is deprecated and automatically replaces the
    deprecated argument with the appropriate new argument."""

    def decorator(func):
        """Holds the original method to perform operations on it."""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """Warns about the deprecated argument and replaces it with the new
            argument."""
            if old_arg in kwargs:
                warnings.warn(
                    f"'{old_arg}' is deprecated. Use '{new_arg}' instead.",
                    warning_cls,
                    stacklevel=2,
                )
                old_value = kwargs[old_arg]
                new_value = kwargs.get(new_arg)
                if new_value is None:
                    new_value = converter(kwargs[old_arg], **kwds)
                    kwargs[new_arg] = new_value
                    logger.warning(
                        f"Using '{new_arg} = {new_value}' for '{func.__name__}()'"
                        f" instead of '{old_arg} = {old_value}'."
                    )
                else:
                    logger.warning(
                        f"Ignoring '{old_arg} = {old_value}' specification for '{func.__name__}()',"
                        f" only '{new_arg} = {new_value}' applies."
                    )
                kwargs.pop(old_arg)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def deprecate_arguments(
    converter,
    warning_cls=PyFluentDeprecationWarning,
):
    """Warns that the arguments provided are deprecated and automatically replaces the
    deprecated arguments with the appropriate new arguments."""

    def decorator(func):
        """Holds the original method to perform operations on it."""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """Warns about the deprecated arguments and replaces them with the new
            arguments."""
            input_kwargs = kwargs.copy()
            kwargs = converter(kwargs)
            new_args = set(kwargs) - set(input_kwargs)
            old_args = set(input_kwargs) - set(kwargs)
            if old_args and new_args:
                warnings.warn(
                    f"The arguments: {', '.join(old_args)} are deprecated. Use {', '.join(new_args)} instead.",
                    warning_cls,
                    stacklevel=2,
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator
