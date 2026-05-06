"""Bridge content strings for Sphinx RST generation.

These strings are injected into generated RST index pages where the underlying
Python module either does not exist (e.g. meshing_legacy) or where the
automodule directive alone does not produce meaningful rendered content.

Each variable is a plain RST snippet that is appended verbatim to the
corresponding ``*_contents.rst`` file by ``api_rstgen.py``.

The :doc: cross-references inside each string are relative to the RST file
into which the content is injected, so they must be written from the
perspective of that file's location under ``doc/source/api/``.
"""

# ---------------------------------------------------------------------------
# meshing_workflow_new.rst
# Injected into: doc/source/api/meshing/meshing_workflow_new.rst
# Describes the Root class of the meshing_workflow datamodel and links to the
# five generated child datamodel pages living under meshing/datamodel/meshing_workflow/.
# ---------------------------------------------------------------------------
meshing_workflow_bridge_content = """meshing.datamodel.meshing_workflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Meshing workflow datamodel API.

Root class
^^^^^^^^^^

- Signature: Root(service, rules, path)
- Base class: PyMenu

Methods
^^^^^^^

- __init__(service, rules, path): Initialize the PyMenu root.

Child classes
^^^^^^^^^^^^^

- :doc:`application <datamodel/meshing_workflow/application/application_contents>`: application group.
- :doc:`general <datamodel/meshing_workflow/general/general_contents>`: general group.
- :doc:`parts <datamodel/meshing_workflow/parts/parts_contents>`: parts group.
- :doc:`parts_files <datamodel/meshing_workflow/parts_files/parts_files_contents>`: parts_files group.
- :doc:`task_object <datamodel/meshing_workflow/task_object/task_object_contents>`: task_object group.

"""

# ---------------------------------------------------------------------------
# meshing_legacy_contents.rst
# Injected into: doc/source/api/meshing_legacy/meshing_legacy_contents.rst
# ansys.fluent.core.meshing_legacy does not exist as an importable module so
# automodule produces nothing.  This section provides a human-readable overview
# and links to the actual generated pages, which live under the sibling meshing/
# folder, hence the ``../meshing/`` relative prefix.
# ---------------------------------------------------------------------------
meshing_legacy_bridge_content = """Legacy meshing API
~~~~~~~~~~~~~~~~~

The legacy meshing interface provides backward-compatible access to earlier meshing workflows and utilities.

Main components
^^^^^^^^^^^^^^^

- :doc:`meshing <../meshing/datamodel/meshing/meshing_contents>`: Core meshing datamodel.
- :doc:`part_management <../meshing/datamodel/part_management/part_management_contents>`: Part management tools.
- :doc:`pm_file_management <../meshing/datamodel/pm_file_management/pm_file_management_contents>`: Part management file operations.
- :doc:`workflow <../meshing/datamodel/workflow/workflow_contents>`: Legacy workflow definitions.
- :doc:`tui <../meshing/tui/tui_contents>`: Text user interface commands.
"""

# ---------------------------------------------------------------------------
# solver_contents.rst
# Injected into: doc/source/api/solver/solver_contents.rst
# Groups the flat toctree entries into two labelled sections so readers can
# distinguish top-level solver modules from the solver datamodel sub-pages.
# ---------------------------------------------------------------------------
solver_bridge_content = """Solver API
~~~~~~~~~~

The solver interface provides settings, TUI access, and solver datamodel workflows.

Main components
^^^^^^^^^^^^^^^

- :doc:`error_message <error_message>`: Solver error message helpers.
- :doc:`flobject <flobject>`: Fluent object wrappers for solver APIs.
- :doc:`settings <settings_root>`: Top-level solver settings object.
- :doc:`tui <tui/tui_contents>`: Solver text user interface commands.

Solver datamodel components
^^^^^^^^^^^^^^^^^^^^^^^^^^^

- :doc:`flicing <datamodel/flicing/flicing_contents>`: Flicing datamodel APIs.
- :doc:`preferences <datamodel/preferences/preferences_contents>`: Solver preferences datamodel APIs.
- :doc:`solver_workflow <datamodel/solver_workflow/solver_workflow_contents>`: Solver workflow datamodel APIs.
- :doc:`workflow <datamodel/workflow/workflow_contents>`: Solver workflow definitions and operations.
"""
