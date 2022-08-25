"""A module that provides machine list construction for distributed parallel
environments, including queueing systems.

Currently supports UGE, LSF, PBS and SLURM by parsing the contents of
the PE_HOSTFILE, LSB_MCPU_HOSTS, PBS_NODEFILE and SLURM_JOB_NODELIST
variables, respectively.
"""
import csv
import os
import subprocess

from ansys.fluent.core.launcher.machine_list import Machine, MachineList


def load_machines(machineDict=None, hostInfo=None, ncores=None):
    """Provide a function to construct a machine list from allocated machines.

    Parameters
    ----------
    machineDict : dict[str, int]
        Optional list of machines provided by the caller.
        This is a list of dictionaries of the form:
            [{'machine-name' : <m-name-1>, 'core-count' : <int>},
             {'machine-name' : <m-name-2>, 'core-count' : <int>},
             ... ]
    hostInfo : str
        Optional host file name or list of machines and cores as a string
        separated by commas and colons.
        Example 1:  'M0:3,M1:2'
        Example 2:  'M0,M0,M0,M1,M1'
    ncores : int
        Optional total core count.
        If provided without machineDict, sets the core count for local parallel.
        If both machineDict and ncores are provided, then the machine list
        determined by machineDict will be limited by the ncores value.

    Returns
    -------
    MachineList
        A list of machines.

    Notes
    -----
    On UGE the PE_HOSTFILE variable is used to find machines, LSB_MCPU_HOSTS
    list for LSF, PBS_NODEFILE for PBS and SLURM_JOB_NODELIST on SLURM.
    Unsupported job schedulers may provide alternative ways of providing a list
    of machines, in that case the list must be pre-parsed and provided via the
    machineDict parameter.

    Depending on the SLURM environment, the hostnames contained within the
    SLURM_JOB_NODELIST variable may not be valid to ssh to. In that case we
    cannot pass these names to the solver. So, test if we can ssh to the first
    host, if not, get 'actual' machine names using scontrol.
    """

    machineList = []

    if machineDict:
        machineList = _construct_machine_list_manual(machineDict)
    elif hostInfo:
        machineList = _parse_host_info(hostInfo)
    elif "PE_HOSTFILE" in os.environ:
        hostFileName = os.environ.get("PE_HOSTFILE")
        machineList = _construct_machine_list_uge(hostFileName)
    elif "LSB_MCPU_HOSTS" in os.environ:
        hostList = os.environ.get("LSB_MCPU_HOSTS")
        machineList = _construct_machine_list_lsf(hostList)
    elif "PBS_NODEFILE" in os.environ:
        hostFileName = os.environ.get("PBS_NODEFILE")
        machineList = _construct_machine_list_pbs(hostFileName)
    elif "SLURM_JOB_NODELIST" in os.environ:
        hostList = os.environ.get("SLURM_JOB_NODELIST")
        machineList = _construct_machine_list_slurm(hostList)
        sshTest = (
            "ssh "
            + str(machineList.machines[0].hostName)
            + " /bin/true > /dev/null 2>&1; echo $?"
        )
        p = subprocess.Popen(sshTest, shell=True, stdout=subprocess.PIPE)
        procOutput = p.communicate()
        if procOutput[0] != b"0\n":
            runCommand = (
                r"scontrol show node ${SLURM_JOB_NODELIST} | "
                r"awk '/NodeAddr=/ {print $1}' | cut -f2 -d="
            )
            p = subprocess.Popen(runCommand, shell=True, stdout=subprocess.PIPE)
            procOutput = p.communicate()
            hostList = procOutput[0].decode("utf-8").replace("\n", ",")
            length = len(hostList)
            hostList = hostList[0 : length - 1]
            machineList = _construct_machine_list_slurm(hostList)
    elif "CCP_NODES" in os.environ:
        hostList = os.environ.get("CCP_NODES")
        machineList = _construct_machine_list_ccs(hostList)
    elif ncores:
        machineList = _get_local_machine(ncores)

    if machineList and ncores:
        # If both machine list and number of cores are provided, edit the
        # machine list to use exactly the number of cores indicated.
        machineList = _restrict_machines_to_core_count(machineList, ncores)

    return machineList


