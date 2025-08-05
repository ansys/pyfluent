.. _ref_release_notes:

Release notes
#############

This document contains the release notes for the project.

.. vale off

.. towncrier release notes start

`0.34.1 <https://github.com/ansys/pyfluent/releases/tag/v0.34.1>`_ - August 04, 2025
====================================================================================

.. tab-set::


  .. tab-item:: Fixed

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Unavailable field data for some surfaces.
          - `#4345 <https://github.com/ansys/pyfluent/pull/4345>`_


`0.34.0 <https://github.com/ansys/pyfluent/releases/tag/v0.34.0>`_ - July 23, 2025
==================================================================================

.. tab-set::


  .. tab-item:: Added

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - beta features access
          - `#4153 <https://github.com/ansys/pyfluent/pull/4153>`_

        * - Set string settings with allowed values via string constants
          - `#4190 <https://github.com/ansys/pyfluent/pull/4190>`_

        * - Support passing objects to surfaces in field data.
          - `#4228 <https://github.com/ansys/pyfluent/pull/4228>`_

        * - add settings named objects
          - `#4232 <https://github.com/ansys/pyfluent/pull/4232>`_

        * - Get raw value for faces connectivity data.
          - `#4244 <https://github.com/ansys/pyfluent/pull/4244>`_

        * - Raise the attribute error with a correct message
          - `#4256 <https://github.com/ansys/pyfluent/pull/4256>`_


  .. tab-item:: Fixed

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - container timeout issue and new environment variables
          - `#4171 <https://github.com/ansys/pyfluent/pull/4171>`_

        * - parameters list() tests
          - `#4215 <https://github.com/ansys/pyfluent/pull/4215>`_

        * - interior zones are inactive in the latest Fluent image
          - `#4217 <https://github.com/ansys/pyfluent/pull/4217>`_

        * - Remove a runtime attribute query for argument-aliases
          - `#4241 <https://github.com/ansys/pyfluent/pull/4241>`_

        * - Remove redundant children from search results
          - `#4258 <https://github.com/ansys/pyfluent/pull/4258>`_

        * - Check localhost for grpc connection before other ips
          - `#4274 <https://github.com/ansys/pyfluent/pull/4274>`_

        * - Builtin commands should execute the command without any additional call.
          - `#4285 <https://github.com/ansys/pyfluent/pull/4285>`_


  .. tab-item:: Dependencies

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - bump the dependencies group with 5 updates
          - `#4230 <https://github.com/ansys/pyfluent/pull/4230>`_

        * - Bump ansys/actions from 9.0 to 10.0 in the actions group
          - `#4231 <https://github.com/ansys/pyfluent/pull/4231>`_


  .. tab-item:: Miscellaneous

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - get_completer_info implementation based on Python's inspect module
          - `#4214 <https://github.com/ansys/pyfluent/pull/4214>`_

        * - Transaction -> batch
          - `#4270 <https://github.com/ansys/pyfluent/pull/4270>`_

        * - Rename copy_docker_files.py
          - `#4278 <https://github.com/ansys/pyfluent/pull/4278>`_

        * - Update allowed_values interface for field_data.
          - `#4286 <https://github.com/ansys/pyfluent/pull/4286>`_

        * - Deprecate fieldinfo.
          - `#4287 <https://github.com/ansys/pyfluent/pull/4287>`_


  .. tab-item:: Documentation

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Update ``CONTRIBUTORS.md`` with the latest contributors
          - `#4221 <https://github.com/ansys/pyfluent/pull/4221>`_

        * - make homepage more appealing
          - `#4223 <https://github.com/ansys/pyfluent/pull/4223>`_

        * - Add podman usage examples and documentation improvements [skip tests]
          - `#4224 <https://github.com/ansys/pyfluent/pull/4224>`_

        * - Fix search box [skip tests]
          - `#4226 <https://github.com/ansys/pyfluent/pull/4226>`_

        * - Clarify usage of recent launch methods [skip tests]
          - `#4248 <https://github.com/ansys/pyfluent/pull/4248>`_

        * - Update user-facing beta feature docs [skip tests]
          - `#4254 <https://github.com/ansys/pyfluent/pull/4254>`_

        * - Update outdated field_info docs [skip tests]
          - `#4257 <https://github.com/ansys/pyfluent/pull/4257>`_

        * - Update search results [skip tests]
          - `#4266 <https://github.com/ansys/pyfluent/pull/4266>`_

        * - Improve meshing field help text [skip tests]
          - `#4289 <https://github.com/ansys/pyfluent/pull/4289>`_

        * - Update ``contributors.md`` with the latest contributors
          - `#4294 <https://github.com/ansys/pyfluent/pull/4294>`_

        * - Update to use objects.
          - `#4295 <https://github.com/ansys/pyfluent/pull/4295>`_


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - static class attributes
          - `#4174 <https://github.com/ansys/pyfluent/pull/4174>`_

        * - update CHANGELOG for v0.33.0
          - `#4206 <https://github.com/ansys/pyfluent/pull/4206>`_

        * - update CHANGELOG for v0.34.dev0
          - `#4209 <https://github.com/ansys/pyfluent/pull/4209>`_

        * - Add SECURITY.md file [skip tests]
          - `#4227 <https://github.com/ansys/pyfluent/pull/4227>`_

        * - Enable beta features
          - `#4235 <https://github.com/ansys/pyfluent/pull/4235>`_

        * - Add a new warning category for fluent development version usage.
          - `#4255 <https://github.com/ansys/pyfluent/pull/4255>`_

        * - Update 26.1 image tag to v26.1.latest
          - `#4281 <https://github.com/ansys/pyfluent/pull/4281>`_

        * - Use the new image name for version >=26.1
          - `#4291 <https://github.com/ansys/pyfluent/pull/4291>`_

        * - Use units release >= 0.7.0
          - `#4296 <https://github.com/ansys/pyfluent/pull/4296>`_


  .. tab-item:: Test

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Updates to optislang integration tests
          - `#4269 <https://github.com/ansys/pyfluent/pull/4269>`_


