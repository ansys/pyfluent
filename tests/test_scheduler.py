"""Provide a module to test the algorithms which parse job scheduler
environments for machines to run on."""
from builtins import range
import os
import socket
import tempfile
import unittest

from ansys.fluent.core.scheduler import build_parallel_options
from ansys.fluent.core.scheduler.load_machines import (
    _construct_machine_list_slurm,
    _parse_host_info,
    _parse_machine_data,
    _restrict_machines_to_core_count,
    load_machines,
)
from ansys.fluent.core.scheduler.machine_list import Machine, MachineList


class TestMachine(unittest.TestCase):
    """A basic test that checks Machine object behavior."""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_initialize_host(self):
        """Test that a Machine initializes as expected."""
        machine = Machine("machine", 20)
        self.assertEqual(machine.host_name, "machine")
        self.assertEqual(machine.number_of_cores, 20)
        self.assertEqual(machine.queue_name, None)
        self.assertEqual(machine.core_list, None)

    def test_modify_host(self):
        """Test that a Machine can be modified."""
        machine = Machine("machine", 20, "allq", "0:0")
        machine.number_of_cores = 12
        self.assertEqual(machine.number_of_cores, 12)
        machine.number_of_cores = machine.number_of_cores + 2
        machine.number_of_cores += 1
        self.assertEqual(machine.number_of_cores, 15)
        machine.number_of_cores -= 3
        self.assertEqual(machine.number_of_cores, 12)


class TestMachineList(unittest.TestCase):
    """Provide a test suite that checks that the MachineList object behaves
    properly."""

    def setUp(self):
        self._machineList = MachineList()

    def tearDown(self):
        self._machineList.reset()

    def test_initialize_machinelist(self):
        """Tests that a host file object initializes properly."""
        newMachineFile = MachineList()
        self.assertIsInstance(newMachineFile, MachineList)
        self.assertEqual(newMachineFile.machines, [])
        self.assertEqual(newMachineFile.num_machines, 0)

    def test_copy_machinelist(self):
        """Tests that the internal copy function works properly."""
        import copy

        newMachineList = copy.deepcopy(self._machineList)
        for m1, m2 in zip(self._machineList.machines, newMachineList.machines):
            self.assertEqual(m1.host_name, m2.host_name)
            self.assertEqual(m1.number_of_cores, m2.number_of_cores)

    def test_add_to_machinelist(self):
        """Tests that a machines can be added to a machine list."""
        self._machineList.add(Machine("machine1", 20, "allq", "0:0"))
        self._machineList.add(Machine("machine2", 20, "allq", "0:0"))
        self.assertEqual(self._machineList.num_machines, 2)

    def test_number_of_cores_and_machines(self):
        """Test that the total and max number of cores and machines is
        working."""
        self._machineList.add(Machine("machine1", 20, "allq", "0:0"))
        self._machineList.add(Machine("machine2", 25, "allq", "0:0"))
        self._machineList.add(Machine("machine3", 15, "allq", "0:0"))
        self.assertEqual(self._machineList.num_machines, 3)
        self.assertEqual(self._machineList.number_of_cores, 60)
        self.assertEqual(self._machineList.max_cores, 25)
        self.assertEqual(self._machineList.min_cores, 15)

    def test_sort_machine_list(self):
        """Test that the machines are sorted in order of decreasing core
        count."""
        self._machineList.add(Machine("machine1", 15, "allq", "0:0"))
        self._machineList.add(Machine("machine2", 10, "allq", "0:0"))
        self._machineList.add(Machine("machine3", 5, "allq", "0:0"))

        # Sort in ascending order
        self._machineList.sort_by_core_count_ascending()
        numCores = self._machineList.machines[0].number_of_cores
        for h in range(1, len(self._machineList.machines)):
            self.assertLessEqual(
                numCores, self._machineList.machines[h].number_of_cores
            )
            numCores = self._machineList.machines[h].number_of_cores

        # Sort in descending order
        self._machineList.sort_by_core_count()
        numCores = self._machineList.machines[0].number_of_cores
        for h in range(1, len(self._machineList.machines)):
            self.assertLessEqual(
                self._machineList.machines[h].number_of_cores, numCores
            )
            numCores = self._machineList.machines[h].number_of_cores

    def test_remote_empty_machines(self):
        self._machineList.add(Machine("machine1", 5))
        self._machineList.add(Machine("machine2", 0))
        self._machineList.remove_empty_machines()
        self.assertEqual(self._machineList.num_machines, 1)
        self.assertEqual(self._machineList.machines[0].host_name, "machine1")

    def test_move_local_host_to_front(self):
        import socket

        localHostName = socket.gethostname()

        self._machineList.add(Machine("M0", 2))
        self._machineList.add(Machine(localHostName, 1))
        self._machineList.add(Machine("M1", 3))
        self._machineList.move_local_host_to_front()
        self.assertEqual(self._machineList.machines[0].host_name, localHostName)
        self.assertEqual(self._machineList.machines[0].number_of_cores, 1)
        self.assertEqual(self._machineList.machines[1].host_name, "M0")
        self.assertEqual(self._machineList.machines[1].number_of_cores, 2)
        self.assertEqual(self._machineList.machines[2].host_name, "M1")
        self.assertEqual(self._machineList.machines[2].number_of_cores, 3)

    def test_deep_copy_machinelist(self):
        self._machineList.add(Machine("wathpc-2-0.local", 23))
        self._machineList.add(Machine("wathpc-2-1.local", 23))
        self._machineList.add(Machine("wathpc-2-2.local", 23))
        self._machineList.add(Machine("wathpc-2-3.local", 23))
        import copy

        machineListCopy = copy.deepcopy(self._machineList)
        for m1, m2 in zip(self._machineList.machines, machineListCopy.machines):
            self.assertEqual(m1.host_name, m2.host_name)
            self.assertEqual(m1.number_of_cores, m2.number_of_cores)


