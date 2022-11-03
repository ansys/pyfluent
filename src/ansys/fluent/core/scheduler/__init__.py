"""A package providing job scheduler support."""

import os
import socket
import sys

from ansys.fluent.core.scheduler.load_machines import load_machines  # noqa: F401
from ansys.fluent.core.scheduler.machine_list import MachineList

_ncoresOpt = "-t%n%"
_machinesOpt = " -cnf=%machineList%"
_procSep = ":"
_machineSep = ","


def build_parallel_options(machine_list: MachineList) -> str:
    """Constructs Fluent's parallel arguments given a list of machines.

    Parameters
    ----------
    machine_list : MachineList
        List of machines obtained by calling `load_machines`.

    Notes
    -----
    When running serial no options are passed back to the caller as Fluent can
    be started without additional arguments in that case.

    If the parallel options are being built on the same machine as Fluent is run
    on, and it's local parallel, then the -cnf argument is not constructed.  On
    Windows HPC the job scheduler returns hostnames as upper case but the socket
    module may return lower case.
    """
    parOpt = ""
    if sys.platform == "win32" and "CCP_NODES" in os.environ:
        localParallel = (
            socket.gethostname().upper() == machine_list[0].host_name.upper()
        )
    else:
        localParallel = socket.gethostname() == machine_list[0].host_name
    if machine_list.num_machines == 1 and localParallel:
        if machine_list.number_of_cores > 1:
            parOpt = _ncoresOpt.replace("%n%", str(machine_list.number_of_cores))
    else:
        parOpt = _ncoresOpt.replace("%n%", str(machine_list.number_of_cores))
        cnfList = (
            machine_list[0].host_name + _procSep + str(machine_list[0].number_of_cores)
        )
        for m in range(1, len(machine_list)):
            cnfList += (
                _machineSep
                + machine_list[m].host_name
                + _procSep
                + str(machine_list[m].number_of_cores)
            )
        parOpt += _machinesOpt.replace("%machineList%", cnfList)
    return parOpt
