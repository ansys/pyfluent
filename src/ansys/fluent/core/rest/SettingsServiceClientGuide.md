# Settings Service REST Client — Architecture & Implementation Guide

## 1. Overview

The Fluent WebServer exposes a **RESTful HTTP API** built on top of Boost.Beast. This guide provides everything an external product team needs to build a **Settings Service REST client** — capable of reading, writing, and introspecting the Fluent settings tree — without depending on any pre-generated client code.

**Scope**: This guide covers the **Settings Service** only (the `/api/solver`, `/api/meshing`, `/api/workflow`, `/api/preferences`, `/api/meshing_utilities`, `/api/aero` endpoints). Other services (monitors, transcript, field data, events, etc.) are out of scope.

> **Transport Protocol**: The Fluent WebServer is a **pure REST/HTTP server**. There is **no gRPC, Protobuf, or any RPC framework** involved. All client–server communication uses standard **HTTP/1.1** over TCP, with optional **TLS (HTTPS)** when SSL certificates are present. Your client only needs a standard HTTP library (e.g. `requests`, `fetch`, `libcurl`, `boost::beast`, `httplib`) — no code generation, no `.proto` files, no gRPC stubs.

---

## 2. Architecture

### 2.1 High-Level System Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     YOUR PRODUCT (Client)                       │
│                                                                 │
│  ┌──────────────┐  ┌──────────────────┐  ┌────────────────────┐ │
│  │HTTP Transport│  │ Settings Service │  │ Domain-Specific    │ │
│  │Layer         │──│ Client           │──│ Logic              │ │
│  │(auth, retry, │  │ (CRUD, commands, │  │ (UI binding, etc.) │ │
│  │ compression) │  │  discovery)      │  │                    │ │
│  └──────┬───────┘  └──────────────────┘  └────────────────────┘ │
│         │                                                       │
└─────────┼───────────────────────────────────────────────────────┘
          │ HTTP/HTTPS
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FLUENT WEBSERVER                            │
│                                                                 │
│  HttpListener ──► SessionDetector ──► HttpSession               │
│                                          │                      │
│                                   RequestHandler (router)       │
│                                          │                      │
│              ┌───────────────────────────┼────────────────┐     │
│              │                           │                │     │
│    SettingsRequestHandler     ConnectionRequestHandler   ...    │
│     /api/solver                /api/connection                  │
│     /api/meshing                                                │
│     /api/workflow                                               │
│     /api/preferences                                            │
│     /api/meshing_utilities                                      │
│     /api/aero                                                   │
│              │                                                  │
│        CxSettingsAPI  ──►  Scheme/Fluent Engine                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Server-Side Request Flow

1. **`HttpListener`** accepts TCP connections.
2. **`SessionDetector`** detects SSL/non-SSL and creates an **`HttpSession`**.
3. **`HttpSession::onRead`** receives the raw HTTP request.
4. **`RequestHandler`** (the router) matches the URL prefix against registered handlers.
5. **`Authorizor`** middleware validates the `Authorization: Bearer <token>` header. Returns `401 Unauthorized` on failure.
6. **`RequestParser`** middleware parses the raw request into an `HttpRequest` struct (method, target, params, body, headers).
7. The matched **`IRequestHandler`** (e.g. `SettingsRequestHandler`) processes the request and returns an `HttpResponse`.
8. **`Compressor`** / **`Cacher`** middlewares post-process the response.
9. **`HttpSession::send`** writes the response asynchronously.

### 2.3 Recommended Client-Side Architecture

```
┌─────────────────────────────────────────────┐
│              SettingsClient                 │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │         Public API Layer            │    │
│  │  getVar()  setVar()  getAttrs()     │    │
│  │  executeCommand()  getStaticInfo()  │    │
│  │  createObject()  deleteObject()     │    │
│  │  renameObject()  executeQuery()     │    │
│  └────────────────┬────────────────────┘    │
│                   │                         │
│  ┌────────────────▼────────────────────┐    │
│  │       HTTP Transport Layer          │    │
│  │  Base URL, Token, Retry, Timeout    │    │
│  │  Compression, Error Mapping         │    │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

---

## 3. Prerequisites & Connection Bootstrap

### 3.1 Obtaining the Server Address

When Fluent starts its webserver, it exposes:

| Property | How to obtain |
|---|---|
| **Port** | `WebServer::getPort()` — written to a connection info file (e.g. `server_info-<session>.txt`) |
| **Protocol** | `http` or `https` depending on SSL certificate availability (`WebServer::canSupportHTTPS()`) |
| **Token** | `WebServer::getToken()` — written to the same connection info file |

Typical base URL: `http://localhost:<port>` or `https://localhost:<port>`

### 3.2 Authentication

**All requests** (except CORS preflight `OPTIONS` without body) **MUST** include:

```
Authorization: Bearer <token>
```

**Failed authentication** returns:

```http
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer realm="fluent" error="invalid_token" error_description="Invalid password"

Invalid password.
```

### 3.3 Permissions Model

Tokens carry one of these permission levels (highest to lowest):

