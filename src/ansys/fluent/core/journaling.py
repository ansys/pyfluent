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

"""A module for controlling the writing of Fluent Python journals."""


class PythonJournalNotSupported(RuntimeError):
    """Raised when Python journal is unsupported."""

    def __init__(self):
        """Initialize PythonJournalNotSupported."""
        super().__init__(
            "Python journaling is available in Fluent version 2023 R1 or later."
        )


class Journal:
    """Control the writing of Fluent Python journals."""

    def __init__(self, app_utilities):
        """__init__ method of Journal class."""
        self._app_utilities = app_utilities

    def _check_python_journaling_support(self):
        if self._app_utilities.get_product_version() == "22.2.0":
            raise PythonJournalNotSupported()

    def start(self, file_name: str):
        """Start writing a Fluent Python journal at the specified file_name."""
        self._check_python_journaling_support()
        self._app_utilities.start_python_journal(journal_name=file_name)

    def stop(self):
        """Stop writing the Fluent Python journal."""
        self._check_python_journaling_support()
        self._app_utilities.stop_python_journal()
