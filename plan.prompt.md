## Plan: ADO Fluent Journal Tests

We will adapt the journal runner to use a standalone Fluent executable on the ADO runner, expand `--write-fluent-journals` to support a marker-based subset, and document the end-to-end flow in ADO_FLUENT_JOURNALS_PLAN.md. The core changes target the current Docker-based runner in .ci/fluent_test_runner.py and the journal generation path in tests/conftest.py. The goal is to keep the existing journal file structure under tests/fluent, preserve launcher args from fixtures, and make the ADO pipeline run only an explicit subset of tests. We will also note required env vars (license, Fluent install) and assumptions about how the ADO runner obtains the repo (clone vs package extra), with clone assumed for now.

**Steps**
1. Update the runner in .ci/fluent_test_runner.py to launch the standalone `fluent` executable via subprocess, replacing Docker-specific mounts while keeping current per-test YAML handling and error detection in `_run_single_test()`.
2. Extend journal generation in tests/conftest.py to filter tests by a dedicated marker (new or existing), while keeping existing skip and Fluent version gating logic intact.
3. Align Makefile and/or ADO pipeline usage so `pytest --write-fluent-journals` and the standalone runner are chained similarly to the current Make target, with ADO-specific env setup documented.
4. Add a planning/usage doc at ADO_FLUENT_JOURNALS_PLAN.md covering runner invocation, required env vars, marker usage, and how the repo is made available in ADO.

**Verification**
- Run `python -m pytest --write-fluent-journals -m <marker>` and confirm tests/fluent wrapper journals are created.
- Run `.ci/fluent_test_runner.py tests` on a machine with standalone Fluent in PATH and validate expected pass/fail output.
- If ADO pipeline exists, run the job that mirrors the above steps.

**Decisions**
- ADO Fluent invocation: standalone `fluent` executable in PATH.
- Journal test scope: marker-based subset.
