# REST Transport for PyFluent — How It Works

> Written for junior developers. No gRPC or Fluent internals assumed.

---

## Big Picture in One Sentence

Instead of talking to Fluent over gRPC (the existing approach), this package
lets you talk to Fluent over plain HTTP (REST), using the same Python settings
API the user already knows.

---

## Part 1 — The Workflow: What Happens Step by Step

### What is "SimBA"?

When Fluent is running, it starts a small embedded web server called **SimBA**
(Simulation Bridge Application). SimBA listens on a port (e.g. 5000) and
exposes all Fluent solver settings as REST endpoints like:

```
http://<fluent-host>:5000/api/fluent_1/static-info
http://<fluent-host>:5000/api/fluent_1/get_var
http://<fluent-host>:5000/api/fluent_1/setup/models/energy/enabled
```

This package is the Python client that talks to those endpoints.

---

### Workflow A — Developer using the full session (most common)

```
User code
  │
  ▼
launch_fluent_rest("10.18.44.175", 5000, auth_token="secret")
  │
  ▼
RestSolverSession.__init__
  │   builds FluentRestClient (knows the host + token)
  │   calls get_root(client)  ← flobject builds the settings tree
  │
  ▼
session.settings.setup.models.energy.enabled()
  │   flobject calls client.get_var("setup/models/energy/enabled")
  │
  ▼
FluentRestClient.get_var
  │   sends:  POST http://10.18.44.175:5000/api/fluent_1/get_var
  │           body: {"path": "setup/models/energy/enabled"}
  │
  ▼
SimBA (inside Fluent) replies:  true
  │
  ▼
Python gets back: True
```

**Real code:**

```python
from ansys.fluent.core.rest import launch_fluent_rest

session = launch_fluent_rest("10.18.44.175", 5000, auth_token="my_password")

# Read a value
is_energy_on = session.settings.setup.models.energy.enabled()
print(is_energy_on)   # True

# Change a value
session.settings.setup.models.energy.enabled.set_state(False)
```

---

### Workflow B — Developer using only the client (lower level)

```python
from ansys.fluent.core.rest import FluentRestClient

client = FluentRestClient("http://10.18.44.175:5000", auth_token="my_password")

# Read
val = client.get_var("setup/models/viscous/model")
print(val)   # "k-epsilon"

# Write
client.set_var("solution/run_calculation/iter_count", 200)

# Execute a command
reply = client.execute_cmd("solution/initialization", "initialize")
print(reply)  # "Initialization complete"
```

No settings tree is built — the client is a direct HTTP wrapper.

---

### Workflow C — Developer working without Fluent (using the mock server)

When there is no real Fluent running, use `FluentRestMockServer`.
It behaves exactly like SimBA but runs in the same Python process in memory.
This is how all unit tests work.

```
User code
  │
  ▼
FluentRestMockServer().start()   ← starts a fake HTTP server on localhost
  │   port e.g. 54321
  │
  ▼
FluentRestClient("http://127.0.0.1:54321")
  │
  ▼
client.get_var("setup/models/energy/enabled")
  │   sends:  POST http://127.0.0.1:54321/api/fluent_1/get_var
  │           body: {"path": "setup/models/energy/enabled"}
  │
  ▼
_Handler.do_POST  (inside mock server)
  │   reads path from body
  │   looks up self._store["vars"]["setup/models/energy/enabled"]
  │
  ▼
Mock server replies:  true
  │
  ▼
Python gets back: True
```

**Real code:**

```python
from ansys.fluent.core.rest import FluentRestMockServer, FluentRestClient

with FluentRestMockServer() as server:
    client = FluentRestClient(server.base_url)
    print(client.get_var("setup/models/energy/enabled"))  # True
    client.set_var("setup/models/energy/enabled", False)
    print(client.get_var("setup/models/energy/enabled"))  # False
# server automatically stops when the `with` block exits
```

---

## Part 2 — Files and Classes: Who Does What

### File map

```
src/ansys/fluent/core/rest/
│
├── __init__.py          Re-exports the public classes so users can write
│                        `from ansys.fluent.core.rest import ...`
│
├── protocol.py          Defines the SettingsProxy interface (14 methods).
│                        No logic — just a contract on paper.
│
├── client.py            FluentRestClient — the real HTTP client.
│                        Sends requests to SimBA or mock server.
│
├── mock_server.py       FluentRestMockServer — fake SimBA for testing.
│                        Runs in a background thread, no Fluent needed.
│
├── rest_session.py      RestSolverSession — wires the client into
│                        flobject so the full settings tree works.
│
├── rest_launcher.py     launch_fluent_rest() — convenience function.
│                        Takes host + port, returns a ready session.
│
└── tests/
    ├── conftest.py           Shared pytest fixtures (server + client).
    ├── test_rest_client.py   Unit tests for client + mock server.
    └── test_rest_integration.py  Integration tests (session, flobject tree).
```

---

### Class: `SettingsProxy` (protocol.py)

**What it is:** A formal list of the 14 methods that any "settings backend"
must have. Think of it as a job description.

