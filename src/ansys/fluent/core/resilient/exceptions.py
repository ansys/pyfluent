# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
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

"""Exceptions raised by the resilient execution runtime.

All of these are raised with ``raise ResilientError(...) from err`` so the
underlying Fluent / settings error is always preserved as the cause.
"""

from __future__ import annotations


class ResilientError(RuntimeError):
    """Base class for all resilient-runtime errors."""


class PathResolutionError(ResilientError, LookupError):
    """Raised when a settings path cannot be resolved on the live session."""


class UnrecoverableStepError(ResilientError):
    """A single step failed and no automatic repair could be applied.

    This is *non-catastrophic*: the session is still usable, but the resolver
    either found no safe fix or exhausted its retry budget.
    """


class FailoverError(ResilientError):
    """Failover could not complete.

    Raised when no healthy standby session is available to take over, or when
    replaying the last good checkpoint onto the standby failed.
    """


class CheckpointError(ResilientError):
    """Raised when a checkpoint cannot be captured, restored, or found."""
