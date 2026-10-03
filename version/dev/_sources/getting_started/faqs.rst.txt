.. _faqs:

Frequently asked questions
==========================

How does PyFluent compare to Fluent user defined functions?
-------------------------------------------------------------
PyFluent automates workflows rather than modifying solver behavior. UDFs, written in C,
remain important for customizing solver behavior. You cannot write UDFs in Python, but you
can use PyFluent's `solver settings objects <https://fluent.docs.pyansys.com/version/dev/user_guide/solver_settings/solver_settings_contents.html>`_ to compile and load them.


How do you learn how to use PyFluent?
-------------------------------------

- Review the examples in the documentation, working first through those provided
  in the :ref:`ref_example_gallery`, then, through those provided in the
  **Examples** sections in the `PyFluent-Visualization
  <https://visualization.fluent.docs.pyansys.com/>`_ guide.
- Record a journal of your actions in Fluent and review the corresponding Python
  script. For comprehensive guidance on journaling, see
  :ref:`ref_journal`.
- Write scripts, using:

  - Autocompletion features in your Python environment or IDE to show available options
    for any given command. For example, in `JupyterLab <https://jupyter.org/>`_, press the
    tab key.


How to set up JupyterLab to get a better code completion for the API code in PyFluent?
--------------------------------------------------------------------------------------
By default, JupyterLab ignores the static typing information provided by PyFluent
and relies on dynamic lookup of the API for code completion. As the dynamic lookup
generally involves gRPC calls to the Fluent server, it can be slow and often times out.
To get a faster code completion experience based on the static typing information
provided by PyFluent, you can install the JupyterLab extension
`jupyterlab-lsp <https://jupyterlab-lsp.readthedocs.io/en/latest/>`_
along with a Python language server like
`python-lsp-server <https://github.com/python-lsp/python-lsp-server>`_
within your JupyterLab environment .


For discussions about developer tools, engineering simulation, and physics for
Ansys software, visit the `Ansys Developer portal
<https://developer.ansys.com/>`_. The `Ansys Discuss
<https://discuss.ansys.com/>`_ page is where users, partners, students, and
Ansys subject matter experts connect, share ideas, discuss the latest
technologies, and ask questions to quickly obtain help and guidance. On this
page, you can filter discussions by category or apply the **Fluent** tag to view
only Fluent-related discussions.