| Level | Value | Capabilities |
|---|---|---|
| `ADMIN` | 0 | Full access, can add/remove tokens |
| `EDIT` | 1 | Read & write settings, execute commands |
| `EDIT_RESULTS` | 2 | Read & write results-related settings |
| `VIEW` | 3 | Read-only access |
| `NONE` | 4 | No access (rejected) |

When permission is insufficient, the server returns `403 Forbidden`.

### 3.4 Health Check

Before any settings operations, validate the connection:

```http
POST /api/connection/ping HTTP/1.1
Authorization: Bearer <token>

→ 200 OK (empty body)
```

---

## 4. Settings Service API Reference

### 4.1 Base URL Prefixes

The `SettingsRequestHandler` is registered under multiple prefixes, each mapping to a different settings root:

| Prefix | Settings Root | Description |
|---|---|---|
| `/api/solver` | `solver` | Solver settings tree |
| `/api/meshing` | `meshing` | Meshing settings tree |
| `/api/meshing_utilities` | `meshing-utilities` | Meshing utility settings |
| `/api/workflow` | `workflow` | Workflow settings tree |
| `/api/preferences` | `preferences` | User preferences tree |
| `/api/aero` | `aero` | Aero-specific settings tree |

All endpoints described below are **relative to these base prefixes**. Example: `GET /api/solver/static-info`.

---

### 4.2 Endpoint Discovery — Static Info

The first call your client should make after authentication. This returns the **complete settings tree schema** — all children, commands, queries, their types, allowed values, and metadata.

```http
GET /api/solver/static-info HTTP/1.1
Authorization: Bearer <token>
```

**Query Parameters:**

| Param | Type | Default | Description |
|---|---|---|---|
| `full` | `"true"/"false"` | `"false"` | When `"true"`, bypasses the cache and fetches fresh info from Fluent. When `"false"`, returns a cached version. |

**Response:** `200 OK` — JSON object representing the full settings tree schema.

**Allowed Methods:** `OPTIONS, HEAD, GET`

> **Architectural Note:** Cache the static info response on the client side. It changes only when a new case is loaded. Use it to build your client-side settings object model dynamically.

---

### 4.3 Reading Settings — GET & get_var

#### 4.3.1 GET on a settings path

Read the current value of any settings node:

```http
GET /api/solver/<settings-path> HTTP/1.1
Authorization: Bearer <token>
```

**Example:**
```http
GET /api/solver/setup/general/solver/time HTTP/1.1
→ 200 OK
"steady"
```

**Query Parameters for GET:**

| Param | Type | Description |
|---|---|---|
| `attrs` | Comma-separated string | Fetch specific attributes instead of value (e.g. `attrs=allowed-values,default`) |
| `children` | Comma-separated string | Fetch attributes only for these children |
| `recursive` | `"true"/"false"` | Fetch attributes recursively |
| `include-children` | `"true"/"false"` | Include children in attribute response |
| `filters` | Comma-separated string | Settings API filters to apply |

**Response:** `200 OK` — JSON value of the settings node.

> For `Command` or `Query` typed endpoints, `GET` without `attrs` returns `204 No Content`.

#### 4.3.2 POST /get_var (Batch read)

For complex read operations with fine-grained child selection:

```http
POST /api/solver/get_var HTTP/1.1
Authorization: Bearer <token>
Content-Type: application/json

{
  "path": "setup/general",
  "child-names": ["solver", "operating-conditions"],
  "excluded-child-names": [],
  "filters": []
}
```

**Body Parameters:**

| Param | Type | Default | Description |
|---|---|---|---|
| `path` | String | `""` | Settings API path |
| `child-names` | Array\<String\> | all children | List of children to include |
| `excluded-child-names` | Array\<String\> | `[]` | List of children to exclude |
| `filters` | Array\<String\> | `[]` | Settings API filters |

**Allowed Methods:** `OPTIONS, POST`

---

### 4.4 Writing Settings — PUT / PATCH

Update the value of a settings node:

```http
PUT /api/solver/<settings-path> HTTP/1.1
Authorization: Bearer <token>
Content-Type: application/json

<new-value>
```

**Example — Set a scalar value:**
```http
PUT /api/solver/setup/general/solver/time HTTP/1.1
Content-Type: application/json

"unsteady-1st-order"
```

**Example — Set multiple children at once:**
```http
PUT /api/solver/setup/general/solver HTTP/1.1
Content-Type: application/json

{
  "time": "unsteady-1st-order",
  "type": "pressure-based"
}
```

**Query Parameters:**

| Param | Type | Default | Description |
|---|---|---|---|
| `send_state` | `"true"/"false"` | `"true"` | Whether to return the updated state in the response |

**Response:** `200 OK` — Updated state of the settings node (if `send_state=true`).

**Renaming Named Object Instances via PUT:**

Two patterns are supported:
```http
# Pattern 1: Include "name" in the body
PUT /api/solver/setup/materials/fluid/air HTTP/1.1
{ "name": "clean_air" }

# Pattern 2: Target the /name path directly
PUT /api/solver/setup/materials/fluid/air/name HTTP/1.1
"clean_air"
```

