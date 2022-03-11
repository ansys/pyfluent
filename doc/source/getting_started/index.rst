
.. _getting_started:

************
Introduction
************
Python is a portable, dynamically typed, interpreted programming language that is easy to learn, 
read, and write. It is free to use and distribute and is supported by a vast support library of 
thousands of available packages.

PyFluent is part of a growing Ansys Python environment that 
lets you use Ansys Fluent within or alongside any other Python environment, whether it 
is in conjunction with other Ansys Python libraries and packages or with other external 
Python products. 

PyFluent launches or connects with a running Fluent process as a server using gRPC interfaces, 
but all you need to interact with is the Python interface of Ansys Fluent.

You can use PyFluent to programmatically create, interact with and control an Ansys Fluent session to 
create your own customized workspace. In addition, you can use PyFluent to enhance your 
productivity with highly configurable, customized scripts.

************
Installation
************

To use PyFluent, you need to have a local installation of Ansys.
The version of Ansys installed will dictate the interface and features
available to you.

Visit `Ansys <https://www.ansys.com/>`_ for more information on
getting a licensed copy of Ansys.

To install a local version of PyFluent, you need to clone the PyFluent repository through 
GitHub Enterprise (https://github.com/pyansys/pyfluent). Other Ansys Python 
packages are also available here or through www.pypi.org. 

Once you have access to a cloned repository,
you can install the pyfluent library by using

.. code::

	git clone https://github.com/pyansys/pyfluent.git
	cd pyfluent
	pip install -e .


***************
Starting Fluent
***************

To see and interact with the Fluent graphical user interface, 
set the following environment variable:

.. code::

		PYFLUENT_SHOW_SERVER_GUI=1

To start Fluent, use the following:

.. code:: python

    >>> from ansys.fluent.core import launch_fluent
    >>> fluent = launch_fluent()
    >>> print(fluent)

    DNW: What comes out here?

Fluent is now active and you can send commands to it as a genuine 
Python class.  For example, if we wanted to ... <add a basic example>:

.. code:: python

    <type some commands here>

Advanced Features
~~~~~~~~~~~~~~~~~
Maybe give some basic example here for each API.
