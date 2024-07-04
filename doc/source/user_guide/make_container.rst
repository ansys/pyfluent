.. _ref_make_container:

Create your Fluent Docker container
===================================

.. warning:: You need a valid Ansys license and an Ansys account to
   follow the steps in this section.

The following procure for creating a Fluent Docker container uses a local
Ubuntu machine to copy the needed files from the Fluent


Requirements
============

* A Linux machine, preferably with Ubuntu 18.04 or later.
  CentOS Linux distribution is not supported anymore.
  This machine needs to have `Docker <https://www.docker.com>`_ installed.

* A valid Ansys account. Your Ansys reseller should have
  provide you with one.

* The following provided files:
  
  * `Dockerfile <https://github.com/ansys/pyfluent/blob/main/docker/fluent/Dockerfile>`_
  * `copy_docker_files.py <https://github.com/ansys/pyfluent/blob/main/docker/fluent/copy_docker_files.py>`_


Procedure
=========

If you have cloned `PyFluent <https://github.com/ansys/pyfluent>`_ locally then change current working directory to
`Docker files <https://github.com/ansys/pyfluent/blob/main/docker/fluent>`_ before executing the following commands
otherwise copy these files in an empty folder and execute the following commands from that folder.

Specify the Ansys installation directory
----------------------------------------

Specify the pre-installed Ansys directory as a command line argument.

.. code:: python

    python copy_docker_files.py <path to 'ansys_inc' directory>

Copy needed files
-----------------

Run the following script to copy needed files from the Ansys installation directory
to the container.

.. code:: python

    python copy_docker_files.py <path to 'ansys_inc' directory>

Not all the installation files are copied. These files indicate the files that are
ignored during the copying:

  * `excludeCEIList.txt <https://github.com/ansys/pyfluent/blob/main/docker/fluent/excludeCEIList.txt>`_
  * `excludeFluentList.txt <https://github.com/ansys/pyfluent/blob/main/docker/fluent/excludeFluentList.txt>`_

Build Docker image
------------------

Execute the following command to build the Docker image.

.. code:: console

    sudo docker build -t ansys_inc:v251 .

The Docker container configuration needed to build the container is described in the
`Dockerfile <https://github.com/ansys/pyfluent/blob/main/docker/fluent/Dockerfile>`_.


Run Docker container using the command line
-------------------------------------------

When you execute the command for running the Docker container in either solver or meshing mode,
you must specify the Ansys license file.

Execute this command to run the Docker container in solver mode.

.. code:: console

    sudo docker run -it --name ansys-inc -e ANSYSLMD_LICENSE_FILE=<license file or server> ansys_inc:v251 3ddp -gu

Execute this command to run the Docker container in meshing mode.

.. code:: console

    sudo docker run -it --name ansys-inc -e ANSYSLMD_LICENSE_FILE=<license file or server> ansys_inc:v251 3ddp -gu -meshing


Run Docker container using PyFluent
-----------------------------------

Install `PyFluent <https://github.com/ansys/pyfluent>`_ and execute the following code
to run the Docker container using PyFluent.

.. code:: python

    import os
    import ansys.fluent.core as pyfluent
    os.environ["ANSYSLMD_LICENSE_FILE"] = "<license file or server>"
    custom_config = {'fluent_image': 'ansys_inc:v251', 'host_mount_path': f"{os.getcwd()}", 'auto_remove': False}
    solver = pyfluent.launch_fluent(container_dict=custom_config)