def _parse_host_info(hostInfo):
    """Parse the host machine information from command-line arguments.

    Returns
    -------
    list[dict] :
        A list of dictionaries formatted as:
        {'machine-name' : ###, 'core-count' : ###}
    """

    if (
        (":" in hostInfo or "," in hostInfo)
        and not "\\" in hostInfo
        and not "/" in hostInfo
    ):
        # Filenames generally shouldn't have ':',
        # so assume it's a string list and parse accordingly
        sMod = 1 if hostInfo[0] == "[" else 0
        sBeg = sMod
        sEnd = len(hostInfo) - sMod
        machineData = hostInfo[sBeg:sEnd].split(",")
    else:
        # Read from the file
        with open(hostInfo, "r") as f:
            machineData = f.read().splitlines()

    return _parse_machine_data(machineData)


def _parse_machine_data(machineData):
    """Parse the host machine data provided as a list of strings.

    Parameters
    ----------
    machineData : list[str]
        The data can be a list of machines such as:
            ["M0","M1","M1"]
        or it can include cores as well:
            ["M0:1","M1:2"]
        or a combination thereof.

    Returns
    -------
    list[dict] :
        The return value is a list of dictionaries formatted as:
        {'machine-name' : ###, 'core-count' : ###}
    """

    machineList = MachineList()

    for datum in machineData:
        # Parse machine name and core count
        if ":" in datum:
            # Machine and core given
            datumPair = datum.split(":")
            machineName = datumPair[0].strip()
            ncores = int(datumPair[1])
        else:
            # Just machine name - assume one core
            machineName = datum.strip()
            ncores = 1

        if machineName == "":
            raise RuntimeError("Problem with machine list format.")

        # Add to existing machine if already in the list
        for machine in machineList.machines:
            if machine.hostName == machineName:
                machine.numberOfCores += ncores
                break
        else:  # machine name not already in machineList
            machineList.add(Machine(machineName, ncores))

    return machineList


def _get_local_machine(ncores):
    """Provide private module function to convert a core count into a machine
    list for a local job."""

    import socket

    hostName = socket.gethostname()
    machineList = MachineList()
    machineList.add(Machine(hostName, ncores))

    return machineList


def _restrict_machines_to_core_count(oldMachineList, ncores):
    """Provide private module function to adjust the number of cores used per
    machine based on a user-supplied core count.

    Parameters
    ----------
    oldMachineList : MachineList
        List of machines to be modified.
    ncores : int
        Updated core count.

    Returns
    -------
    MachineList
       New MachineList constrained to number of requested cores.

    Notes
    -----
    Every machine contributes cores to the new list until ncores is reached.
    However, the original machine order is preserved.  This ensures that all
    machines are maximally utilized.  The old machine list is sorted by core
    count so that uneven distributions favor machines with more cores. If a
    total of x cores are available on the machines and x <= ncores, then the
    returned machine list will be identical to the input.
    """

    if ncores >= oldMachineList.numberOfCores:
        return oldMachineList

    # Get indices ordering the machines from largest to smallest core count
    machineListOrder = [
        i[0]
        for i in sorted(
            enumerate(oldMachineList.machines),
            key=lambda x: x[1].numberOfCores,
            reverse=True,
        )
    ]

    newMachineList = MachineList()
    for m in oldMachineList.machines:
        newMachineList.add(Machine(m.hostName, 0, m.queueName, m.coreList))

    ncoresRemain = ncores
    while ncoresRemain != 0:
        for i in machineListOrder:
            oldMachine = oldMachineList.machines[i]
            if oldMachine.numberOfCores != 0 and ncoresRemain != 0:
                newMachineList.machines[i].numberOfCores += 1
                oldMachine.numberOfCores -= 1
                ncoresRemain -= 1
                if ncoresRemain == 0:
                    break

    return newMachineList


