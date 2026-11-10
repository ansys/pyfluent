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

"""Product-agnostic resilient-mode engine.

This package depends only on the Python standard library. It talks to a product
exclusively through a :class:`ResilientAdapter`, and its modules import each
other with relative imports only, so it can move to a standalone distribution
without code changes. A unit test enforces that no module here imports a product
package.
"""

import logging

from .adapter import ErrorClasses, ResilientAdapter
from .attach import (
    ResilientSession,
    disable_resilient_mode,
    enable_resilient_mode,
    is_resilient,
)
from .config import CheckpointConfig, PoolConfig, ResilientConfig
from .controller import ResilientController
from .exceptions import (
    CheckpointError,
    FailoverError,
    ResilientError,
    ResilientFailoverWarning,
    ResilientWarning,
)
from .journal import CommandOp, Journal, ObjectOp, SetOp
from .pool import WarmSessionPool
from .types import (
    Checkpoint,
    Classification,
    ErrorCategory,
    EventKind,
    ResilientEvent,
    Severity,
    StepOutcome,
)

# Library logging: records reach the application's handlers when it configures
# logging, and are never printed through Python's last-resort handler otherwise.
# Warnings and events already report what resilient mode does.
logging.getLogger("ansys.resilient").addHandler(logging.NullHandler())

__all__ = [
    "Checkpoint",
    "CheckpointConfig",
    "CheckpointError",
    "Classification",
    "CommandOp",
    "ErrorCategory",
    "ErrorClasses",
    "EventKind",
    "FailoverError",
    "Journal",
    "ObjectOp",
    "PoolConfig",
    "ResilientAdapter",
    "ResilientConfig",
    "ResilientController",
    "ResilientError",
    "ResilientEvent",
    "ResilientFailoverWarning",
    "ResilientSession",
    "ResilientWarning",
    "SetOp",
    "Severity",
    "StepOutcome",
    "WarmSessionPool",
    "disable_resilient_mode",
    "enable_resilient_mode",
    "is_resilient",
]
