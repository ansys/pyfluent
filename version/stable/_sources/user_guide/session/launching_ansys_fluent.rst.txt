.. _ref_launch_guide:

Launching and connecting to Fluent
==================================

This document provides a comprehensive guide for launching and connecting to Ansys Fluent sessions using PyFluent, the Python interface for Fluent. 
It covers multiple methods to start Fluent, including launching from a local installation, containerized environments (Docker or Podman), and connecting 
to existing Fluent sessions. Detailed examples illustrate how to initialize Fluent in various modes such as meshing, solution, and pre/post processing.

Additionally, the guide explains advanced launching options such as setting precision, dimensions, and parallel execution configurations. 
It also covers integration with job schedulers like Slurm, enabling efficient high-performance computing workflows. 
Furthermore, instructions for launching Fluent within PIM environments and detailed procedures for cross-platform remote connections and file transfers between Windows, Linux, and WSL hosts are provided.

This reference aims to equip users with the knowledge and tools required to flexibly and efficiently manage Fluent sessions in diverse computing environments.

Launch from local installation
------------------------------

.. vale Google.Spacing = NO

The :meth:`from_install() <ansys.fluent.core.session_utilities.SessionBase.from_install>` method launches Fluent using a locally installed version of Ansys Fluent.

Use this method when:

- You have Fluent installed on your local machine.
- You want to run Fluent from Python without needing tools like Docker or Podman.

**Example:**

.. code-block:: python

  import ansys.fluent.core as pyfluent
  meshing = pyfluent.Meshing.from_install()
  pure_meshing = pyfluent.PureMeshing.from_install()
  solver = pyfluent.Solver.from_install()
  solver_aero = pyfluent.SolverAero.from_install()
  solver_icing = pyfluent.SolverIcing.from_install()
  pre_post = pyfluent.PrePost.from_install()   


Launch in a container
---------------------

The :meth:`from_container() <ansys.fluent.core.session_utilities.SessionBase.from_container>` method launches Fluent inside a Docker container.

Use this method when:

- You are working in a containerized setup.
- You need to configure port mappings.
- You're running isolated or parallel sessions.

**Example:**

.. code-block:: python

  import os
  os.environ["PYFLUENT_LAUNCH_CONTAINER"] = "1"
  os.environ["PYFLUENT_USE_DOCKER_COMPOSE"] = "1"  # or os.environ["PYFLUENT_USE_PODMAN_COMPOSE"] = "1"

  import ansys.fluent.core as pyfluent
  from ansys.fluent.core.utils.networking import get_free_port

  port_1 = get_free_port()
  port_2 = get_free_port()
  container_dict = {"ports": {f"{port_1}": port_1, f"{port_2}": port_2}}

  meshing = pyfluent.Meshing.from_container(container_dict=container_dict, product_version=pyfluent.FluentVersion.v252)
  pure_meshing = pyfluent.PureMeshing.from_container(container_dict=container_dict, product_version=pyfluent.FluentVersion.v252)
  solver = pyfluent.Solver.from_container(container_dict=container_dict, product_version=pyfluent.FluentVersion.v252)
  solver_aero = pyfluent.SolverAero.from_container(container_dict=container_dict, product_version=pyfluent.FluentVersion.v252)
  solver_icing = pyfluent.SolverIcing.from_container(container_dict=container_dict, product_version=pyfluent.FluentVersion.v252)
  pre_post = pyfluent.PrePost.from_container(container_dict=container_dict, product_version=pyfluent.FluentVersion.v252)


Connect to an existing session
------------------------------

The :meth:`from_connection() <ansys.fluent.core.session_utilities.SessionBase.from_connection>` method connects to a previously launched Fluent session.

Use this method when:

- Fluent was launched externally or earlier.
- You need to connect from a different process or system.

**Example:**