def _construct_machine_list_uge(hostFileName):
    """Provide private module function to parse the UGE host file."""
    csv.register_dialect("pemachines", delimiter=" ", skipinitialspace=True)
    machineList = MachineList()
    with open(hostFileName, "r") as peFile:
        peReader = csv.reader(peFile, dialect="pemachines")
        for row in peReader:
            if len(row) == 0:
                break
            m = Machine(row[0], int(row[1]), row[2], None if len(row) == 4 else row[3])
            machineList.add(m)
    return machineList


def _construct_machine_list_lsf(hostList):
    """Provide private module function to parse the LSF host list."""
    machineList = MachineList()
    splitHostList = hostList.split()
    im = 0
    while im < len(splitHostList):
        machineList.add(Machine(splitHostList[im], int(splitHostList[im + 1])))
        im += 2
    return machineList


def _construct_machine_list_pbs(hostFileName):
    """Provide private module function to parse the PBS host file."""
    # PBS_NODE file has one machine name per line per core allocated on the machine.
    # It's identical to a Fluent host file format.  This code accumulates the total
    # core count on each machine.
    machineDict = {}
    with open(hostFileName, "r") as pbsFile:
        for hostname in pbsFile:
            hostname = hostname.rstrip("\r\n")
            if hostname in machineDict:
                machineDict[hostname].numberOfCores += 1
            else:
                machineDict[hostname] = Machine(hostname, 1)

    # Convert accumulated dictionary to a MachineList
    machineList = MachineList()
    for m in list(machineDict.values()):
        machineList.add(m)
    return machineList


