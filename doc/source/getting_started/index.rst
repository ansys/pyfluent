.. _getting_started:

===============
Getting Started
===============
To use PyFluent, you need to have a local installation of Ansys.

Visit `Ansys <https://www.ansys.com/>`_ for more information on
getting a licensed copy of Ansys.

************
Installation
************

To use PyFluent, you need to have a local installation of Ansys. The version of
Ansys installed will dictate the interface and features available to you.

Visit `Ansys <https://www.ansys.com/>`_ for more information on getting a
licensed copy of Ansys.

To install a local version of PyFluent, you need to clone the PyFluent
repository through GitHub Enterprise (https://github.com/pyansys/pyfluent).
Other Ansys Python packages are also available here or through www.pypi.org. 

Once you have access to a cloned repository, you can install the pyfluent
library by using

.. code::

	git clone https://github.com/pyansys/pyfluent.git
	cd pyfluent
	pip install -e .


***************
Starting Fluent
***************

To see and interact with the Fluent graphical user interface, set the following
environment variable:

.. code::

		PYFLUENT_SHOW_SERVER_GUI=1

To start Fluent, use the following:

.. code:: python

    >>> from ansys.fluent.core import launch_fluent
    >>> fluent = launch_fluent()
    >>> print(fluent)

    DNW: What comes out here?

Fluent is now active and you can send commands to it as a genuine Python class.
For example, if we wanted to ... <add a basic example>:

.. code:: python

    <type some commands here>



