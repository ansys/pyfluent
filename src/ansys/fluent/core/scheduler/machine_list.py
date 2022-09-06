"""A module used to provide abstract machine objects for queue system
interfaces.

This module provides two objects that help with interfacing python scripts with
the job scheduler environments:

  Machine
    This is used to represent a single machine allocated by the queue system
    and query details about it.

  MachineList
    This is used to load and query a queue system machine file.  Instances
    of this object hold a collection of Machine objects that are initialized
    when the machine file is loaded.
"""

from builtins import object
import copy


class Machine(object):
    """Provides an interface for a single machine allocated by a queue
    system."""

    def __init__(self, hostName, numberOfCores, queueName=None, coreList=None):
        """Constructs a machine from the information provided.

        Parameters
        ----------
        hostName : str
            Host name of the machine
        numberOfCores : int
            The number of cores allocated on the machine
        queueName : str
            Optionally specifies the queue the machine is executing in.
        coreList : list[int]
            Optionally provides the list of allocated core IDs.
        """
        self._hostName = hostName
        self._numberOfCores = numberOfCores
        self._queueName = queueName
        self._coreList = coreList

    def __repr__(self):
        """Returns a string representation for the machine."""
        return (
            "Hostname:"
            + self._hostName
            + ", Cores: "
            + str(self._numberOfCores)
            + ", Queue: "
            + self._queueName
        )

    @property
    def host_name(self):
        """Returns the hostname listed in the machine file."""
        return self._hostName

    @property
    def number_of_cores(self):
        """Returns the number of cores allocated on the machine."""
        return self._numberOfCores

    @number_of_cores.setter
    def number_of_cores(self, value):
        self._numberOfCores = value

    @property
    def queue_name(self):
        """Returns the name of the queue the machine is allocated in."""
        return self._queueName

    @property
    def core_list(self):
        """Returns a list of core IDs allocated on the machine."""
        return self._coreList


class MachineList(object):
    """Provides an interface to list of machines allocated by a queue
    system."""

    def __init__(self, machinesIn=[]):
        """Constructs and initializes an empty machine file object."""
        self._machines = []
        for machine in machinesIn:
            self._machines.append(machine)

    def __len__(self):
        return self.num_machines

    def __iter__(self):
        return self._machines.__iter__()

    def __getitem__(self, index):
        return self._machines[index]

    def __deepcopy__(self, memo):
        machineList = []
        for m in self.machines:
            machineList.append(m)
        return MachineList(copy.deepcopy(machineList, memo))

    def reset(self):
        """Resets the machine file data to the initial values."""
        self._machines = []

    def add(self, m):
        self._machines.append(m)

    def remove(self, m):
        self._machines.remove(m)

    def sort_by_core_count(self):
        """Sorts the machines by core count, reordering the existing data."""
        self._machines.sort(key=lambda machine: machine.number_of_cores, reverse=True)

    def sort_by_core_count_ascending(self):
        """Sorts the machines by core count, reordering the existing data."""
        self._machines.sort(key=lambda machine: machine.number_of_cores)

    def remove_empty_machines(self):
        """Removes all machines with 0 cores."""
        self._machines = [m for m in self._machines if m.number_of_cores > 0]

    def move_local_host_to_front(self):
        """Moves the local host machine to the front of the machine list,
        creating it if it does not exist."""
        import socket

        localHostName = socket.gethostname()
        localHostNameComponents = localHostName.split(".")
        localHostIndex = -1
        for im, m in enumerate(self._machines):
            # Check if hostName == localHostName, comparing as much of the name as possible
            hostNameComponents = m.host_name.split(".")
            imin = min(len(localHostNameComponents), len(hostNameComponents))
            if hostNameComponents[:imin] == localHostNameComponents[:imin]:
                localHostIndex = im
        # If the local host is in the list move it to the beginning
        if localHostIndex > -1:
            localMachine = self._machines.pop(localHostIndex)
            # Place the object in the front of the list
            self._machines.insert(0, localMachine)

    @property
    def machines(self):
        """Returns the entire list of machines."""
        return self._machines

    @property
    def num_machines(self):
        """Returns the total number of machines."""
        return len(self._machines)

    @property
    def number_of_cores(self):
        """Returns the total number of cores."""
        return sum([m.number_of_cores for m in self._machines])

    @property
    def max_cores(self):
        """Returns the maximum number of cores."""
        return max([m.number_of_cores for m in self._machines])

    @property
    def min_cores(self):
        """Returns the minimum number of cores."""
        return min([m.number_of_cores for m in self._machines])
