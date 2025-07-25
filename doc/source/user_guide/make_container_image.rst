.. _ref_make_container_image:

Containerization of Fluent
==========================

.. warning:: You need a valid Ansys license to follow the steps in this section.

This document provides instructions and guidelines on how to containerize
Fluent for efficient and secure deployment and management.


Prerequisites
-------------

1. A Linux machine with `Docker <https://www.docker.com>`_ installed.

2. A valid Ansys license. Your Ansys reseller should have provided you with one.

3. PyFluent source. You can clone `PyFluent <https://github.com/ansys/pyfluent>`_ or download the zip from `here <https://github.com/ansys/pyfluent/archive/refs/heads/main.zip>`_.


Procedure
---------

1. Set current working directory
++++++++++++++++++++++++++++++++

Within the PyFluent source navigate to the ``docker`` directory.

2. Copy needed files
++++++++++++++++++++

Specify the pre-installed Ansys directory and ``docker/fluent_<version>`` directory for the particular Fluent release as a
command line arguments and run this script to copy needed files from the Ansys installation directory to the particular Fluent release directory:

.. code:: python

    python copy_ansys_files.py <path to 'ansys_inc' directory> <path to 'docker/fluent_<version>' directory>

* These files indicate the files that are excluded during the copying:

  * `excludeCEIList.txt <https://github.com/ansys/pyfluent/blob/main/docker/fluent_252/excludeCEIList.txt>`_
  * `excludeFluentList.txt <https://github.com/ansys/pyfluent/blob/main/docker/fluent_252/excludeFluentList.txt>`_

1. Above excluded files are not needed to run typical Fluent workflows.

2. If you find that some of the excluded files are needed to run your workflows then you can remove those files from the exclusion list.

3. Build the Docker image
+++++++++++++++++++++++++

Specify ``docker/fluent_<version>`` directory for the particular Fluent release and execute this command to build the Docker image:

.. code:: console

    sudo docker build -t ansys_inc <path to 'docker/fluent_<version>' directory>

The Docker container configuration needed to build the container image is described in the ``docker/fluent_<version>/Dockerfile``.


Run Docker container using the command line
-------------------------------------------

When you run the Docker container, you must specify the Ansys license file.

To launch the container in solution mode, use:

.. code:: console

    sudo docker run -it --name ansys-inc -e ANSYSLMD_LICENSE_FILE=<license file or server> ansys_inc 3ddp -gu

To launch the container in meshing mode, use:

.. code:: console

    sudo docker run -it --name ansys-inc -e ANSYSLMD_LICENSE_FILE=<license file or server> ansys_inc 3ddp -gu -meshing


Run Docker container using PyFluent
-----------------------------------

1. Install `PyFluent <https://github.com/ansys/pyfluent>`_.
2. Use the following Python code to run the container:

.. code:: python

    import os
    import ansys.fluent.core as pyfluent
    os.environ["ANSYSLMD_LICENSE_FILE"] = "<license file or server>"
    custom_config = {'fluent_image': 'ansys_inc:latest', 'mount_source': f"{os.getcwd()}", 'auto_remove': False}
    solver_session = pyfluent.launch_fluent(container_dict=custom_config, user_docker_compose=True)


Run Podman container using the command line
-------------------------------------------

Follow these steps to pull and run a Fluent container using Podman.

1. Pull the Docker image into Podman:

.. code:: console

    sudo podman pull docker-daemon:ansys-inc:latest


2. Verify the image in the local Podman registry:

.. code:: console

    sudo podman images


When you run the Podman container, you must specify the Ansys license file.

To launch the container in solution mode, use:

.. code:: console

    sudo podman run -it --name ansys-inc -e ANSYSLMD_LICENSE_FILE=<license file or server> ansys_inc 3ddp -gu

To launch the container in meshing mode, use:

.. code:: console

    sudo podman run -it --name ansys-inc -e ANSYSLMD_LICENSE_FILE=<license file or server> ansys_inc 3ddp -gu -meshing


Run Podman container using PyFluent
-----------------------------------

1. Install `PyFluent <https://github.com/ansys/pyfluent>`_. 
2. Use the following Python code to run the container:

.. code:: python

    import os
    import ansys.fluent.core as pyfluent
    os.environ["ANSYSLMD_LICENSE_FILE"] = "<license file or server>"
    custom_config = {'fluent_image': 'ansys_inc:latest', 'mount_source': f"{os.getcwd()}", 'auto_remove': False}
    solver_session = pyfluent.launch_fluent(container_dict=custom_config, use_podman_compose=True)

