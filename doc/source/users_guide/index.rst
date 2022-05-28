.. _ref_user_guide:

==========
User Guide
==========
This guide provides a general overview of the basics and usage of the
PyFluent library.


..
   This toctreemust be a top level index to get it to show up in
   pydata_sphinx_theme

.. toctree::
   :maxdepth: 1
   :hidden:

   launching_ansys_fluent
   meshing_workflows
   general_settings
   solver_settings
   models
   materials
   cell_zone_conditions
   boundary_conditions
   solution
   postprocessing
   parametric_workflows
   settings_apis_beta


PyFluent Basic Overview
======================
The :func:`launch_fluent() <ansys.fluent.core.launch_fluent>` function
within the ``ansys-fluent-core`` library creates an instance of
:class:`fluent <ansys.fluent.core.fluent._fluentCore>` in the background and sends
commands to that service.  Errors and warnings are processed
Pythonically letting the user develop a script real-time without
worrying about if it will function correctly when deployed in batch
mode.

fluent can be started from python in gRPC mode using
:func:`launch_fluent() <ansys.fluent.core.launch_fluent>`.  This starts
fluent in a temporary directory by default.  You can change this to
your current directory with:

.. code:: python

    import os
    from ansys.fluent.core import launch_fluent

    path = os.getcwd()
    fluent = launch_fluent(run_location=path)

fluent is now active and you can send commands to it as a genuine a
Python class.  For example, if we wanted to create a surface using
keypoints we could run:

.. code:: python

    fluent.run('/PREP7')
    fluent.run('K, 1, 0, 0, 0')
    fluent.run('K, 2, 1, 0, 0')
    fluent.run('K, 3, 1, 1, 0')
    fluent.run('K, 4, 0, 1, 0')
    fluent.run('L, 1, 2')
    fluent.run('L, 2, 3')
    fluent.run('L, 3, 4')
    fluent.run('L, 4, 1')
    fluent.run('AL, 1, 2, 3, 4')

fluent interactively returns the result of each command and it is
stored to the logging module.  Errors are caught immediately.  For
example, if you input an invalid command:

.. code:: python

    >>> fluent.run('AL, 1, 2, 3')

   fluentRuntimeError: 
   AL, 1, 2, 3

   DEFINE AREA BY LIST OF LINES
   LINE LIST =     1    2    3
   (TRAVERSED IN SAME DIRECTION AS LINE     1)

   *** ERROR ***                           CP =       0.338   TIME= 09:45:36
   Keypoint 1 is referenced by only one line.  Improperly connected line   
   set for AL command.                                                     

This ``fluentRuntimeError`` was caught immediately, and this means that
you can write your fluent scripts in python, run them interactively and
then as a batch without worrying if the script will run correctly if
you had instead outputted it to a script file.

The :class:`fluent <ansys.fluent.core.fluent._fluentCore>` class supports much more
than just sending text to fluent and includes higher level wrapping
allowing for better scripting and interaction with fluent.  See the
:ref:`ref_examples` for an overview of the various advanced
methods to visualize, script, and interact with fluent.


Calling fluent Pythonically
~~~~~~~~~~~~~~~~~~~~~~~~~~
fluent functions can be called directly from an instance of
:class:`fluent <ansys.fluent.core.fluent._fluentCore>` in a pythonic manner.  This is
to simplify calling ANSYS, especially when inputs are variables within
Python.  For example, the following two commands are equivalent:

.. code:: python

    fluent.k(1, 0, 0, 0)
    fluent.run('K, 1, 0, 0, 0')

This approach has some obvious advantages, chiefly that it's a easier
to script as ``ansys-fluent-core`` takes care of the string formatting for you.
For example, inputting points from a numpy array:

.. code:: python

   # make 10 random keypoints in ANSYS
   points = np.random.random((10, 3))
   for i, (x, y, z) in enumerate(points):
       fluent.k(i + 1, x, y, z)

