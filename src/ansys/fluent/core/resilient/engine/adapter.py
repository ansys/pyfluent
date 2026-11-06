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

"""The product seam of the resilient engine.

The engine never imports a product. Everything that differs between products --
how a session reports a fatal error, which exceptions it raises, how a checkpoint
is written and read, how a standby session is launched -- is implemented by a
subclass of :class:`ResilientAdapter`.
"""

from __future__ import annotations

import abc
from dataclasses import dataclass
from typing import Any, Callable

from .types import ActivationCandidate


def instance_attr(obj: Any, name: str) -> Any:
    """Return ``obj.name`` without triggering ``__getattr__`` fallbacks.

    Product sessions often forward unknown attributes to their settings tree (and
    therefore to the server). Probing them with ``getattr`` would issue remote
    calls, so the engine reads its own bookkeeping attributes with this helper.
    Returns ``None`` when the attribute does not exist.
    """
    try:
        return object.__getattribute__(obj, name)
    except AttributeError:
        return None


@dataclass
class ErrorClasses:
    """Exception classes a product raises for settings errors.

    Any member may be ``None``; the classifier then relies on message heuristics
    and live introspection.
    """

    inactive: type | None = None
    read_only: type | None = None
    disallowed: type | None = None
    invalid_arg: type | None = None


class ResilientAdapter(abc.ABC):
    """Product-specific behavior required by the resilient engine.

    Subclasses must implement the abstract methods. Every other method has a
    default that suits sessions exposing a ``settings`` root and a
    ``_settings_service`` attribute.
    """

    #: Product name used in messages.
    product_name: str = "product"
    #: Dotted prefixes a user may prepend to a settings path.
    path_prefixes: tuple[str, ...] = ("settings.",)
    #: Attribute holding the server-side name of a settings object.
    scheme_name_attr: str = "obj_name"
    #: Command names that cannot be undone by setting values (a checkpoint is
    #: written before them when ``auto_checkpoint`` is enabled).
    irreversible_commands: frozenset[str] = frozenset()
    #: Commands for which the clean-stop sentinel is a benign interrupt.
    interruptible_commands: frozenset[str] = frozenset()
    #: Commands that are recorded but never replayed onto a standby session.
    non_replayable_commands: frozenset[str] = frozenset()
    #: Command-name prefixes that are recorded but never replayed (for example
    #: commands that only write output files).
    non_replayable_prefixes: tuple[str, ...] = ()
    #: File suffix of a checkpoint artifact.
    checkpoint_suffix: str = ""

    # -- settings tree and service ---------------------------------------

    def settings_root(self, session: Any) -> Any:
        """Return the settings root of a session."""
        return session.settings

    def settings_service(self, session: Any) -> Any:
        """Return the settings service of a session, or ``None``."""
        return instance_attr(session, "_settings_service")

    def set_settings_service(self, session: Any, service: Any) -> None:
        """Install a settings service on a session."""
        session._settings_service = service

    @abc.abstractmethod
    def invalidate_settings_cache(self, session: Any) -> None:
        """Drop the cached settings root so that it is rebuilt on next access."""

    # -- health ------------------------------------------------------------

    @abc.abstractmethod
    def is_fatal(self, session: Any) -> bool:
        """Return whether the product reported a fatal error for the session."""

    def fatal_details(self, session: Any) -> str | None:
        """Return details of a fatal error, if any."""
        return None

    @abc.abstractmethod
    def is_server_healthy(self, session: Any) -> bool:
        """Return whether the server answers a health check. Must never raise."""

    # -- errors --------------------------------------------------------------

    def error_classes(self) -> ErrorClasses:
        """Return the exception classes the product raises for settings errors."""
        return ErrorClasses()

    # -- session lifecycle ---------------------------------------------------

    def launch(self, **kwargs: Any) -> Any:
        """Launch a new session with the product's launch function.

        Raises
        ------
        NotImplementedError
            If the product does not support launching standby sessions.
        """
        raise NotImplementedError(
            f"The {self.product_name} adapter cannot launch standby sessions."
        )

    def standby_launcher(self, session: Any) -> Callable[[], Any] | None:
        """Return a callable that launches a session like ``session``, if known."""
        return None

    def exit_session(self, session: Any) -> None:
        """Exit a session. Must never raise."""
        exit_fn = getattr(session, "exit", None)
        if callable(exit_fn):
            try:
                exit_fn()
            except Exception:  # noqa: BLE001  # nosec B110
                pass

    def register_exit_callback(
        self, session: Any, callback: Callable[[], None]
    ) -> bool:
        """Register ``callback`` to run when ``session`` exits.

        Returns whether the callback was registered.
        """
        return False

    # -- checkpoints ---------------------------------------------------------

    def shares_client_filesystem(self, session: Any) -> bool:
        """Return whether the server reads and writes the client's file system."""
        return True

    def can_checkpoint(self, session: Any) -> bool:
        """Return whether the session currently holds state worth checkpointing."""
        return True

    def checkpoint_artifacts(self, file_path: str, *, include_data: bool) -> list[str]:
        """Return every file a checkpoint written to ``file_path`` consists of."""
        return [file_path]

    @abc.abstractmethod
    def write_checkpoint(
        self, session: Any, file_path: str, *, include_data: bool
    ) -> bool:
        """Write a checkpoint of the session to ``file_path``.

        Returns whether solution data was included.
        """

    @abc.abstractmethod
    def read_checkpoint(
        self, session: Any, file_path: str, *, include_data: bool
    ) -> None:
        """Restore the session from the checkpoint at ``file_path``."""

    # -- recovery knowledge --------------------------------------------------

    def activation_candidates(self, session: Any) -> tuple[ActivationCandidate, ...]:
        """Return settings that may activate inactive targets, in priority order."""
        return ()

    # -- command helpers -----------------------------------------------------

    @staticmethod
    def command_name(command_path: str) -> str:
        """Return the normalized last segment of a command path.

        Server-side names such as ``"solution/run-calculation/read-case"`` are
        normalized to Python-style names (``"read_case"``) so that adapters can
        list commands by their Python names.
        """
        leaf = command_path.replace("/", ".").rsplit(".", 1)[-1].strip()
        return leaf.replace("-", "_").replace(" ", "_").lower()

    def is_irreversible(self, command_path: str) -> bool:
        """Return whether a command cannot be undone by setting values."""
        return self.command_name(command_path) in self.irreversible_commands

    def is_interruptible(self, command_path: str) -> bool:
        """Return whether a command may stop with the clean-stop sentinel."""
        return self.command_name(command_path) in self.interruptible_commands

    def is_replayable(self, command_path: str) -> bool:
        """Return whether a recorded command is replayed onto a standby session."""
        name = self.command_name(command_path)
        if name in self.non_replayable_commands:
            return False
        return not name.startswith(self.non_replayable_prefixes)