**Allowed Methods for PUT:** All endpoint types **except** `Command` and `Query`.

---

### 4.5 Querying Attributes — get_attrs

Fetch metadata attributes for any settings path:

```http
POST /api/solver/get_attrs HTTP/1.1
Authorization: Bearer <token>
Content-Type: application/json

{
  "path": "setup/general/solver/time",
  "attrs": ["allowed-values", "default", "type"],
  "children": [],
  "recursive": false,
  "filters": []
}
```

**Body Parameters:**

| Param | Type | Default | Description |
|---|---|---|---|
| `path` | String | `""` | Settings API path |
| `attrs` | Array\<String\> | `[]` | Attribute names to fetch |
| `children` | Array\<String\> | `[]` | Children paths relative to `path` |
| `recursive` | Bool | `false` | Fetch recursively |
| `include-children` | Bool | `false` | Include children |
| `filters` | Array\<String\> | `[]` | Settings API filters |

Commonly used attributes: `allowed-values`, `default`, `type`, `active?`, `read-only?`, `min`, `max`, `children`, `commands`, `queries`, `object-names`, `user-creatable?`, `renamable?`, `deletable?`, `duplicatable?`

**Allowed Methods:** `OPTIONS, POST`

---

### 4.6 Executing Commands — POST

Commands are action endpoints (e.g., initialize, iterate, export):

```http
POST /api/solver/<path-to-command> HTTP/1.1
Authorization: Bearer <token>
Content-Type: application/json

{
  "arg1": "value1",
  "arg2": 42
}
```

**Query Parameters:**

| Param | Type | Default | Description |
|---|---|---|---|
| `force` | `"true"/"false"` | not set | When `"true"`, skips confirmation prompt check |

**Confirmation Prompt Flow:**

1. Client sends `POST` without `force=true`.
2. If a confirmation prompt is defined, server returns `409 Conflict`:
   ```json
   { "show-prompt": "Are you sure you want to initialize?" }
   ```
3. Client shows the prompt to the user.
4. If confirmed, client resends with `?force=true`.

**Sub-commands of Command endpoints:**

| Sub-path | Method | Description |
|---|---|---|
| `<command>/create_instance` | POST | Create a new instance of a parameterized command |
| `<command>/get_confirmation_prompt` | POST | Explicitly fetch the confirmation prompt text |

**Allowed Methods:** `OPTIONS, POST`

---

### 4.7 Executing Queries — POST

Queries are read-only action endpoints:

```http
POST /api/solver/<path-to-query> HTTP/1.1
Authorization: Bearer <token>
Content-Type: application/json

{
  "arg1": "value1"
}
```

**Response:** `200 OK` — query result as JSON.

**Allowed Methods:** `OPTIONS, POST`

---

### 4.8 Named Object Management (CRUD)

Named objects (e.g., materials, boundary conditions) support full CRUD:

#### Create
```http
POST /api/solver/<parent-path> HTTP/1.1
Content-Type: application/json

{
  "name": "my_new_object",
  "property1": "value1"
}
```
**Response:** `201 Created` — State of the newly created object.

#### Read
```http
GET /api/solver/<parent-path>/<object-name> HTTP/1.1
```

#### Update
```http
PUT /api/solver/<parent-path>/<object-name> HTTP/1.1
Content-Type: application/json

{ "property1": "new_value" }
```

#### Delete
```http
DELETE /api/solver/<parent-path>/<object-name> HTTP/1.1
```
**Response:** `200 OK` — Last known state of the deleted object.

#### Rename
```http
PUT /api/solver/<parent-path>/<old-name> HTTP/1.1
Content-Type: application/json

{ "name": "new_name" }
```

---

### 4.9 List Object Management

List objects support resizing:

```http
POST /api/solver/<list-object-path> HTTP/1.1
Content-Type: application/json

{ "new-size": 5 }
```

**Response:** `200 OK` — Resize result.

---

### 4.10 Discovering Allowed Methods — OPTIONS

Send `OPTIONS` to **any** endpoint to discover what HTTP methods are allowed and what parameters are expected:

```http
OPTIONS /api/solver/setup/general/solver/time HTTP/1.1
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
{
  "children": ["child1", "child2"],
  "commands": ["cmd1"],
  "queries": ["query1"],
  "arguments": [],
  "object-names": [],
  "allowed-values": ["steady", "unsteady-1st-order", "unsteady-2nd-order"],
  "user_creatable": false,
  "renamable": false,
  "deletable": false,
  "duplicatable": false,
  "editable": true,
  "query parameters for GET request": {
    "attrs": "Comma separated list of attributes.",
    "children": "Comma separated list of children for which attributes should be fetched.",
    "recursive": "Boolean indicating if attributes should be fetched recursively."
  },
  "query parameters for PUT request": {
    "send_state": "Boolean indicating if the resource state should be sent back in the response, Default - true."
  }
}
```

The response `Allow` header also lists valid methods (e.g. `OPTIONS, HEAD, GET, PUT, PATCH`).

**Allowed methods depend on endpoint type:**

