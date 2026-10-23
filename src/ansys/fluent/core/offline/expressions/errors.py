# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Exception types for the expression builder."""


class ExpressionBuildError(Exception):
    """Raised when an expression tree cannot be built or rendered."""

    def __init__(self, message: str, *, node=None, slot: str | None = None):
        super().__init__(message)
        self.node = node
        self.slot = slot
