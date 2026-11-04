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

"""Session to session data transfer, supporting Fluent in all modes."""

from functools import partial
import logging
import os
from pathlib import Path, PurePosixPath
from typing import TYPE_CHECKING

from ansys.fluent.core.module_config import config
from ansys.fluent.core.utils.execution import asynchronous

if TYPE_CHECKING:
    from collections.abc import Iterable

    from ansys.fluent.core.meshing.session.base_meshing import BaseMeshing
    from ansys.fluent.core.solver.session.solver import Solver

network_logger = logging.getLogger("pyfluent.networking")


class MeshWriteError(RuntimeError):
    """Raised when mesh write is unsuccessful."""

    def __init__(self):
        """Initializes MeshWriteError."""
        super().__init__("Could not write mesh from meshing session.")


@asynchronous
def _read_case_into(solver, file_type, file_name, full_file_name_container=None):
    network_logger.info(f"Trying to read case: {file_name}")
    try:
        solver._file_transfer_service.upload(file_name=file_name)
    except AttributeError:
        pass
    if full_file_name_container:
        solver.settings.file.read(
            file_name=full_file_name_container, file_type=file_type
        )
    else:
        solver.settings.file.read(file_name=file_name, file_type=file_type)
    network_logger.info(f"Have read case: {file_name}")


def _read_case_into_each(solvers, file_type, file_name, full_file_name_container=None):
    reads = []
    for solver in solvers:
        reads.append(
            _read_case_into(solver, file_type, file_name, full_file_name_container)
        )
    for r in reads:
        r.result()


def transfer_case(  # noqa: C901
    source_instance: "BaseMeshing | Solver",
    solvers: "Iterable[Solver]",
    file_type: str = "case",
    file_name_stem: str | None = None,
    num_files_to_try: int = 1,
    clean_up_temp_file: bool = True,
    overwrite_previous: bool = True,
    workdir: str | None = None,
    container_workdir: str | None = None,
) -> None:
    """Transfer a case or mesh from a source session (meshing or solver)
    to one or more destination solver sessions.

    Parameters
    ----------
    source_instance : BaseMeshing | Solver
        Meshing or solver session instance to transfer the case or mesh from.
    solvers : Iterable[Solver]
        Sequence of solver instances to transfer the case or mesh to.
    file_type : str, optional
        ``"case"`` or ``"mesh"``. Defaults to ``"case"``.
    file_name_stem : str, optional
        File name stem. If not specified (``None``), a default stem
        (``"temp_case_file"``) is used.
    num_files_to_try : int, optional
        Number of files to try to write, each with a different generated name.
        Defaults to ``1``.
    clean_up_temp_file : bool, optional
        Whether to remove the file at the end. Defaults to ``True``.
    overwrite_previous : bool, optional
        Whether to overwrite the file if it already exists. Defaults to ``True``.
    workdir : str, optional
        Working directory that is accessible by the Fluent client as well as PyFluent.
    container_workdir : str, optional
        If using a Fluent container image, specifies the working directory that is accessible by the Fluent client
        inside the container, which should also be mounted to the container from the
        host system path specified in ``workdir``.

    Returns
    -------
    None

    Raises
    ------
    MeshWriteError
        If mesh cannot be written from ``source_instance``.
    """
    inside_container = source_instance.connection_properties.inside_container
    if not workdir:
        workdir = Path(config.examples_path)
    else:
        workdir = Path(workdir)
    if inside_container:
        if not container_workdir:
            network_logger.warning(
                "Fluent is running inside a container, and no 'container_workdir' was specified for "
                "'transfer_case'. Assuming that the default container mount path "
                f"'{config.container_mount_target}' is being used. "
            )
            container_workdir = PurePosixPath(config.container_mount_target)
            network_logger.debug(f"container_workdir: {container_workdir}")
        else:
            container_workdir = PurePosixPath(container_workdir)
    for idx in range(num_files_to_try):
        file_name_tmp = (file_name_stem or "temp_case_file") + "_" + str(idx)
        if inside_container:
            file_name_container = container_workdir / file_name_tmp
            network_logger.debug(f"file_name: {file_name_tmp}")
            network_logger.debug(f"file_name_container: {file_name_container}")
        network_logger.info(
            f"Trying to save mesh from meshing session: {file_name_tmp}"
        )
        full_file_name = Path(
            str(file_name_tmp) + "." + ("msh.h5" if file_type == "mesh" else "cas.h5")
        )
        if inside_container:
            full_file_name_container = PurePosixPath(
                str(file_name_container)
                + "."
                + ("msh.h5" if file_type == "mesh" else "cas.h5")
            )
            network_logger.debug(
                f"full_file_name_container: {full_file_name_container}"
            )
        if overwrite_previous or not os.path.isfile(full_file_name):
            network_logger.info(f"Saving mesh from meshing session: {file_name_tmp}")
            file_menu = source_instance.tui.file
            if inside_container:
                writer = partial(
                    (
                        file_menu.write_mesh
                        if file_type == "mesh"
                        else file_menu.write_case
                    ),
                    str(full_file_name_container),
                )
            else:
                writer = partial(
                    (
                        file_menu.write_mesh
                        if file_type == "mesh"
                        else file_menu.write_case
                    ),
                    str(full_file_name),
                )
            if os.path.isfile(full_file_name):
                writer("y")
            else:
                writer()
            try:
                source_instance._file_transfer_service.download(
                    file_name=full_file_name
                )
            except AttributeError:
                pass
            network_logger.info(f"Saved mesh from meshing session: {full_file_name}")
            if inside_container:
                _read_case_into_each(
                    solvers,
                    file_type,
                    str(full_file_name),
                    str(full_file_name_container),
                )
            else:
                _read_case_into_each(solvers, file_type, str(full_file_name))
            if clean_up_temp_file:
                try:
                    os.remove(full_file_name)
                except Exception as ex:
                    network_logger.warning(
                        f"Encountered exception while cleaning up during case transfer {ex}"
                    )
            return
    raise MeshWriteError()