| Endpoint Type | Allowed Methods |
|---|---|
| Child (group/leaf) | `OPTIONS, HEAD, GET, PUT, PATCH` |
| Child (with named objects) | `OPTIONS, HEAD, GET, PUT, PATCH, POST` |
| ChildObjectType (named instance) | `OPTIONS, HEAD, GET, PUT, PATCH, POST, DELETE` |
| Command | `OPTIONS, HEAD, GET, POST` |
| Query | `OPTIONS, HEAD, GET, POST` |
| CommandHelper | `OPTIONS, POST` |

---

### 4.11 Field-Level Help

Fetch contextual help for a specific settings path:

```http
GET /api/solver/field_level_help?path=setup/general/solver/time HTTP/1.1
Authorization: Bearer <token>
```

**Allowed Methods:** `OPTIONS, HEAD, GET`

---

### 4.12 Modified Settings

Retrieve only settings that differ from their default values:

```http
GET /api/solver/modified_settings?path=setup/general HTTP/1.1
Authorization: Bearer <token>
```

**Query Parameters:**

| Param | Type | Default | Description |
|---|---|---|---|
| `path` | String | `""` | Settings path |
| `filters` | Comma-separated string | `[]` | Settings API filters |

**Allowed Methods:** `OPTIONS, HEAD, GET`

---

### 4.13 Named Objects Map

Get a map of all named objects:

```http
GET /api/solver/named_objects_map HTTP/1.1
Authorization: Bearer <token>
```

**Query Parameters:**

| Param | Type | Default | Description |
|---|---|---|---|
| `filters` | Comma-separated string | `[]` | Settings API filters |

**Allowed Methods:** `OPTIONS, HEAD, GET`

---

### 4.14 Context Menu

Get context menu items for selected settings objects:

```http
POST /api/solver/get_context_menu HTTP/1.1
Authorization: Bearer <token>
Content-Type: application/json

{
  "paths": ["setup/materials/fluid/air"],
  "surfaces": [],
  "filters": []
}
```

**Allowed Methods:** `OPTIONS, POST`

---

### 4.15 MIME Data

#### Get supported MIME types
```http
GET /api/solver/mime_data/types HTTP/1.1
```

#### Get MIME data
```http
GET /api/solver/mime_data?path=<settings-path>&children=child1,child2 HTTP/1.1
```

#### Set MIME data
```http
PUT /api/solver/mime_data HTTP/1.1
Content-Type: application/json

{
  "path": "<settings-path>",
  "data": { ... }
}
```

#### Check if MIME data can be applied
```http
POST /api/solver/mime_data/check HTTP/1.1
Content-Type: application/json

{
  "path": "<settings-path>",
  "data": { ... }
}
```

---

## 5. Endpoint Type System

The server organizes settings into a typed tree. Understanding these types is crucial for building a correct client:

| Type | Description | Example |
|---|---|---|
| **Child** | A group node or leaf value | `setup/general/solver` |
| **Command** | An executable action with arguments | `solution/initialization/initialize` |
| **Query** | A read-only executable with arguments | `solution/report-definitions/compute` |
| **Argument** | A parameter of a command/query | Arguments within a command |
| **ChildObjectType** | A named-object instance template | Individual material under `materials/fluid` |
| **CommandObjectType** | A command-instance template | Instance within a parameterized command |
| **CommandHelper** | Sub-operations for commands | `create_instance`, `get_confirmation_prompt` |

---

## 6. Request / Response Format Conventions

### 6.1 Common Headers

**Request headers your client MUST send:**

| Header | Value | Required |
|---|---|---|
| `Authorization` | `Bearer <token>` | Always (except OPTIONS preflight) |
| `Content-Type` | `application/json` | For POST, PUT, PATCH |

**Response headers the server may return:**

| Header | Description |
|---|---|
| `Server` | Server identification string |
| `Access-Control-Allow-Origin` | CORS header |
| `Allow` | Allowed methods (on OPTIONS response) |
| `Content-Encoding` | `gzip` if response is compressed |
| `ETag` | Cache validator |

### 6.2 Error Handling

| HTTP Status | Meaning | Client Action |
|---|---|---|
| `200 OK` | Success | Process response |
| `201 Created` | Object created | Process new object state |
| `204 No Content` | GET on command/query (no value) | No action needed |
| `400 Bad Request` | Malformed request body/params | Fix request |
| `401 Unauthorized` | Invalid or missing token | Re-authenticate |
| `403 Forbidden` | Insufficient permissions | Upgrade token or inform user |
| `404 Not Found` | Path does not exist or invalid | Check path validity |
| `405 Method Not Allowed` | HTTP method not supported | Check `Allow` header |
| `409 Conflict` | Command needs user confirmation | Show prompt, retry with `?force=true` |
| `500 Internal Server Error` | Server-side failure | Log error message, retry or inform user |

Error responses contain a plain-text error message in the body.

### 6.3 Compression

The server supports **gzip** response compression. To request it:

```
Accept-Encoding: gzip
```

### 6.4 Caching

The server may return `ETag` headers. Your client can send:

```
If-None-Match: <etag-value>
```

