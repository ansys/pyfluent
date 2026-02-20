# ADO Fluent Journal Tests

Plan and usage for generating and running Fluent Python journal tests in Azure DevOps using a standalone Fluent executable.

## Goals
- Generate Fluent journal wrappers from PyFluent pytest suites (no Docker required).
- Run journals with the standalone `fluent` executable on ADO runners.
- Keep generated structure under `tests/fluent/**` consistent with pytest fixtures.

## Prerequisites
- Fluent installed on the ADO runner; `fluent` available on `PATH` (or override with `--fluent-cmd`).
- License: `ANSYSLMD_LICENSE_FILE` set in the environment.
- Python deps: `pip install -r requirements/requirements_build.txt` and `pip install ansys-fluent-core[reader]` (or `[reader,tests]` if tests require extras).

## Generate journals
- From repo root: `python -m pytest --write-fluent-journals`
- Behavior:
  - Writes per-test wrappers to `tests/fluent/<module>/<test>/test.py` with `test.yaml` containing `launcher_args` from fixtures.
  - Skips tests marked `@pytest.mark.skip` or incompatible `fluent_version` (only `latest` or current dev supported).
  - Includes all tests that use a fixture exposing `fluent_launcher_args` (see `tests/fluent_fixtures.py`).

## Run journals with standalone Fluent
- From repo root: `python .ci/fluent_test_runner.py tests`
- Options: `--fluent-cmd <path>` to override the executable name.
- Honors `MAX_WORKERS_FLUENT_TESTS` for parallelism (default 4; set to 1 if needed).
- Adds copied test tree to `PYTHONPATH`; fails fast if `ANSYSLMD_LICENSE_FILE` is missing; raises on Fluent stderr `Error:` lines or non-zero exit.

## ADO pipeline sketch
- Steps:
  1) Checkout repo (or install package extra `ansys-fluent-core[tests]` if cloning is not used).
  2) Install deps (`requirements_build` and `ansys-fluent-core[reader]`).
  3) `python -m pytest --write-fluent-journals`
  4) `python .ci/fluent_test_runner.py tests`
- Env:
  - `ANSYSLMD_LICENSE_FILE`: license server
  - `MAX_WORKERS_FLUENT_TESTS`: optional parallelism control
  - `PATH` must contain `fluent` if not using `--fluent-cmd`

## Fixture coverage
- `tests/fluent_fixtures.py` mirrors all Fluent-launching fixtures and relevant helpers from `tests/**`, including meshing/solver variants, `_wo_exit`, `_t4`, unitless/static mixer, mixing elbow case/data, disk/periodic, plus helper fixtures (`reset_examples_path`, `slurm_future`, `disable_slurm_in_current_machine`, `warning_record`, `use_runtime_python_classes`).

## Notes
- Journal generation now has no marker filter; all compatible Fluent tests are emitted.
- Python journaling is unsupported on Fluent 22.2; tests are gated by `fluent_version` markers accordingly.
