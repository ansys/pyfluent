import os

import ansys.fluent.core as pyfluent

_THIS_DIR = os.path.dirname(__file__)
_VERSION_FILE = os.path.join(
    _THIS_DIR, "..", "src", "ansys", "fluent", "core", "fluent_version.py"
)


def _print_fluent_version():
    session = pyfluent.launch_fluent()
    eval = session.scheme_eval.scheme_eval
    with open(_VERSION_FILE, "w+", encoding="utf8") as f:
        f.write(f'FLUENT_BUILD_TIME = "{eval("(inquire-build-time)")}"\n')
        f.write(f'FLUENT_BUILD_ID = "{eval("(inquire-build-id)")}"\n')
        f.write(f'FLUENT_REVISION = "{eval("(inquire-src-vcs-id)")}"\n')
        f.write(f'FLUENT_BRANCH = "{eval("(inquire-src-vcs-branch)")}"\n')
    session.exit()


if __name__ == "__main__":
    _print_fluent_version()