`0.34.dev0 <https://github.com/ansys/pyfluent/releases/tag/v0.34.dev0>`_ - June 24, 2025
========================================================================================

.. tab-set::


  .. tab-item:: Added

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Make graphics driver null except in gui / hidden_gui modes
          - `#4149 <https://github.com/ansys/pyfluent/pull/4149>`_

        * - Add builtin commands
          - `#4164 <https://github.com/ansys/pyfluent/pull/4164>`_

        * - Add helper methods to specify a set of Fluent versions
          - `#4172 <https://github.com/ansys/pyfluent/pull/4172>`_


  .. tab-item:: Fixed

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Backward compatibility of health_check
          - `#4146 <https://github.com/ansys/pyfluent/pull/4146>`_

        * - removing invalid pyproject.toml entry
          - `#4148 <https://github.com/ansys/pyfluent/pull/4148>`_

        * - container launch issues
          - `#4163 <https://github.com/ansys/pyfluent/pull/4163>`_

        * - Fix an issue with API code cache restore
          - `#4167 <https://github.com/ansys/pyfluent/pull/4167>`_

        * - Fix an issue in returning parameter units
          - `#4177 <https://github.com/ansys/pyfluent/pull/4177>`_

        * - Relax error message comparison in test
          - `#4180 <https://github.com/ansys/pyfluent/pull/4180>`_

        * - Fix an issue when settings child is also an alias.
          - `#4188 <https://github.com/ansys/pyfluent/pull/4188>`_

        * - nightly optislang integration tests
          - `#4189 <https://github.com/ansys/pyfluent/pull/4189>`_

        * - No warning for None values and remove a doc dependency
          - `#4197 <https://github.com/ansys/pyfluent/pull/4197>`_


  .. tab-item:: Miscellaneous

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Semantic search enhancements
          - `#4098 <https://github.com/ansys/pyfluent/pull/4098>`_

        * - Move Fields class to module level.
          - `#4102 <https://github.com/ansys/pyfluent/pull/4102>`_

        * - Rename meshing_rule_file_names [skip tests]
          - `#4112 <https://github.com/ansys/pyfluent/pull/4112>`_

        * - Run each test in its own directory
          - `#4115 <https://github.com/ansys/pyfluent/pull/4115>`_

        * - Update app utilities dict interface
          - `#4116 <https://github.com/ansys/pyfluent/pull/4116>`_


  .. tab-item:: Documentation

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Update ``CONTRIBUTORS.md`` with the latest contributors
          - `#4086 <https://github.com/ansys/pyfluent/pull/4086>`_, `#4168 <https://github.com/ansys/pyfluent/pull/4168>`_

        * - Add newline after block statements in examples code for copy-pasting to Python interpreter [skip tests]
          - `#4090 <https://github.com/ansys/pyfluent/pull/4090>`_

        * - minor changes.
          - `#4109 <https://github.com/ansys/pyfluent/pull/4109>`_

        * - Update solver and meshing in examples [skip tests]
          - `#4110 <https://github.com/ansys/pyfluent/pull/4110>`_

        * - Update event docs. [skip tests]
          - `#4118 <https://github.com/ansys/pyfluent/pull/4118>`_

        * - Address inconsistencies in naming svars.
          - `#4119 <https://github.com/ansys/pyfluent/pull/4119>`_

        * - Correct a typo [skip tests]
          - `#4123 <https://github.com/ansys/pyfluent/pull/4123>`_

        * - Rename solver and meshing in user docs [skip tests]
          - `#4142 <https://github.com/ansys/pyfluent/pull/4142>`_

        * - Add section for jupyterlab code-completion in FAQ [skip-tests]
          - `#4196 <https://github.com/ansys/pyfluent/pull/4196>`_


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - update CHANGELOG for v0.32.dev1
          - `#4080 <https://github.com/ansys/pyfluent/pull/4080>`_

        * - update CHANGELOG for v0.32.0
          - `#4084 <https://github.com/ansys/pyfluent/pull/4084>`_

        * - update CHANGELOG for v0.33.dev0
          - `#4085 <https://github.com/ansys/pyfluent/pull/4085>`_

        * - Remove post_objects from core repo.
          - `#4089 <https://github.com/ansys/pyfluent/pull/4089>`_

        * - skip test_search
          - `#4104 <https://github.com/ansys/pyfluent/pull/4104>`_

        * - Update examples wrt viz
          - `#4106 <https://github.com/ansys/pyfluent/pull/4106>`_

        * - Update the warning throw from '_get_create_instance_args'
          - `#4120 <https://github.com/ansys/pyfluent/pull/4120>`_

        * - Expose field data request objects from core module.
          - `#4138 <https://github.com/ansys/pyfluent/pull/4138>`_

        * - Add warning while using Fluent develop branch.
          - `#4140 <https://github.com/ansys/pyfluent/pull/4140>`_

        * - Fix examples workflow [skip tests]
          - `#4141 <https://github.com/ansys/pyfluent/pull/4141>`_

        * - Set permissions for CI [skip tests]
          - `#4144 <https://github.com/ansys/pyfluent/pull/4144>`_

        * - Resolve unpinned tag security warnings [skip tests]
          - `#4152 <https://github.com/ansys/pyfluent/pull/4152>`_

        * - Fix github caching for codegen
          - `#4158 <https://github.com/ansys/pyfluent/pull/4158>`_

        * - Perform deprecation call from generated data.
          - `#4162 <https://github.com/ansys/pyfluent/pull/4162>`_

        * - update CHANGELOG for v0.32.2
          - `#4173 <https://github.com/ansys/pyfluent/pull/4173>`_

        * - Disable codacy [skip tests]
          - `#4176 <https://github.com/ansys/pyfluent/pull/4176>`_

        * - Delete remove docker image step [skip tests]
          - `#4200 <https://github.com/ansys/pyfluent/pull/4200>`_

        * - Fix nightly dev test run workflow
          - `#4201 <https://github.com/ansys/pyfluent/pull/4201>`_

        * - Fix nightly dev docs [skip tests]
          - `#4203 <https://github.com/ansys/pyfluent/pull/4203>`_


