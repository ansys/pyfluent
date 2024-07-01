"""Module containing entry-point code for PyFluent."""

import sys

if __name__ == "__main__":
    # put these items automatically into scope for a user-friendly session
    import ansys.fluent.core as pyfluent  # noqa: F401
    from ansys.fluent.core import launch_fluent  # noqa: F401
    from ansys.fluent.core.start import start

    # launch or connect
    # - or just start with PyFluent modules in scope (above imports)
    session = start(sys.argv[1] if len(sys.argv) > 1 else None)

    # copying locals dict so that locs and code don't pollute the dict
    locs = locals().copy()
    import code

    code.interact(local=locs)