.. code-block:: python

   import ansys.fluent.core as pyfluent

   # Launch to retrieve credentials
   solver = pyfluent.Solver.from_local_install()
   print(solver.health_check.check_health())

   ip = solver.connection_properties.ip
   password = solver.connection_properties.password
   port = solver.connection_properties.port

   # Connect to the session
   solver_connected = pyfluent.Solver.from_connection(ip=ip, password=password, port=port)
   print(solver_connected.health_check.check_health())

   solver.exit()
   solver_connected.exit()


Launch in `PIM <https://pypim.docs.pyansys.com/version/stable/>`_ mode
----------------------------------------------------------------------

The :meth:`from_pim() <ansys.fluent.core.session_utilities.SessionBase.from_pim>` method launches Fluent in `PIM <https://pypim.docs.pyansys.com/version/stable/>`_ mode.

Use this method when:

- PyFluent is used within a `PIM <https://pypim.docs.pyansys.com/version/stable/>`_ configured environment.

**Example:**

.. code-block:: python

  import ansys.fluent.core as pyfluent
  meshing = pyfluent.Meshing.from_pim()
  pure_meshing = pyfluent.PureMeshing.from_pim()
  solver = pyfluent.Solver.from_pim()
  solver_aero = pyfluent.SolverAero.from_pim()
  solver_icing = pyfluent.SolverIcing.from_pim()
  pre_post = pyfluent.PrePost.from_pim()  


.. vale Google.Spacing = YES

Using :func:`launch_fluent() <ansys.fluent.core.launcher.launcher.launch_fluent>`
---------------------------------------------------------------------------------

You can use the :func:`launch_fluent() <ansys.fluent.core.launcher.launcher.launch_fluent>`
function to start Fluent from Python. This code starts Fluent in the background and starts
Fluent's gRPC server so that commands can be sent to it from the Python interpreter:

.. code:: python

  >>> import ansys.fluent.core as pyfluent
  >>> solver_session = pyfluent.launch_fluent()


You can use the :func:`connect_to_fluent() <ansys.fluent.core.launcher.launcher.connect_to_fluent>`
function to connect to a running Fluent session that has already started the gRPC server. There are
some options for starting Fluent's gRPC server:

1. Start Fluent with ``<fluent_executable> -sifile=<server_info_file_name>``, or
2. Execute the ``server/start-server`` solution mode TUI command in Fluent, or
3. Execute ``File -> Applications -> Server -> Start...`` from the Fluent GUI ribbon menu in solution mode.

On starting the gRPC server, Fluent writes out a server-info file at ``<server_info_file_name>`` and
prints this information in the console. If you do not specify a particular ``<server_info_file_name>``,
it is automatically generated.

This code connects to a running Fluent session where the server-info file is server.txt in the working
directory:

.. code:: python

  >>> import ansys.fluent.core as pyfluent
  >>> solver_session = pyfluent.connect_to_fluent(
  >>>     server_info_file_name="server.txt"
  >>> )


Launcher options
----------------
The following examples show different ways that you can launch Fluent locally.
For more information, see :func:`launch_fluent() <ansys.fluent.core.launcher.launcher.launch_fluent>`.

Solution mode
~~~~~~~~~~~~~
These two examples show equivalent ways to launch Fluent in solution mode:

.. code:: python

  >>> solver_session = pyfluent.launch_fluent(mode=pyfluent.FluentMode.SOLVER)
  

.. code:: python

  >>> solver_session = pyfluent.launch_fluent()


Meshing mode
~~~~~~~~~~~~
This example shows how to launch Fluent in meshing mode:

.. code:: python

  >>> meshing_session = pyfluent.launch_fluent(
  >>>      mode=pyfluent.FluentMode.MESHING
  >>> )


Pre/Post mode
~~~~~~~~~~~~~
Run Ansys Fluent with only the setup and postprocessing capabilities available. It does not allow you to perform calculations.

This example shows how to launch Fluent in Pre/Post mode:

