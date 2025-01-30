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

"""Provides a module to fix text documentation for a data object."""

from io import StringIO


def escape_wildcards(doc: str):
    """Escape wildcards."""
    new_doc = StringIO()
    prev_c = None
    for i, c in enumerate(doc):
        if c == "*":
            if prev_c == "\\":
                new_doc.write(r"\*")
            else:
                new_doc.write(r"\\*")
        else:
            new_doc.write(c)
        prev_c = c
    return new_doc.getvalue()


def fix_definition_list_in_class_doc(doc: str):
    """Fix definition list in class docstring."""
    old_lines = doc.splitlines(keepends=True)
    new_lines = []
    for i, line in enumerate(old_lines):
        if line.strip().startswith("-") and not line.strip().startswith("--"):
            if i == 0:
                new_lines.append("\n")
                new_lines.append(line)
            elif i == len(old_lines) - 1:
                new_lines.append(line)
                new_lines.append("\n")
            else:
                prev_line = old_lines[i - 1].strip()
                if prev_line and not prev_line.startswith("-"):
                    new_lines.append("\n")
                new_lines.append(line)
                next_line = old_lines[i + 1].strip()
                if next_line and not next_line.startswith("-"):
                    new_lines.append("\n")
        else:
            new_lines.append(line)
    return "".join(new_lines)


def fix_settings_doc(doc: str):
    """Fix settings docstring."""
    doc = escape_wildcards(doc)
    return fix_definition_list_in_class_doc(doc)
