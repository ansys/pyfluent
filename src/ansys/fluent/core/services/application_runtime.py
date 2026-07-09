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

"""High-level application runtime wrappers.

This module owns the business-logic layer on top of the ApplicationRuntime gRPC
service. The grpc service implementation lives in:

* ``ansys.fluent.core._grpc_services.application_runtime_service`` (v1 proto API)
* ``ansys.fluent.core._grpc_services.application_runtime_service_v0`` (v0 proto API)

Class hierarchy
---------------
``ApplicationRuntime``
    gRPC-based implementation (v1 proto API).

``ApplicationRuntimeV261V252``
    Shared implementation for 25R2 and 26R1.

``ApplicationRuntimeV261(ApplicationRuntimeV261V252)``
    gRPC-based implementation valid till 26R1 (v0 proto API).

``ApplicationRuntimeV252(ApplicationRuntimeV261V252)``
    gRPC-based implementation valid till 25R2 (v0 proto API). ``EnableBeta``
    was not yet implemented; delegates to Scheme instead.

``ApplicationRuntimeOld``
    Scheme-based fallback used for Fluent versions before 25R2.
"""

from enum import Enum
import os
import platform

from ansys.fluent.core._types import PathType
from ansys.fluent.core.services.abstract_application_runtime import (
    AbstractApplicationRuntime,
    BuildInfo,
    ProcessInfo,
)
from ansys.fluent.core.streaming_services.events_streaming import SolverEvent
from ansys.fluent.core.utils.fluent_version import FluentVersion


class ApplicationRuntime(AbstractApplicationRuntime):
    """Application runtime backed by the ApplicationRuntime gRPC service."""

    def __init__(self, service):
        """Initialize ApplicationRuntime."""
        self.service = service

    def get_product_version(self) -> FluentVersion:
        """Get product version."""
        return FluentVersion(self.service.get_product_version())

    def get_build_info(self) -> BuildInfo:
        """Get build info."""
        build_time, build_id, vcs_revision, vcs_branch = self.service.get_build_info()
        return BuildInfo(
            build_time=build_time,
            build_id=build_id,
            vcs_revision=vcs_revision,
            vcs_branch=vcs_branch,
        )

    def get_controller_process_info(self) -> ProcessInfo:
        """Get controller process info."""
        process_id, hostname, working_directory = (
            self.service.get_controller_process_info()
        )
        return ProcessInfo(
            process_id=process_id,
            hostname=hostname,
            working_directory=working_directory,
        )

    def get_solver_process_info(self) -> ProcessInfo:
        """Get solver process info."""
        process_id, hostname, working_directory = self.service.get_solver_process_info()
        return ProcessInfo(
            process_id=process_id,
            hostname=hostname,
            working_directory=working_directory,
        )

    def get_app_mode(self) -> Enum:
        """Get app mode."""
        from ansys.fluent.core import FluentMode

        return FluentMode(self.service.get_mode())

    def get_dimension(self) -> Enum:
        """Get dimension."""
        from ansys.fluent.core import Dimension

        return Dimension(self.service.get_dimension())

    def get_precision(self) -> Enum:
        """Get precision."""
        from ansys.fluent.core import Precision

        return Precision(self.service.get_precision())

    def get_processor_count(self) -> int:
        """Get processor count."""
        return self.service.get_processor_count()

    def get_ui_mode(self) -> Enum:
        """Get UI mode."""
        from ansys.fluent.core import UIMode

        return UIMode(self.service.get_ui_mode())

    def get_graphics_driver(self) -> Enum:
        """Get graphics driver."""
        if platform.system() == "Windows":
            from ansys.fluent.core import FluentWindowsGraphicsDriver

            return FluentWindowsGraphicsDriver(self.service.get_graphics_driver())
        else:
            from ansys.fluent.core import FluentLinuxGraphicsDriver

            return FluentLinuxGraphicsDriver(self.service.get_graphics_driver())

    def get_gpu_config(self) -> bool | list[int]:
        """Get GPU config."""
        return self.service.get_gpu_config()

    def start_python_journal(self, journal_name: str | None = None) -> int:
        """Start python journal."""
        return self.service.start_python_journal(journal_name=journal_name)

    def stop_python_journal(self, journal_id: str | None = None) -> str:
        """Stop python journal."""
        return self.service.stop_python_journal(journal_id=journal_id)

    def is_beta_enabled(self) -> bool:
        """Return whether beta features are enabled."""
        return self.service.is_beta_enabled()

    def enable_beta(self) -> None:
        """Enable beta features."""
        self.service.enable_beta()

    def exit(self) -> None:
        """Exit the server."""
        self.service.exit()

    def set_working_directory(self, path: PathType) -> None:
        """Change the client cortex working directory."""
        self.service.set_working_directory(path=path)


