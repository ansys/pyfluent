"""Session to session data transfer, supporting Fluent in all modes."""


from functools import partial
import logging
import os
from pathlib import Path, PurePosixPath
import tempfile
from typing import Optional

import ansys.fluent.core as pyfluent
from ansys.fluent.core.launcher.fluent_container import DEFAULT_CONTAINER_MOUNT_PATH
from ansys.fluent.core.utils.execution import asynchronous

network_logger = logging.getLogger("pyfluent.networking")


@asynchronous
def _read_case_into(solver, file_type, file_name, full_file_name_container=None):
    network_logger.info(f"Trying to read case: {file_name}")
    solver.upload(file_name)
    if full_file_name_container:
        solver.file.read(file_name=full_file_name_container, file_type=file_type)
    else:
        solver.file.read(file_name=file_name, file_type=file_type)
    network_logger.info(f"Have read case: {file_name}")


def _read_case_into_each(solvers, file_type, file_name, full_file_name_container=None):
    reads = []
    for solver in solvers:
        reads.append(
            _read_case_into(solver, file_type, file_name, full_file_name_container)
        )
    for r in reads:
        r.result()


def transfer_case(
    source_instance,
    solvers,
    file_type: str,
    file_name_stem: str,
    num_files_to_try: int,
    clean_up_temp_file: bool,
    overwrite_previous: bool,
    workdir: Optional[str] = None,
    container_workdir: Optional[str] = None,
):
    """Transfer case between instances.

    Parameters
    ----------
    source_instance : object
        Fluent instance (tested for meshing instance)
    solvers : iterable
        Sequence of solver instances
    file_type : str
        "case" or "mesh"
    file_name_stem : str
        Optional file name stem
    num_files_to_try : int
        Optional number of files to try to write,
        each with a different generated name.
        Defaults to 1
    clean_up_temp_file: bool
        Whether to remove the file at the end
    overwrite_previous: bool
        Whether to overwrite the file if it already exists
    workdir : str, optional
        Working directory that is accessible by the Fluent client as well as PyFluent.
    container_workdir : str, optional
        If using a Fluent container image, specifies the working directory that is accessible by the Fluent client
        inside the container, which should also be mounted to the container from the
        host system path specified in ``workdir``.

    Returns
    -------
    None
    """
    inside_container = source_instance.connection_properties.inside_container
    if not workdir:
        workdir = Path(pyfluent.EXAMPLES_PATH)
    else:
        workdir = Path(workdir)
    if inside_container:
        if not container_workdir:
            network_logger.warning(
                "Fluent is running inside a container, and no 'container_workdir' was specified for "
                "'transfer_case'. Assuming that the default container mount path "
                f"'{DEFAULT_CONTAINER_MOUNT_PATH}' is being used. "
            )
            container_workdir = PurePosixPath(DEFAULT_CONTAINER_MOUNT_PATH)
            network_logger.debug(f"container_workdir: {container_workdir}")
        else:
            container_workdir = PurePosixPath(container_workdir)
    for idx in range(num_files_to_try):
        file_name_tmp = (file_name_stem or "temp_case_file") + "_" + str(idx)
        folder = Path(tempfile.mkdtemp(prefix="temp_store-", dir=workdir))
        file_name = folder / file_name_tmp
        if inside_container:
            file_name_container = container_workdir / folder.name / file_name_tmp
            network_logger.debug(f"file_name: {file_name}")
            network_logger.debug(f"file_name_container: {file_name_container}")
        network_logger.info(f"Trying to save mesh from meshing session: {file_name}")
        full_file_name = Path(
            str(file_name) + "." + ("msh.h5" if file_type == "mesh" else "cas.h5")
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
            network_logger.info(f"Saving mesh from meshing session: {file_name}")
            file_menu = source_instance.tui.file
            if inside_container:
                writer = partial(
                    file_menu.write_mesh
                    if file_type == "mesh"
                    else file_menu.write_case,
                    str(full_file_name_container),
                )
            else:
                writer = partial(
                    file_menu.write_mesh
                    if file_type == "mesh"
                    else file_menu.write_case,
                    str(full_file_name),
                )
            if os.path.isfile(full_file_name):
                writer("y")
            else:
                writer()
            source_instance.download(full_file_name, ".")
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
    raise RuntimeError("Could not write mesh from meshing session.")
