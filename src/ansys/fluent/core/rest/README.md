# PyFluent REST Transport

HTTP transport layer for PyFluent, connecting to Fluent's embedded SimBA server via REST instead of gRPC. Implements the same proxy interface expected by `flobject.get_root()`, enabling transparent protocol substitution.

## Architecture

```
src/ansys/fluent/core/rest/
├── __init__.py          # Public exports
├── client.py            # FluentRestClient — HTTP client
├── rest_session.py      # RestSolverSession — wires client to flobject
├── rest_launcher.py     # launch_fluent_rest() — convenience function
└── tests/
    ├── conftest.py          # Shared fixtures (auto-skip when server unreachable)
    └── test_real_server.py  # 27 tests against live Fluent/SimBA server
```

## Components

### `FluentRestClient` (client.py)

HTTP client implementing the 14-method proxy interface required by `flobject`. Uses stdlib `urllib` — no external dependencies.

```python
from ansys.fluent.core.rest import FluentRestClient

client = FluentRestClient(
    "http://10.18.44.175:5000",
    auth_token="<token>",
    component="fluent_1",
)

# Read
val = client.get_var("setup/models/energy/enabled")  # True

# Write
client.set_var("setup/models/energy/enabled", False)

# Named objects
names = client.get_object_names("setup/boundary-conditions/velocity-inlet")
# ['hot-inlet', 'cold-inlet']
```

### `RestSolverSession` (rest_session.py)

Wires `FluentRestClient` into `flobject.get_root()` to build a full settings tree.

```python
from ansys.fluent.core.rest import launch_fluent_rest

session = launch_fluent_rest("10.18.44.175", 5000, auth_token="<token>")
session.settings.setup.models.energy.enabled()           # Read
session.settings.setup.models.energy.enabled.set_state(False)  # Write
```

## Running Tests

```bash
# All tests (auto-skip if server unreachable)
pytest src/ansys/fluent/core/rest/tests/ -v -m real_server
```

## Known Limitations

- No reconnect/retry logic
- No async support
- Meshing session (`fluent_meshing_1`) untested