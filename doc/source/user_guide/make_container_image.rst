.. _ref_make_container_image:

Containerization of Fluent
==========================

.. warning:: You need a valid Ansys license to follow the steps in this section.

This document provides instructions and guidelines on how to containerize
Fluent for efficient and secure deployment and management.


Prerequisites
-------------

* A Linux machine with `Docker <https://www.docker.com>`_ installed.

* A valid Ansys license. Your Ansys reseller should have provided you with one.

* The following provided files:
  
  * `Dockerfile <https://github.com/ansys/pyfluent/blob/main/docker/fluent/Dockerfile>`_
  * `copy_docker_files.py <https://github.com/ansys/pyfluent/blob/main/docker/fluent/copy_docker_files.py>`_


Procedure
---------

* If you have cloned `PyFluent <https://github.com/ansys/pyfluent>`_ locally then change the current working directory to
`Docker files <https://github.com/ansys/pyfluent/blob/main/docker/fluent>`_ before executing these commands.

* If you haven't cloned `PyFluent <https://github.com/ansys/pyfluent>`_ locally then copy `Docker files <https://github.com/ansys/pyfluent/blob/main/docker/fluent>`_ into an empty folder and
execute these commands from that folder.

Copy needed files
+++++++++++++++++

Specify the pre-installed Ansys directory as a command line argument and run this script to copy needed files from the
Ansys installation directory to the current working directory:

.. code:: python

    python copy_docker_files.py <path to 'ansys_inc' directory>

Not all the installation files are copied. These files indicate the files that are ignored during the copying:

  * `excludeCEIList.txt <https://github.com/ansys/pyfluent/blob/main/docker/fluent/excludeCEIList.txt>`_
  * `excludeFluentList.txt <https://github.com/ansys/pyfluent/blob/main/docker/fluent/excludeFluentList.txt>`_


1. We have excluded these files because we have determined that they are not needed to run typical Fluent workflows.

2. If you find that some of the excluded files are need to run your workflows then you can remove those files from the exclusion list and repeat the build process to create a new image.

Build the Docker image
++++++++++++++++++++++

Execute this command to build the Docker image:

.. code:: console

    sudo docker build -t ansys_inc .

The Docker container configuration needed to build the container image is described in the
`Dockerfile <https://github.com/ansys/pyfluent/blob/main/docker/fluent/Dockerfile>`_.


Run Docker container using the command line
-------------------------------------------

When you run the Docker container, you must specify the Ansys license file.

Execute this command to run the Docker container in solver mode:

.. code:: console

    sudo docker run -it --name ansys-inc -e ANSYSLMD_LICENSE_FILE=<license file or server> ansys_inc 3ddp -gu

Execute this command to run the Docker container in meshing mode:

.. code:: console

    sudo docker run -it --name ansys-inc -e ANSYSLMD_LICENSE_FILE=<license file or server> ansys_inc 3ddp -gu -meshing


Run Docker container using PyFluent
-----------------------------------

Install `PyFluent <https://github.com/ansys/pyfluent>`_ and execute this code
to run the Docker container using PyFluent:

.. code:: python

    import os
    import ansys.fluent.core as pyfluent
    os.environ["ANSYSLMD_LICENSE_FILE"] = "<license file or server>"
    custom_config = {'fluent_image': 'ansys_inc:latest', 'host_mount_path': f"{os.getcwd()}", 'auto_remove': False}
    solver = pyfluent.launch_fluent(container_dict=custom_config)

