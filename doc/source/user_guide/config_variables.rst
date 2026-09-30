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

PyFluent's public APIs carry accurate type annotations, so you can check them at runtime with
the type-checker of your choice, the same way you would for any other dependency. PyFluent does
not install or activate a type-checker itself.

For example, with `beartype <https://beartype.readthedocs.io>`_, installed with the
``type-checking`` extra:

.. code-block:: bash

    pip install ansys-fluent-core[type-checking]

apply its import hook to the module or subpackage you want checked **before** importing it:

.. code-block:: python

    >>> from beartype.claw import beartype_package
    >>> beartype_package("ansys.fluent.core.utils.fluent_version")
    >>> import ansys.fluent.core

.. note::

    ``ansys`` and ``ansys.fluent`` are :pep:`420` namespace packages, so
    ``beartype_this_package()`` cannot be used from within PyFluent itself, and
    ``beartype_package("ansys")`` or ``beartype_package("ansys.fluent")`` will not work either.
    Target ``ansys.fluent.core`` or one of its submodules explicitly.

.. warning::

    Applying the hook to the whole ``ansys.fluent.core`` package is not yet
    supported: some modules contain ``TYPE_CHECKING``-only forward references
    that a runtime checker cannot resolve eagerly, and checking a descriptor's
    ``__set_name__`` can be called before the owning class is fully defined.
    Target the specific module or subpackage whose APIs you want checked
    instead. Broadening safe coverage across the whole package is tracked as
    future work.

A call with an argument of the wrong type then raises beartype's own exception, for example
``BeartypeCallHintParamViolation``, at the call site instead of surfacing later as an obscure
failure:

.. code-block:: python

    >>> some_function(wrong_type_argument)
    Traceback (most recent call last):
        ...
    beartype.roar.BeartypeCallHintParamViolation: ...

Some PyFluent classes rely on dynamic attribute proxying or are parameterized generics that most
runtime type-checkers cannot check safely; these are marked internally so that any checker you
apply skips them.
