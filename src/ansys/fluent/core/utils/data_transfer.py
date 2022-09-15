from functools import partial
import os

from ansys.fluent.core.utils.async_execution import asynchronous
from ansys.fluent.core.utils.logging import LOG


@asynchronous
def read_case_into(target, mesh_only, file_name):
    LOG.info(f"Trying to read case: {file_name}")
    target.upload(file_name)
    target.file.read(file_name=file_name, file_type="mesh" if mesh_only else "case")
    LOG.info(f"Have read case: {file_name}")


def read_case_into_each(targets, mesh_only, file_name):
    reads = []
    for target in targets:
        reads.append(read_case_into(target, mesh_only, file_name))
    for r in reads:
        r.result()


def transfer_case(
    source,
    targets,
    mesh_only,
    file_name_stem,
    num_files_to_try,
    clean_up_temp_file,
    overwrite_previous,
):
    for idx in range(num_files_to_try):
        file_name = (file_name_stem or "temp_case_file_") + "_" + str(idx)
        folder = os.getenv("TMP", os.getenv("TMPDIR", "."))
        file_name = os.path.join(folder, file_name)
        LOG.info(f"Trying to save mesh from meshing session: {file_name}")
        if overwrite_previous or not os.path.isfile(file_name):
            LOG.info(f"Saving mesh from meshing session: {file_name}")
            file_menu = source.tui.file
            writer = partial(
                file_menu.write_mesh if mesh_only else file_menu.write_case, file_name
            )
            if os.path.isfile(file_name):
                writer("y")
            else:
                writer()
            full_file_name = file_name + "." + ("msh.h5" if mesh_only else "cas.h5")
            source.download(full_file_name, ".")
            LOG.info(f"Saved mesh from meshing session: {full_file_name}")
            read_case_into_each(targets, mesh_only, full_file_name)
            if clean_up_temp_file:
                try:
                    os.remove(full_file_name)
                except BaseException as ex:
                    LOG.warn(
                        f"Encountered exception while cleaning up during case transfer {ex}"
                    )
            return
    raise RuntimeError("Could not write mesh from meshing session.")
