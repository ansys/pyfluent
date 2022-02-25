.. _contributing:

============
Contributing
============

Ansys welcomes all PyAnsys code contributions and wants you to
understand how to contribute. While we maintain PyAnsys libraries
and thoroughly review all submissions, we want to foster a community
that supports user questions and develops new features to make
our libraries powerful tools for all users. As such, we
encourage you to submit questions, report bugs, request new
features, contribute code, and start discussions.

This page provides general information about contributing code to a
PyAnsys respository. Contribution information specific to a particular
repository appears on the ``Contributing`` page in the respective
respository's documentation, including:

- Instructions for cloning the source repository from GitHub
- URL to the repository's ``Issues`` page

Creating Issues
---------------
You create issues to submit questions, report bugs, and request new
features. When you create an issue, ensure that you provide sufficient
context, such as application versions and reproduction steps. Also use
an issue label like "Documentation" to indicate the issue category.

PyAnsys developers and community members will respond to and hopefully
resolve your issue. Once an issue is resolved, you are encouraged to
close it yourself. Otherwise, after a period of inactivity, the PyAnsys
project support team will use discretion as to whether to close it.

Should it turn out that your issue is closed erroneously, perhaps because
a bug fix implemented to resolve your issue did not work, you can re-open
it with a comment that explains why you have done so. If you need to contact the
PyAnsys project support team directly, email `pyansys.support@ansys.com <pyansys.support@ansys.com>`_.

For convenience, here are URLs for ``Issues`` pages for
public Ansys repositories:

- `OpenAPI Common Issues <https://github.com/pyansys/openapi-common/issues>`_
- `PyAEDT Issues <https://github.com/pyansys/pyaedt/issues>`_
- `PyDPF-Core Issues <https://github.com/pyansys/pydpf-core/issues>`_
- `PyDPF-Post Issues <https://github.com/pyansys/pydpf-post/issues>`_
- `PyMAPDL Issues <https://github.com/pyansys/pymapdl/issues>`_
- `PyMAPDL-Reader Issues <https://github.com/pyansys/pymapdl-reader/issues>`_

Submitting Questions
~~~~~~~~~~~~~~~~~~~~
For general or technical questions about the code in a PyAnsys repository or
about its application or software usage, create issues on the ``Issues`` page
of the repository. This allows PyAnsys developers and community members with
the needed expertise to collectively address them. It also makes their responses
available to all users.

Reporting Bugs
~~~~~~~~~~~~~~
If you encounter a bug or your workflow crashes while using code in a PyAnsys
repository, create an issue on the repository's ``Issues`` page and tag it with
an appropriate label so that it can be promptly addressed. In describing the
issue, be as descriptive as possible so that the issue can be reproduced.
Whenever possible, provide a traceback, screenshots, and sample files that might
help the community to address the issue.

Requesting New Features
~~~~~~~~~~~~~~~~~~~~~~~
We encourage you to submit ideas for improving the code in a PyAnsys
repository. To suggest a new feature, create an issue on the repository's
``Issues`` page and tag this issue with the ``Feature Request`` label.
Use a descriptive title and provide ample background information to help the
community decide how the feature might be implemented. For example, if you
would like to see a reader added for a specific file format, in the issue,
provide a link to documentation for this file format and possibly some sample
files and screenshots. The community will then use the issue thread to discuss
the request and provide feedback on how the feature might best be implemented.

Contributing New Code
---------------------
When you are ready to start contributing code, see:

- :ref:`development_practices` for information on how PyAnsys development is
  conducted
- :ref:`best_practices` for information on how to style and format your
  code to adhere to PyAnsys standards

Starting Discussions
--------------------
For general questions about development practices, you should create discussions
rather than issues. Each PyAnsys repository has its own ``Discussions`` page.
For example, to ask a question about a PyFluent development practice, you would
create a discussion on the `PyFluent Discussions <https://github.com/pyansys/pyfluent/discussions>`_
page. It is possible for discussions to lead to the creation of issues.

.. note::
    Because the ``Discussions`` page is still a GitHub beta feature, usage
    may change in the future.
    
Cloning the Source Repository
-----------------------------
As mentioned earlier, specific instructions for cloning a source
repository from GitHub appear on the ``Contributing`` page in the
respective repository's documentation. In the following code for cloning and
installing the latest version of a PyAnsys repository, ``<pyansy-repository>``
is a placeholder for the name of the repository.

.. code::

    git clone https://github.com/pyansys/<pyansys-repository>
    cd <pyansys-repository>
    pip install -e .

For example, to clone and install the latest version of pyfluent
you would run the following:

.. code::

    git clone https://github.com/pyansys/pyfluent
    cd pyfluent
    pip install -e .

If you want to eventually push a contribution to a
PyAnsys repository, consider creating a `fork <https://docs.github.com/en/get-started/quickstart/fork-a-repo>`_
of the repository. For information on how to contribute through
GitHub, see :ref:`development_practices`, paying particular attention to :ref:`branch_naming`
when you are ready to create a pull request.

Licensing
---------
All contributed code will be licensed under the MIT License. For more information, see
:ref:`license_file`. The ``LICENSE`` file containing the MIT License must be included in
the root directory of a PyAnsys repository.

If you did not write the code that you are contributing yourself, it is your
responsibility to ensure that the existing license for this code is compatible and
included in the contributed files. You must obtain permission from the original
author to relicense the code.

