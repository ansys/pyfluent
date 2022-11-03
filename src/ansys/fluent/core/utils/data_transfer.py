from functools import partial
import os
import tempfile

import ansys.fluent.core as pyfluent
from ansys.fluent.core.utils.async_execution import asynchronous
from ansys.fluent.core.utils.logging import LOG


@asynchronous
def read_case_into(solver, file_type, file_name):
    LOG.info(f"Trying to read case: {file_name}")
    solver.upload(file_name)
    solver.file.read(file_name=file_name, file_type=file_type)
    LOG.info(f"Have read case: {file_name}")


def read_case_into_each(solvers, file_type, file_name):
    reads = []
    for solver in solvers:
        reads.append(read_case_into(solver, file_type, file_name))
    for r in reads:
        r.result()


def transfer_case(
    source_instance,
    solvers,
    file_type,
    file_name_stem,
    num_files_to_try,
    clean_up_temp_file,
    overwrite_previous,
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
    clean_up_mesh_file: bool
        Whether to remove the file at the end
    overwrite_previous: bool
        Whether to overwrite the file if it already exists
    Returns
    -------
    None
    """
    for idx in range(num_files_to_try):
        file_name = (file_name_stem or "temp_case_file_") + "_" + str(idx)
        folder = tempfile.mkdtemp(prefix="temp_store-", dir=pyfluent.EXAMPLES_PATH)
        file_name = os.path.join(folder, file_name)
        LOG.info(f"Trying to save mesh from meshing session: {file_name}")
        if overwrite_previous or not os.path.isfile(file_name):
            LOG.info(f"Saving mesh from meshing session: {file_name}")
            file_menu = source_instance.tui.file
            writer = partial(
                file_menu.write_mesh if file_type == "mesh" else file_menu.write_case,
                file_name,
            )
            if os.path.isfile(file_name):
                writer("y")
            else:
                writer()
            full_file_name = (
                file_name + "." + ("msh.h5" if file_type == "mesh" else "cas.h5")
            )
            source_instance.download(full_file_name, ".")
            LOG.info(f"Saved mesh from meshing session: {full_file_name}")
            read_case_into_each(solvers, file_type, full_file_name)
            if clean_up_temp_file:
                try:
                    os.remove(full_file_name)
                except BaseException as ex:
                    LOG.warn(
                        f"Encountered exception while cleaning up during case transfer {ex}"
                    )
            return
    raise RuntimeError("Could not write mesh from meshing session.")
