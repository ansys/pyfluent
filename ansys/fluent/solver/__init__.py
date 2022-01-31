# This is an auto-generated file.  DO NOT EDIT!

from ansys.fluent.session import Session
from ansys.fluent.launcher.launcher import launch_fluent

from ansys.fluent.solver import tui
from ansys.fluent.solver.tui import (
    adjoint,
    display,
    define,
    file,
    icing,
    mesh,
    parameters__and__customization,
    parallel,
    plot,
    preferences,
    report,
    results,
    solution,
    solve,
    setup,
    surface,
    simulation_reports,
    server,
    turbo_post,
    views,
    parametric_study,
    turbo_workflow,
)

from ansys.fluent.solver.logging import (
    set_log_level,
    enable_logging_to_stdout,
    disable_logging_to_stdout,
    enable_logging_to_file,
    disable_logging_to_file,
)


Session.Tui.register_module(tui)

