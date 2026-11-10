# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT

"""Exception types for the expression builder."""


class ExpressionBuildError(Exception):
    """Raised when an expression tree cannot be built or rendered."""

    node: object | None
    slot: str | None

    def __init__(
        self, message: str, node: object | None = None, slot: str | None = None
    ) -> None:
        # Forward all arguments so pickle and copy.copy can reconstruct the
        # exception via ``cls(*exc.args)``; keyword-only parameters would make
        # that reconstruction impossible.
        super().__init__(message, node, slot)
        self.node = node
        self.slot = slot

    def __str__(self) -> str:
        """Return the error message."""
        return str(self.args[0])
