# PyFluent REST Settings Transport — Step 1 Exploration

## What Is This?

Fluent is a simulation solver. PyFluent is the Python library that lets you
control Fluent from code — change settings, run simulations, read results.

Normally PyFluent talks to Fluent over **gRPC**, which is Google's high-speed
binary communication protocol. It works great, but it ties PyFluent tightly to
gRPC.

The goal of this work (**Issue #4959**) is to prove that PyFluent can work just
as well over a plain **REST API** (the same kind of API that every web service
uses). If we can do that, PyFluent becomes more flexible — it can talk to
Fluent however it needs to, without any single transport being baked in.

This folder contains **Step 1**: a standalone Python REST client and a matching
mock server, so we can develop and test the idea without a real Fluent instance.

---

## The Big Picture (Plain English)

Think of it like ordering food:

| Concept | Restaurant Analogy |
|---|---|
| **Fluent solver** | The kitchen — it does the actual cooking (simulation) |
| **PyFluent settings** | The menu — a structured list of things you can configure |
| **gRPC transport** | A private phone line between the waiter and the kitchen |
| **REST transport** | A standard walkie-talkie anyone can use |
| **`FluentRestClient`** | The waiter who speaks walkie-talkie |
| **`FluentRestMockServer`** | A fake kitchen used for training waiters |

Right now PyFluent only has the private phone line (gRPC). This project adds
the walkie-talkie (REST) as an equally valid option.

---

## Folder Structure

```
src/ansys/fluent/core/rest/
│
├── __init__.py          ← Entry point. Import FluentRestClient and
│                          FluentRestMockServer from here.
│
├── client.py            ← The REST client.
│                          Speaks HTTP to a Fluent REST server.
│                          Uses only Python's built-in urllib — no extra packages.
│
├── mock_server.py       ← A fake Fluent server for testing.
│                          Runs in memory. Uses only Python's built-in
│                          http.server — no Flask, no extra packages.
│
├── README.md            ← This file.
│
└── tests/
    ├── conftest.py      ← Shared test fixtures (start/stop the mock server).
    └── test_rest_client.py  ← 40 tests covering every feature.
```

---

## How It Works

### 1. The Settings Tree

Fluent has hundreds of settings organised like a folder tree:

```
setup/
  models/
    energy/
      enabled          ← True or False
    viscous/
      model            ← "k-epsilon", "laminar", etc.
  boundary_conditions/
    velocity_inlet/
      inlet/
        momentum/
          velocity_magnitude/
            value      ← 1.0 (m/s)
solution/
  run_calculation/
    iter_count         ← 100
```

Every setting is identified by its **path** — a slash-separated string like
`"setup/models/energy/enabled"`.

### 2. The REST API Contract

`FluentRestClient` talks to a server using simple HTTP requests. Each
operation maps to one HTTP call:

| What you want to do | HTTP call |
|---|---|
| Read a setting | `GET /settings/var?path=setup/models/energy/enabled` |
| Write a setting | `PUT /settings/var?path=setup/models/energy/enabled` + body `{"value": false}` |
| Get the full settings tree structure | `GET /settings/static-info` |
| List child objects (e.g. boundary names) | `GET /settings/object-names?path=setup/boundary_conditions/velocity_inlet` |
| Create a new named object | `POST /settings/create?path=...&name=wall-1` |
| Delete a named object | `DELETE /settings/object?path=...&name=wall-1` |
| Rename a named object | `PATCH /settings/rename?path=...` + body `{"old": "wall-1", "new": "wall-2"}` |
| Count items in a list | `GET /settings/list-size?path=...` |
| Run a command (e.g. initialise) | `POST /settings/commands/initialize?path=solution/initialization` |
| Run a query (e.g. get zone names) | `POST /settings/queries/get_zone_names?path=...` |
| Get attribute metadata | `GET /settings/attrs?path=...&attrs=allowed-values` |

All responses come back as **JSON**.

> **Note:** This is a *provisional* contract designed to match the shape of
> Fluent's gRPC settings API. When Ansys publishes the official Fluent REST
> API spec, only the endpoint paths in `client.py` need updating — the rest of
> PyFluent stays the same.

### 3. The Mock Server

Because the real Fluent REST API does not exist yet, `FluentRestMockServer`
acts as a stand-in. It:

- Runs in a background thread inside the same Python process.
- Stores all settings in a Python dictionary (in memory).
- Comes pre-loaded with a small but realistic set of solver settings.
- Starts on a random free port so multiple tests can run at the same time without
  clashing.

### 4. The flobject Connection (Why This Matters)

PyFluent's settings system is built around a module called **flobject**. When
you write:

```python
solver.settings.setup.models.energy.enabled = True
```

`flobject` is the code that makes `solver.settings` feel like a real Python
object tree. Under the hood it calls through a **proxy** object.

Currently that proxy is `SettingsService` (the gRPC one). But `flobject` does
not care *how* the proxy works — it just calls methods like `get_var`,
`set_var`, `execute_cmd`, etc.

`FluentRestClient` has **exactly the same method signatures**, so in Step 2 of
this project it can be dropped in as the proxy directly:

```python
# Today (gRPC)
root = flobject.get_root(flproxy=grpc_settings_service, ...)

# Tomorrow (REST) — one line change
root = flobject.get_root(flproxy=FluentRestClient("http://localhost:8000"), ...)
```

No changes to `flobject` at all.

---

## Quick Start

```python
from ansys.fluent.core.rest import FluentRestClient, FluentRestMockServer

# Start a fake Fluent server (for demo/testing)
server = FluentRestMockServer()
server.start()

# Connect a client
client = FluentRestClient(server.base_url)

# Read a setting
print(client.get_var("setup/models/energy/enabled"))   # True

# Change a setting
client.set_var("setup/models/energy/enabled", False)
print(client.get_var("setup/models/energy/enabled"))   # False

# List boundary conditions
print(client.get_object_names("setup/boundary_conditions/velocity_inlet"))
# ['inlet']

# Create a new wall boundary
client.create("setup/boundary_conditions/wall", "wall-1")

# Run a command
reply = client.execute_cmd("solution/initialization", "initialize")
print(reply)   # 'Initialization complete'

# Check the full settings tree structure
info = client.get_static_info()
print(info["type"])          # 'group'
print(list(info["children"])) # ['setup', 'solution']

# Stop the server when done
server.stop()
```

### Use as a context manager (recommended)

```python
with FluentRestMockServer() as server:
    client = FluentRestClient(server.base_url)
    print(client.get_var("solution/run_calculation/iter_count"))  # 100
# Server is automatically stopped here
```

### Pointing at a real server

When the real Fluent REST server is available, just change the URL:

```python
client = FluentRestClient("http://my-fluent-machine:8000", auth_token="my-token")
```

Everything else stays the same.

---

## Running the Tests

From the `pyfluent/` directory:

```bash
pytest src/ansys/fluent/core/rest/tests/ -v
```

No Fluent installation needed. All 40 tests run against the in-memory mock
server.

What the tests cover:

| Test class | What it checks |
|---|---|
| `TestMockServer` | Server lifecycle (start, stop, context manager, independent state) |
| `TestGetStaticInfo` | Settings tree structure returned correctly |
| `TestGetSetVar` | Read/write all value types (bool, string, int, float, dict, list) |
| `TestGetAttrs` | Attribute metadata (allowed values, active flag) |
| `TestNamedObjects` | Create, list, delete, rename named objects |
| `TestListSize` | List-object size queries |
| `TestExecuteCmd` | Command execution (registered + unregistered) |
| `TestExecuteQuery` | Query execution (registered + unregistered) |
| `TestHelpers` | `is_interactive_mode()`, `has_wildcard()` |
| `TestFluentRestError` | Error representation and status codes |

---

## No Extra Dependencies

Both `FluentRestClient` and `FluentRestMockServer` use **only Python's standard
library**:

| Need | Module used |
|---|---|
| HTTP client | `urllib.request`, `urllib.parse`, `urllib.error` |
| HTTP server | `http.server`, `socketserver` |
| Background thread | `threading` |
| JSON | `json` |

Nothing to `pip install` beyond what PyFluent already requires.

---

## Key Design Decisions

| Decision | Reason |
|---|---|
| Endpoint paths are in one `_Endpoints` class | Easy to update when the real Fluent REST spec arrives |
| `FluentRestClient` method names match the gRPC `SettingsService` | Drop-in replacement for `flobject` in Step 2 |
| Mock server uses random port by default | Tests can run in parallel without port conflicts |
| Each mock server instance has its own store (deep copy) | Tests are fully isolated from each other |
| `has_wildcard()` runs locally (no HTTP call) | Simple string check — no need to ask the server |
| `is_interactive_mode()` always returns `False` | REST is non-interactive by nature |

---

## What Comes Next (Step 2)

Step 1 (this folder) proved the REST client works in isolation.

Step 2 will wire it into the full PyFluent stack:

1. **`my-simple-launcher`** — a tiny launcher that connects to a REST-enabled
   Fluent instead of starting gRPC.
2. **`my-session-class`** — a lightweight session that holds a
   `FluentRestClient` instead of a `SettingsService`.
3. **`flobject` unchanged** — pass `FluentRestClient` as `flproxy` and the
   entire `solver.settings` tree works transparently over REST.

The end result: one line of code changes the transport from gRPC to REST. The
user never needs to know which one is running underneath.
