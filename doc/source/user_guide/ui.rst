.. _ref_ui:

Interactive Settings UI
=======================

The interactive **Settings UI** provides an intuitive way to explore and modify
settings objects exposed by PyFluent. It lets you navigate through the hierarchy,
expand sections, and directly interact with individual parameters or commands.

As you expand sections, the UI displays the **path** to each settings object.
These paths can be reused in automation scripts with PyFluent. You can launch the UI
with any settings object, from the root ``solver.settings`` to a specific branch.

The UI supports two modes:

* **Web mode** when running from a standalone Python script.
* **Inline mode** inside a Jupyter Notebook.

Launching the UI
----------------

Import the ``ui`` function and pass in a settings object:

.. code-block:: python

   import ansys.fluent.core as pyfluent
   from ansys.fluent.core.ui import ui

   solver = pyfluent.launch_fluent()

   # Launch the UI for the full settings tree
   ui(solver.settings)

You can also launch the UI for a specific subset of settings:

.. code-block:: python

   # Case file read operations
   ui(solver.settings.file.read_case)

   # Physical models configuration
   ui(solver.settings.setup.models)

Features
--------

* **Expandable sections**: Browse the hierarchy of settings
  objects by expanding and collapsing sections.
* **Path display**: Each expanded section shows its fully qualified path
  for easy reuse in scripts.
* **Interactive fields**: Parameters can be edited directly from the UI.
* **Flexible scope**: Start at the root (``solver.settings``) or
  any branch of the settings tree.
* **Multiple environments**:
  - Web mode for standalone Python scripts.
  - Inline mode inside Jupyter Notebooks.

Use Cases
---------

The interactive Settings UI is particularly useful for:

* Exploring solver settings without memorizing full paths.
* Rapidly editing parameters during solver setup.
* Teaching and demonstrations, where hierarchical navigation and paths
  aid understanding.
* Embedding interactive solver configuration directly in notebooks
  for reproducible workflows.

``ui`` bridges programmatic control with interactive exploration,
letting you configure Fluent in the way that best fits your workflow.