`0.32.2 <https://github.com/ansys/pyfluent/releases/tag/v0.32.2>`_ - June 17, 2025
==================================================================================

.. tab-set::


  .. tab-item:: Fixed

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Fix performance issues while settings boundary condition
          - `#4166 <https://github.com/ansys/pyfluent/pull/4166>`_


`0.32.0 <https://github.com/ansys/pyfluent/releases/tag/v0.32.0>`_ - May 29, 2025
=================================================================================

.. tab-set::


  .. tab-item:: Added

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Remote file transfer strategy
          - `#4062 <https://github.com/ansys/pyfluent/pull/4062>`_

        * - Context managers
          - `#4073 <https://github.com/ansys/pyfluent/pull/4073>`_


  .. tab-item:: Miscellaneous

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - scheme_eval.
          - `#4042 <https://github.com/ansys/pyfluent/pull/4042>`_

        * - health_check
          - `#4048 <https://github.com/ansys/pyfluent/pull/4048>`_

        * - pyfluent_enums -> launch_options
          - `#4054 <https://github.com/ansys/pyfluent/pull/4054>`_


  .. tab-item:: Documentation

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Update ``CONTRIBUTORS.md`` with the latest contributors
          - `#4030 <https://github.com/ansys/pyfluent/pull/4030>`_

        * - Update automotive brake thermal analysis [skip tests]
          - `#4049 <https://github.com/ansys/pyfluent/pull/4049>`_


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - update CHANGELOG for v0.31.0
          - `#4044 <https://github.com/ansys/pyfluent/pull/4044>`_

        * - update CHANGELOG for v0.32.dev0
          - `#4047 <https://github.com/ansys/pyfluent/pull/4047>`_

        * - skip tests for nightly tests to pass [skip tests]
          - `#4056 <https://github.com/ansys/pyfluent/pull/4056>`_

        * - clean up units business
          - `#4057 <https://github.com/ansys/pyfluent/pull/4057>`_

        * - Update 2d Meshing test.
          - `#4072 <https://github.com/ansys/pyfluent/pull/4072>`_


  .. tab-item:: Test

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Activate 2d meshing tests for 25 R1
          - `#3281 <https://github.com/ansys/pyfluent/pull/3281>`_