Additionally, exceptions are caught and handled within Python.

.. code:: python

    >>> fluent.run('AL, 1, 2, 3')

   Exception: 
   AL, 1, 2, 3

   DEFINE AREA BY LIST OF LINES
   LINE LIST =     1    2    3
   (TRAVERSED IN SAME DIRECTION AS LINE     1)

   *** ERROR ***                           CP =       0.338   TIME= 09:45:36
   Keypoint 1 is referenced by only one line.  Improperly connected line   
   set for AL command.                                                     


For longer scripts, instead of sending commands to fluent as in the
area creation example, we can instead run:

.. code:: python

    # clear existing geometry
    fluent.finish()
    fluent.clear()

    # create a square area using keypoints
    fluent.prep7()
    fluent.k(1, 0, 0, 0)
    fluent.k(2, 1, 0, 0)
    fluent.k(3, 1, 1, 0)
    fluent.k(4, 0, 1, 0)    
    fluent.l(1, 2)
    fluent.l(2, 3)
    fluent.l(3, 4)
    fluent.l(4, 1)
    fluent.al(1, 2, 3, 4)

This approach has some obvious advantages, chiefly that it's a bit
easier to script as :class:`fluent <ansys.fluent.core.fluent._fluentCore>`
takes care of the string formatting for you.  For example, inputting
points from a numpy array:

.. code:: python

   import numpy as np

   # make 10 random keypoints in fluent
   points = np.random.random((10, 3))
   for i, (x, y, z) in enumerate(points):
       fluent.k(i + 1, x, y, z)

Additionally, each function with the fluent class has help associated
within it.  For example:

.. code:: python

    >>> help(fluent.k)

    Help on method K in module ansys.fluent.core.fluent_grpc.fluentGrpc:

    k(npt='', x='', y='', z='') method of ansys.fluent.core.fluent_grpc.fluentGrpc
    instance

        Defines a keypoint.

        APDL Command: K

        Parameters
        ----------
        npt
            Reference number for keypoint.  If zero, the lowest
            available number is assigned [NUMSTR].

        x, y, z
            Keypoint location in the active coordinate system (may be
            R, θ, Z or R, θ, Φ).  If X = P, graphical picking is
            enabled and all other fields (including NPT) are ignored
            (valid only in the GUI).

        Examples
        --------
        Create a keypoint at (1, 1, 2)

        >>> fluent.k(1, 1, 1, 2)

        Notes
        -----
        Defines a keypoint in the active coordinate system [CSYS] for
        line, area, and volume descriptions.  A previously defined
        keypoint of the same number will be redefined.  Keypoints may
        be redefined only if it is not yet attached to a line or is
        not yet meshed.  Solid modeling in a toroidal system is not
        recommended.


Remote Stability Considerations
-------------------------------
.. note::
   This is only valid for instances of fluent launched in 2021R1 or
   newer launching with ``mode=grpc`` (default).

When connecting to a remote instance of fluent, there are some cases
where the fluent server will exit unexpectedly.  These issues are being
corrected and will be solved in 2021R2, but for the time being, there
are several ways to improve performance and stability of MADPL:

- When possible, pass ``mute=True`` to individual fluent commands or
  set it globally with :func:`fluent.mute
  <ansys.fluent.core.fluent_grpc.fluentGrpc>`.  This disables streaming
  back the response from fluent for each command and will marginally
  improve performance and stability.  Consider having a debug flag in
  your program or script so you can enable or disable logging and
  verbosity when needed.

.. note::
   fluent 2021R1 has a stability issue with :func:`fluent.input()
   <ansys.fluent.core.fluent.input>`.  Avoid using input files if
   possible.  Attempt to :func:`fluent.upload()
   <ansys.fluent.core.fluent.upload>` nodes and elements and read them
   in via :func:`fluent.nread() <ansys.fluent.core.fluent.nread>` and
   :func:`fluent.eread() <ansys.fluent.core.fluent.eread>`.
