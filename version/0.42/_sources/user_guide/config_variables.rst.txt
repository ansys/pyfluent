.. _ref_config_variables:

Configuration variables
=======================

The PyFluent library provides a set of configuration variables that can be used to control various aspects of its behavior at runtime.
These variables are accessible through the ``config`` object available in the ``ansys.fluent.core`` module.

The following code demonstrates how to access and modify the path within the Fluent container which is mapped to the host system:

.. code-block:: python

    >>> from ansys.fluent.core import config
    >>> config.container_mount_target  # default value
    '/home/container/workdir'
    >>> config.container_mount_target = '/home/my_user/workdir'  # set a new value
    >>> config.container_mount_target  # new value
    '/home/my_user/workdir'
