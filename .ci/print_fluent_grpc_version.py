"""Get gRPC version from Fluent image and print it to the console."""

import ansys.fluent.core as pyfluent

if __name__ == "__main__":
    session = pyfluent.launch_fluent()
    session.scheme_eval.scheme_eval('(%py-exec "import grpc")')
    print(session.scheme_eval.scheme_eval('(%py-eval "grpc.__version__")'))
