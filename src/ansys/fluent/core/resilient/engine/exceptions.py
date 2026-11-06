# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

"""Exceptions and warnings raised by the resilient engine.

Errors raised by the product itself (for example a value the server rejects) are
never wrapped: when resilient mode cannot repair a step, the original exception
propagates unchanged so existing ``except`` clauses keep working.
"""


class ResilientError(RuntimeError):
    """Base class for errors raised by the resilient engine itself."""


class PathResolutionError(ResilientError, LookupError):
    """Raised when a settings path cannot be resolved on the live session."""


class CheckpointError(ResilientError):
    """Raised when a checkpoint cannot be written, found, or restored."""


class FailoverError(ResilientError):
    """Raised when a standby session cannot take over from a dead session."""


class ResilientWarning(UserWarning):
    """Base class for warnings emitted by resilient mode."""


class ResilientRecoveryWarning(ResilientWarning):
    """Resilient mode changed a value or enabled a model to complete a write."""


class ResilientFailoverWarning(ResilientWarning):
    """A standby session took over from a session that died."""