The server returns `304 Not Modified` if the resource hasn't changed.

---

## 7. Transport Protocol — HTTP & HTTPS

### 7.1 Protocol Selection (No gRPC)

The Fluent WebServer uses **exclusively HTTP/1.1 REST** for all client–server communication.

| What is used | What is NOT used |
|---|---|
| HTTP/1.1 over TCP | ~~gRPC~~ |
| HTTPS (TLS 1.2+) over TCP | ~~Protobuf / proto files~~ |
| JSON request/response bodies | ~~HTTP/2 multiplexing~~ |
| Standard HTTP methods (GET, POST, PUT, DELETE, OPTIONS, PATCH, HEAD) | ~~RPC stubs / code generation~~ |
| Bearer token authentication | ~~mTLS client certificates~~ |

**Implications for your client:**
- You need **only a standard HTTP client library** — no gRPC runtime, no protobuf compiler, no generated stubs.
- All data is exchanged as **JSON over HTTP** — human-readable, easily debuggable with tools like `curl`, Postman, or browser DevTools.
- WebSocket connections (for transcript, events, etc.) also operate over the same TCP/TLS port — but those are outside the scope of this Settings Service guide.

### 7.2 HTTP (Plain TCP)

When no SSL certificates are available, the server starts in **HTTP mode** (plain TCP):

```
http://localhost:<port>/api/solver/...
```

- All data is transmitted **unencrypted**.
- Suitable for **localhost-only** development and same-machine communication.
- The server listens on a single port for all HTTP traffic.

### 7.3 HTTPS (TLS/SSL)

When SSL certificates are present and loaded successfully, the server supports **HTTPS mode**:

```
https://localhost:<port>/api/solver/...
```

- Data is encrypted using **TLS 1.2+** (SSLv2 is explicitly disabled).
- The server uses **server-side certificates only** — no mutual TLS / client certificates.
- **Required for production** and any remote (non-localhost) connections.

### 7.4 Server-Side Auto-Detection

The server uses a **dual-mode auto-detection** mechanism on a **single port**. It does NOT run HTTP and HTTPS on separate ports.

**How it works internally:**

1. `HttpListener` accepts a raw TCP socket.
2. `SessionDetector` uses Boost.Beast's `async_detect_ssl()` to peek at the first bytes of the connection.
3. If a TLS ClientHello handshake is detected → `HttpSession` is created with an `SslStream` (HTTPS mode).
4. If no TLS handshake is detected → `HttpSession` is created with a plain `TcpStream` (HTTP mode).
5. The `HttpSession::m_isSSL` flag tracks which mode the connection is operating in.

```
  Client connects to port N
          │
          ▼
  ┌─────────────────────┐
  │  SessionDetector     │
  │  async_detect_ssl()  │
  └────────┬────────────┘
           │
     ┌─────┴──────┐
     │            │
   SSL?         No SSL?
     │            │
     ▼            ▼
  SslStream    TcpStream
  (HTTPS)      (HTTP)
     │            │
     ▼            ▼
  HttpSession  HttpSession
  m_isSSL=true m_isSSL=false
```

**Key point**: Both HTTP and HTTPS clients can connect to the **same port**. The server auto-detects per-connection.

### 7.5 Client-Side Protocol Handling

Your client should handle protocol selection as follows:

```
1. Read connection info file → get port, token, and HTTPS availability flag
2. Determine base URL:
     if HTTPS available → "https://localhost:<port>"
     else              → "http://localhost:<port>"
3. Configure HTTP client accordingly:
     if HTTPS → enable TLS, optionally disable certificate verification for self-signed certs
     if HTTP  → standard TCP connection
```

**Python example — dual-mode connection:**
```python
import requests
import urllib3

def create_session(port: int, token: str, use_https: bool = False) -> requests.Session:
    session = requests.Session()
    session.headers["Authorization"] = f"Bearer {token}"
    session.headers["Content-Type"] = "application/json"
    
    if use_https:
        # For self-signed certificates in development
        session.verify = False
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    session.base_url = f"{'https' if use_https else 'http'}://localhost:{port}"
    return session
```

**TypeScript example — dual-mode connection:**
```typescript
import https from "https";

function createClient(port: number, token: string, useHttps: boolean) {
  const protocol = useHttps ? "https" : "http";
  const baseUrl = `${protocol}://localhost:${port}`;
  
  // For self-signed certificates in development
  const agent = useHttps
    ? new https.Agent({ rejectUnauthorized: false })
    : undefined;

  return { baseUrl, token, agent };
}
```

**C++ example — dual-mode connection:**
```cpp
// With cpp-httplib
#include <httplib.h>

