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

Exposure Level Configuration
-----------------------------

By default, the settings API only exposes stable API objects. To access beta and alpha features programmatically,
you can set the default exposure level via the configuration or the environment variable:

.. code-block:: python

    >>> from ansys.fluent.core import config
    >>> config.default_exposure_level  # default value
    'stable'
    >>> config.default_exposure_level = 'beta'  # allow beta objects
    >>> config.default_exposure_level = 'alpha'  # allow alpha and beta objects
    >>> config.default_exposure_level = 'stable'  # revert to stable only

Alternatively, set the ``PYFLUENT_EXPOSURE_LEVEL`` environment variable:

.. code-block:: bash

    export PYFLUENT_EXPOSURE_LEVEL=beta
    python your_script.py

Valid values are ``"stable"`` (default), ``"beta"``, and ``"alpha"`` (most permissive).
This setting applies globally to all settings roots created after it is changed.