`0.31.0 <https://github.com/ansys/pyfluent/releases/tag/v0.31.0>`_ - May 21, 2025

`0.32.dev0 <https://github.com/ansys/pyfluent/releases/tag/v0.32.dev0>`_ - May 22, 2025

.. tab-set::


  .. tab-item:: Added

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Docker compose support
          - `#3872 <https://github.com/ansys/pyfluent/pull/3872>`_

        * - Update launch function API design
          - `#3919 <https://github.com/ansys/pyfluent/pull/3919>`_

        * - physical quantities baseline code
          - `#3988 <https://github.com/ansys/pyfluent/pull/3988>`_

        * - physical quantities 2
          - `#4015 <https://github.com/ansys/pyfluent/pull/4015>`_

        * - Check if fluent exe exists in AWP_ROOT path while determining the Fluent version to launch
          - `#4024 <https://github.com/ansys/pyfluent/pull/4024>`_

        * - Extend use of VariableCatalog
          - `#4033 <https://github.com/ansys/pyfluent/pull/4033>`_


  .. tab-item:: Fixed

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - manual stage for add-license-header [skip tests]
          - `#3944 <https://github.com/ansys/pyfluent/pull/3944>`_

        * - Handle exceptions from third-party libraries during docker call
          - `#3994 <https://github.com/ansys/pyfluent/pull/3994>`_

        * - Fix server-side error in builtin settings objects
          - `#3996 <https://github.com/ansys/pyfluent/pull/3996>`_

        * - Improve subprocess.Popen handling
          - `#4003 <https://github.com/ansys/pyfluent/pull/4003>`_

        * - Decorator warning message
          - `#4021 <https://github.com/ansys/pyfluent/pull/4021>`_


  .. tab-item:: Documentation

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Update meshing doc after switching to solver
          - `#3962 <https://github.com/ansys/pyfluent/pull/3962>`_

        * - Update ``CONTRIBUTORS.md`` with the latest contributors
          - `#3964 <https://github.com/ansys/pyfluent/pull/3964>`_, `#4013 <https://github.com/ansys/pyfluent/pull/4013>`_

        * - Adding Mixing Tank Example [skip tests]
          - `#3966 <https://github.com/ansys/pyfluent/pull/3966>`_

        * - Add Docker and Podman compose docs [skip tests]
          - `#4001 <https://github.com/ansys/pyfluent/pull/4001>`_

        * - Show deprecated APIs
          - `#4007 <https://github.com/ansys/pyfluent/pull/4007>`_

        * - use variable catalog
          - `#4025 <https://github.com/ansys/pyfluent/pull/4025>`_


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - update CHANGELOG for v0.31.dev1
          - `#3974 <https://github.com/ansys/pyfluent/pull/3974>`_

        * - Fix code style [skip tests]
          - `#3977 <https://github.com/ansys/pyfluent/pull/3977>`_, `#3978 <https://github.com/ansys/pyfluent/pull/3978>`_

        * - update CHANGELOG for v0.30.5
          - `#3981 <https://github.com/ansys/pyfluent/pull/3981>`_

        * - Update error message for attribute errors from Solver.
          - `#3982 <https://github.com/ansys/pyfluent/pull/3982>`_

        * - Search for undocumented fields in codebase
          - `#3984 <https://github.com/ansys/pyfluent/pull/3984>`_

        * - v0.30.5 changelog [skip tests]
          - `#3986 <https://github.com/ansys/pyfluent/pull/3986>`_

        * - Add a file describing the columns of field_level_help.csv
          - `#3995 <https://github.com/ansys/pyfluent/pull/3995>`_

        * - Refactor settings_root
          - `#4016 <https://github.com/ansys/pyfluent/pull/4016>`_

        * - Minor improvements.
          - `#4018 <https://github.com/ansys/pyfluent/pull/4018>`_

        * - Fix datatype in field_level_help.csv [skip tests]
          - `#4029 <https://github.com/ansys/pyfluent/pull/4029>`_

  .. tab-item:: Test

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Update test w.r.t. recent exposure flag changes in data-model.
          - `#4031 <https://github.com/ansys/pyfluent/pull/4031>`_