std::unique_ptr<httplib::Client> createClient(const std::string& host, int port, bool useHttps) {
    if (useHttps) {
        auto client = std::make_unique<httplib::SSLClient>(host, port);
        client->enable_server_certificate_verification(false); // for self-signed certs
        return client;
    }
    return std::make_unique<httplib::Client>(host, port);
}
```

### 7.6 SSL Certificate Setup (Server)

For reference, the server loads SSL certificates from these locations:

| File | Format | Description |
|---|---|---|
| `webserver.crt` | PEM | Server certificate chain |
| `webserver.key` | PEM | Server private key |
| `dh.pem` | PEM | Diffie-Hellman parameters |

**Certificate search order:**
1. `FLUENT_WEBSERVER_CERTIFICATE_ROOT` environment variable (custom path)
2. `FLUENT_PROD_DIR/../../FluidsOne/web/certificate` (default installation path)

If certificates are not found, the server falls back to **HTTP-only mode** (no error, just a log message).

**Client-side implications:**
- The server's certificate may be self-signed in development environments.
- Your client should support an option to **skip server certificate verification** for development.
- In production, use properly signed certificates and enable verification.

> **Security Note**: Always use HTTPS for remote (non-localhost) connections. HTTP should only be used for same-machine communication in trusted environments.

---

## 8. Request Threading Model

Understanding the server threading model helps you build a responsive client:

| RequestType | Thread | Behavior |
|---|---|---|
| `SERVER_REQUEST` | Any thread | Processed immediately. Used for `static-info` (cached), `field_level_help`, `OPTIONS` preflight. |
| `CORTEX_REQUEST` | Main thread | Queued if busy, processed when main thread is available. Safe even when Fluent is iterating. |
| `FLUENT_REQUEST` | Main thread | Queued, only processed when Fluent is **idle**. Most settings read/write operations are this type. |

**Client implications:**
- `static-info` (without `full=true`) is fast and always available — good for initialization.
- Settings reads/writes are `FLUENT_REQUEST` — they may be delayed while Fluent is iterating. Implement appropriate timeouts.
- Consider using the [Pause/Resume protocol](#8-pause--resume-protocol) for batch operations during iteration.

---

## 9. Client Implementation Guide

### 10.1 Recommended Module Structure

```
settings-client/
├── transport/
│   ├── http_client          # Low-level HTTP calls (GET, POST, PUT, DELETE, OPTIONS)
│   ├── auth                 # Token management, header injection
│   ├── retry                # Retry logic with backoff
│   └── errors               # Error class hierarchy mapped to HTTP status codes
├── services/
│   └── settings_service     # High-level Settings API methods
├── models/
│   ├── static_info          # Parsed static-info tree model
│   ├── settings_value       # Value wrapper (scalar, map, array)
│   └── endpoint_type        # Enum: Child, Command, Query, etc.
├── discovery/
│   └── connection_info      # Reads port/token from connection file
└── client                   # Facade that composes all of the above
```

### 10.2 Building the HTTP Transport Layer

Your transport layer should:

1. **Manage base URL and token** — injected at construction.
2. **Add `Authorization: Bearer <token>`** to every request.
3. **Support all HTTP methods:** GET, HEAD, POST, PUT, PATCH, DELETE, OPTIONS.
4. **Set `Content-Type: application/json`** for request bodies.
5. **Handle gzip decompression** if `Accept-Encoding: gzip` is sent.
6. **Map HTTP error codes** to typed exceptions:
   - `401` → `AuthenticationError`
   - `403` → `PermissionError`
   - `404` → `NotFoundError`
   - `405` → `MethodNotAllowedError`
   - `409` → `ConfirmationRequiredError` (extract prompt from `show-prompt`)
   - `500` → `ServerError`
7. **Implement retry with exponential backoff** for `500` errors and timeouts.
8. **Configure sensible timeouts** — settings requests may take time if Fluent is busy.

### 10.3 Building the Settings Service Client

Your Settings Service client should expose these core methods:

```
class SettingsService:
    # Discovery
    get_static_info(root, full=False) → dict

    # Read operations
    get_var(root, path, filters=[]) → any
    get_var_batch(root, path, child_names=[], excluded=[], filters=[]) → dict
    get_attrs(root, path, attrs, children=[], recursive=False, filters=[]) → dict
    get_modified_settings(root, path="", filters=[]) → dict
    get_named_objects_map(root, filters=[]) → dict

    # Write operations
    set_var(root, path, value, send_state=True) → any
    
    # Command/Query execution
    execute_command(root, path, args={}, force=False) → any
    execute_query(root, path, args={}) → any
    get_confirmation_prompt(root, path, args={}) → str
    create_command_instance(root, path) → any
    
    # Named object CRUD
    create_object(root, parent_path, name="", properties={}) → any
    delete_object(root, parent_path, object_name) → any
    rename_object(root, parent_path, old_name, new_name) → any
    
    # List object
    resize_list_object(root, path, new_size) → any

    # Introspection
    get_options(root, path) → dict
    get_field_level_help(root, path) → dict
```

Where `root` is one of: `solver`, `meshing`, `workflow`, `preferences`, `meshing_utilities`, `aero`.

### 10.4 Example: Python Client

```python
import requests
from typing import Any, Optional
from dataclasses import dataclass

ROOT_PREFIX_MAP = {
    "solver": "/api/solver",
    "meshing": "/api/meshing",
    "workflow": "/api/workflow",
    "preferences": "/api/preferences",
    "meshing_utilities": "/api/meshing_utilities",
    "aero": "/api/aero",
}