**Why it matters:** Both the old gRPC backend (`SettingsService`) and the new
REST backend (`FluentRestClient`) follow this job description. That means
`flobject.get_root()` does not care which one it gets — it just calls the same
14 methods.

**14 methods:**

| Method | What it does |
|--------|-------------|
| `get_static_info()` | Returns the full schema of all settings |
| `get_var(path)` | Gets the current value at a path |
| `set_var(path, value)` | Sets a value at a path |
| `get_attrs(path, attrs)` | Gets metadata (e.g. allowed values) for a setting |
| `get_object_names(path)` | Lists named children (e.g. boundary names) |
| `create(path, name)` | Creates a new named child object |
| `delete(path, name)` | Deletes a named child object |
| `rename(path, new, old)` | Renames a named child object |
| `get_list_size(path)` | Gets the length of a list-type setting |
| `resize_list_object(path, size)` | Resizes a list-type setting |
| `execute_cmd(path, cmd, **kwds)` | Runs a command (e.g. initialize) |
| `execute_query(path, query, **kwds)` | Runs a read-only query |
| `has_wildcard(name)` | Checks if a name contains `*`, `?`, `[` |
| `is_interactive_mode()` | Always returns False for REST client |

---

### Class: `FluentRestClient` (client.py)

**What it is:** The HTTP client. The main workhorse.

**How it works:**

```
FluentRestClient("http://host:5000", auth_token="pw", component="fluent_1")
        │
        │  _api_base = "api/fluent_1"
        │  _base_url = "http://host:5000"
        │
        ├─ get_static_info()
        │     → GET  http://host:5000/api/fluent_1/static-info
        │
        ├─ get_var("setup/models/energy/enabled")
        │     → POST http://host:5000/api/fluent_1/get_var
        │            body: {"path": "setup/models/energy/enabled"}
        │
        ├─ set_var("setup/models/energy/enabled", False)
        │     → PUT  http://host:5000/api/fluent_1/setup/models/energy/enabled
        │            body: {"value": false}
        │
        ├─ get_attrs("setup/models/viscous/model", ["allowed-values"])
        │     → POST http://host:5000/api/fluent_1/get_attrs
        │            body: {"path": "...", "attrs": ["allowed-values"]}
        │
        ├─ create("setup/boundary_conditions/wall", "wall-1")
        │     → POST http://host:5000/api/fluent_1/setup/boundary_conditions/wall
        │            body: {"name": "wall-1"}
        │
        ├─ delete("setup/boundary_conditions/wall", "wall-1")
        │     → DELETE http://host:5000/api/fluent_1/setup/boundary_conditions/wall/wall-1
        │
        ├─ rename("setup/boundary_conditions/wall", new="w2", old="wall-1")
        │     → PUT  http://host:5000/api/fluent_1/setup/boundary_conditions/wall
        │            body: {"rename": {"new": "w2", "old": "wall-1"}}
        │
        └─ execute_cmd("solution/initialization", "initialize")
              → POST http://host:5000/api/fluent_1/solution/initialization/initialize
                     body: {}
```

**Key internal helper — `_request(method, endpoint, body=None)`:**

Every public method calls `_request()`. It:
1. Builds the full URL: `base_url/endpoint`
2. Serialises `body` to JSON
3. Adds `Authorization: Bearer <token>` header
4. Sends the HTTP request using Python stdlib `urllib`
5. Parses the JSON response
6. If status is 4xx/5xx, raises `FluentRestError(status, detail)`

No third-party libraries (no requests, no httpx) — pure Python stdlib.

---

### Class: `FluentRestMockServer` (mock_server.py)

**What it is:** A fake SimBA server. Runs in-process in a background thread.
Identical REST API to the real Fluent server, backed by a dictionary in memory.

**How it is structured:**

```
FluentRestMockServer
  │
  ├── self.store  (a dict with all in-memory state)
  │     ├── "vars"           → {"setup/models/energy/enabled": True, ...}
  │     ├── "named_objects"  → {"setup/boundary_conditions/velocity_inlet": ["inlet"]}
  │     ├── "list_sizes"     → {"some/list/path": 1}
  │     ├── "attrs"          → {"setup/models/viscous/model": {"attrs": {...}}}
  │     ├── "static_info"    → {the full schema dict}
  │     ├── "command_handlers" → {("solution/initialization", "initialize"): fn}
  │     └── "query_handlers"   → {("setup/bc/velocity_inlet", "get_zone_names"): fn}
  │
  ├── start()   → spawns background thread running socketserver.TCPServer
  ├── stop()    → shuts down thread
  └── base_url  → "http://127.0.0.1:<port>"

Inside the thread: _Handler (a BaseHTTPRequestHandler subclass)
  ├── do_GET    → handles GET  /api/fluent_1/{path}
  ├── do_POST   → handles POST /api/fluent_1/get_var
  │                         POST /api/fluent_1/get_attrs
  │                         POST /api/fluent_1/{path}/{command}
  │                         POST /api/fluent_1/{path}  (create named object)
  ├── do_PUT    → handles PUT  /api/fluent_1/{path}  (set value / resize / rename)
  └── do_DELETE → handles DELETE /api/fluent_1/{path}/{name}
```

