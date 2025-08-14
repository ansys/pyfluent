# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
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

"""Session utilities."""

from typing import Any, Dict

import ansys.fluent.core as pyfluent
from ansys.fluent.core.launcher.container_launcher import DockerLauncher
from ansys.fluent.core.launcher.launch_options import (
    Dimension,
    FluentLinuxGraphicsDriver,
    FluentMode,
    FluentWindowsGraphicsDriver,
    Precision,
    UIMode,
)
from ansys.fluent.core.launcher.pim_launcher import PIMLauncher
from ansys.fluent.core.launcher.standalone_launcher import StandaloneLauncher
from ansys.fluent.core.utils.fluent_version import FluentVersion


class SessionBase:
    """Base class for Fluent sessions.

    This class is not intended to be used directly. Instead, use
    the `from_connection`, `from_container`, `from_install`,
    or `from_pim` functions to create a session.
    """

    _session_mode = {
        "Meshing": FluentMode.MESHING,
        "PureMeshing": FluentMode.PURE_MESHING,
        "PrePost": FluentMode.PRE_POST,
        "Solver": FluentMode.SOLVER,
        "SolverAero": FluentMode.SOLVER_AERO,
        "SolverIcing": FluentMode.SOLVER_ICING,
    }

    @classmethod
    def from_install(
        cls,
        ui_mode: UIMode | str | None = None,
        graphics_driver: (
            FluentWindowsGraphicsDriver | FluentLinuxGraphicsDriver | str
        ) = None,
        product_version: FluentVersion | str | float | int | None = None,
        dimension: Dimension | int | None = None,
        precision: Precision | str | None = None,
        processor_count: int | None = None,
        journal_file_names: None | str | list[str] = None,
        start_timeout: int = 60,
        additional_arguments: str = "",
        env: Dict[str, Any] = {},  # noqa: B006
        cleanup_on_exit: bool = True,
        dry_run: bool = False,
        start_transcript: bool = True,
        case_file_name: str | None = None,
        case_data_file_name: str | None = None,
        lightweight_mode: bool | None = None,
        py: bool | None = None,
        gpu: bool | None = None,
        cwd: str | None = None,
        fluent_path: str | None = None,
        topy: str | list | None = None,
        start_watchdog: bool | None = None,
        file_transfer_service: Any | None = None,
    ):
        """
        Launch a Fluent session in standalone mode.

        Parameters
        ----------
        ui_mode : UIMode
            Defines the user interface mode for Fluent. Options correspond to values in the ``UIMode`` enum.
        graphics_driver : FluentWindowsGraphicsDriver or FluentLinuxGraphicsDriver
            Specifies the graphics driver for Fluent. Options are from the ``FluentWindowsGraphicsDriver`` enum
            (for Windows) or the ``FluentLinuxGraphicsDriver`` enum (for Linux).
        product_version : FluentVersion or str or float or int, optional
            Indicates the version of Ansys Fluent to launch. For example, to use version 2025 R1, pass
            ``FluentVersion.v251``, ``"25.1.0"``, ``"25.1"``, ``25.1``, or ``251``. Defaults to ``None``,
            which uses the newest installed version.
        dimension : Dimension or int, optional
            Specifies the geometric dimensionality of the Fluent simulation. Defaults to ``None``,
            which corresponds to ``Dimension.THREE``. Acceptable values are from the ``Dimension`` enum
            (``Dimension.TWO`` or ``Dimension.THREE``) or integers ``2`` and ``3``.
        precision : Precision or str, optional
            Defines the floating point precision. Defaults to ``None``, which corresponds to
            ``Precision.DOUBLE``. Acceptable values are from the ``Precision`` enum (``Precision.SINGLE``
            or ``Precision.DOUBLE``) or strings ``"single"`` and ``"double"``.
        processor_count : int, optional
            Specifies the number of processors to use. Defaults to ``None``, which uses 1 processor.
            In job scheduler environments, this value limits the total number of allocated cores.
        journal_file_names : str or list of str, optional
            Path(s) to a Fluent journal file(s) that Fluent will execute. Defaults to ``None``.
        start_timeout : int, optional
            Maximum time in seconds allowed for connecting to the Fluent server. Defaults to 60 seconds.
        additional_arguments : str, optional
            Additional command-line arguments for Fluent, formatted as they would be on the command line.
        env : dict[str, str], optional
            A mapping for modifying environment variables in Fluent. Defaults to ``None``.
        cleanup_on_exit : bool, optional
            Determines whether to shut down the connected Fluent session when exiting PyFluent or calling
            the session's `exit()` method. Defaults to True.
        dry_run : bool, optional
            If True, does not launch Fluent but prints configuration information instead. The `call()` method
            returns a tuple containing the launch string and server info file name. Defaults to False.
        start_transcript : bool, optional
            Indicates whether to start streaming the Fluent transcript in the client. Defaults to True;
            streaming can be controlled via `transcript.start()` and `transcript.stop()` methods on the session object.
        case_file_name : str, optional
            Name of the case file to read into the Fluent session. Defaults to None.
        case_data_file_name : str, optional
            Name of the case data file. If both case and data files are provided, they are read into the session.
        lightweight_mode : bool, optional
            If True, runs in lightweight mode where mesh settings are read into a background solver session,
            replacing it once complete. This parameter is only applicable when `case_file_name` is provided; defaults to False.
        py : bool, optional
            If True, runs Fluent in Python mode. Defaults to None.
        gpu : bool, optional
            If True, starts Fluent with GPU Solver enabled.
        cwd : str, optional
            Working directory for the Fluent client.
        fluent_path: str, optional
            User-specified path for Fluent installation.
        topy :  bool or str, optional
            A flag indicating whether to write equivalent Python journals from provided journal files; can also specify
            a filename for the new Python journal.
        start_watchdog : bool, optional
            When `cleanup_on_exit` is True, defaults to True; an independent watchdog process ensures that any local
            GUI-less Fluent sessions started by PyFluent are properly closed when the current Python process ends.
        file_transfer_service : Any
            Service for uploading/downloading files to/from the server.

        Raises
        ------
        UnexpectedKeywordArgument
            If an unexpected keyword argument is provided.

        Notes
        -----
        In job scheduler environments (e.g., SLURM, LSF, PBS), resources and compute nodes are allocated,
        and core counts are queried from these environments before being passed to Fluent.
        """
        mode = cls._session_mode[cls.__name__]
        argvals = locals().copy()
        argvals.pop("cls", None)  # Remove the class reference from the arguments
        launcher = StandaloneLauncher(**argvals)
        return launcher()

    @classmethod
    def from_container(
        cls,
        ui_mode: UIMode | str | None = None,
        graphics_driver: (
            FluentWindowsGraphicsDriver | FluentLinuxGraphicsDriver | str | None
        ) = None,
        product_version: FluentVersion | str | float | int | None = None,
        dimension: Dimension | int | None = None,
        precision: Precision | str | None = None,
        processor_count: int | None = None,
        start_timeout: int = 60,
        additional_arguments: str = "",
        container_dict: dict | None = None,
        dry_run: bool = False,
        cleanup_on_exit: bool = True,
        start_transcript: bool = True,
        py: bool | None = None,
        gpu: bool | None = None,
        start_watchdog: bool | None = None,
        file_transfer_service: Any | None = None,
    ):
        """
        Launch a Fluent session in container mode.

        Parameters
        ----------
        ui_mode : UIMode
            Defines the user interface mode for Fluent. Options correspond to values in the ``UIMode`` enum.
        graphics_driver : FluentWindowsGraphicsDriver or FluentLinuxGraphicsDriver
            Specifies the graphics driver for Fluent. Options are from the ``FluentWindowsGraphicsDriver`` enum
            (for Windows) or the ``FluentLinuxGraphicsDriver`` enum (for Linux).
        product_version :  FluentVersion or str or float or int, optional
            Indicates the version of Ansys Fluent to launch. For example, to use version 2025 R1, pass
            any of ``FluentVersion.v251``, ``"25.1.0"``, ``"25.1"``, ``25.1``, or ``251``. Defaults to ``None``,
            which uses the newest installed version.
        dimension : Dimension or int, optional
            Specifies the geometric dimensionality of the Fluent simulation. Defaults to ``None``,
            which corresponds to ``Dimension.THREE``. Acceptable values include ``Dimension.TWO``,
            ``Dimension.THREE``, or integers ``2`` and ``3``.
        precision : Precision or str, optional
            Defines the floating point precision. Defaults to ``None``, which corresponds to
            ``Precision.DOUBLE``. Acceptable values include ``Precision.SINGLE``,
            ``Precision.DOUBLE``, or strings ``"single"`` and ``"double"``.
        processor_count : int, optional
            Specifies the number of processors to use. Defaults to ``None``, which uses 1 processor.
            In job scheduler environments, this value limits the total number of allocated cores.
        start_timeout : int, optional
            Maximum allowable time in seconds for connecting to the Fluent server. Defaults to 60 seconds.
        additional_arguments : str, optional
            Additional command-line arguments for Fluent, formatted as they would be on the command line.
        container_dict : dict, optional
            Configuration dictionary for launching Fluent inside a Docker container. See also
            :mod:`~ansys.fluent.core.launcher.fluent_container`.
        dry_run : bool, optional
            If True, does not launch Fluent but prints configuration information instead. If dry running a
            container start, this method will return the configured ``container_dict``. Defaults to False.
        cleanup_on_exit : bool
            Determines whether to shut down the connected Fluent session upon exit or when calling
            the session's `exit()` method. Defaults to True.
        start_transcript : bool
            Indicates whether to start streaming the Fluent transcript in the client. Defaults to True;
            streaming can be controlled via `transcript.start()` and `transcript.stop()` methods on the session object.
        py : bool, optional
            If True, runs Fluent in Python mode. Defaults to None.
        gpu : bool, optional
            If True, starts Fluent with GPU Solver enabled.
        start_watchdog : bool, optional
            If True and `cleanup_on_exit` is True, an independent watchdog process is run to ensure that any local
            GUI-less Fluent sessions started by PyFluent are properly closed when the current Python process ends.
        file_transfer_service : Any, optional
            Service for uploading/downloading files to/from the server.

        Returns
        -------
        Meshing | PureMeshing | Solver | SolverIcing | dict
            Session object or configuration dictionary if ``dry_run`` is True.

        Raises
        ------
        UnexpectedKeywordArgument
            If an unexpected keyword argument is provided.

        Notes
        -----
        In job scheduler environments (e.g., SLURM, LSF, PBS), resources and compute nodes are allocated,
        and core counts are queried from these environments before being passed to Fluent.
        """
        mode = cls._session_mode[cls.__name__]
        argvals = locals().copy()
        argvals.pop("cls", None)
        launcher = DockerLauncher(**argvals)
        return launcher()

    @classmethod
    def from_pim(
        cls,
        ui_mode: UIMode | str | None = None,
        graphics_driver: (
            FluentWindowsGraphicsDriver | FluentLinuxGraphicsDriver | str | None
        ) = None,
        product_version: FluentVersion | str | float | int | None = None,
        dimension: Dimension | int | None = None,
        precision: Precision | str | None = None,
        processor_count: int | None = None,
        start_timeout: int = 60,
        additional_arguments: str = "",
        cleanup_on_exit: bool = True,
        dry_run: bool | None = None,
        start_transcript: bool = True,
        gpu: bool | None = None,
        start_watchdog: bool | None = None,
        file_transfer_service: Any | None = None,
    ):
        """
        Launch a Fluent session in `PIM <https://pypim.docs.pyansys.com/version/stable/>`_ mode.

        Parameters
        ----------
        ui_mode : UIMode or str, optional
            Defines the user interface mode for Fluent. Options correspond to values in the ``UIMode`` enum.
        graphics_driver : FluentWindowsGraphicsDriver or FluentLinuxGraphicsDriver
            Specifies the graphics driver for Fluent. Options are from the ``FluentWindowsGraphicsDriver`` enum
            (for Windows) or the ``FluentLinuxGraphicsDriver`` enum (for Linux).
        product_version : FluentVersion or str or float or int, optional
            Indicates the version of Ansys Fluent to launch. For example, to use version 2025 R1, pass
            any of ``FluentVersion.v251``, ``"25.1.0"``, ``"25.1"``, ``25.1``, or ``251``. Defaults to ``None``,
            which uses the newest installed version.
        dimension : Dimension or int, optional
            Specifies the geometric dimensionality of the Fluent simulation. Defaults to ``None``,
            which corresponds to ``Dimension.THREE``. Acceptable values include ``Dimension.TWO``,
            ``Dimension.THREE``, or integers ``2`` and ``3``.
        precision : Precision or str, optional
            Defines the floating point precision. Defaults to ``None``, which corresponds to
            ``Precision.DOUBLE``. Acceptable values include ``Precision.SINGLE``,
            ``Precision.DOUBLE``, or strings ``"single"`` and ``"double"``.
        processor_count : int, optional
            Specifies the number of processors to use. Defaults to ``None``, which uses 1 processor.
            In job scheduler environments, this value limits the total number of allocated cores.
        start_timeout : int, optional
            Maximum allowable time in seconds for connecting to the Fluent server. Defaults to 60 seconds.
        additional_arguments : str, optional
            Additional command-line arguments for Fluent, formatted as they would be on the command line.
        cleanup_on_exit : bool
            Determines whether to shut down the connected Fluent session upon exit or when calling
            the session's `exit()` method. Defaults to True.
        dry_run : bool, optional
            If True, does not launch Fluent but prints configuration information instead. If dry running a
            PIM start, this method will return a configuration dictionary. Defaults to False.
        start_transcript : bool
            Indicates whether to start streaming the Fluent transcript in the client. Defaults to True;
            streaming can be controlled via `transcript.start()` and `transcript.stop()` methods on the session object.
        gpu : bool, optional
            If True, starts Fluent with GPU Solver enabled.
        start_watchdog : bool, optional
            If True and `cleanup_on_exit` is True, an independent watchdog process is run to ensure that any local
            GUI-less Fluent sessions started by PyFluent are properly closed when the current Python process ends.
        file_transfer_service : Any, optional
            Service for uploading/downloading files to/from the server.

        Returns
        -------
        Union[Meshing, PureMeshing, Solver, SolverIcing, dict]
            Session object or configuration dictionary if ``dry_run`` is True.

        Raises
        ------
        UnexpectedKeywordArgument
            If an unexpected keyword argument is provided.

        Notes
        -----
        In job scheduler environments (e.g., SLURM, LSF, PBS), resources and compute nodes are allocated,
        and core counts are queried from these environments before being passed to Fluent.
        """
        mode = cls._session_mode[cls.__name__]
        argvals = locals().copy()
        argvals.pop("cls", None)
        launcher = PIMLauncher(**argvals)
        return launcher()

    @classmethod
    def from_connection(
        cls,
        ip: str | None = None,
        port: int | None = None,
        server_info_file_name: str | None = None,
        password: str | None = None,
    ):
        """Connect to an existing Fluent server instance.

        Parameters
        ----------
        ip : str, optional
            IP address for connecting to an existing Fluent instance. The
            IP address defaults to ``"127.0.0.1"``. You can also use the environment
            variable ``PYFLUENT_FLUENT_IP=<ip>`` to set this parameter.
            The explicit value of ``ip`` takes precedence over ``PYFLUENT_FLUENT_IP=<ip>``.
        port : int, optional
            Port to listen on for an existing Fluent instance. You can use the
            environment variable ``PYFLUENT_FLUENT_PORT=<port>`` to set a default
            value. The explicit value of ``port`` takes precedence over
            ``PYFLUENT_FLUENT_PORT=<port>``.
        server_info_file_name: str
            Path to server-info file written out by Fluent server. The default is
            ``None``. PyFluent uses the connection information in the file to
            connect to a running Fluent session.
        password : str, optional
            Password to connect to existing Fluent instance.

        Raises
        ------
        TypeError
            If the session type does not match the expected session type.
        """
        session = pyfluent.connect_to_fluent(
            ip=ip,
            port=port,
            server_info_file_name=server_info_file_name,
            password=password,
        )

        expected = "Solver" if cls.__name__ == "PrePost" else cls.__name__
        actual = session.__class__.__name__

        if actual != expected:
            raise TypeError(
                f"Session type mismatch: expected {expected}, got {actual}."
            )

        return session


class Meshing(SessionBase):
    """Encapsulates a Fluent server for meshing session connection."""

    pass


class PureMeshing(SessionBase):
    """Encapsulates a Fluent server for pure meshing session connection."""

    pass


class PrePost(SessionBase):
    """Encapsulates a Fluent server for pre-post session connection."""

    pass


class Solver(SessionBase):
    """Encapsulates a Fluent server for solver session connection."""

    pass


class SolverAero(SessionBase):
    """Encapsulates a Fluent server for solver aero session connection."""

    pass


class SolverIcing(SessionBase):
    """Encapsulates a Fluent server for solver icing session connection."""

    pass