`0.31.dev1 <https://github.com/ansys/pyfluent/releases/tag/v0.31.dev1>`_ - April 29, 2025
=========================================================================================

`0.30.5 <https://github.com/ansys/pyfluent/releases/tag/v0.30.5>`_ - April 29, 2025
===================================================================================

.. tab-set::


  .. tab-item:: Added

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Enhanced error handling in Settings API
          - `#3825 <https://github.com/ansys/pyfluent/pull/3825>`_

        * - Object based field data access (unifying the interface).
          - `#3827 <https://github.com/ansys/pyfluent/pull/3827>`_

        * - Support PRE_POST mode
          - `#3853 <https://github.com/ansys/pyfluent/pull/3853>`_

        * - codegen for datamodel command arguments
          - `#3865 <https://github.com/ansys/pyfluent/pull/3865>`_

        * - Register multiple event types in register_callback()
          - `#3924 <https://github.com/ansys/pyfluent/pull/3924>`_

        * - Support unsuppressing prompts in scheme_eval
          - `#3963 <https://github.com/ansys/pyfluent/pull/3963>`_


  .. tab-item:: Fixed

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - deprecated flag for flobject.py
          - `#3953 <https://github.com/ansys/pyfluent/pull/3953>`_

        * - Make version attr private to avoid conflict with child setting with same name.
          - `#3830 <https://github.com/ansys/pyfluent/pull/3830>`_

        * - Get dependency version [skip tests]
          - `#3842 <https://github.com/ansys/pyfluent/pull/3842>`_

        * - Updates for linux support & visualization minor changes
          - `#3843 <https://github.com/ansys/pyfluent/pull/3843>`_

        * - field-level-help at runtime for datamodel_se objects
          - `#3859 <https://github.com/ansys/pyfluent/pull/3859>`_

        * - Avoid file name as native Python package
          - `#3861 <https://github.com/ansys/pyfluent/pull/3861>`_

        * - Minor issue in task.add_child_and_update
          - `#3875 <https://github.com/ansys/pyfluent/pull/3875>`_

        * - Fix missing field-level help at various levels
          - `#3879 <https://github.com/ansys/pyfluent/pull/3879>`_

        * - Remove license header hook [skip tests]
          - `#3925 <https://github.com/ansys/pyfluent/pull/3925>`_

        * - Fix for the exit scenario while launching in lightweight mode
          - `#3935 <https://github.com/ansys/pyfluent/pull/3935>`_

        * - Create directory within the current user's home
          - `#3937 <https://github.com/ansys/pyfluent/pull/3937>`_

        * - Update mount_source for container FTS [skip tests]
          - `#3941 <https://github.com/ansys/pyfluent/pull/3941>`_

        * - Nightly meshing tests.
          - `#3943 <https://github.com/ansys/pyfluent/pull/3943>`_

        * - Nightly dev doc CI run.
          - `#3945 <https://github.com/ansys/pyfluent/pull/3945>`_

        * - Fix deprecated behaviour
          - `#3948 <https://github.com/ansys/pyfluent/pull/3948>`_

        * - Raise AttributeError for non-existing meshing objects after switch_to solver.
          - `#3949 <https://github.com/ansys/pyfluent/pull/3949>`_

        * - deprecated flag for flobject.py
          - `#3953 <https://github.com/ansys/pyfluent/pull/3953>`_

        * - Update reduction test and re-implement it.
          - `#3958 <https://github.com/ansys/pyfluent/pull/3958>`_

        * - Enable Scheme mode when py=False is set
          - `#3961 <https://github.com/ansys/pyfluent/pull/3961>`_


  .. tab-item:: Dependencies

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Update ansys-units version
          - `#3826 <https://github.com/ansys/pyfluent/pull/3826>`_


  .. tab-item:: Miscellaneous

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - field data transaction
          - `#3819 <https://github.com/ansys/pyfluent/pull/3819>`_

        * - internal interface of field data
          - `#3858 <https://github.com/ansys/pyfluent/pull/3858>`_

        * - Update test_remote_grpc_fts_container
          - `#3915 <https://github.com/ansys/pyfluent/pull/3915>`_

        * - Add timeout_loop for health check
          - `#3917 <https://github.com/ansys/pyfluent/pull/3917>`_

        * - Update enhanced meshing wf tests w.r.t. docs.
          - `#3930 <https://github.com/ansys/pyfluent/pull/3930>`_

        * - Update field data output.
          - `#3934 <https://github.com/ansys/pyfluent/pull/3934>`_


  .. tab-item:: Documentation

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Update ``CONTRIBUTORS.md`` with the latest contributors
          - `#3902 <https://github.com/ansys/pyfluent/pull/3902>`_

        * - Direct users to use virtual env if Ansys Python is used.
          - `#3904 <https://github.com/ansys/pyfluent/pull/3904>`_

        * - Update file transfer docs
          - `#3916 <https://github.com/ansys/pyfluent/pull/3916>`_

        * - Added an end-to-end example focused on Turbomachinery [skip tests]
          - `#3947 <https://github.com/ansys/pyfluent/pull/3947>`_


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - update CHANGELOG for v0.31.dev0
          - `#3821 <https://github.com/ansys/pyfluent/pull/3821>`_

        * - Replace FLUENT_PRECISION_MODE global with runtime check
          - `#3829 <https://github.com/ansys/pyfluent/pull/3829>`_

        * - update CHANGELOG for v0.30.1
          - `#3838 <https://github.com/ansys/pyfluent/pull/3838>`_

        * - Do not sync labels [skip tests]
          - `#3840 <https://github.com/ansys/pyfluent/pull/3840>`_

        * - update CHANGELOG for v0.30.2
          - `#3849 <https://github.com/ansys/pyfluent/pull/3849>`_

        * - Reduce timeout for unittests
          - `#3851 <https://github.com/ansys/pyfluent/pull/3851>`_

        * - Update nightly doc build workflow [skip tests]
          - `#3854 <https://github.com/ansys/pyfluent/pull/3854>`_

        * - Workflow to use latest Fluent image in CI [skip tests]
          - `#3867 <https://github.com/ansys/pyfluent/pull/3867>`_

        * - Add script to write field-level help info from server [skip tests]
          - `#3921 <https://github.com/ansys/pyfluent/pull/3921>`_

        * - update CHANGELOG for v0.30.3
          - `#3928 <https://github.com/ansys/pyfluent/pull/3928>`_

        * - update CHANGELOG for v0.30.4
          - `#3955 <https://github.com/ansys/pyfluent/pull/3955>`_

        * - Update 2d meshing test and doc.
          - `#3965 <https://github.com/ansys/pyfluent/pull/3965>`_


  .. tab-item:: Test

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Test that Fluent error message is recovered in PyFluent
          - `#3824 <https://github.com/ansys/pyfluent/pull/3824>`_

        * - Update test.
          - `#3881 <https://github.com/ansys/pyfluent/pull/3881>`_

        * - Enable the tests which are now passing in nightly
          - `#3893 <https://github.com/ansys/pyfluent/pull/3893>`_


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