.. code:: python

  >>> pre_post_session = pyfluent.launch_fluent(mode=pyfluent.FluentMode.PRE_POST)


Precision
~~~~~~~~~
This example shows how to launch Fluent in solution mode
and set the floating point precision:

.. code:: python

  >>> solver_session = pyfluent.launch_fluent(
  >>>      precision=pyfluent.Precision.DOUBLE
  >>> )


Dimension
~~~~~~~~~
This example shows how to launch Fluent in solution mode and set the
modeling dimension to two:

.. code:: python

  >>> solver_session = pyfluent.launch_fluent(
  >>>      precision=pyfluent.Precision.DOUBLE,
  >>>      dimension=pyfluent.Dimension.TWO
  >>> )


Local parallel
~~~~~~~~~~~~~~
This example shows how to launch Fluent in solution mode and set the
number of processors for local parallel execution:

.. code:: python

  >>> solver_session = pyfluent.launch_fluent(
  >>>      precision=pyfluent.Precision.DOUBLE,
  >>>      dimension=pyfluent.Dimension.TWO,
  >>>      processor_count=2
  >>> )


Distributed parallel
~~~~~~~~~~~~~~~~~~~~
This example shows how to launch Fluent in solution mode with 16 processors
distributed across more than one machine:

.. code:: python

  >>> solver_session = pyfluent.launch_fluent(
  >>>     precision=pyfluent.Precision.DOUBLE,
  >>>     dimension=pyfluent.Dimension.THREE,
  >>>     processor_count=16
  >>>     additional_arguments="-cnf=m1:8,m2:8",
  >>> )


Logging support
---------------
PyFluent has an option to run with logging enabled.
This command enables logging:

.. code:: python

  >>> pyfluent.logger.enable()


For more details, see :ref:`ref_logging_guide`.

Scheduler support
-----------------
When PyFluent is used within a job scheduler environment, the :func:`launch_fluent()
<ansys.fluent.core.launcher.launcher.launch_fluent>` function automatically determines
the list of machines and core counts with which to start Fluent. The supported
scheduler environments are Altair Grid Engine (formerly UGE), Sun Grid Engine (SGE),
Load Sharing Facility (LSF), Portable Batch System (PBS), and Slurm.

This example shows a bash shell script that can be submitted to a Slurm
scheduler using the ``sbatch`` command:

.. code:: bash

   #!/bin/bash
   #SBATCH --job-name="pyfluent"
   #SBATCH --nodes=8
   #SBATCH --ntasks=32
   #SBATCH --output="%x_%j.log"
   #SBATCH --partition=mpi01
   #
   # Change to the directory where the Slurm job was submitted
   #
   cd $SLURM_SUBMIT_DIR
   #
   # Activate your favorite Python environment
   #
   export AWP_ROOT252=/apps/ansys_inc/v252
   . ./venv/bin/activate
   #
   # Run a PyFluent script
   #
   python run.py


Here are a few notes about this example:

- Eight machines with a total of 32 cores are requested. Fluent is started with
  the appropriate command line arguments passed to ``-t`` and ``-cnf``.
- The variable ``AWP_ROOT251`` is configured so that PyFluent can find
  the Fluent installation.
- The code assumes that a Python virtual environment was pre-configured with
  PyFluent installed before the job script is submitted to Slurm. You could
  also configure the virtual environment as part of the job script if desired.
- The ``run.py`` file can contain any number of PyFluent commands using any of
  the supported interfaces.

Within the scheduler environment, the
:func:`launch_fluent() <ansys.fluent.core.launcher.launcher.launch_fluent>`
function can be used in a few different ways. This example shows how to start
the three-dimensional, double precision version of Fluent on all the requested
machines and cores:

.. code:: python

  >>> solver_session = pyfluent.launch_fluent(
  >>>      precision=pyfluent.Precision.DOUBLE,
  >>>      dimension=pyfluent.Dimension.THREE
  >>> )


You can use the ``processor_count`` argument to set the number of cores that
Fluent uses:

