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

Runtime type-checking
---------------------

PyFluent can check the type annotations of its own APIs while they are called, so that an
argument of the wrong type is reported at the call itself instead of surfacing later as an
obscure failure. This is intended for development and testing, and is disabled by default.

It relies on `beartype <https://beartype.readthedocs.io>`_, which is installed with the
``type-checking`` extra:

.. code-block:: bash

    pip install ansys-fluent-core[type-checking]

Type-checking is applied by an import hook, so it has to be requested through the
``PYFLUENT_RUNTIME_TYPE_CHECKING`` environment variable **before** PyFluent is imported.
Setting ``config.runtime_type_checking`` afterwards has no effect and issues a warning, because
modules which are already imported cannot be checked retrospectively.

.. code-block:: bash

    export PYFLUENT_RUNTIME_TYPE_CHECKING=1

The ``config.runtime_type_checking`` variable reports whether type-checking is active in the
current process:

.. code-block:: python

    >>> from ansys.fluent.core import config
    >>> config.runtime_type_checking
    True

Passing an argument of the wrong type then raises a ``beartype.roar.BeartypeCallHintParamViolation``.

If the ``type-checking`` extra is not installed, PyFluent warns and continues with
type-checking disabled.
