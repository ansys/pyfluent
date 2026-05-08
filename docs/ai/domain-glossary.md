# Domain Glossary

Short definitions for terms commonly used in this repository.

- Fluent
  - Ansys CFD solver platform used by PyFluent.
- PyFluent
  - Python client library (ansys-fluent-core) for interacting with Fluent.
- Session
  - Active connection/context for driving Fluent from Python.
- Solver mode
  - Fluent mode focused on solving configured CFD cases.
- Meshing mode
  - Fluent mode focused on mesh creation and preparation.
- TUI
  - Text User Interface command tree exposed by Fluent.
- Datamodel
  - Structured object model/API representation of Fluent settings and state.
- Settings API
  - Pythonic access layer for Fluent solver settings.
- Generated API
  - Source artifacts produced by generation scripts from upstream definitions.
- Codegen
  - Process/scripts that generate API modules (for example codegen/allapigen.py).
- Fluent version marker
  - Test/runtime gating tied to specific Fluent versions.
- Standalone tests
  - Tests marked to run outside containerized or special CI environments.
