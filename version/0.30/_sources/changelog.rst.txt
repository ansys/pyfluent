.. _ref_release_notes:

Release notes
#############

This document contains the release notes for the project.

.. vale off

.. towncrier release notes start

`0.30.5 <https://github.com/ansys/pyfluent/releases/tag/v0.30.5>`_ - April 29, 2025
===================================================================================

.. tab-set::


  .. tab-item:: Fixed

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - deprecated flag for flobject.py
          - `#3953 <https://github.com/ansys/pyfluent/pull/3953>`_


`0.30.4 <https://github.com/ansys/pyfluent/releases/tag/v0.30.4>`_ - April 24, 2025
===================================================================================

.. tab-set::


  .. tab-item:: Fixed

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Skip test_reduction_does_not_modify_case [skip tests]
          - `#3939 <https://github.com/ansys/pyfluent/pull/3939>`_

        * - Preprocess xml content before sending it to ElementTree parser
          - `#3951 <https://github.com/ansys/pyfluent/pull/3951>`_


`0.30.3 <https://github.com/ansys/pyfluent/releases/tag/v0.30.3>`_ - April 11, 2025
===================================================================================

.. tab-set::


  .. tab-item:: Documentation

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Update enhanced meshing workflow docs.
          - `#3874 <https://github.com/ansys/pyfluent/pull/3874>`_


`0.30.2 <https://github.com/ansys/pyfluent/releases/tag/v0.30.2>`_ - March 18, 2025
===================================================================================

.. tab-set::


  .. tab-item:: Fixed

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Use defusedxml
          - `#3841 <https://github.com/ansys/pyfluent/pull/3841>`_


`0.30.1 <https://github.com/ansys/pyfluent/releases/tag/v0.30.1>`_ - March 18, 2025
===================================================================================

.. tab-set::


  .. tab-item:: Added

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Remove lxml
          - `#3832 <https://github.com/ansys/pyfluent/pull/3832>`_


`0.30.dev4 <https://github.com/ansys/pyfluent/releases/tag/v0.30.dev4>`_ - March 11, 2025
=========================================================================================

.. tab-set::


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - update CHANGELOG for v0.30.dev4
          - `#3815 <https://github.com/ansys/pyfluent/pull/3815>`_


`0.30.dev4 <https://github.com/ansys/pyfluent/releases/tag/v0.30.dev4>`_ - March 10, 2025
=========================================================================================

.. tab-set::


  .. tab-item:: Added

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Utility to test viability of grpc connection
          - `#3766 <https://github.com/ansys/pyfluent/pull/3766>`_

        * - Use 'deprecated-version' flag for settings-api classes
          - `#3802 <https://github.com/ansys/pyfluent/pull/3802>`_


  .. tab-item:: Fixed

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Keep switch-to-meshing as hidden to fix Fluent journal replay.
          - `#3792 <https://github.com/ansys/pyfluent/pull/3792>`_

        * - Fix python_name issue in runtime python classes
          - `#3797 <https://github.com/ansys/pyfluent/pull/3797>`_


  .. tab-item:: Documentation

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - add solver to example usage command
          - `#3788 <https://github.com/ansys/pyfluent/pull/3788>`_

        * - Add doc for journal conversion [skip tests]
          - `#3791 <https://github.com/ansys/pyfluent/pull/3791>`_

        * - Fix built in settings doc [skip tests]
          - `#3807 <https://github.com/ansys/pyfluent/pull/3807>`_


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - update CHANGELOG for v0.30.dev3
          - `#3790 <https://github.com/ansys/pyfluent/pull/3790>`_

        * - Remove compare_flobject.py [skip tests]
          - `#3793 <https://github.com/ansys/pyfluent/pull/3793>`_

        * - Resolve dependency conflict
          - `#3800 <https://github.com/ansys/pyfluent/pull/3800>`_


`0.30.dev3 <https://github.com/ansys/pyfluent/releases/tag/v0.30.dev3>`_ - 2025-02-28
=====================================================================================

Fixed
^^^^^

