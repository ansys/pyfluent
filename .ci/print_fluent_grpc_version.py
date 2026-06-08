"""Get gRPC version from Fluent image and print it to the console."""

import ansys.fluent.core as pyfluent
from ansys.fluent.core.docker.utils import get_grpc_launcher_args_for_gh_runs

if __name__ == "__main__":
    kwds = get_grpc_launcher_args_for_gh_runs()
    session = pyfluent.launch_fluent(**kwds)
    session.scheme_eval.scheme_eval('(%py-exec "import grpc")')
    print(session.scheme_eval.scheme_eval('(%py-eval "grpc.__version__")'))
