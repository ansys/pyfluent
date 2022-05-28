Launching Ansys Fluent Locally
-----------------------------------------
To run, ``ansys.mapdl.core`` needs to know the location of the MAPDL
binary.  Most of the time this can be automatically determined, but
non-standard installs will need to provide the location of MAPDL.
When running for the first time, ``ansys-mapdl-core`` will request the
location of the MAPDL executable if it cannot automatically find it.
You can test your installation of PyMAPDL and set it up by running
the :func:`launch_mapdl() <ansys.mapdl.core.launch_mapdl>`:

.. code:: python

    from ansys.mapdl.core import launch_mapdl
    mapdl = launch_mapdl()

Python will automatically attempt to detect your MAPDL binary based on
environmental variables.  If it is unable to find a copy of MAPDL, you
will be prompted for the location of the MAPDL executable.  Here is a
sample input for Linux:

.. code::

    Enter location of MAPDL executable: /usr/ansys_inc/v212/ansys/bin/ansys212

and for Windows:

.. code::

    Enter location of MAPDL executable: C:\Program Files\ANSYS Inc\v212\ANSYS\bin\winx64\ansys212.exe

The settings file is stored locally and you will not not need to enter
the path again.  If you need to change the default ansys path
(i.e. changing the default version of MAPDL), run the following:

.. code:: python

    from ansys.mapdl import core as pymapdl
    new_path = 'C:\\Program Files\\ANSYS Inc\\v212\\ANSYS\\bin\\winx64\\ansys212.exe'
    pymapdl.change_default_ansys_path(new_path)

Also see :func:`change_default_ansys_path() <ansys.mapdl.core.change_default_ansys_path>` and
:func:`find_ansys() <ansys.mapdl.core.find_ansys>`.

Additionally, it is possible to specify the executable using the keyword argument ``exec_file``. 
In Linux:

.. code:: python

    from ansys.mapdl.core import launch_mapdl

    mapdl = launch_mapdl(exec_file='/usr/ansys_inc/v212/ansys/bin/ansys212')


And in Windows:

.. code:: python

    from ansys.mapdl.core import launch_mapdl

    mapdl = launch_mapdl(exec_file='C://Program Files//ANSYS Inc//v212//ANSYS//bin//winx64//ansys212.exe')

You could also specify a custom executable by adding the correspondent flag (``-custom``) to the additional switches keyword argument.

.. code:: python

    from ansys.mapdl.core import launch_mapdl

    custom_exec = '/usr/ansys_inc/v212/ansys/bin/ansys212t'
    add_switch = f" -custom {custom_exec}"
    mapdl = launch_mapdl(additional_switches=add_switch)



API Reference
~~~~~~~~~~~~~
For more details for controlling how MAPDL launches locally, see the
function description of :func:`launch_mapdl() <ansys.mapdl.core.launch_mapdl>`.