class ConfirmationRequired(Exception):
    def __init__(self, prompt: str):
        self.prompt = prompt
        super().__init__(prompt)


@dataclass
class SettingsClient:
    base_url: str   # e.g. "http://localhost:5000"
    token: str       # Bearer token

    @property
    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def _prefix(self, root: str) -> str:
        return ROOT_PREFIX_MAP.get(root, f"/api/{root}")

    def _url(self, root: str, path: str = "") -> str:
        prefix = self._prefix(root)
        if path:
            return f"{self.base_url}{prefix}/{path}"
        return f"{self.base_url}{prefix}"

    def _check(self, resp: requests.Response) -> Any:
        if resp.status_code == 401:
            raise PermissionError("Authentication failed")
        if resp.status_code == 403:
            raise PermissionError(resp.text)
        if resp.status_code == 404:
            raise KeyError(resp.text)
        if resp.status_code == 409:
            prompt = resp.json().get("show-prompt", "")
            raise ConfirmationRequired(prompt)
        resp.raise_for_status()
        if resp.status_code == 204:
            return None
        try:
            return resp.json()
        except Exception:
            return resp.text

    # ── Discovery ──────────────────────────────────────

    def ping(self) -> bool:
        resp = requests.post(
            f"{self.base_url}/api/connection/ping",
            headers=self._headers,
        )
        return resp.status_code == 200

    def get_static_info(self, root: str = "solver", full: bool = False) -> dict:
        params = {"full": "true"} if full else {}
        resp = requests.get(
            self._url(root, "static-info"),
            headers=self._headers,
            params=params,
        )
        return self._check(resp)

    # ── Read ───────────────────────────────────────────

    def get_var(self, root: str, path: str, filters: list[str] | None = None) -> Any:
        params = {}
        if filters:
            params["filters"] = ",".join(filters)
        resp = requests.get(
            self._url(root, path),
            headers=self._headers,
            params=params,
        )
        return self._check(resp)

    def get_attrs(self, root: str, path: str, attrs: list[str],
                  children: list[str] | None = None,
                  recursive: bool = False) -> dict:
        body = {"path": path, "attrs": attrs, "recursive": recursive}
        if children:
            body["children"] = children
        resp = requests.post(
            self._url(root, "get_attrs"),
            headers=self._headers,
            json=body,
        )
        return self._check(resp)

    # ── Write ──────────────────────────────────────────

    def set_var(self, root: str, path: str, value: Any,
                send_state: bool = True) -> Any:
        params = {}
        if not send_state:
            params["send_state"] = "false"
        resp = requests.put(
            self._url(root, path),
            headers=self._headers,
            json=value,
            params=params,
        )
        return self._check(resp)

    # ── Commands ───────────────────────────────────────

    def execute_command(self, root: str, path: str,
                        args: dict | None = None,
                        force: bool = False) -> Any:
        params = {"force": "true"} if force else {}
        resp = requests.post(
            self._url(root, path),
            headers=self._headers,
            json=args or {},
            params=params,
        )
        return self._check(resp)

    # ── Named Objects ──────────────────────────────────

    def create_object(self, root: str, parent_path: str,
                      name: str = "", properties: dict | None = None) -> Any:
        body = properties or {}
        if name:
            body["name"] = name
        resp = requests.post(
            self._url(root, parent_path),
            headers=self._headers,
            json=body,
        )
        return self._check(resp)

    def delete_object(self, root: str, path: str) -> Any:
        resp = requests.delete(
            self._url(root, path),
            headers=self._headers,
        )
        return self._check(resp)

    def get_options(self, root: str, path: str) -> dict:
        resp = requests.options(
            self._url(root, path),
            headers=self._headers,
        )
        return self._check(resp)


# ── Usage ────────────────────────────────────────────────

if __name__ == "__main__":
    client = SettingsClient(base_url="http://localhost:5000", token="my-token")

    # Health check
    assert client.ping()

    # Discover the settings tree
    schema = client.get_static_info("solver")

    # Read a setting
    time_value = client.get_var("solver", "setup/general/solver/time")
    print(f"Time scheme: {time_value}")

    # Write a setting
    client.set_var("solver", "setup/general/solver/time", "unsteady-1st-order")

    # Execute a command with confirmation handling
    try:
        client.execute_command("solver", "solution/initialization/initialize")
    except ConfirmationRequired as e:
        user_confirmed = input(f"{e.prompt} (y/n): ").lower() == "y"
        if user_confirmed:
            client.execute_command(
                "solver",
                "solution/initialization/initialize",
                force=True,
            )