class ApplicationRuntimeV261V252:
    """Application runtime for Fluent 26R1 and 25R2.

    ``is_wildcard`` is migrated to settings in 27R1.
    ``is_solution_data_available`` is migrated to field_data in 27R1.
    ``register_pause_on_solution_events`` is migrated to events in 27R1.
    ``resume_on_solution_event`` is migrated to events in 27R1.
    ``unregister_pause_on_solution_events`` is migrated to events in 27R1.
    """

    def __init__(self, service, scheme):
        """Initialize ApplicationRuntime."""
        self.service = service
        self.scheme = scheme

    def get_product_version(self) -> FluentVersion:
        """Get product version."""
        return FluentVersion(self.service.get_product_version())

    def get_build_info(self) -> BuildInfo:
        """Get build info."""
        build_time, build_id, vcs_revision, vcs_branch = self.service.get_build_info()
        return BuildInfo(
            build_time=build_time,
            build_id=build_id,
            vcs_revision=vcs_revision,
            vcs_branch=vcs_branch,
        )

    def get_controller_process_info(self) -> ProcessInfo:
        """Get controller process info."""
        process_id, hostname, working_directory = (
            self.service.get_controller_process_info()
        )
        return ProcessInfo(
            process_id=process_id,
            hostname=hostname,
            working_directory=working_directory,
        )

    def get_solver_process_info(self) -> ProcessInfo:
        """Get solver process info."""
        process_id, hostname, working_directory = self.service.get_solver_process_info()
        return ProcessInfo(
            process_id=process_id,
            hostname=hostname,
            working_directory=working_directory,
        )

    def get_app_mode(self) -> Enum:
        """Get app mode."""
        from ansys.fluent.core import FluentMode

        return FluentMode(self.service.get_app_mode())

    def get_dimension(self) -> Enum:
        """Get dimension."""
        from ansys.fluent.core import Dimension

        if self.scheme.eval("(rp-3d?)"):
            return Dimension.THREE
        else:
            return Dimension.TWO

    def get_precision(self) -> Enum:
        """Get precision."""
        from ansys.fluent.core import Precision

        if self.scheme.eval("(rp-double?)"):
            return Precision.DOUBLE
        else:
            return Precision.SINGLE

    def get_processor_count(self) -> int:
        """Get processor count."""
        return self.scheme.eval("(string->number (rpgetvar 'parallel/nprocs_string))")

    def get_ui_mode(self) -> Enum:
        """Get UI mode."""
        from ansys.fluent.core import UIMode

        if not self.scheme.eval("(cx-gui?)") and not self.scheme.eval("(cx-graphics?)"):
            return UIMode.NO_GUI_OR_GRAPHICS
        elif not self.scheme.eval("(cx-gui?)"):
            return UIMode.NO_GUI
        elif self.scheme.eval("(cx-gui-hidden?)"):
            return UIMode.HIDDEN_GUI
        elif not self.scheme.eval("(cx-graphics?)"):
            return UIMode.NO_GRAPHICS
        else:
            return UIMode.GUI

    def get_graphics_driver(self) -> Enum:
        """Get graphics driver.

        Raises
        ------
        ValueError
            If the graphics driver is unknown.
        """
        driver_str = "null"
        if self.scheme.eval("(cx-graphics?)"):
            driver_str = self.scheme.eval("(cx-get-current-graphics-driver)")
            if not driver_str:
                driver_str = "auto"
        if platform.system() == "Windows":
            from ansys.fluent.core import FluentWindowsGraphicsDriver

            if driver_str == "null":
                return FluentWindowsGraphicsDriver.NULL
            elif driver_str == "msw":
                return FluentWindowsGraphicsDriver.MSW
            elif driver_str == "dx11":
                return FluentWindowsGraphicsDriver.DX11
            elif driver_str == "opengl2":
                return FluentWindowsGraphicsDriver.OPENGL2
            elif driver_str == "opengl":
                return FluentWindowsGraphicsDriver.OPENGL
            elif driver_str == "auto":
                return FluentWindowsGraphicsDriver.AUTO
            else:
                raise ValueError(f"Unknown graphics driver: {driver_str}")
        else:
            from ansys.fluent.core import FluentLinuxGraphicsDriver

            if driver_str == "null":
                return FluentLinuxGraphicsDriver.NULL
            elif driver_str == "x11":
                return FluentLinuxGraphicsDriver.X11
            elif driver_str == "opengl2":
                return FluentLinuxGraphicsDriver.OPENGL2
            elif driver_str == "opengl":
                return FluentLinuxGraphicsDriver.OPENGL
            elif driver_str == "auto":
                return FluentLinuxGraphicsDriver.AUTO
            else:
                raise ValueError(f"Unknown graphics driver: {driver_str}")

    def get_gpu_config(self) -> bool | list[int]:
        """Get GPU config.

        Raises
        ------
        ValueError
            If the GPU ID string cannot be parsed.
        """
        if not self.scheme.eval("(gpuapp-enabled?)"):
            return False
        config_str = self.scheme.eval("(rpgetvar 'parallel/gpgpu-selected)")
        if config_str == "True":
            return True
        if config_str == "False" or not config_str:
            return False
        config_str = config_str.strip("[]")
        try:
            return [int(token) for token in config_str.split(",") if token]
        except ValueError:
            raise ValueError(
                f"Failed to parse malformed GPU ID string configuration: {config_str!r}"
            )

    def start_python_journal(self, journal_name: str | None = None) -> int:
        """Start python journal."""
        return self.service.start_python_journal(journal_name=journal_name)

    def stop_python_journal(self, journal_id: str | None = None) -> str:
        """Stop python journal."""
        return self.service.stop_python_journal(journal_id=journal_id)

    def is_beta_enabled(self) -> bool:
        """Return whether beta features are enabled."""
        return self.service.is_beta_enabled()

    def exit(self) -> None:
        """Exit the server."""
        self.service.exit()

    def set_working_directory(self, path: PathType) -> None:
        """Change the client cortex working directory."""
        self.service.set_working_directory(path=path)

    def is_wildcard(self, input: str | None = None) -> bool:
        """Return whether *input* contains a wildcard pattern."""
        return self.service.is_wildcard(input=input)

    def is_solution_data_available(self) -> bool:
        """Return whether solution data is currently available."""
        return self.service.is_solution_data_available()

    def register_pause_on_solution_events(self, solution_event: SolverEvent) -> int:
        """Register pause on solution events."""
        return self.service.register_pause_on_solution_events(
            solution_event=solution_event
        )

    def resume_on_solution_event(self, registration_id: int) -> None:
        """Resume on solution event."""
        return self.service.resume_on_solution_event(registration_id=registration_id)

    def unregister_pause_on_solution_events(self, registration_id: int) -> None:
        """Unregister pause on solution events."""
        return self.service.unregister_pause_on_solution_events(
            registration_id=registration_id
        )