def _construct_machine_list_slurm(hostList):
    """Provide a private module function to parse the SLURM host and task
    lists.

    The SLURM system provides a comma separated list of host names.  The host
    names may be listed individually or consecutive host names may have IDs that
    are provided by a set within brackets:

    SLURM_JOB_NODELIST = machinea[2-5,7,14-15],machineb,machinec[008-010,012,017-019],machined[099-101] ...

    Consecutive IDs may be prefixed (or pre-padded) with zeros so that the
    string representation of each machine ID always has the same length as the
    number of digits required to represent the last machine ID in the bracketed
    range.

    The cores allocated to each machine come in a separate variable

    SLURM_TASKS_PER_NODE = '10,3,12(x2),4,15(x5)'

    An (x#) after the core count indicates that the core count is repeated #
    times.  The order is the same as SLURM_JOB_NODELIST.
    """  # noqa
    import re

    machineList = MachineList()
    splitHostList = hostList.split(",")
    coresPerMachine = 1
    ntasksPerNodeSet = False
    if "SLURM_NTASKS_PER_NODE" in os.environ:
        coresPerMachine = int(os.environ.get("SLURM_NTASKS_PER_NODE"))
        ntasksPerNodeSet = True

    # Regular expression to identify if a host entry contains a single range of machines
    pRange = re.compile(r"\[.*\]")
    # Regular expressions to identify a single machine ID within brackets
    pIDOne = re.compile(r"^.*\[(\d*)$")
    pIDOneNext = re.compile(r"^(\d*)")
    # Regular expressions to identify a range of machine IDs within brackets
    pIDRangeFirst = re.compile(r"^.*\[(\d*)-(\d*).*$")
    pIDRangeNext = re.compile(r"^(\d*)-(\d*)")
    # Regular expressions to identify if the IDs in a range use zero padding
    pIdsPadded = re.compile(r"^.*\[(0\d*)-\d*.*$")
    pIdsPaddedNext = re.compile(r"(0\d*)-\d*")
    # Regular expression to identify the machine name prefix for a range
    pMachinePrefix = re.compile(r"(^.*)\[")

    entry = 0
    while entry < len(splitHostList):
        hosts = splitHostList[entry]
        prefixMatch = pMachinePrefix.match(hosts)
        # Machine has no brackets, just add to the list
        if not prefixMatch:
            machineList.add(Machine(hosts, coresPerMachine))
            entry += 1
        # Add all machines in the bracketed range if one is provided
        else:
            machinePrefix = prefixMatch.group(1)
            # Check if first bracket entry is "M[a-b" or "M[a".  Check for a range first.
            machineIDs = pIDRangeFirst.match(hosts)
            if machineIDs:
                idfirst = int(machineIDs.group(1))
                idlast = int(machineIDs.group(2))
                paddedIDs = pIdsPadded.match(hosts)
                for id in range(idfirst, idlast + 1):
                    if paddedIDs:
                        machineName = machinePrefix + str(id).rjust(
                            len(paddedIDs.group(1)), "0"
                        )
                    else:
                        machineName = machinePrefix + str(id)
                    machineList.add(Machine(machineName, coresPerMachine))
            else:
                machineIDs = pIDOne.match(hosts)
                id = int(machineIDs.group(1))
                numch = len(re.compile(r"^.*\[(\d*)$").match(hosts).group(1))
                machineName = machinePrefix + str(id).rjust(numch, "0")
                machineList.add(Machine(machineName, coresPerMachine))

            entry += 1
            # If a host has more than one numbered range, process them.
            if len(pRange.findall(hosts)) == 0:
                if entry < len(splitHostList):
                    hosts = splitHostList[entry]
                    # Check if next entry is "a-b" or "a".  Check for a range first.
                    machineIDs = pIDRangeNext.match(hosts)
                    if machineIDs:
                        singleID = False
                    else:
                        singleID = True
                        machineIDs = pIDOneNext.match(hosts)
                    while machineIDs:
                        if singleID:
                            id = int(machineIDs.group(0))
                            numch = len(re.compile(r"^(\d*)").match(hosts).group(0))
                            machineName = machinePrefix + str(id).rjust(numch, "0")
                            machineList.add(Machine(machineName, coresPerMachine))
                        else:
                            idfirst = int(machineIDs.group(1))
                            idlast = int(machineIDs.group(2))
                            paddedIDs = pIdsPaddedNext.match(hosts)
                            for id in range(idfirst, idlast + 1):
                                if paddedIDs:
                                    machineName = machinePrefix + str(id).rjust(
                                        len(paddedIDs.group(1)), "0"
                                    )
                                else:
                                    machineName = machinePrefix + str(id)
                                machineList.add(Machine(machineName, coresPerMachine))

                        entry += 1
                        if entry < len(splitHostList):
                            hosts = splitHostList[entry]
                            machineIDs = pIDRangeNext.match(hosts)
                            if machineIDs:
                                singleID = False
                            else:
                                machineIDs = pIDOneNext.match(hosts)
                                if machineIDs and len(machineIDs.group(0)) > 0:
                                    singleID = True
                                else:
                                    singleID = False
                                    machineIDs = None
                        else:
                            machineIDs = None

    if not ntasksPerNodeSet and "SLURM_TASKS_PER_NODE" in os.environ:
        splitCoreList = os.environ["SLURM_TASKS_PER_NODE"].split(",")
        coresPerMachine = []
        for numcores in splitCoreList:
            beg = numcores.find("(x")
            if beg > 0:
                end = numcores.find(")")
                for _ in range(int(numcores[beg + 2 : end])):
                    coresPerMachine.append(int(numcores[0:beg]))
            else:
                coresPerMachine.append(int(numcores))
        icores = 0
        for machine in machineList.machines:
            machine.numberOfCores = coresPerMachine[icores]
            icores += 1

    return machineList


def _construct_machine_list_ccs(hostList):
    """Provide private module function to parse the Windows HPC/CCS host list.

    Parameters
    ----------
    hostList : str
        A single string with the following format:

        "#hosts host1 #cores1 host2 #cores2 host3 #cores3 ... hostN #coresN"
    """
    machineList = MachineList()
    splitHostList = hostList.split()
    numMachines = int(splitHostList[0])
    im = 1
    for _ in range(numMachines):
        machineList.add(Machine(splitHostList[im], int(splitHostList[im + 1])))
        im += 2
    return machineList


def _construct_machine_list_manual(machineDict):
    """Provide a private module function to convert a machine list dictionary
    into a list of machine objects."""
    machineList = MachineList()
    for m in machineDict:
        machineList.add(Machine(m["machine-name"], m["core-count"]))
    return machineList
