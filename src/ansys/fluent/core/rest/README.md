# PyFluent REST Transport

HTTP/REST transport layer for PyFluent — connects to the Fluent embedded SimBA web server
via HTTP instead of gRPC. Implements the same `flobject` proxy interface so the full solver
settings tree works transparently over REST without any changes to `flobject`.

> **Status:** Experimental — Issue [#4959](https://github.com/ansys/pyfluent/issues/4959)

---

## Requirements

| Requirement | Details |
|-------------|---------|
| Fluent 2026 R1 (v261) or later | Must support `-ws` web server launch flag |
| `FLUENT_WEBSERVER_TOKEN` env var | Shared secret — any string |
| No extra Python packages | Pure stdlib: `urllib`, `socket`, `hashlib`, `subprocess` |

---

## File Structure

```
src/ansys/fluent/core/rest/
├── __init__.py              # Public exports: launch_webserver, connect_to_webserver
├── client.py                # FluentRestClient — pure stdlib HTTP client
├── rest_session.py          # RestSolverSession — wires client into flobject
├── rest_launcher.py         # launch_webserver(), connect_to_webserver()
├── xyz.py                   # Step-by-step developer smoke-test script
└── tests/
    ├── conftest.py              # Shared fixtures (auto-skip when server unreachable)
    ├── test_client_unit.py      # Unit tests for FluentRestClient (no server needed)
    └── test_launcher_unit.py    # Unit tests for launcher + session (no server needed)
```

---

## Architecture

```
launch_webserver(start_timeout=60)
       │
       ├─ subprocess.Popen(fluent.exe -ws -ws-port=PORT)
       │
       ├─ _wait_for_server(port, timeout=start_timeout)
       │     ├─ Phase 1: TCP socket.create_connection  ← port open?
       │     └─ Phase 2: GET /api/connection/run_mode  ← solver ready?
       │                 (400 = not ready yet, 401 = ready, 2xx = ready)
       │                 (_wait_for_server defaults to 120 when called directly)
       │
       └─ RestSolverSession(base_url, auth_token)
             │
             ├─ FluentRestClient          ← REST proxy (substitutes gRPC proxy)
             │     └─ SHA-256 Bearer auth on every request
             │
             └─ flobject.get_root()       ← UNCHANGED
                   └─ session.settings.setup.models.energy.enabled()
```

---

## Quick Start

### Step 1 — Set the auth token

```python
import os
os.environ["FLUENT_WEBSERVER_TOKEN"] = "my-secret-token"
```

Or in PowerShell before running:
```powershell
$Env:FLUENT_WEBSERVER_TOKEN = "my-secret-token"
```

### Step 2 — Launch Fluent web server

```python
from ansys.fluent.core.rest import launch_webserver

session = launch_webserver(product_version="261")
# Waits until TCP port is open AND solver is ready — no race conditions
print("Connected:", session.ip, session.port)
```

### Step 3 — Or connect to an already-running server

```python
from ansys.fluent.core.rest import connect_to_webserver

session = connect_to_webserver(
    ip="127.0.0.1",
    port=50075,               # port Fluent is listening on
    auth_token="my-secret-token",
)
```

### Step 4 — Create a REST client directly

```python
from ansys.fluent.core.rest.client import FluentRestClient

client = FluentRestClient(
    f"http://127.0.0.1:{session.port}",
    auth_token=os.environ["FLUENT_WEBSERVER_TOKEN"],
    component="fluent_1",
)
```

---

## Common Operations

### Read a case file

```python
# Auto-retries on "400 Fluent not running" for up to 120 s
client.execute_cmd("file", "read-case", file_name=r"D:\cases\elbow.cas.h5")

# Case + data together
client.execute_cmd("file", "read-case-data", file_name=r"D:\cases\elbow.cas.h5")

# Data only
client.execute_cmd("file", "read-data", file_name=r"D:\cases\elbow.dat.h5")
```

### Read settings

```python
print(client.get_var("setup/models/energy/enabled"))   # True / False
print(client.get_var("setup/models/viscous/model"))    # "k-epsilon" etc.
print(client.get_var("setup/general/solver/type"))     # "pressure-based" etc.
```

### Modify settings

```python
client.set_var("setup/models/energy/enabled", True)
client.set_var("setup/models/viscous/model", "k-epsilon")

# Confirm the change
print(client.get_var("setup/models/energy/enabled"))   # True
print(client.get_var("setup/models/viscous/model"))    # "k-epsilon"
```

### List named objects

```python
inlets  = client.get_object_names("setup/boundary-conditions/velocity-inlet")
outlets = client.get_object_names("setup/boundary-conditions/pressure-outlet")
walls   = client.get_object_names("setup/boundary-conditions/wall")
print("Inlets :", inlets)
print("Outlets:", outlets)
print("Walls  :", walls)
```

### High-level settings tree (same as gRPC)

```python
# Identical API to gRPC sessions — flobject is unchanged
print(session.settings.setup.models.energy.enabled())
session.settings.setup.models.energy.enabled.set_state(True)
```

### Check interactive mode

```python
print(client.is_interactive_mode())   # True / False
```

### Read full settings schema

```python
schema = client.get_static_info()
print(list(schema.keys())[:10])
```

### Terminate Fluent

```python
session.exit()
# On Windows: taskkill /F /T — kills entire process tree (solver + GUI + web server)
# On Linux:   proc.terminate() → proc.kill() fallback
```

---

## Authentication

The token is **SHA-256 hashed** automatically before every request:

```
Authorization: Bearer <sha256(token.encode()).hexdigest()>
```

Always set the **raw token** in `FLUENT_WEBSERVER_TOKEN` — hashing happens internally.

```python
os.environ["FLUENT_WEBSERVER_TOKEN"] = "my-secret-token"  # raw value here
```

> **Security note:** SHA-256 hashing reduces raw token exposure but is not a substitute
> for HTTPS. Use `https://` URLs and TLS in production environments.

---

## Server Readiness — How It Works

`launch_webserver` uses a two-phase wait before returning the session:

| Phase | Check | Interval | Exit condition |
|-------|-------|----------|----------------|
| 1 — TCP | `socket.create_connection(port)` | 2 s | Port opens |
| 2 — Solver | `GET /api/connection/run_mode` | 3 s | Any response except `400` |

- `400 Fluent not running` → solver still initialising → keep polling
- `401 Unauthorized` → server + solver fully up → proceed (auth handled after)
- `2xx` → proceed immediately

Both phases share one deadline (`start_timeout`, default 180 s) — **no infinite loop possible**.

Additionally, `execute_cmd` independently retries on `400 Fluent not running` for up to
120 s / every 5 s at the call site, covering the rare case where the readiness probe passed
but the case-read endpoint is not yet accepting commands.

---

## Running Tests

```bash
# Unit tests — no Fluent server required
pytest src/ansys/fluent/core/rest/tests/test_client_unit.py -v --noconftest
pytest src/ansys/fluent/core/rest/tests/test_launcher_unit.py -v --noconftest

# Both together
pytest src/ansys/fluent/core/rest/tests/ -v --noconftest
```

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `FLUENT_WEBSERVER_TOKEN` | **Yes** | Shared secret between client and Fluent web server |
| `FLUENT_REST_PORT` | No | Port for integration tests against a live server |
| `FLUENT_REST_HOST` | No | Host for integration tests (default: `127.0.0.1`) |
| `PYFLUENT_FLUENT_ROOT` | No | Override path to Fluent installation |

---

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `TimeoutError: did not start within 180s` | Fluent startup too slow | Pass `start_timeout=300` to `launch_webserver` |
| `HTTP 401: Invalid password` | Token mismatch | Ensure same token in env var and Fluent process |
| `HTTP 400: Fluent not running` | Solver not fully initialised | Handled automatically — retries 120 s |
| `HTTP 0: ConnectionRefused` | Port not open yet | `_wait_for_server` handles this — increase `start_timeout` |
| `FileNotFoundError: settings_261.py` | Codegen files missing | Run codegen or pass correct `product_version` |
| `KeyError: 'type'` in `get_root` | Solver returned empty schema | `_build_settings_with_retry` retries — increase retries/delay if needed |
| Fluent GUI stays open after `session.exit()` | Old `proc.terminate()` only killed wrapper | Fixed — now uses `taskkill /F /T` on Windows |

---

## Known Limitations

- HTTP only — no TLS/HTTPS support yet
- `connect_to_webserver` does not wait for server readiness — caller must ensure server is up
- Meshing session (`fluent_meshing_1`) untested

---

## License

Licensed under the [MIT License](../../../../LICENSE).

## Contributing

See [CONTRIBUTING.md](../../../../CONTRIBUTING.md).

## Security

To report a security vulnerability, see [SECURITY.md](../../../../SECURITY.md).
