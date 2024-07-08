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

3. Clone `PyFluent <https://github.com/ansys/pyfluent>`_ or download the files from any of the following directories into an empty folder according to the Ansys version you have.

  * `Ansys Fluent 2022 R2 <https://github.com/ansys/pyfluent/blob/main/docker/fluent_222>`_
  * `Ansys Fluent 2023 R1 <https://github.com/ansys/pyfluent/blob/main/docker/fluent_231>`_
  * `Ansys Fluent 2023 R2 <https://github.com/ansys/pyfluent/blob/main/docker/fluent_232>`_
  * `Ansys Fluent 2024 R1 <https://github.com/ansys/pyfluent/blob/main/docker/fluent_241>`_
  * `Ansys Fluent 2024 R2 <https://github.com/ansys/pyfluent/blob/main/docker/fluent_242>`_


Procedure
---------

1. Set current working directory
++++++++++++++++++++++++++++++++

* If you have cloned `PyFluent <https://github.com/ansys/pyfluent>`_ locally then change the current working directory to any of the
`fluent_222 <https://github.com/ansys/pyfluent/blob/main/docker/fluent_222>`_, `fluent_231 <https://github.com/ansys/pyfluent/blob/main/docker/fluent_231>`_,
`fluent_232 <https://github.com/ansys/pyfluent/blob/main/docker/fluent_232>`_, `fluent_241 <https://github.com/ansys/pyfluent/blob/main/docker/fluent_241>`_,
`fluent_242 <https://github.com/ansys/pyfluent/blob/main/docker/fluent_242>`_ directories according to the Ansys version you have.

* If you haven't cloned `PyFluent <https://github.com/ansys/pyfluent>`_ locally then change the current working directory to the folder into which you have downloaded the files from any of the `fluent_222 <https://github.com/ansys/pyfluent/blob/main/docker/fluent_222>`_, `fluent_231 <https://github.com/ansys/pyfluent/blob/main/docker/fluent_231>`_,
`fluent_232 <https://github.com/ansys/pyfluent/blob/main/docker/fluent_232>`_, `fluent_241 <https://github.com/ansys/pyfluent/blob/main/docker/fluent_241>`_,
`fluent_242 <https://github.com/ansys/pyfluent/blob/main/docker/fluent_242>`_ directories according to the Ansys version you have.


2. Copy needed files
++++++++++++++++++++

Specify the pre-installed Ansys directory as a command line argument and run this script to copy needed files from the
Ansys installation directory to the current working directory:

.. code:: python

    python copy_docker_files.py <path to 'ansys_inc' directory>


* These files indicate the files that are excluded during the copying:

  * `excludeCEIList.txt <https://github.com/ansys/pyfluent/blob/main/docker/fluent/excludeCEIList.txt>`_
  * `excludeFluentList.txt <https://github.com/ansys/pyfluent/blob/main/docker/fluent/excludeFluentList.txt>`_

1. We have excluded these files because we have determined that they are not needed to run typical Fluent workflows.

2. If you find that some of the excluded files are needed to run your workflows then you can remove those files from the exclusion list.

3. Build the Docker image
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