class TestLoadMachines(unittest.TestCase):
    """Provide a test suite that checks that loadMachines behaves properly."""

    def setUp(self):
        self._machineList = MachineList()

    def tearDown(self):
        self._machineList.reset()

    def test_machine_info(self):
        info = [
            {"machine-name": "M0", "core-count": 1},
            {"machine-name": "M1", "core-count": 6},
        ]
        machineList = load_machines(machine_info=info)
        self.assertEqual(machineList.number_of_cores, 7)

    def test_restrict_machines(self):
        info = [
            {"machine-name": "M0", "core-count": 1},
            {"machine-name": "M1", "core-count": 1},
        ]
        machineList = load_machines(machine_info=info)
        old_machine_list = _restrict_machines_to_core_count(
            machineList, ncores=machineList.number_of_cores
        )
        self.assertEqual(machineList, old_machine_list)

    def test_pe_hostfile(self):
        with tempfile.NamedTemporaryFile(delete=False) as fp:
            fp.write(b"m1\r\n\r\nm2 3 None None\r\nm3 4\r\nm4 2 queueName1")
            os.environ["PE_HOSTFILE"] = fp.name
        machineList = load_machines()
        os.unlink(fp.name)
        self.assertEqual(machineList.number_of_cores, 10)
        self.assertEqual(machineList.machines[1].host_name, "m2")
        self.assertEqual(machineList.machines[2].number_of_cores, 4)
        self.assertEqual(machineList.machines[3].queue_name, "queueName1")
        del os.environ["PE_HOSTFILE"]

    def test_lsb_mcpu(self):
        os.environ["LSB_MCPU_HOSTS"] = "m1 3 m2 3"
        machineList = load_machines()
        self.assertEqual(machineList.number_of_cores, 6)
        del os.environ["LSB_MCPU_HOSTS"]

    def test_pbs_nodefile(self):
        with tempfile.NamedTemporaryFile(delete=False) as fp:
            fp.write(b"m1\r\n\r\nm2\r\nm2\r\nm2")
            os.environ["PBS_NODEFILE"] = fp.name
        machineList = load_machines()
        os.unlink(fp.name)
        self.assertEqual(machineList[1].number_of_cores, 3)
        del os.environ["PBS_NODEFILE"]

    def test_no_environment(self):
        machineList = load_machines()
        self.assertEqual(machineList[0].host_name, socket.gethostname())
        self.assertEqual(machineList.number_of_cores, 1)

    def test_no_environment_cores(self):
        machineList = load_machines(ncores=4)
        self.assertEqual(machineList[0].host_name, socket.gethostname())
        self.assertEqual(machineList.number_of_cores, 4)

    def test_constrain_machines1(self):
        machineList = load_machines(host_info="M0:2,M1:3,M2:2", ncores=4)
        expectedValue = {"M0": 1, "M1": 2, "M2": 1}
        self.assertEqual(len(machineList.machines), 3)
        for machine in machineList.machines:
            self.assertEqual(machine.number_of_cores, expectedValue[machine.host_name])
        # Ensure that the order is preserved
        self.assertEqual(machineList.machines[0].host_name, "M0")
        fluentOpts = build_parallel_options(machineList)
        self.assertEqual(fluentOpts, "-t4 -cnf=M0:1,M1:2,M2:1")

    def test_constrain_machines2(self):
        with tempfile.NamedTemporaryFile(delete=False) as fp:
            fp.write(b"M0:2,M1:3,M2:2")
        machineList = load_machines(host_info=fp.name, ncores=3)
        expectedValue = {"M0": 1, "M1": 1, "M2": 1}
        os.unlink(fp.name)
        self.assertEqual(len(machineList.machines), 3)
        for machine in machineList.machines:
            self.assertEqual(machine.number_of_cores, expectedValue[machine.host_name])
        # Ensure that the order is preserved
        self.assertEqual(machineList.machines[0].host_name, "M0")
        fluentOpts = build_parallel_options(machineList)
        self.assertEqual(fluentOpts, "-t3 -cnf=M0:1,M1:1,M2:1")

    def test_overload_machines1(self):
        machineList = load_machines(host_info="M0:2,M1:1", ncores=10)
        expectedValue = {"M0": 2, "M1": 1}
        self.assertEqual(len(machineList.machines), 2)
        for machine in machineList.machines:
            self.assertEqual(machine.number_of_cores, expectedValue[machine.host_name])
        # Ensure that the order is preserved
        self.assertEqual(machineList.machines[0].host_name, "M0")
        fluentOpts = build_parallel_options(machineList)
        self.assertEqual(fluentOpts, "-t3 -cnf=M0:2,M1:1")

    def test_overload_machines2(self):
        machineList = load_machines(host_info="M0,M0,M1", ncores=10)
        expectedValue = {"M0": 2, "M1": 1}
        self.assertEqual(len(machineList.machines), 2)
        for machine in machineList.machines:
            self.assertEqual(machine.number_of_cores, expectedValue[machine.host_name])
        # Ensure that the order is preserved
        self.assertEqual(machineList.machines[0].host_name, "M0")
        fluentOpts = build_parallel_options(machineList)
        self.assertEqual(fluentOpts, "-t3 -cnf=M0:2,M1:1")

    def test_winhpc(self):
        os.environ["CCP_NODES"] = "3 M0 8 M1 8 M2 16"
        machineList = load_machines()
        self.assertEqual(machineList.num_machines, 3)
        self.assertEqual(machineList.number_of_cores, 32)
        self.assertEqual(machineList.machines[0].host_name, "M0")
        self.assertEqual(machineList.machines[1].host_name, "M1")
        self.assertEqual(machineList.machines[2].host_name, "M2")
        fluentOpts = build_parallel_options(machineList)
        self.assertEqual(fluentOpts, "-t32 -cnf=M0:8,M1:8,M2:16")
        del os.environ["CCP_NODES"]

    def test_slurm_single_num(self):
        os.environ["SLURM_JOB_NODELIST"] = "M[1-2],M[3]"
        os.environ["SLURM_TASKS_PER_NODE"] = "8,10(x2)"
        hostList = os.environ.get("SLURM_JOB_NODELIST")
        machineList = _construct_machine_list_slurm(hostList)
        self.assertEqual(machineList[1].number_of_cores, 10)
        self.assertEqual(machineList[2].number_of_cores, 10)
        self.assertEqual(machineList[2].host_name, "M3")
        del os.environ["SLURM_JOB_NODELIST"]
        del os.environ["SLURM_TASKS_PER_NODE"]

    def test_slurm_no_brackets(self):
        os.environ["SLURM_JOB_NODELIST"] = "M0,M1,M2"
        os.environ["SLURM_NTASKS_PER_NODE"] = "8"
        hostList = os.environ.get("SLURM_JOB_NODELIST")
        machineList = _construct_machine_list_slurm(hostList)
        self.assertEqual(machineList.num_machines, 3)
        self.assertEqual(machineList.number_of_cores, 24)
        self.assertEqual(machineList.machines[0].host_name, "M0")
        self.assertEqual(machineList.machines[1].host_name, "M1")
        self.assertEqual(machineList.machines[2].host_name, "M2")
        fluentOpts = build_parallel_options(machineList)
        self.assertEqual(fluentOpts, "-t24 -cnf=M0:8,M1:8,M2:8")
        del os.environ["SLURM_JOB_NODELIST"]
        del os.environ["SLURM_NTASKS_PER_NODE"]

    def test_slurm_no_padding(self):
        os.environ["SLURM_JOB_NODELIST"] = "M[0-2]"
        os.environ["SLURM_NTASKS_PER_NODE"] = "12"
        hostList = os.environ.get("SLURM_JOB_NODELIST")
        machineList = _construct_machine_list_slurm(hostList)
        self.assertEqual(machineList.num_machines, 3)
        self.assertEqual(machineList.number_of_cores, 36)
        self.assertEqual(machineList.machines[0].host_name, "M0")
        self.assertEqual(machineList.machines[1].host_name, "M1")
        self.assertEqual(machineList.machines[2].host_name, "M2")
        fluentOpts = build_parallel_options(machineList)
        self.assertEqual(fluentOpts, "-t36 -cnf=M0:12,M1:12,M2:12")
        del os.environ["SLURM_JOB_NODELIST"]
        del os.environ["SLURM_NTASKS_PER_NODE"]

    def test_slurm_hosts_with_dash(self):
        os.environ["SLURM_JOB_NODELIST"] = "M-n50-[0-1],M-p50-[9-11]"
        os.environ["SLURM_NTASKS_PER_NODE"] = "12"
        hostList = os.environ.get("SLURM_JOB_NODELIST")
        machineList = _construct_machine_list_slurm(hostList)
        self.assertEqual(machineList.num_machines, 5)
        self.assertEqual(machineList.number_of_cores, 60)
        self.assertEqual(machineList.machines[0].host_name, "M-n50-0")
        self.assertEqual(machineList.machines[1].host_name, "M-n50-1")
        self.assertEqual(machineList.machines[2].host_name, "M-p50-9")
        self.assertEqual(machineList.machines[3].host_name, "M-p50-10")
        self.assertEqual(machineList.machines[4].host_name, "M-p50-11")
        del os.environ["SLURM_JOB_NODELIST"]
        del os.environ["SLURM_NTASKS_PER_NODE"]

    def test_slurm_with_padding(self):
        os.environ["SLURM_JOB_NODELIST"] = "MC[008-009,010,011,012-014]"
        os.environ["SLURM_TASKS_PER_NODE"] = "8,10(x2),12(x3),10"
        hostList = os.environ.get("SLURM_JOB_NODELIST")
        machineList = _construct_machine_list_slurm(hostList)
        self.assertEqual(machineList.num_machines, 7)
        self.assertEqual(machineList.number_of_cores, 74)
        self.assertEqual(machineList.machines[0].host_name, "MC008")
        self.assertEqual(machineList.machines[0].number_of_cores, 8)
        self.assertEqual(machineList.machines[1].host_name, "MC009")
        self.assertEqual(machineList.machines[1].number_of_cores, 10)
        self.assertEqual(machineList.machines[2].host_name, "MC010")
        self.assertEqual(machineList.machines[2].number_of_cores, 10)
        self.assertEqual(machineList.machines[3].host_name, "MC011")
        self.assertEqual(machineList.machines[3].number_of_cores, 12)
        self.assertEqual(machineList.machines[4].host_name, "MC012")
        self.assertEqual(machineList.machines[4].number_of_cores, 12)
        self.assertEqual(machineList.machines[5].host_name, "MC013")
        self.assertEqual(machineList.machines[5].number_of_cores, 12)
        self.assertEqual(machineList.machines[6].host_name, "MC014")
        self.assertEqual(machineList.machines[6].number_of_cores, 10)
        del os.environ["SLURM_JOB_NODELIST"]
        del os.environ["SLURM_TASKS_PER_NODE"]

    def test_slurm_with_padding_one_hostlist(self):
        os.environ["SLURM_JOB_NODELIST"] = "MD[099-101]"
        os.environ["SLURM_NTASKS_PER_NODE"] = "12"
        hostList = os.environ.get("SLURM_JOB_NODELIST")
        machineList = _construct_machine_list_slurm(hostList)
        self.assertEqual(machineList.num_machines, 3)
        self.assertEqual(machineList.number_of_cores, 36)
        self.assertEqual(machineList.machines[0].host_name, "MD099")
        self.assertEqual(machineList.machines[1].host_name, "MD100")
        self.assertEqual(machineList.machines[2].host_name, "MD101")
        del os.environ["SLURM_JOB_NODELIST"]
        del os.environ["SLURM_NTASKS_PER_NODE"]

    def test_slurm_no_padding_commas(self):
        os.environ["SLURM_JOB_NODELIST"] = "M[2-3,4,5-7,8-11,12-14,15-16]"
        os.environ["SLURM_NTASKS_PER_NODE"] = "12"
        hostList = os.environ.get("SLURM_JOB_NODELIST")
        machineList = _construct_machine_list_slurm(hostList)
        self.assertEqual(machineList.num_machines, 15)
        self.assertEqual(machineList.number_of_cores, 180)
        self.assertEqual(machineList.machines[0].host_name, "M2")
        self.assertEqual(machineList.machines[1].host_name, "M3")
        self.assertEqual(machineList.machines[2].host_name, "M4")
        self.assertEqual(machineList.machines[3].host_name, "M5")
        self.assertEqual(machineList.machines[4].host_name, "M6")
        self.assertEqual(machineList.machines[5].host_name, "M7")
        self.assertEqual(machineList.machines[6].host_name, "M8")
        self.assertEqual(machineList.machines[7].host_name, "M9")
        self.assertEqual(machineList.machines[8].host_name, "M10")
        self.assertEqual(machineList.machines[9].host_name, "M11")
        self.assertEqual(machineList.machines[10].host_name, "M12")
        self.assertEqual(machineList.machines[11].host_name, "M13")
        self.assertEqual(machineList.machines[12].host_name, "M14")
        self.assertEqual(machineList.machines[13].host_name, "M15")
        self.assertEqual(machineList.machines[14].host_name, "M16")
        del os.environ["SLURM_JOB_NODELIST"]
        del os.environ["SLURM_NTASKS_PER_NODE"]

    def test_slurm_very_complex(self):
        os.environ[
            "SLURM_JOB_NODELIST"
        ] = "M[2-3,4,5-7,8-11,12-14,15-16],MB,MC[008-009,010-011,012-014],MD[099-101]"
        os.environ["SLURM_NTASKS_PER_NODE"] = "24"
        hostList = os.environ.get("SLURM_JOB_NODELIST")
        machineList = _construct_machine_list_slurm(hostList)
        self.assertEqual(machineList.num_machines, 26)
        self.assertEqual(machineList.number_of_cores, 624)
        self.assertEqual(machineList.machines[0].host_name, "M2")
        self.assertEqual(machineList.machines[0].number_of_cores, 24)
        self.assertEqual(machineList.machines[7].host_name, "M9")
        self.assertEqual(machineList.machines[14].host_name, "M16")
        self.assertEqual(machineList.machines[15].host_name, "MB")
        self.assertEqual(machineList.machines[16].host_name, "MC008")
        self.assertEqual(machineList.machines[19].host_name, "MC011")
        self.assertEqual(machineList.machines[22].host_name, "MC014")
        self.assertEqual(machineList.machines[24].host_name, "MD100")
        del os.environ["SLURM_JOB_NODELIST"]
        del os.environ["SLURM_NTASKS_PER_NODE"]


