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

"""Module for context managers used in PyFluent."""

from contextlib import contextmanager
from threading import local

_thread_local = local()


def _get_stack():
    if not hasattr(_thread_local, "stack"):
        _thread_local.stack = []
    return _thread_local.stack


@contextmanager
def using(session):
    """Context manager to use a Fluent session."""
    stack = _get_stack()
    stack.append(session)
    try:
        yield
    finally:
        stack.pop()


def _get_active_session():
    stack = _get_stack()
    if stack:
        return stack[-1]


class ReadCase:
    """Context manager to read a Fluent case file."""

    def __init__(self, session=None, case_file: str | None = None):
        self.session = session or _get_active_session()
        self.case_file = case_file

    def __enter__(self):
        if not self.case_file:
            raise ValueError("A case file path must be provided to read.")
        self.session.settings.file.read_case(file_name=self.case_file)
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        pass
