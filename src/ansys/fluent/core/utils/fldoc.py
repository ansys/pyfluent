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

"""Provides a module to produce text documentation for a data object."""

import pprint
import pydoc
import sys


def docother(self, object, name=None, mod=None, parent=None, maxlen=None, doc=None):
    """Produce text documentation for a data object."""
    if isinstance(object, list):
        indent_len = len(name and name + " = " or "") + 1
        rep = pprint.pformat(object, width=maxlen, compact=True, indent=indent_len)
        rep = "[" + rep[1:].lstrip()
    else:
        rep = self.repr(object)
        if maxlen:
            line = (name and name + " = " or "") + rep
            chop = maxlen - len(line)
            if chop < 0:
                rep = rep[:chop] + "..."
    line = (name and self.bold(name) + " = " or "") + rep
    #  The source have been changed in 3.9, cpython commit id fbf2786c4c89430e2067016603078cf3500cfe94
    if sys.version_info < (3, 9):
        if doc is not None:
            line += "\n" + self.indent(str(doc))
    else:
        if not doc:
            doc = pydoc.getdoc(object)
        if doc:
            line += "\n" + self.indent(str(doc)) + "\n"
    return line
