# Copilot Instructions for PyFluent

## Project Overview
PyFluent is a Python package that provides Pythonic access to Ansys Fluent, enabling seamless integration of Fluent's capabilities within the Python ecosystem. The codebase follows a service-oriented architecture with clear boundaries between core components.

## Key Architectural Patterns

### Session Management
- Sessions are the core abstraction, represented by different session types:
  - `Meshing`: Main meshing session with full capabilities
  - `PureMeshing`: Focused meshing session without solver features 
  - `Solver`: Core solver session
  - `SolverAero`: Specialized aero solver session
  - `SolverIcing`: Specialized icing solver session
- All session types inherit from `SessionBase` (`src/ansys/fluent/core/session_utilities.py`)
- Sessions are created through factory methods like `from_install()`, `from_container()`, `from_connection()`, `from_pim()`

### Workflow System
- Meshing operations use a task-based workflow system
- Key workflow types:
  - `WatertightWorkflow`: For watertight geometry processing
  - `FaultTolerantWorkflow`: For handling imperfect geometries
  - `TwoDimensionalWorkflow`: For 2D meshing operations
- Workflows contain ordered task sequences for operations like import, sizing, meshing
- Tasks follow a parent-child relationship pattern

### Service Interfaces 
- Services are organized around key capabilities:
  - `SchemeEval`: Core Fluent scheme evaluation
  - `DataModelService`: Data model access and manipulation
  - `FileTransferService`: File operations between client/server
  - `FieldDataService`: Field data access and manipulation

## Development Workflows

### Testing
- Tests are organized by component under `tests/`
- Key test fixtures available in `tests/conftest.py`
- Use appropriate test markers:
  - `@pytest.mark.fluent_version`: For version-specific tests
  - `@pytest.mark.codegen_required`: For tests needing code generation
  - `@pytest.mark.nightly`: For longer-running integration tests

### Example Scripts and Documentation
- Example scripts are located in `examples/00-fluent/`
- Each example script follows a standard structure:
  1. Copyright and MIT License header
  2. reStructuredText documentation section:
     - Title with reference anchor (e.g., `.. _species_transport:`)
     - Clear section headers (`===` for main title, `---` for sections, `~~~` for subsections)
     - Problem description and learning objectives
     - Mathematical equations using :math: directive
     - Reference links to other examples/docs
  3. Implementation sections:
     - Each section marked with `# %%` for Jupyter notebook compatibility
     - Clear section comments explaining each step
     - Working code examples demonstrating PyFluent usage
  4. Logical sections as per Fluent Setup, Solution, Results  
        Setup
        ├── General
        ├── Models
        ├── Materials
        ├── Motion Definitions
        ├── Cell Zone Conditions
        ├── Boundary Conditions
        ├── Mesh Interfaces
        ├── Boundary Interfaces
        ├── Auxiliary Geometry Definitions
        ├── Dynamic Mesh
        ├── Reference Values
        ├── Reference Frames
        ├── Named Expressions
        └── Curvilinear Coordinate System
        Solution
        ├── Methods
        ├── Controls
        ├── Report Definitions
        ├── Q Monitors
        ├── Cell Registers
        ├── Automatic Mesh Adaption
        ├── Initialization
        └── Calculation Activities
            └── Run Calculation
        Results
        ├── Surfaces
        ├── Graphics
        ├── Plots
        ├── Dashboard
        ├── Animations
        └── Reports
        Parameters & Customization
        Simulation Reports

### Common Development Tasks
- Creating new session: Use appropriate factory method from `SessionBase`
- Adding workflow tasks: 
  - Extend existing workflow classes
  - Follow task naming conventions (snake_case)
  - Implement required task interfaces
- Testing workflow changes:
  - Use `test_meshing_workflow.py` as reference
  - Validate task sequencing and dependencies

## Important File Locations
- Core session handling: `src/ansys/fluent/core/session.py`
- Workflow implementations: `src/ansys/fluent/core/session_base_meshing.py`
- Service interfaces: `src/ansys/fluent/core/services/`
- Test fixtures and utilities: `tests/conftest.py`, `tests/fluent_fixtures.py`
- Example scripts: `examples/00-fluent/*.py`

## Project Conventions
- Use snake_case for Python identifiers
- Follow session/service pattern for new components
- Document API changes in changelog.d/
- Maintain backward compatibility through proper deprecation
- Version-specific code should use `@fluent_version` decorators
- Example script documentation should follow reStructuredText format with consistent section hierarchy