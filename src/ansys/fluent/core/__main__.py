"""Module containing entry-point code for PyFluent."""

if __name__ == "__main__":
    # put these items automatically into scope
    import ansys.fluent.core as pyfluent  # noqa: F401
    from ansys.fluent.core import launch_fluent  # noqa: F401
    from ansys.fluent.core.start import start

    solver = start()
    import code

    code.interact(local=locals())