- Better way to copy the current function argument values `#3751 <https://github.com/ansys/pyfluent/pull/3751>`_
- Minor issues in PyConsole. `#3770 <https://github.com/ansys/pyfluent/pull/3770>`_
- Invalid surface_ids check for field_data. `#3773 <https://github.com/ansys/pyfluent/pull/3773>`_
- Resolve MRO for _InputFile `#3774 <https://github.com/ansys/pyfluent/pull/3774>`_
- Support Group type argument during codegen `#3777 <https://github.com/ansys/pyfluent/pull/3777>`_
- update pyi files to match release `#3778 <https://github.com/ansys/pyfluent/pull/3778>`_
- Fix for nested alias `#3780 <https://github.com/ansys/pyfluent/pull/3780>`_
- input/output types for completer icons `#3781 <https://github.com/ansys/pyfluent/pull/3781>`_


Miscellaneous
^^^^^^^^^^^^^

- Remove vulnerabilities check `#3768 <https://github.com/ansys/pyfluent/pull/3768>`_
- Remove 'rename' from Enhanced Meshing Workflow top level. `#3776 <https://github.com/ansys/pyfluent/pull/3776>`_


Documentation
^^^^^^^^^^^^^

- Update local doc build instructions [skip tests] `#3756 <https://github.com/ansys/pyfluent/pull/3756>`_
- search engine optimization `#3761 <https://github.com/ansys/pyfluent/pull/3761>`_
- clean doc strs `#3762 <https://github.com/ansys/pyfluent/pull/3762>`_
- Update cheat sheet link [skip tests] `#3772 <https://github.com/ansys/pyfluent/pull/3772>`_
- Update meshing docs [skip-tests]. `#3779 <https://github.com/ansys/pyfluent/pull/3779>`_


Maintenance
^^^^^^^^^^^

- update CHANGELOG for v0.30.dev2 `#3759 <https://github.com/ansys/pyfluent/pull/3759>`_
- Reduce min grpcio-status version `#3764 <https://github.com/ansys/pyfluent/pull/3764>`_
- Specify PyFluent package version at a single location `#3767 <https://github.com/ansys/pyfluent/pull/3767>`_

`0.30.dev2 <https://github.com/ansys/pyfluent/releases/tag/v0.30.dev2>`_ - 2025-02-20
=====================================================================================

Miscellaneous
^^^^^^^^^^^^^

- Update PyLocalContainer to update _collection. `#3757 <https://github.com/ansys/pyfluent/pull/3757>`_


Maintenance
^^^^^^^^^^^

- update CHANGELOG for v0.30.dev1 `#3753 <https://github.com/ansys/pyfluent/pull/3753>`_

`0.30.dev1 <https://github.com/ansys/pyfluent/releases/tag/v0.30.dev1>`_ - 2025-02-19
=====================================================================================

Added
^^^^^

- Use new data-model api. `#3728 <https://github.com/ansys/pyfluent/pull/3728>`_


Fixed
^^^^^

- Enable app_utilities test for 25R2 `#3702 <https://github.com/ansys/pyfluent/pull/3702>`_
- Safely delete para env vars `#3745 <https://github.com/ansys/pyfluent/pull/3745>`_


Miscellaneous
^^^^^^^^^^^^^

- Update docstring and check file extension in Mesh class `#3727 <https://github.com/ansys/pyfluent/pull/3727>`_
- Rename warnings.py to fix examples workflow `#3734 <https://github.com/ansys/pyfluent/pull/3734>`_
- Revert the new dm api as default. `#3742 <https://github.com/ansys/pyfluent/pull/3742>`_
- __collection -> _collection for MutableMappings. `#3749 <https://github.com/ansys/pyfluent/pull/3749>`_


Documentation
^^^^^^^^^^^^^

- Update launch_fluent snippets [skip tests] `#3726 <https://github.com/ansys/pyfluent/pull/3726>`_
- Build nightly dev docs with Fluent 25.2 `#3736 <https://github.com/ansys/pyfluent/pull/3736>`_


Maintenance
^^^^^^^^^^^

- update CHANGELOG for v0.30.dev0 `#3724 <https://github.com/ansys/pyfluent/pull/3724>`_
- Add workflow for examples [skip tests] `#3730 <https://github.com/ansys/pyfluent/pull/3730>`_
- Fix examples workflow [skip tests] `#3732 <https://github.com/ansys/pyfluent/pull/3732>`_
- Fix labels [skip tests] `#3741 <https://github.com/ansys/pyfluent/pull/3741>`_

`0.30.dev0 <https://github.com/ansys/pyfluent/releases/tag/v0.30.dev0>`_ - 2025-02-07
=====================================================================================

