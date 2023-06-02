import os

import ansys.fluent.core as pyfluent


def run():
    if os.getenv("RUN_FROM_DOCKER") == "1":
        os.environ["PYFLUENT_LAUNCH_CONTAINER"] = "1"
        os.environ["FLUENT_IMAGE_TAG"] = "otel"
        os.environ[
            "ANSYSLMD_LICENSE_FILE"
        ] = "1055@host.docker.internal"  # license server from the host machine
        solver = pyfluent.launch_fluent(start_instance=False)
    else:
        solver = pyfluent.launch_fluent(show_gui=True, cleanup_on_exit=False)
    print(solver.preferences.Appearance.Ruler())
    solver.preferences.Appearance.Ruler = True
    print(solver.preferences.Appearance.Ruler())


if __name__ == "__main__":
    run()