```

## 10. Best Practices & Production Readiness

### Connection Management
- **Read the connection info file** at startup to get port and token. Do not hardcode.
- **Implement reconnection logic** — Fluent may restart the webserver under certain operations.
- **Use `/api/connection/ping`** as a heartbeat (but note: frequent pings reset the inactivity timer).

### Performance
- **Cache `static-info`** on the client. It only changes on case load. Use `full=false` (default).
- **Use `get_var` with `child-names`** to fetch only what you need instead of the entire tree.
- **Use `get_attrs` with specific attribute names** instead of fetching all attributes.
- **Use `filters`** to reduce response payload size.
- **Send `Accept-Encoding: gzip`** for large responses (like `static-info`).
- **Batch settings writes** into a single `PUT` on a parent path with a dict body rather than multiple individual writes.

### Responsiveness
- **Use the pause/resume protocol** when performing batch operations during an active solve. This ensures requests are served immediately rather than queued.
- **Set `initiator` to `"app"`** for programmatic pause (vs. user-initiated pause).
- **Always resume** after your batch operation — use try/finally or RAII patterns.

### Error Handling
- **Handle 409 Conflict gracefully** — it means a confirmation prompt is required. Either show the prompt or re-send with `force=true`.
- **Handle 404 Not Found** — settings paths can change when a new case is loaded. Refresh `static-info` and retry.
- **Handle 401 Unauthorized** — token may have been rotated. Re-read the connection info file.

### Security
- **Never log or store tokens in plain text** in production.
- **Prefer HTTPS** when the server has SSL certificates available.
- **Use short-lived tokens** and the `add_token`/`remove_token` endpoints for multi-user scenarios.

---

## 11. Troubleshooting

| Symptom | Likely Cause | Resolution |
|---|---|---|
| All requests return `401` | Invalid/expired token | Re-read connection info file for fresh token |
| Settings reads hang or timeout | Fluent is busy iterating | Use pause/resume, or increase client timeout |
| `404` on a previously valid path | Case was reloaded, settings tree changed | Re-fetch `static-info` and rebuild path map |
| `405 Method Not Allowed` | Wrong HTTP verb for endpoint type | Send `OPTIONS` to discover allowed methods |
| `500 Internal Server Error` | Server-side exception | Check Fluent transcript/log. Enable server logging with `LOG_REST_REQUEST_AND_RESPONSE`. |
| No response / connection refused | Server not started or wrong port | Verify connection info file and server status |
| Compressed response is garbled | Missing decompression | Ensure client handles `Content-Encoding: gzip` |

**Enabling server-side logging:**

Set environment variables before starting Fluent:
```
FLUENT_LOG_MODE=FILE
FLUENT_LOG_DIR=<directory-path>
```

Then in code or via the API, set log level to `LOG_REST_REQUEST_AND_RESPONSE` for full request/response logging.

---

## 12. Appendix — Quick Reference Card

### Endpoint Quick Reference

| Operation | Method | URL Pattern | Body |
|---|---|---|---|
| Get static schema | `GET` | `/api/{root}/static-info` | — |
| Read setting value | `GET` | `/api/{root}/{path}` | — |
| Read setting attrs | `GET` | `/api/{root}/{path}?attrs=a,b` | — |
| Batch read values | `POST` | `/api/{root}/get_var` | `{path, child-names, ...}` |
| Batch read attrs | `POST` | `/api/{root}/get_attrs` | `{path, attrs, ...}` |
| Write setting | `PUT` | `/api/{root}/{path}` | `<value>` |
| Execute command | `POST` | `/api/{root}/{path}` | `{args...}` |
| Execute query | `POST` | `/api/{root}/{path}` | `{args...}` |
| Create named object | `POST` | `/api/{root}/{parent}` | `{name, ...}` |
| Delete named object | `DELETE` | `/api/{root}/{parent}/{name}` | — |
| Rename named object | `PUT` | `/api/{root}/{parent}/{old}` | `{name: "new"}` |
| Resize list object | `POST` | `/api/{root}/{path}` | `{new-size: N}` |
| Discover methods | `OPTIONS` | `/api/{root}/{path}` | — |
| Get field help | `GET` | `/api/{root}/field_level_help?path=...` | — |
| Get modified settings | `GET` | `/api/{root}/modified_settings?path=...` | — |
| Get named object map | `GET` | `/api/{root}/named_objects_map` | — |
| Health check | `POST` | `/api/connection/ping` | — |
| Pause solver | `POST` | `/api/connection/pause` | `{timeout, initiator}` |
| Resume solver | `POST` | `/api/connection/resume` | `{initiator}` |

### curl Cheat Sheet

```bash
TOKEN="your-token-here"
BASE="http://localhost:5000"

# Ping
curl -X POST "$BASE/api/connection/ping" -H "Authorization: Bearer $TOKEN"

# Get static info
curl "$BASE/api/solver/static-info" -H "Authorization: Bearer $TOKEN"

# Read a value
curl "$BASE/api/solver/setup/general/solver/time" -H "Authorization: Bearer $TOKEN"

# Write a value
curl -X PUT "$BASE/api/solver/setup/general/solver/time" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '"unsteady-1st-order"'

# Execute a command with force
curl -X POST "$BASE/api/solver/solution/initialization/initialize?force=true" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{}'

# Discover allowed methods
curl -X OPTIONS "$BASE/api/solver/setup/general/solver/time" \
     -H "Authorization: Bearer $TOKEN"

# Pause solver
curl -X POST "$BASE/api/connection/pause" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"timeout": 300, "initiator": "app"}'
```