class ApplicationRuntimeV261(ApplicationRuntimeV261V252):
    """Application runtime for Fluent 26R1.

    ``enable_beta`` is implemented in the 26R1 server.
    """

    def __init__(self, service, scheme):
        """Initialize ApplicationRuntimeV252."""
        super().__init__(service, scheme)

    def enable_beta(self) -> None:
        """Enable beta features."""
        self.service.enable_beta()


class ApplicationRuntimeV252(ApplicationRuntimeV261V252):
    """Application runtime for Fluent 25R2.

    ``enable_beta`` is not implemented on the 25R2 server so it falls
    back to a Scheme call.
    """

    def __init__(self, service, scheme):
        """Initialize ApplicationRuntimeV252."""
        super().__init__(service, scheme)

    def enable_beta(self) -> None:
        """Enable beta features via Scheme (25R2 fallback)."""
        self.scheme.eval(
            '(fl-execute-cmd "file" "beta-settings" (list (cons "enable?" #t)))'
        )


class ApplicationRuntimeOld:
    """Application runtime backed by Scheme evaluation (Fluent < 25R2)."""

    def __init__(self, scheme_eval):
        """Initialize ApplicationRuntimeOld."""
        self.scheme = scheme_eval

    def get_product_version(self) -> FluentVersion:
        """Get product version."""
        return FluentVersion(
            ".".join(self.scheme.string_eval("(cx-version)").strip("()").split())
        )

    def get_build_info(self) -> BuildInfo:
        """Get build info."""
        return BuildInfo(
            build_time=self.scheme.eval("(inquire-build-time)"),
            build_id=self.scheme.eval("(inquire-build-id)"),
            vcs_revision=self.scheme.eval("(inquire-src-vcs-id)"),
            vcs_branch=self.scheme.eval("(inquire-src-vcs-branch)"),
        )

    def get_controller_process_info(self) -> ProcessInfo:
        """Get controller process info."""
        return ProcessInfo(
            process_id=self.scheme.eval("(cx-cortex-id)"),
            hostname=self.scheme.eval("(cx-cortex-host)"),
            working_directory=self.scheme.eval("(cortex-pwd)"),
        )

    def get_solver_process_info(self) -> ProcessInfo:
        """Get solver process info."""
        return ProcessInfo(
            process_id=self.scheme.eval("(cx-client-id)"),
            hostname=self.scheme.eval("(cx-client-host)"),
            working_directory=self.scheme.eval("(cx-send '(cx-client-pwd))"),
        )

    def get_app_mode(self) -> Enum:
        """Get app mode."""
        from ansys.fluent.core import FluentMode

        if self.scheme.eval("(cx-solver-mode?)"):
            mode_str = self.scheme.eval('(getenv "PRJAPP_APP")')
            if mode_str == "flaero_server":
                return FluentMode.SOLVER_AERO
            elif mode_str == "flicing":
                return FluentMode.SOLVER_ICING
            else:
                return FluentMode.SOLVER
        else:
            return FluentMode.MESHING

    def get_dimension(self) -> Enum:
        """Get dimension."""
        from ansys.fluent.core import Dimension

        if self.scheme.eval("(rp-3d?)"):
            return Dimension.THREE
        else:
            return Dimension.TWO

    def get_precision(self) -> Enum:
        """Get precision."""
        from ansys.fluent.core import Precision

        if self.scheme.eval("(rp-double?)"):
            return Precision.DOUBLE
        else:
            return Precision.SINGLE

    def get_processor_count(self) -> int:
        """Get processor count."""
        return self.scheme.eval("(string->number (rpgetvar 'parallel/nprocs_string))")

    def get_ui_mode(self) -> Enum:
        """Get UI mode."""
        from ansys.fluent.core import UIMode

        if not self.scheme.eval("(cx-gui?)") and not self.scheme.eval("(cx-graphics?)"):
            return UIMode.NO_GUI_OR_GRAPHICS
        elif not self.scheme.eval("(cx-gui?)"):
            return UIMode.NO_GUI
        elif self.scheme.eval("(cx-gui-hidden?)"):
            return UIMode.HIDDEN_GUI
        elif not self.scheme.eval("(cx-graphics?)"):
            return UIMode.NO_GRAPHICS
        else:
            return UIMode.GUI

    def get_graphics_driver(self) -> Enum:
        """Get graphics driver.

        Raises
        ------
        ValueError
            If the graphics driver is unknown.
        """
        driver_str = "null"
        if self.scheme.eval("(cx-graphics?)"):
            driver_str = self.scheme.eval("(cx-get-current-graphics-driver)")
            if not driver_str:
                driver_str = "auto"
        if platform.system() == "Windows":
            from ansys.fluent.core import FluentWindowsGraphicsDriver

            if driver_str == "null":
                return FluentWindowsGraphicsDriver.NULL
            elif driver_str == "msw":
                return FluentWindowsGraphicsDriver.MSW
            elif driver_str == "dx11":
                return FluentWindowsGraphicsDriver.DX11
            elif driver_str == "opengl2":
                return FluentWindowsGraphicsDriver.OPENGL2
            elif driver_str == "opengl":
                return FluentWindowsGraphicsDriver.OPENGL
            elif driver_str == "auto":
                return FluentWindowsGraphicsDriver.AUTO
            else:
                raise ValueError(f"Unknown graphics driver: {driver_str}")
        else:
            from ansys.fluent.core import FluentLinuxGraphicsDriver

            if driver_str == "null":
                return FluentLinuxGraphicsDriver.NULL
            elif driver_str == "x11":
                return FluentLinuxGraphicsDriver.X11
            elif driver_str == "opengl2":
                return FluentLinuxGraphicsDriver.OPENGL2
            elif driver_str == "opengl":
                return FluentLinuxGraphicsDriver.OPENGL
            elif driver_str == "auto":
                return FluentLinuxGraphicsDriver.AUTO
            else:
                raise ValueError(f"Unknown graphics driver: {driver_str}")

    def get_gpu_config(self) -> bool | list[int]:
        """Get GPU config.

        Raises
        ------
        ValueError
            If the GPU ID string cannot be parsed.
        """
        if not self.scheme.eval("(gpuapp-enabled?)"):
            return False
        config_str = self.scheme.eval("(rpgetvar 'parallel/gpgpu-selected)")
        if config_str == "True":
            return True
        if config_str == "False" or not config_str:
            return False
        config_str = config_str.strip("[]")
        try:
            return [int(token) for token in config_str.split(",") if token]
        except ValueError:
            raise ValueError(
                f"Failed to parse malformed GPU ID string configuration: {config_str!r}"
            )

    def start_python_journal(self, journal_name: str | None = None) -> int:
        """Start python journal."""
        if journal_name:
            self.scheme.exec([f'(api-start-python-journal "{journal_name}")'])
        else:
            self.scheme.eval("(define pyfluent-journal-str-port (open-output-string))")
            self.scheme.eval("(api-echo-python-port pyfluent-journal-str-port)")
            return "1"

    def stop_python_journal(self, journal_id: str | None = None) -> str:
        """Stop python journal."""
        if journal_id:
            self.scheme.eval("(api-unecho-python-port pyfluent-journal-str-port)")
            journal_str = self.scheme.eval(
                "(close-output-port pyfluent-journal-str-port)"
            )
            return journal_str
        else:
            self.scheme.exec(["(api-stop-python-journal)"])

    def is_beta_enabled(self) -> bool:
        """Return whether beta features are enabled."""
        return self.scheme.eval("(is-beta-feature-available?)")

    def enable_beta(self):
        """Enable beta features.

        Raises
        ------
        RuntimeError
            Not supported before Fluent 2025 R2.
        """
        raise RuntimeError(
            "Enabling beta is not supported by PyFluent for Fluent versions before 2025 R2."
        )

    def is_wildcard(self, input: str | None = None) -> bool:
        """Return whether *input* contains a wildcard pattern."""
        return self.scheme.eval(f'(has-fnmatch-wild-card? "{input}")')

    def is_solution_data_available(self) -> bool:
        """Return whether solution data is currently available."""
        return self.scheme.eval("(data-valid?)")

    def register_pause_on_solution_events(self, solution_event: SolverEvent) -> int:
        """Register pause on solution events."""
        unique_id: int = self.scheme.eval(
            f"""
            (let
                ((ids
                    (let loop ((i 1))
                        (define next-id (string->symbol (format #f "pyfluent-~d" i)))
                        (if (check-monitor-existence next-id)
                            (loop (1+ i))
                            (list i next-id)
                            )
                        )
                    ))
                (register-solution-monitor
                    (cadr ids)
                    (lambda (niter time)
                        (if (integer? niter)
                            (begin
                                (events/transmit 'auto-pause (cons (car ids) niter))
                                (grpcserver/auto-pause (is-server-running?) (cadr ids))
                                )
                            )
                        ()
                        )
                    {"#t" if solution_event == SolverEvent.TIMESTEP_ENDED else "#f"}
                    )
                (car ids)
                )
        """
        )
        return unique_id

    def resume_on_solution_event(self, registration_id: int) -> None:
        """Resume on solution event."""
        self.scheme.eval(
            f"(grpcserver/auto-resume (is-server-running?) 'pyfluent-{registration_id})"
        )

    def unregister_pause_on_solution_events(self, registration_id: int) -> None:
        """Unregister pause on solution events."""
        self.scheme.eval(f"(cancel-solution-monitor 'pyfluent-{registration_id})")

    def exit(self) -> None:
        """Exit the server."""
        self.scheme.exec(("(exit-server)",))

    def set_working_directory(self, path: PathType) -> None:
        """Change the client cortex working directory."""
        self.scheme.eval(f'(syncdir "{os.fspath(path)}")')
