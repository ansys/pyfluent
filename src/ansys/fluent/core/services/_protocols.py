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

"""Provides protocol definitions for gRPC services."""

# pylint: disable=missing-function-docstring

from collections.abc import Generator, Sequence
from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    import grpc

    from ansys.fluent.core.utils.fluent_version import SolverEvent


class ServiceProtocol(Protocol):
    """Protocol for gRPC service classes."""

    if TYPE_CHECKING:

        def __init__(
            self, channel: "grpc.Channel", metadata: list[tuple[str, str]]
        ) -> None: ...


class EventsServiceProtocol(Protocol):
    """Protocol for EventsService (v0 and v1 share same interface)."""

    def register_pause_on_solution_events(
        self, solution_event: "SolverEvent"
    ) -> int: ...

    def resume_on_solution_event(self, registration_id: int) -> None: ...

    def unregister_pause_on_solution_events(self, registration_id: int) -> None: ...

    def event_from_proto_field(self, field_name: str) -> str: ...

    def _construct_event_info(
        self, response: Any, event: Any, event_info_cls: Any
    ) -> Any: ...

    def _process_streaming(
        self,
        id: Any,
        stream_begin_method: Any,
        started_evt: Any,
        *args: Any,
        **kwargs: Any,
    ) -> Any: ...

    def begin_streaming(
        self, request: Any, started_evt: Any, id: str, stream_begin_method: str
    ) -> Generator[Any, None, None]: ...

    def end_streaming(self, id: str, stream_begin_method: str) -> None: ...


class MonitorServiceProtocol(Protocol):
    """Protocol for MonitorService (v0 and v1 share same interface)."""

    def get_monitors_info(self) -> dict[str, Any]: ...

    def _process_streaming(
        self,
        id: Any,
        stream_begin_method: Any,
        started_evt: Any,
        *args: Any,
        **kwargs: Any,
    ) -> Any: ...

    def begin_streaming(
        self, request: Any, started_evt: Any, id: str, stream_begin_method: str
    ) -> Generator[Any, None, None]: ...

    def end_streaming(self, id: str, stream_begin_method: str) -> None: ...


class ApplicationRuntimeServiceProtocol(Protocol):
    """Protocol for ApplicationRuntimeService (v1 base)."""

    def get_product_version(self) -> str: ...

    def get_build_info(self) -> tuple[str, str, str, str]: ...

    def get_controller_process_info(self) -> tuple[int, str, str]: ...

    def get_solver_process_info(self) -> tuple[int, str, str]: ...

    def get_mode(self) -> str: ...

    def get_dimension(self) -> int: ...

    def get_precision(self) -> str: ...

    def get_processor_count(self) -> int: ...

    def get_ui_mode(self) -> str: ...

    def get_graphics_driver(self) -> str: ...

    def get_gpu_config(self) -> bool | list[int]: ...

    def start_python_journal(self, journal_name: str | None = None) -> str: ...

    def stop_python_journal(self, journal_id: str | None = None) -> str: ...

    def is_beta_enabled(self) -> bool: ...

    def enable_beta(self) -> None: ...

    def exit(self) -> None: ...

    def set_working_directory(self, path: Any) -> None: ...

    def set_idle_timeout(self, timeout: int) -> None: ...


class ApplicationRuntimeServiceV0Protocol(ApplicationRuntimeServiceProtocol):
    """Protocol for ApplicationRuntimeService v0 (extends v1 base with v0-specific methods)."""

    def get_app_mode(self) -> str: ...

    def is_wildcard(self, input: str | None = None) -> bool: ...

    def is_solution_data_available(self) -> bool: ...

    def register_pause_on_solution_events(
        self, solution_event: "SolverEvent"
    ) -> int: ...

    def resume_on_solution_event(self, registration_id: int) -> None: ...

    def unregister_pause_on_solution_events(self, registration_id: int) -> None: ...


class SchemeEvalProtocol(Protocol):
    """Protocol for scheme evaluator (SchemeInterpreterService or SchemeInterpreter wrapper)."""

    def eval(self, scm_input: str, suppress_prompts: bool = True) -> Any: ...

    def exec(
        self, commands: Sequence[str], wait: bool = True, silent: bool = True
    ) -> str: ...

    def string_eval(self, input: str) -> str: ...