.. code:: python

  >>> solver_session = pyfluent.launch_fluent(
  >>>     precision=pyfluent.Precision.DOUBLE,
  >>>     dimension=pyfluent.Dimension.THREE,
  >>>     processor_count=16,
  >>> )


Passing the ``processor_count`` parameter like this forces execution of Fluent on 16
cores, despite the fact that the Slurm submission requests 32 total cores from
the job scheduler. This behavior may be useful in situations where the scheduler
environment allocates all the cores on a machine and you know that Fluent may
not scale well on all the allocated cores.

Finally, if you want to ignore the scheduler allocation, you can pass either the ``-t``
argument or both the ``-t`` and ``-cnf`` arguments to the
:func:`launch_fluent() <ansys.fluent.core.launcher.launcher.launch_fluent>` function
using the ``additional_arguments`` parameter. For local parallel execution, simply pass the
``-t`` argument:

.. code:: python

  >>> solver_session = pyfluent.launch_fluent(
  >>>     precision=pyfluent.Precision.DOUBLE,
  >>>     dimension=pyfluent.Dimension.THREE,
  >>>     additional_arguments="-t16"
  >>> )


For distributed parallel processing, you usually pass both parameters:

.. code:: python

  >>> solver_session = pyfluent.launch_fluent(
  >>>     precision=pyfluent.Precision.DOUBLE,
  >>>     dimension=pyfluent.Dimension.THREE,
  >>>     additional_arguments="-t16 -cnf=m1:8,m2:8",
  >>> )


The :func:`launch_fluent() <ansys.fluent.core.launcher.launcher.launch_fluent>` function
also supports the ``scheduler_options`` parameter to submit the Fluent job to a Slurm
scheduler without using any bash script:

.. code:: python

  >>> slurm = pyfluent.launch_fluent(
  >>>     scheduler_options={
  >>>         "scheduler": "slurm",
  >>>         "scheduler_headnode": "<headnode>",
  >>>         "scheduler_queue": "<queue>",
  >>>         "scheduler_account": "<account>"
  >>>     },
  >>>     additional_arguments="-t16 -cnf=m1:8,m2:8",
  >>> )
  >>> solver_session = slurm.result()


.. vale off

The keys ``scheduler_headnode``, ``scheduler_queue`` and ``scheduler_account`` are
optional and should be specified in a similar manner to Fluent's scheduler options.
Here, the :func:`launch_fluent <ansys.fluent.core.launcher.launcher.launch_fluent>`
function returns a :class:`SlurmFuture <ansys.fluent.core.launcher.slurm_launcher.SlurmFuture>`
instance from which the PyFluent session can be extracted. For a detailed usage, see the
documentation of the :mod:`slurm_launcher <ansys.fluent.core.launcher.slurm_launcher>`
module.

.. vale on

The ``scheduler_options`` parameter doesn't support the automatic scheduler allocation,
the ``-t`` and ``-cnf`` arguments must be passed to the
:func:`launch_fluent() <ansys.fluent.core.launcher.launcher.launch_fluent>` function
using the ``additional_arguments`` parameter for distributed parallel processing.

Launching a `PIM <https://pypim.docs.pyansys.com/version/stable/>`_ session
---------------------------------------------------------------------------
When PyFluent is used within a `PIM <https://pypim.docs.pyansys.com/version/stable/>`_ configured environment, 
the :func:`launch_fluent() <ansys.fluent.core.launcher.launcher.launch_fluent>` function automatically launches 
Fluent session in `PIM <https://pypim.docs.pyansys.com/version/stable/>`_ mode and in that same environment it 
can be launched explicitly using :func:`create_launcher() <ansys.fluent.core.launcher.launcher.create_launcher>` as follows:

.. code:: python

  >>> from ansys.fluent.core.launcher.launcher import create_launcher
  >>> from ansys.fluent.core.launcher.launch_options import LaunchMode, FluentMode

  >>> pim_meshing_launcher = create_launcher(LaunchMode.PIM, mode=FluentMode.MESHING)
  >>> pim_meshing_session = pim_meshing_launcher()

  >>> pim_solver_launcher = create_launcher(LaunchMode.PIM)
  >>> pim_solver_session = pim_solver_launcher()


Launching Fluent in container mode with Docker Compose or Podman Compose
------------------------------------------------------------------------

Use PyFluent with Docker Compose or Podman Compose to run Fluent in a consistent, reproducible containerized environment.

1. **Docker Compose**

    Prerequisites:

    - `Docker <https://www.docker.com/>`_
    - `Docker Compose <https://docs.docker.com/compose/>`_


2. **Podman Compose**

    Prerequisites:

    - `Podman <https://podman.io/>`_
    - `Podman Compose <https://docs.podman.io/en/latest/markdown/podman-compose.1.html>`_


Example:

Set environment variables to select the container engine:

.. code:: python

  >>> import os
  >>> os.environ["PYFLUENT_LAUNCH_CONTAINER"] = "1"
  >>> os.environ["PYFLUENT_USE_DOCKER_COMPOSE"] = "1" # or os.environ["PYFLUENT_USE_PODMAN_COMPOSE"] = "1"


Then launch:

.. code:: python

  >>> import ansys.fluent.core as pyfluent
  >>> from ansys.fluent.core import examples
  >>> solver_session = pyfluent.launch_fluent()
  >>> case_file_name = examples.download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
  >>> solver_session.file.read(file_name=case_file_name, file_type="case")
  >>> solver_session.exit()


Connect to a Fluent container running inside WSL from a Windows host
--------------------------------------------------------------------

1. Launch Fluent container inside WSL

.. code:: console

    docker run -it -p 63084:63084 -v /mnt/d/testing:/testing -e "ANSYSLMD_LICENSE_FILE=<license file or server>" -e "REMOTING_PORTS=63084/portspan=2" ghcr.io/ansys/pyfluent:v25.2.0 3ddp -gu -sifile=/testing/server.txt
    /ansys_inc/v252/fluent/fluent25.2.0/bin/fluent -r25.2.0 3ddp -gu -sifile=/testing/server.txt

2. Connect from PyFluent running on a Windows host

.. code:: python

  >>> import ansys.fluent.core as pyfluent
  >>> solver_session = pyfluent.connect_to_fluent(ip="localhost", port=63084, password=<password written `server.txt`>)


Connecting to a Fluent container running inside Linux from a Windows host
-------------------------------------------------------------------------

1. Launch Fluent container inside Linux

.. code:: console

    ansys_inc/v251/fluent/bin/fluent 3ddp -gu -sifile=server.txt
    cat server.txt
    10.18.19.151:44383
    hbsosnni

2. Connect from PyFluent running on a Windows host

.. code:: python

  >>> import ansys.fluent.core as pyfluent
  >>> solver_session = pyfluent.connect_to_fluent(ip="10.18.19.151", port=44383, password="hbsosnni")


Connecting to Fluent on Windows from a Linux or WSL host
--------------------------------------------------------

This guide describes how to connect to an ANSYS Fluent instance running on a Windows machine from a Linux or WSL host. 
It also includes steps to enable remote file transfer.

  Prerequisites:

    - `Docker <https://www.docker.com/>`_
    - `Build file transfer server <https://filetransfer-server.tools.docs.pyansys.com/version/stable/intro.html#>`_

A. **Set Up Fluent and File Transfer Server on Windows**

1. **Launch Fluent**

   Open a command prompt and run:

   .. code:: console

      ANSYS Inc\v252\fluent\ntbin\win64\fluent.exe 3ddp -sifile=server_info.txt
      type server_info.txt

   Example output:
   ``10.18.44.179:51344``, ``5scj6c8l``

