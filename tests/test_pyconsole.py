from pathlib import Path
import sys

import pytest

import ansys.fluent.core as pyfluent


def _in_venv():
    return sys.prefix != sys.base_prefix


def _get_grpc_version_in_pyfluent_env():
    import grpc

    return grpc.__version__


def _get_grpc_version_in_fluent_env():
    session = pyfluent.launch_fluent()
    session.scheme_eval.scheme_eval('(%py-exec "import grpc")')
    return session.scheme_eval.scheme_eval('(%py-eval "grpc.__version__")')

def _is_pyconsole_activated(session):
    return session.scheme_eval("(%cx-pyconsole-activated?)")


# Note: this test won't work with editable install of PyFluent because the PyFluent package files are not copied
# to the expected location in the Fluent container. To run this test, install PyFluent without the -e option.
@pytest.mark.fluent_version("dev")
def test_pyconsole_launch():
    if not _in_venv():
        pytest.skip("This test must be run in a virtual environment.")

    grpc_version_pyfluent = _get_grpc_version_in_pyfluent_env()
    grpc_version_fluent = _get_grpc_version_in_fluent_env()
    if grpc_version_pyfluent > grpc_version_fluent:
        pytest.skip(
            "gRPC version in PyFluent environment is higher than in Fluent environment. gRPC and related dependencies must be updated in Fluent environment."
        )
    elif grpc_version_pyfluent < grpc_version_fluent:
        pytest.skip(
            "gRPC version in Fluent environment is higher than in PyFluent environment. gRPC and related dependencies must be updated in PyFluent environment."
        )

    src_pyfluent_dir = str(Path(pyfluent.__file__).parents[3])
    version_for_file_name = pyfluent.FluentVersion.current_dev().number
    dst_pyfluent_dir = f"/ansys_inc/v{version_for_file_name}/commonfiles/CPython/3_10/linx64/Release/Ansys/PyFluentCore"
    solver_container_dict = pyfluent.launch_fluent(start_container=True, dry_run=True, py=True)
    solver_container_dict["volumes"].append(f"{src_pyfluent_dir}:{dst_pyfluent_dir}")
    solver_session = pyfluent.launch_fluent(container_dict=solver_container_dict)
    assert solver_session is not None
    assert _is_pyconsole_activated(solver_session) is True

    meshing_container_dict = pyfluent.launch_fluent(start_container=True, dry_run=True, py=True, mode=pyfluent.FluentMode.MESHER)
    meshing_container_dict["volumes"].append(f"{src_pyfluent_dir}:{dst_pyfluent_dir}")
    meshing_session = pyfluent.launch_fluent(container_dict=meshing_container_dict)
    assert meshing_session is not None
    assert _is_pyconsole_activated(meshing_session) is True
