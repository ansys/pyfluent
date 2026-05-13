# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
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

"""Mixin for managing the lifecycle of command arguments in datamodel services."""

from abc import ABC, abstractmethod
import logging
from threading import RLock

logger = logging.getLogger("pyfluent.datamodel")


class CommandArgumentsCleanupMixin(ABC):
    """Shared command-argument lifecycle cleanup for datamodel services."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._command_arguments: set[tuple[str, str, str, str]] = set()
        self._command_arguments_lock = RLock()
        self._shutdown_cleanup_started = False

    @staticmethod
    def _command_arguments_key(
        rules: str, path: str, command: str, commandid: str
    ) -> tuple[str, str, str, str]:
        return (rules, path, command, commandid)

    def register_command_arguments(
        self, rules: str, path: str, command: str, commandid: str
    ) -> None:
        """Register command arguments for explicit cleanup during shutdown."""
        with self._command_arguments_lock:
            if self._shutdown_cleanup_started:
                return
            self._command_arguments.add(
                self._command_arguments_key(rules, path, command, commandid)
            )

    def release_command_arguments(
        self, rules: str, path: str, command: str, commandid: str
    ) -> None:
        """Release command arguments when their Python wrapper is deleted."""
        key = self._command_arguments_key(rules, path, command, commandid)
        with self._command_arguments_lock:
            was_registered = key in self._command_arguments
            self._command_arguments.discard(key)
            shutdown_cleanup_started = self._shutdown_cleanup_started

        if was_registered and not shutdown_cleanup_started:
            self._delete_command_arguments_rpc(rules, path, command, commandid)

    def delete_all_command_arguments(self) -> None:
        """Delete all tracked command arguments as part of shutdown finalization."""
        with self._command_arguments_lock:
            self._shutdown_cleanup_started = True
            command_arguments = list(self._command_arguments)
            self._command_arguments.clear()

        for rules, path, command, commandid in command_arguments:
            try:
                self._delete_command_arguments_rpc(rules, path, command, commandid)
            except Exception as exc:
                logger.info(
                    "delete_all_command_arguments %s: %s",
                    type(exc).__name__,
                    exc,
                )

    def delete_command_arguments(
        self, rules: str, path: str, command: str, commandid: str
    ) -> None:
        """Delete command arguments and stop tracking them."""
        with self._command_arguments_lock:
            self._command_arguments.discard(
                self._command_arguments_key(rules, path, command, commandid)
            )
        self._delete_command_arguments_rpc(rules, path, command, commandid)

    @abstractmethod
    def _delete_command_arguments_rpc(
        self, rules: str, path: str, command: str, commandid: str
    ) -> None:
        """Issue RPC to delete command arguments."""
        pass