**Key helper — `_strip_prefix(path)`:**
Every handler calls this first. It strips `api/fluent_1/` from the start of the
URL path and returns the settings path (e.g. `"setup/models/energy/enabled"`).
This is how the mock stays component-agnostic — `fluent_1` or `fluent_meshing_1`
both work.

---

### Class: `RestSolverSession` (rest_session.py)

**What it is:** The high-level "session" object. It does two things:
1. Creates a `FluentRestClient`
2. Passes it to `flobject.get_root()` which builds the full Python settings tree

After that, `session.settings.setup.models.energy.enabled()` just works — all
the Python attribute access is handled by `flobject`, which internally calls
`client.get_var(...)` / `client.set_var(...)` etc.

```
RestSolverSession("http://host:5000", auth_token="pw")
    │
    ├─ self._client = FluentRestClient("http://host:5000", auth_token="pw")
    └─ self._settings = get_root(self._client, version="")
                           ↑
                   flobject reads client.get_static_info()
                   and builds a tree of Python objects matching
                   the schema. Every leaf object holds a reference
                   to the client and calls get_var/set_var on demand.
```

---

### Function: `launch_fluent_rest` (rest_launcher.py)

**What it is:** A thin convenience wrapper. Saves you from manually building
the URL string.

```python
# These two are equivalent:

session = launch_fluent_rest("10.18.44.175", 5000, auth_token="pw")

session = RestSolverSession(
    "http://10.18.44.175:5000",
    auth_token="pw",
    component="fluent_1",
)
```

Supports `component` parameter — pass `"fluent_meshing_1"` for a meshing session.

---

### How the classes call each other (the whole chain)

```
launch_fluent_rest(host, port, auth_token)
    │
    └─► RestSolverSession.__init__
            │
            ├─► FluentRestClient.__init__          (sets up _api_base, _auth_token)
            │
            └─► flobject.get_root(client)
                    │
                    └─► client.get_static_info()   (1st HTTP call, gets schema)
                            │
                            └─► _request("GET", "api/fluent_1/static-info")
                                    │
                                    └─► urllib → SimBA or MockServer

                    Then for every later user access:
                    session.settings.X.Y.Z()
                        │
                        └─► client.get_var("X/Y/Z")
                                └─► _request("POST", "api/fluent_1/get_var", body={"path":"X/Y/Z"})
```

---

## Part 3 — What is Pending

### 1. Real authentication token (BLOCKER for live server)

The Fluent server requires a Bearer token set when Fluent started.
**We do not know this token yet.**

```
GET http://10.18.44.175:5000/api/fluent_1/static-info
Authorization: Bearer <????>
→ 401 Invalid password
```

**Action needed:** Find out the password by checking how the Fluent session was
started (it is set via a `-sifile` argument or an environment variable when
launching Fluent). Ask whoever started the Fluent session.

---

### 2. Verify mock server responses match real SimBA exactly

The mock server was built from reading `/openapi.json` from the live server.
However, some response shapes (especially for `get_var` on group paths,
`get_attrs` recursive mode, and list-type settings) have not been verified
against a real Fluent response with a valid token.

**Action needed:** Once the correct token is available, run the script
`test_real_server.py` against the live server and compare responses.

---

### 3. `test_real_server.py` needs updating

The file exists but still has placeholder notes. Once the token is known,
it should be updated to run a suite of real-server assertions covering all
14 proxy methods.

---

### 4. Meshing session support is untested

`component="fluent_meshing_1"` was wired in (constructor parameter exists,
`_api_base` changes correctly) but there is no test or example for a meshing
workflow.

**Action needed:** Start a Fluent meshing session, confirm the component name
is `fluent_meshing_1`, and add a test or example.

---

### 5. No reconnect / retry logic

If the Fluent server drops the connection mid-session, `FluentRestClient`
raises an exception with no retry. For production use, a simple retry wrapper
(e.g. 3 attempts with back-off) should be added around `_request()`.

---

### 6. No async support

`FluentRestClient` uses `urllib` which is synchronous / blocking. For
long-running commands (e.g. running a calculation for many iterations),
the calling thread is blocked. A future improvement would be to add an
async variant using `asyncio` + `aiohttp`.

---

### 7. `resize_list_object` is untested against real server

The mock handles it, and there is a unit test for the mock. But there is no
integration test that confirms a real Fluent list-type setting accepts the
`{"size": n}` body format.

---

## Quick Reference Card

| I want to… | I use… |
|---|---|
| Connect to a running Fluent server | `launch_fluent_rest(host, port, auth_token=...)` |
| Read/write settings via Python attributes | `session.settings.setup.models...` |
| Read/write settings directly via path | `client.get_var("a/b/c")` / `client.set_var("a/b/c", val)` |
| Test without a Fluent instance | `FluentRestMockServer().start()` |
| Use meshing session instead of solver | Pass `component="fluent_meshing_1"` |
| Handle HTTP errors | Catch `FluentRestError` — has `.status` (int) and message |
| Check the formal API contract | `SettingsProxy` in `protocol.py` |