2. **Retrieve Connection Details**

   Get the IP address, port, and password from the `server_info.txt` file.  
   Example:
   - IP: ``10.18.44.179``
   - Port: ``51344``
   - Password: ``5scj6c8l``

3. **Start the File Transfer Server**

   From Fluent's working directory, start the container for file-transfer server.

   .. code:: console

      docker run -p 50000:50000 -v %cd%:/home/container/workdir filetransfer-tool-server

4. **Allow Inbound TCP Connections**

   Configure the Windows Firewall:

   - Open: **Control Panel > Windows Defender Firewall > Advanced Settings > Inbound Rules**
   - Right-click **Inbound Rules**, select **New Rule**
   - Choose **Port**, click **Next**
   - Keep **TCP** selected
   - Enter the ports in **Specific local ports**: `51344, 50000` then click **Next**
   - Select **Allow the connection**, click **Next**
   - Leave all profiles (Domain, Private, Public) checked, click **Next**
   - Name the rule: `Inbound TCP for Fluent`

Note: Delete the added inbound rule after the Fluent session is closed.

B. **Connect from Linux or WSL Host**

Run the following Python code to connect to Fluent and transfer files:

.. code:: python

   from ansys.fluent.core import connect_to_fluent
   from ansys.fluent.core.utils.file_transfer_service import RemoteFileTransferStrategy

   file_service = RemoteFileTransferStrategy("10.18.44.179", 50000)
   solver_session = connect_to_fluent(ip="10.18.44.179", port=51344, password="5scj6c8l", file_transfer_service=file_service)

   # `mixing_elbow.cas.h5` will be uploaded to remote Fluent working directory
   solver_session.file.read_case(file_name="/home/user_name/mixing_elbow.cas.h5")

   # `elbow_remote.cas.h5` will be downloaded to local working directory
   solver_session.file.write_case(file_name="elbow_remote.cas.h5")


Connecting to Fluent on Linux or WSL from a Windows host
--------------------------------------------------------

This guide describes how to connect to an ANSYS Fluent instance running on a Linux or WSL machine from a Windows host. 
It also includes steps to enable remote file transfer.

  Prerequisites:

    - `Docker <https://www.docker.com/>`_
    - `Build file transfer server <https://filetransfer-server.tools.docs.pyansys.com/version/stable/intro.html#>`_

A. **Set Up Fluent and File Transfer Server on Linux or WSL**

1. **Launch Fluent**

   Open a shell and run:

   .. code:: console

      ansys_inc/v252/fluent/bin/fluent 3ddp -sifile=server_info.txt
      cat server_info.txt

   Example output:
   ``10.18.19.150:41429``, ``u5s3iivh``

2. **Retrieve Connection Details**

   Get the IP address, port, and password from the `server_info.txt` file.  
   Example:
   - IP: ``10.18.19.150``
   - Port: ``41429``
   - Password: ``u5s3iivh``

3. **Start the File Transfer Server**

   From Fluent's working directory, start the container for file-transfer server.

   .. code:: console

      docker run -p 50000:50000 -v `pwd`:/home/container/workdir -u `id -u`:`id -g` filetransfer-tool-server

B. **Connect from Windows Host**

Run the following Python code to connect to Fluent and transfer files:

.. code:: python

   from ansys.fluent.core import connect_to_fluent
   from ansys.fluent.core.utils.file_transfer_service import RemoteFileTransferStrategy

   file_service = RemoteFileTransferStrategy("10.18.19.150", 50000)
   solver_session = connect_to_fluent(ip="10.18.19.150", port=41429, password="u5s3iivh", file_transfer_service=file_service)

   # `mixing_elbow.cas.h5` will be uploaded to remote Fluent working directory
   solver_session.file.read_case(file_name="D:\path_to_file\mixing_elbow.cas.h5")

   # `elbow_remote.cas.h5` will be downloaded to local working directory
   solver_session.file.write_case(file_name="elbow_remote.cas.h5")

