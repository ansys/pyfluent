.. _ref_make_container:

Create your Fluent docker container
===================================

.. warning:: You need a valid Ansys license and an Ansys account to
   follow the steps detailed in this section.

You can create your Fluent docker container by following the steps given on this page.
This guide will use a local Ubuntu machine to copy the needed files from the Fluent 
installation directory to the container.


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

Specify the Ansys installation directory
----------------------------------------

Specify the pre-installed Ansys directory in the following function of 
`copy_docker_files.py <https://github.com/ansys/pyfluent/blob/main/docker/fluent/copy_docker_files.py>`_. 

.. code:: python

    copy_files(src="<path to ``ansys_inc`` directory>")

Copy needed files
-----------------

Change local directory where `copy_docker_files.py <https://github.com/ansys/pyfluent/blob/main/docker/fluent/copy_docker_files.py>`_ 
is located and run this script to copy needed files from the Ansys installation directory 
to the container.

.. code:: python

    python copy_docker_files.py

Not all the installation files are copied, the files ignored during the copying are 
detailed in the following files.

  * `excludeCEIList.txt <https://github.com/ansys/pyfluent/blob/main/docker/fluent/excludeCEIList.txt>`_
  * `excludeFluentList.txt <https://github.com/ansys/pyfluent/blob/main/docker/fluent/excludeFluentList.txt>`_

Build Docker image
------------------

Execute the following command where `Dockerfile <https://github.com/ansys/pyfluent/blob/main/docker/fluent/Dockerfile>`_ is 
located to build ``ansys_inc`` Docker image in the current directory.

.. code:: console

    sudo docker build -t ansys_inc .

The Docker container configuration needed to build the container is detailed in the
`Dockerfile <https://github.com/ansys/pyfluent/blob/main/docker/fluent/Dockerfile>`_.


Run the Docker container 
========================

Run the Docker container using the command line
-----------------------------------------------

Execute the following command to run the Docker container in solver mode. 
Please note, that you will have to specify the Ansys license file.

Execute the following command to run the Docker container in solver mode.

.. code:: console

    sudo docker run -it --name ansys-inc -e ANSYSLMD_LICENSE_FILE=<ansys_license_file> ansys_inc  3ddp -gu

Execute the following command to run the Docker container in meshing mode.

.. code:: console

    sudo docker run -it --name ansys-inc -e ANSYSLMD_LICENSE_FILE=<ansys_license_file> ansys_inc  3ddp -gu -meshing


Run Docker container using PyFluent
-----------------------------------

Install `PyFluent <https://github.com/ansys/pyfluent>`_ and execute the following code
to run the Docker container using PyFluent.

.. code:: python

    import os
    import ansys.fluent.core as pyfluent
    os.environ["PYFLUENT_LAUNCH_CONTAINER"] = "1"
    os.environ["FLUENT_IMAGE_TAG"] = "latest"
    os.environ["ANSYSLMD_LICENSE_FILE"] = "<ansys_license_file>"
    custom_config = {'fluent_image': 'ansys_inc:latest', 'host_mount_path': f"{os.getcwd()}", 'auto_remove': False}
    solver = pyfluent.launch_fluent(container_dict=custom_config)


Summary
=======


* **Step 1:** Specify Ansys installation directory.

* **Step 2:** Copy needed files.

* **Step 3:** Build Docker image.

* **Step 4:** Run the Docker container using the command line or
run the Docker container using PyFluent.
