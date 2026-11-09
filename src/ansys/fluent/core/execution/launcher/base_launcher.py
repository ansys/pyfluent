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

"""Base class shared by the Fluent launchers."""

from __future__ import annotations

from typing import Any
import warnings

from ansys.fluent.core.diagnostics.exceptions import InvalidArgument
from ansys.fluent.core.execution.launcher.error_warning_messages import (
    CERTIFICATES_FOLDER_NOT_PROVIDED_AT_LAUNCH,
)
from ansys.fluent.core.execution.launcher.launch_options import (
    FluentMode,
    _get_argvals_and_session,
    get_remote_grpc_options,
)
from ansys.fluent.core.execution.launcher.launcher_utils import (
    _validate_lightweight_with_case_data,
    _validate_lightweight_with_journal,
)
from ansys.framework.process import BaseLauncher


class FluentLauncher(BaseLauncher):
    """Base class for Fluent launchers.

    Attributes
    ----------
    argvals : dict
        Resolved launch arguments.
    new_session : type
        Session class for the launch mode.
    file_transfer_service : Any
        Service for uploading and downloading files to and from the server.
    """

    new_session: type
    file_transfer_service: Any = None

    @property
    def _argvals(self) -> dict[str, Any]:
        return self.argvals

    @property
    def _new_session(self) -> type:
        return self.new_session

    def _set_argvals(
        self, argvals: dict[str, Any], file_transfer_service: Any = None
    ) -> None:
        """Resolve the launch arguments and the session class for the launch mode."""
        self.argvals, self.new_session = _get_argvals_and_session(argvals)
        self.file_transfer_service = file_transfer_service

    @staticmethod
    def _resolve_grpc_security(
        certificates_folder: str | None, insecure_mode: bool
    ) -> tuple[str | None, bool]:
        """Resolve gRPC TLS options for a server reached from another host.

        Raises
        ------
        ValueError
            If neither ``certificates_folder`` nor ``insecure_mode`` is set, or both
            are set.
        """
        certificates_folder, insecure_mode = get_remote_grpc_options(
            certificates_folder, insecure_mode
        )
        if certificates_folder is None and not insecure_mode:
            raise ValueError(CERTIFICATES_FOLDER_NOT_PROVIDED_AT_LAUNCH)
        return certificates_folder, insecure_mode

    def _validate_case_and_lightweight(self) -> None:
        """Validate case/data and lightweight-mode arguments.

        Lightweight mode is disabled with a warning when combined with journals or a
        case data file.

        Raises
        ------
        InvalidArgument
            If a case data file is given in meshing mode.
        """
        if FluentMode.is_meshing(self.argvals.get("mode")) and self.argvals.get(
            "case_data_file_name"
        ):
            raise InvalidArgument("Case and data file cannot be read in meshing mode.")

        for validate, other_argument in (
            (_validate_lightweight_with_journal, "journal_file_names"),
            (_validate_lightweight_with_case_data, "case_data_file_name"),
        ):
            should_disable, warning_msg = validate(
                self.argvals.get("lightweight_mode"), self.argvals.get(other_argument)
            )
            if should_disable:
                warnings.warn(warning_msg, UserWarning, stacklevel=2)
                self.argvals["lightweight_mode"] = False