Added
^^^^^

- remove application of mapped metadata `#3713 <https://github.com/ansys/pyfluent/pull/3713>`_


Fixed
^^^^^

- Update dependencies [skip tests] `#3710 <https://github.com/ansys/pyfluent/pull/3710>`_
- Update token and contributing doc [skip tests] `#3718 <https://github.com/ansys/pyfluent/pull/3718>`_


Miscellaneous
^^^^^^^^^^^^^

- some minor test improvements `#3711 <https://github.com/ansys/pyfluent/pull/3711>`_


Documentation
^^^^^^^^^^^^^

- Update built-in settings doc and fix doc warnings [skip-tests] `#3708 <https://github.com/ansys/pyfluent/pull/3708>`_
- Fix warnings in field data and reduction docs [skip tests] `#3712 <https://github.com/ansys/pyfluent/pull/3712>`_
- Update docs to connect Fluent launched on Linux [skip tests] `#3721 <https://github.com/ansys/pyfluent/pull/3721>`_


Maintenance
^^^^^^^^^^^

- Get hanging test names by parsing the GitHub logs [skip tests] `#3714 <https://github.com/ansys/pyfluent/pull/3714>`_
- update CHANGELOG for v0.29.0 `#3719 <https://github.com/ansys/pyfluent/pull/3719>`_

`0.29.0 <https://github.com/ansys/pyfluent/releases/tag/v0.29.0>`_ - 2025-02-06
===============================================================================

Added
^^^^^

- Implement automatic changelog `#3667 <https://github.com/ansys/pyfluent/pull/3667>`_
- Change working directory `#3691 <https://github.com/ansys/pyfluent/pull/3691>`_


Fixed
^^^^^

- Dimensionality correction in PIM launcher `#3673 <https://github.com/ansys/pyfluent/pull/3673>`_


Dependencies
^^^^^^^^^^^^

- Update local doc build instructions `#3671 <https://github.com/ansys/pyfluent/pull/3671>`_
- bump sphinx from 7.4.7 to 8.1.3 `#3696 <https://github.com/ansys/pyfluent/pull/3696>`_
- bump sphinx-autodoc-typehints from 2.3.0 to 3.0.1 `#3697 <https://github.com/ansys/pyfluent/pull/3697>`_
- bump the dependencies group across 1 directory with 4 updates `#3700 <https://github.com/ansys/pyfluent/pull/3700>`_
- Bump version to v0.29.0 `#3705 <https://github.com/ansys/pyfluent/pull/3705>`_


Miscellaneous
^^^^^^^^^^^^^

- Update type of parameter `#3681 <https://github.com/ansys/pyfluent/pull/3681>`_
- Use consistent file save format in the example scripts `#3682 <https://github.com/ansys/pyfluent/pull/3682>`_
- Raise an exception for Python journaling in 22R2 `#3684 <https://github.com/ansys/pyfluent/pull/3684>`_
- Update mesh file format `#3686 <https://github.com/ansys/pyfluent/pull/3686>`_
- Add verbose option for allapigen.py `#3690 <https://github.com/ansys/pyfluent/pull/3690>`_
- Update launchers `#3694 <https://github.com/ansys/pyfluent/pull/3694>`_


Documentation
^^^^^^^^^^^^^

- Document how to launch a PIM session `#3679 <https://github.com/ansys/pyfluent/pull/3679>`_
- Update file transfer docs for PIM [skip tests] `#3689 <https://github.com/ansys/pyfluent/pull/3689>`_
- Update launcher docs [skip tests] `#3698 <https://github.com/ansys/pyfluent/pull/3698>`_
- Fix examples gallery [skip tests] `#3699 <https://github.com/ansys/pyfluent/pull/3699>`_
- Hyperlink to key APIs [skip tests] `#3701 <https://github.com/ansys/pyfluent/pull/3701>`_
- Remove parameters section for settings commands [skip tests] `#3703 <https://github.com/ansys/pyfluent/pull/3703>`_


Maintenance
^^^^^^^^^^^

- Integrate ansys-tools-report `#3675 <https://github.com/ansys/pyfluent/pull/3675>`_
- Unpin twine version `#3683 <https://github.com/ansys/pyfluent/pull/3683>`_
- Update license file `#3687 <https://github.com/ansys/pyfluent/pull/3687>`_

.. vale on