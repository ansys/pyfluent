"""A package providing job scheduler support."""

from ansys.fluent.core.scheduler.load_machines import load_machines  # noqa: F401
from ansys.fluent.core.scheduler.machine_list import MachineList

_fluentOpt = "-t%n% -cnf=%machineList%"
_procSep = ":"
_machineSep = ","


def build_parallel_options(machine_list: MachineList) -> str:
    """Constructs Fluent's parallel arguments given a list of machines.

    Parameters
    ----------
    machine_list : MachineList
        List of machines obtained by calling `load_machines`.
    """
    parOpt = _fluentOpt.replace("%n%", str(machine_list.number_of_cores))
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
    parOpt = parOpt.replace("%machineList%", cnfList)
    return parOpt
