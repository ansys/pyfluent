# PyFluent REST Transport

HTTP transport layer for PyFluent, connecting to Fluent's embedded SimBA server via REST instead of gRPC. Implements the same proxy interface expected by `flobject.get_root()`, enabling transparent protocol substitution.

## Installation

```bash
pip install ansys-fluent-core
```

## Architecture

```
src/ansys/fluent/core/rest/
├── __init__.py          # Public exports
├── client.py            # FluentRestClient — HTTP client
├── rest_session.py      # RestSolverSession — wires client to flobject
├── rest_launcher.py     # launch_fluent_rest() — convenience function
└── tests/
    ├── conftest.py          # Shared fixtures (auto-skip when server unreachable)
    ├── test_client_unit.py  # Unit tests (no server required)
    └── test_real_server.py  # Integration tests against live Fluent/SimBA server
```

## Components

### `FluentRestClient` (client.py)

HTTP client implementing the proxy interface required by `flobject`. Uses stdlib `urllib` — no external dependencies.

```python
from ansys.fluent.core.rest import FluentRestClient

client = FluentRestClient(
    "http://localhost:8000",
    auth_token="<token>",
    component="fluent_1",
)

# Read
val = client.get_var("setup/models/energy/enabled")  # True

# Write
client.set_var("setup/models/energy/enabled", False)

# Named objects
names = client.get_object_names("setup/boundary-conditions/velocity-inlet")
```

### `RestSolverSession` (rest_session.py)

Wires `FluentRestClient` into `flobject.get_root()` to build a full settings tree.

```python
from ansys.fluent.core.rest import launch_fluent_rest

session = launch_fluent_rest("localhost", 8000, auth_token="<token>")
session.settings.setup.models.energy.enabled()           # Read
session.settings.setup.models.energy.enabled.set_state(False)  # Write
```

## Running Tests

```bash
# Unit tests (no server required)
pytest src/ansys/fluent/core/rest/tests/test_client_unit.py -v

# Integration tests (requires FLUENT_REST_HOST env var)
FLUENT_REST_HOST=<ip> FLUENT_REST_PORT=<port> FLUENT_REST_TOKEN=<token> \
    pytest src/ansys/fluent/core/rest/tests/test_real_server.py -v -m real_server
```

## Known Limitations

- Meshing session (`fluent_meshing_1`) untested

## License

This project is licensed under the [MIT License](../../../../LICENSE).

## Contributing

Contributions are welcome. Please see [CONTRIBUTING.md](../../../../CONTRIBUTING.md) for guidelines.

## Code of Conduct

This project has adopted the [Contributor Covenant Code of Conduct](../../../../CODE_OF_CONDUCT.md).

## Security

To report a security vulnerability, please see [SECURITY.md](../../../../SECURITY.md).