class TestMachineListCmdLine(unittest.TestCase):
    """Provide a test suite that checks the machine list parser."""

    def setUp(self):
        self._expectedValues = {"M0": 2, "M1": 4}

    def tearDown(self):
        pass

    def test_parse_machine_data(self):
        machineDataList = [["M0:2", "M1:2", "M1:2"], ["M0", "M0", "M1", "M1:3"]]

        for machineData in machineDataList:
            machineList = _parse_machine_data(machineData)
            for machine in machineList.machines:
                self.assertEqual(
                    machine.number_of_cores, self._expectedValues[machine.host_name]
                )

    def test_cmd_string(self):
        hostLists = ["M0:2,M1:2,M1:2", "M0,M0,M1,M1:3"]

        for hostList in hostLists:
            machineList = _parse_host_info(hostList)
            for machine in machineList.machines:
                self.assertEqual(
                    machine.number_of_cores, self._expectedValues[machine.host_name]
                )

    def test_no_machine_name(self):
        hostList = "M0:2,M1:2,"
        with self.assertRaises(RuntimeError) as cm:
            _parse_host_info(hostList)
        self.assertEqual(str(cm.exception), "Problem with machine list format.")

    def test_host_file(self):
        import os.path

        hostfile = "hosts.txt"
        # This unit test only runs if the file exists
        if os.path.isfile(hostfile):
            machineList = _parse_host_info(hostfile)
            for machine in machineList.machines:
                self.assertEqual(
                    machine.number_of_cores, self._expectedValues[machine.host_name]
                )


suite1 = unittest.TestLoader().loadTestsFromTestCase(TestMachine)
suite2 = unittest.TestLoader().loadTestsFromTestCase(TestMachineList)
suite3 = unittest.TestLoader().loadTestsFromTestCase(TestLoadMachines)
suite4 = unittest.TestLoader().loadTestsFromTestCase(TestMachineListCmdLine)
alltests = unittest.TestSuite([suite1, suite2, suite3, suite4])
unittest.TextTestRunner(verbosity=2).run(alltests)

if __name__ == "__main__":
    unittest.main()
