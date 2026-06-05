# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""REST client for Fluent DataModel settings endpoints.

This client talks to ``/api/{component}/...`` and sends
``Authorization: Bearer <sha256(auth_token)>`` when a token is configured.
Most HTTP failures are raised as :class:`FluentRestError`.
"""

import hashlib
import json
import logging
import ssl
import time
from typing import Any
import urllib.error
import urllib.parse
import urllib.request
import warnings

logger = logging.getLogger(__name__)

# HTTP status codes eligible for automatic retry.
_RETRYABLE_STATUS_CODES = frozenset({502, 503, 504})

# HTTP methods safe to retry automatically (idempotent).
_RETRYABLE_METHODS = frozenset({"GET", "HEAD", "OPTIONS"})


class FluentRestError(RuntimeError):
    """HTTP error returned by the Fluent REST server."""

    def __init__(self, status: int, message: str) -> None:
        self.status = status
        super().__init__(f"HTTP {status}: {message}")


class FluentRestClient:
    """HTTP client for the Fluent DataModel REST API.

    Parameters
    ----------
    base_url : str
        Root URL of the Fluent REST server, e.g. ``"http://127.0.0.1:<port>"``.
        A trailing slash is stripped automatically.
    auth_token : str, optional
        Raw bearer token (the password set when Fluent was started).  Before
        each request the token is SHA-256 hashed and sent as
        ``Authorization: Bearer <sha256(auth_token)>``.
    component : str, optional
        DataModel component name.  Defaults to ``"fluent_1"`` (solver).
        Use ``"fluent_meshing_1"`` for a meshing session.
    timeout : float, optional
        Socket timeout in seconds for every request.  Defaults to ``30.0``.
    max_retries : int, optional
        Maximum number of automatic retries on transient connection errors
        (``URLError``) or HTTP 502/503/504 responses.  Defaults to ``0``
        (no retries — fail immediately).
    retry_delay : float, optional
        Base delay in seconds between retries.  Uses exponential back-off:
        ``retry_delay * 2 ** attempt``.  Defaults to ``1.0``.
    ssl_context : ssl.SSLContext, optional
        Custom SSL context for HTTPS connections. Defaults to ``None``.
    """

    def __init__(
        self,
        base_url: str,
        *,
        auth_token: str | None = None,
        component: str = "fluent_1",
        timeout: float = 30.0,
        max_retries: int = 0,
        retry_delay: float = 1.0,
        ssl_context: ssl.SSLContext | None = None,
    ) -> None:
        self._validate_base_url(base_url, auth_token, ssl_context)
        if timeout <= 0:
            raise ValueError("timeout must be > 0")
        if max_retries < 0:
            raise ValueError("max_retries must be >= 0")
        if retry_delay < 0:
            raise ValueError("retry_delay must be >= 0")
        self._base_url = base_url.rstrip("/")
        self._auth_token = auth_token
        self._component = component
        self._timeout = timeout
        self._max_retries = max_retries
        self._retry_delay = retry_delay
        self._ssl_context = ssl_context
        self._api_base = f"api/{component}"
        self._is_closed = False

    @property
    def _is_secure(self) -> bool:
        """Return True if the connection is HTTPS, False otherwise."""
        return self._base_url.startswith("https://")

    # ------------------------------------------------------------------
    # Validation (SRP: input validation is a single, isolated concern)
    # ------------------------------------------------------------------

    @staticmethod
    def _validate_base_url(
        base_url: str,
        auth_token: str | None,
        ssl_context: ssl.SSLContext | None,
    ) -> None:
        """Validate *base_url* and warn on insecure auth transport.

        Raises
        ------
        ValueError
            If *base_url* has an unsupported scheme or no host.
        """
        parsed = urllib.parse.urlparse(base_url)
        if parsed.scheme not in {"http", "https"}:
            raise ValueError("scheme must be http or https")
        if not parsed.netloc:
            raise ValueError("base_url must include host")
        if auth_token and parsed.scheme == "http" and ssl_context is None:
            warnings.warn(
                "auth_token is being sent over plain HTTP. "
                "Use https:// to protect credentials in transit.",
                stacklevel=2,
            )

    # ------------------------------------------------------------------
    # HTTP transport internals
    # ------------------------------------------------------------------

    @staticmethod
    def _encode_path(path: str) -> str:
        """Percent-encode each segment of a slash-delimited path."""
        return "/".join(urllib.parse.quote(seg, safe="") for seg in path.split("/"))

    def _url(self, endpoint: str) -> str:
        """Build a full URL from *base_url* + *endpoint*."""
        return f"{self._base_url}/{endpoint}"

    def _build_auth_header(self) -> str | None:
        """Return the ``Authorization`` header value, or ``None``."""
        if not self._auth_token:
            return None
        return f"Bearer {hashlib.sha256(self._auth_token.encode()).hexdigest()}"

    def _build_request(
        self,
        method: str,
        url: str,
        body: Any = None,
    ) -> urllib.request.Request:
        """Assemble an :class:`urllib.request.Request`.

        Serialises *body* to JSON if provided and attaches auth headers.
        """
        data: bytes | None = None
        headers: dict[str, str] = {}
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        auth = self._build_auth_header()
        if auth:
            headers["Authorization"] = auth
        return urllib.request.Request(
            url, data=data, headers=headers, method=method.upper()
        )

    @staticmethod
    def _parse_error_detail(exc: urllib.error.HTTPError) -> str:
        """Return a readable error message from an HTTP error response."""
        try:
            raw = exc.read().decode("utf-8", errors="replace")
            # Server returns plain text, not JSON
            if raw.strip():
                return raw.strip()
            return exc.reason
        except Exception:
            return exc.reason

    def _send_once(self, req: urllib.request.Request) -> Any:
        """Execute one HTTP request and decode JSON response content.

        Returns ``None`` for empty response bodies and ``{}`` for non-JSON
        non-empty bodies.
        """
        with urllib.request.urlopen(
            req, timeout=self._timeout, context=self._ssl_context
        ) as resp:  # nosec B310
            raw = resp.read()
            if not raw.strip():
                return None
            try:
                return json.loads(raw)
            except (json.JSONDecodeError, ValueError):
                return {}

    def _request(
        self,
        method: str,
        endpoint: str,
        *,
        body: Any = None,
    ) -> Any:
        """Send an HTTP request with retry for idempotent methods only."""
        if self._is_closed:
            raise FluentRestError(0, "Session is closed")
        url = self._url(endpoint)
        req = self._build_request(method, url, body)

        retries = self._max_retries if method.upper() in _RETRYABLE_METHODS else 0
        for attempt in range(retries + 1):
            try:
                return self._send_once(req)
            except urllib.error.HTTPError as exc:
                detail = self._parse_error_detail(exc)
                if exc.code in _RETRYABLE_STATUS_CODES and attempt < retries:
                    time.sleep(self._retry_delay * (2**attempt))
                    continue
                raise FluentRestError(exc.code, detail) from exc
            except urllib.error.URLError as exc:
                if attempt < retries:
                    time.sleep(self._retry_delay * (2**attempt))
                    continue
                raise FluentRestError(0, str(exc.reason)) from exc
            except OSError as exc:
                # Catches RemoteDisconnected, ConnectionResetError,
                # ConnectionAbortedError — all signs the server died.
                raise FluentRestError(0, str(exc)) from exc

    # ------------------------------------------------------------------
    # Settings API — read / write
    # ------------------------------------------------------------------

    def get_static_info(self) -> dict[str, Any]:
        """Return the full settings schema (GET static-info)."""
        return self._request("GET", f"{self._api_base}/static-info")

    def get_var(self, path: str) -> Any:
        """Return the value at *path* (POST ``get_var``)."""
        return self._request(
            "POST", f"{self._api_base}/get_var", body={"path": path.lstrip("/")}
        )

    def set_var(self, path: str, value: Any) -> None:
        """Set the value at *path* (PUT {path})."""
        self._request("PUT", f"{self._api_base}/{self._encode_path(path)}", body=value)

    def get_attrs(self, path: str, attrs: list[str], recursive: bool = False) -> Any:
        """Return selected attributes for *path* (GET with ``attrs=...``).

        Raises
        ------
        FluentRestError
            If the request fails.
        """
        params = {"attrs": ",".join(attrs)}
        if recursive:
            params["recursive"] = "true"
        query = urllib.parse.urlencode(params)
        return self._request(
            "GET", f"{self._api_base}/{self._encode_path(path)}?{query}"
        )

    def get_object_names(self, path: str) -> list[str]:
        """Return child object names at *path* (GET {path}); return ``[]`` on 404.

        Raises
        ------
        FluentRestError
            If the request fails with a non-404 HTTP error.
        """
        try:
            result = self._request("GET", f"{self._api_base}/{self._encode_path(path)}")
        except FluentRestError as exc:
            if exc.status == 404:
                return []
            raise
        if isinstance(result, list):
            return result
        if isinstance(result, dict):
            # Real Fluent returns named objects as dict with names as keys:
            # {"hot-inlet": {...}, "cold-inlet": {...}}
            return list(result.keys())
        return []

    def create(self, path: str, name: str = "", properties: dict | None = None) -> Any:
        """Create a child object at *path* (POST {path}).

        Raises
        ------
        FluentRestError
            If the request fails.
        """
        body = dict(properties) if properties else {}
        if name:
            body["name"] = name
        return self._request(
            "POST", f"{self._api_base}/{self._encode_path(path)}", body=body
        )

    def delete(self, path: str, name: str, *, ignore_not_found: bool = False) -> None:
        """Delete named object *name* at *path* (DELETE {path}/{name}).

        Raises
        ------
        FluentRestError
            If deletion fails, except when ``ignore_not_found=True`` and the
            server returns HTTP 404.
        """
        encoded_name = urllib.parse.quote(name, safe="")
        try:
            self._request(
                "DELETE", f"{self._api_base}/{self._encode_path(path)}/{encoded_name}"
            )
        except FluentRestError as exc:
            if ignore_not_found and exc.status == 404:
                return
            raise

    def rename(self, path: str, new: str, old: str) -> None:
        """Rename *old* to *new* at *path* (PUT {path}/{old})."""
        encoded_old = urllib.parse.quote(old, safe="")
        self._request(
            "PUT",
            f"{self._api_base}/{self._encode_path(path)}/{encoded_old}",
            body={"name": new},
        )

    def delete_child_objects(
        self,
        path: str,
        obj_type: str,
        child_names: list[str],
    ) -> None:
        """Delete specific named children of *obj_type* under *path*."""
        for name in child_names:
            self.delete(f"{path}/{obj_type}", name)

    def delete_all_child_objects(self, path: str, obj_type: str) -> None:
        """Delete all named children of *obj_type* under *path*."""
        names = self.get_object_names(f"{path}/{obj_type}")
        self.delete_child_objects(path, obj_type, names)

    def get_list_size(self, path: str) -> int:
        """Return element count at *path* (GET {path}); return 0 on 404.

        Raises
        ------
        FluentRestError
            If the request fails with a non-404 HTTP error.
        """
        try:
            result = self._request("GET", f"{self._api_base}/{self._encode_path(path)}")
        except FluentRestError as exc:
            if exc.status == 404:
                return 0
            raise
        if isinstance(result, list):
            return len(result)
        if isinstance(result, dict):
            # Explicit size field from list-objects
            if "size" in result:
                return result["size"]
            # Named-object containers: count the keys (object names)
            return len(result)
        return 0

    def resize_list_object(self, path: str, size: int) -> None:
        """Resize the list-object at *path* to *size* elements (POST {path})."""
        self._request(
            "POST",
            f"{self._api_base}/{self._encode_path(path)}",
            body={"new-size": size},
        )

    def _execute(self, path: str, name: str, **kwds) -> Any:
        """POST a command/query endpoint and return the raw response payload."""
        encoded_name = urllib.parse.quote(name, safe="")
        return self._request(
            "POST",
            f"{self._api_base}/{self._encode_path(path)}/{encoded_name}",
            body=kwds,
        )

    def execute_cmd(self, path: str, command: str, force: bool = True, **kwds) -> Any:
        """Execute *command* at *path*; appends ``force=true`` when requested."""
        encoded = urllib.parse.quote(command, safe="")
        endpoint = f"{self._api_base}/{self._encode_path(path)}/{encoded}"
        if force:
            endpoint += "?force=true"
        return self._request("POST", endpoint, body=kwds)

    def execute_query(self, path: str, query: str, **kwds) -> Any:
        """Execute *query* at *path* (POST {path}/{query})."""
        return self._execute(path, query, **kwds)

    # ------------------------------------------------------------------
    # Session lifecycle
    # ------------------------------------------------------------------

    def exit(self) -> None:
        """Request shutdown via ``POST /api/app/exit`` and mark session closed.

        HTTP 403/409 are raised to the caller. Other failures are treated as
        shutdown-in-progress and suppressed.

        Raises
        ------
        FluentRestError
            If shutdown is blocked by the server (HTTP 403 or 409).
        """
        if self._is_closed:
            return
        try:
            self._request("POST", "api/app/exit")
        except FluentRestError as exc:
            if exc.status in (403, 409):
                logger.warning("Exit blocked (HTTP %d): %s", exc.status, exc)
                raise
            # Connection lost or other error → server already down
        except OSError:
            # Server died mid-response
            pass
        self._is_closed = True
        logger.info("Fluent server terminated.")

    def __enter__(self) -> "FluentRestClient":
        """Enter the context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the context manager — calls :meth:`exit`."""
        self.exit()



"""
# The Single Level of Abstraction Principle

## The Central Problem: Three Versions of Every Piece of Code

When you read a function, you are reading only one of three things that exist simultaneously:

1. **What was written** — the literal code on the screen.
2. **What was intended** — the idea in the author's mind when they wrote it.
3. **What is correct** — what the code should actually do to be right.

This is the central difficulty of programming. Only version 1 is ever visible to a reader — whether they are reviewing, understanding, or changing the code. Versions 2 and 3 are invisible. They live in the author's head, in a requirements document somewhere, or nowhere at all.

The **Single Level of Abstraction Principle (SLAP)** is a design rule that directly addresses this gap. It states that all the code inside a function should operate at the same conceptual level. No line should reach down into low-level mechanics while neighbouring lines speak in high-level business terms. When a function respects this principle, it becomes possible — often for the first time — for a reader to see not just what was written, but what was intended. And once intent is visible, correctness can be judged.

What follows is a walkthrough of real production code that illustrates what happens when the principle is violated, what it costs, and what it looks like to fix it.

---

## The Code

Here is a pair of methods from PyFluent. Read them carefully before continuing.

```python
def exit(self) -> None:
    ""Gracefully shut down the Fluent session.

    Raises
    ------
        FluentServerShutdown
            If the session has already been closed.
    ""
    if self._is_closed:
        raise FluentServerShutdown("Session is already closed.")
    try:
        self._execute("/", "exit")
    except Exception:
        pass  # nosec B110 - server drops the connection on exit — expected
    self._is_closed = True
    logger.info("Fluent server exited.")

def _execute(self, path: str, name: str, **kwds) -> Any:
    ""Post a command or query and return the ``"reply"`` payload.

    Retries automatically when the server returns
    ``400 Fluent not running`` — the solver may still be initialising
    after the web server port opened.  Gives up after *_SOLVER_READY_TIMEOUT*
    seconds and re-raises the original error.
    ""
    _SOLVER_READY_TIMEOUT = 120  # seconds
    _SOLVER_RETRY_DELAY = 5  # seconds between retries
    start = time.monotonic()
    while True:
        try:
            encoded_name = urllib.parse.quote(name, safe="")
            result = self._request(
                "POST",
                f"{self._api_base}/{self._encode_path(path)}/{encoded_name}",
                body=kwds,
            )
            return result.get("reply") if isinstance(result, dict) else result
        except FluentRestError as exc:
            elapsed = time.monotonic() - start
            if (
                exc.status == 400
                and "Fluent not running" in str(exc)
                and elapsed < _SOLVER_READY_TIMEOUT
            ):
                logger.debug(
                    "Solver not ready yet (400 Fluent not running) — "
                    "retrying in %ds (elapsed=%.0fs / %ds)...",
                    _SOLVER_RETRY_DELAY,
                    elapsed,
                    _SOLVER_READY_TIMEOUT,
                )
                time.sleep(_SOLVER_RETRY_DELAY)
                continue
            raise

@staticmethod
def _encode_path(path: str) -> str:
    ""Percent-encode each segment of a slash-delimited path.

    Fluent object names may contain URL-sensitive characters such as
    spaces, ``#``, ``?``, or ``%``.  Each segment is individually
    quoted so the resulting URL is always valid.
    ""
    return "/".join(urllib.parse.quote(seg, safe="") for seg in path.split("/"))
```

There is a lot happening here. We will move through it gradually.

---

## A Contrast Hidden in Plain Sight

Look at the inside of `_execute`. It builds a URL to post to. In doing so it encodes both a `path` and a `name`. Here is how each is handled:

```python
encoded_name = urllib.parse.quote(name, safe="")
result = self._request(
    "POST",
    f"{self._api_base}/{self._encode_path(path)}/{encoded_name}",
    ...
)
```

The `path` is encoded by calling `self._encode_path(path)`. The `name` is encoded inline using `urllib.parse.quote(name, safe="")`.

These two lines do conceptually identical things — they encode a URL component so that special characters are safe to transmit. But they do it at two completely different levels of abstraction. `_encode_path` is named after what it means. `urllib.parse.quote` is named after what it does mechanically.

When you read `self._encode_path(path)`, you read intent. The name tells you the purpose of the call; you do not need to understand its implementation to understand the code around it. You can immediately ask: does encoding the path make sense here? Is it the right thing to do? You are reading version 2 alongside version 1, and that makes version 3 — correctness — something you can evaluate.

When you read `urllib.parse.quote(name, safe="")`, you have no such luxury. The name of the function tells you about its implementation: it percent-encodes a string. It tells you nothing about why it is being called here. To understand its purpose, you must read the lines around it, understand what `name` represents in this context, figure out that it is a URL component that needs to be safe-transmitted, and only then can you reconstruct the intent. The reader is forced to induce the intention from the surrounding code rather than read it directly. This is how code becomes hard to read: not because any individual line is complex, but because the reader carries the burden of perpetually reconstructing intent that was never written down.

The fix is straightforward: extract a method named after the intention.

```python
encoded_name = self._encode_name(name)
```

This single rename closes the gap. Now both the path and the name are encoded through methods that name the operation at the same conceptual level as everything around them.

The deeper lesson here is that `_encode_path` already existed, which means the author already knew how to write at the right level. The inconsistency is a sign that SLAP violations tend to be accidental and local rather than a matter of principle. They slip in line by line, and each one individually seems harmless. The damage accumulates.

---

## When a Three-Part Condition Tells You Three Different Things

Now look at the retry logic inside `_execute`:

```python
if (
    exc.status == 400
    and "Fluent not running" in str(exc)
    and elapsed < _SOLVER_READY_TIMEOUT
):
```

This condition has three clauses. They are not three equal parts of one idea. The first two are about the exception — what kind of error occurred. The third is about time — whether we are still within the window where retrying is worth attempting. These are two entirely separate concerns packed into one expression with `and`.

When a reader encounters this, they must do two things at once: understand the semantics of the error, and understand the continuation policy. They also have to notice — without any guidance from the code — that the first two clauses are related to each other and the third is separate. This mental overhead is exactly what SLAP violations cost: not confusion about any one line, but the constant overhead of performing the author's reasoning work on their behalf.

The remedy is to make the structure visible by naming the concerns separately:

```python
if (
    _error_allows_retry(exc)
    and _within_retry_deadline(elapsed)
):
```

Now the structure is explicit. There are two concerns. One is about the error; one is about time. They can be understood and evaluated independently.

We can raise the level one step further:

```python
if _should_retry(exc, elapsed):
```

This reads like a policy decision, which is exactly what it is. The implementation of that decision lives elsewhere, in functions that can be read, understood, and tested in isolation:

```python
def _should_retry(exc, elapsed):
    return _error_allows_retry(exc) and _within_retry_deadline(elapsed)

def _error_allows_retry(exc):
    return _error_means_bad_request(exc) and _error_means_fluent_not_running(exc)

def _within_retry_deadline(elapsed):
    return elapsed < _SOLVER_READY_TIMEOUT

def _error_means_bad_request(exc):
    return exc.status == 400

def _error_means_fluent_not_running(exc):
    return "Fluent not running" in str(exc)
```

Notice what happened to `_error_allows_retry`. It retries if the error is a bad request (`400`) **and** if Fluent is not running. Read that aloud: *we retry if the request was bad and Fluent is not running*. Does that make sense? The combination is at least worth questioning — and it can now be questioned, because the logic is readable for the first time. This is a significant outcome: by raising the conceptual level, we have made a potentially dubious business rule visible, where before it was buried inside an inscrutable compound condition. Raising the abstraction level does not just improve readability; it enables code review.

A word on naming. An intermediate version of the bad-request check might be called `_error_is_400`. This name fails to raise the conceptual level because it simply restates the implementation in words. Renaming it `_error_means_bad_request` is what closes the gap. The name now carries the semantic intent — a 400 status code means the server considers the request malformed — rather than just mirroring the numeric literal. Naming is not a cosmetic activity. It is the primary mechanism by which intent is made visible.

---

## Comments: A Symptom, Not a Cure

There is a comment on the `except` block in the original `exit` method:

```python
except Exception:
    pass  # nosec B110 - server drops the connection on exit — expected
```

This comment is doing important work. It is explaining why a broad, silent exception catch is acceptable. Without it, any reader would rightfully be alarmed: swallowing all exceptions is one of the most dangerous patterns in Python. The comment is necessary precisely because the code does not say what it means.

This is a common pattern. Code written at a low conceptual level is routinely accompanied by explanatory comments, because the code itself cannot bear the weight of communicating its purpose. The comments fill the gap. This feels like a solution, but it is not. It adds clutter — now there is more text to read, more to maintain. Comments drift. Code changes and comments go unupdated. There is no mechanism that keeps a comment synchronised with the code it describes the way a function name is inseparable from its implementation. A comment is a promise the codebase cannot enforce.

The real solution is to write code that does not need the comment. We will see exactly how to do that for this case shortly.

---

## Testability as a Natural Consequence

The five functions produced by the retry-condition refactor — `_should_retry`, `_error_allows_retry`, `_within_retry_deadline`, `_error_means_bad_request`, `_error_means_fluent_not_running` — share a useful property: each one can be tested in complete isolation.

Before the refactor, the logic `exc.status == 400 and "Fluent not running" in str(exc)` could only be tested by constructing an entire scenario involving `_execute`, a mock HTTP layer, and a manufactured exception. The logic was tangled up with the retry loop, the timeout logic, and the sleep. Writing a test for it was expensive enough that it probably would not be written at all.

After the refactor, testing whether a given exception allows a retry is a two-line test that constructs a mock exception and calls `_error_allows_retry`. The act of naming the logic and extracting it into a function makes it independently reachable by tests.

This is not a coincidence. Kent Beck's rules of simple design place these properties in order of priority:

1. All the tests pass.
2. There is no duplication.
3. The code expresses the intent of the programmer.
4. Classes and methods are minimised.

These rules are not independent of each other. Code that expresses intent at a consistent conceptual level tends to be naturally modular and naturally testable. SLAP is one of the primary mechanisms by which rule 3 is achieved. When rule 3 is satisfied, rule 1 becomes much easier to satisfy too.

---

## How Abstraction Failures Propagate: The `exit` Method

The problems in `_execute` are not contained within `_execute`. They propagate upward into `exit`, which calls it. This is how abstraction failures compound.

Look at `exit` again:

```python
def exit(self) -> None:
    if self._is_closed:
        raise FluentServerShutdown("Session is already closed.")
    try:
        self._execute("/", "exit")
    except Exception:
        pass  # nosec B110 - server drops the connection on exit — expected
    self._is_closed = True
    logger.info("Fluent server exited.")
```

`_execute` is a general-purpose dispatcher. Its name says: I execute things. It accepts arbitrary string paths and names. It is a low-level tool designed to forward any request to the server. Using it inside `exit` — a method with a very specific, high-level purpose — imports all of `_execute`'s low-level character into `exit`. The call site `self._execute("/", "exit")` does not say *send an exit request to the server*. It says *post something to the path `/` with the name `"exit"`*. The reader must do the translation.

The exception handling is worse. `except Exception` catches everything. It was placed here because, as the comment explains, the Fluent server drops the connection when it shuts down, and that drop manifests as an exception. But because the exception type is unspecified, this handler would also silently swallow network errors, programming errors, and any other unexpected failure. And here is the real danger: `self._is_closed = True` is set unconditionally after that broad catch. If `_execute` raises for any reason other than a connection drop, the code will still mark the session as closed. A subsequent caller attempting `exit` will receive `FluentServerShutdown("Session is already closed.")` even though the server never actually shut down. The server becomes unkillable.

This is a direct consequence of operating at the wrong abstraction level. The intent — handle the expected connection drop, propagate everything else — cannot be implemented correctly when the exception type carries no semantic information. `Exception` is too broad to be the basis of a strategic decision.

---

## Raising the Level of `exit`: Step by Step

The first step is to introduce a method that expresses the specific intent: sending an exit request.

```python
def exit(self) -> None:
    if self._is_closed:
        raise ServerAlreadyShutDown()
    try:
        self._sendExitRequest()
    except ServerDroppedConnectionOnExit:
        pass  # nosec B110 - server drops the connection on exit — expected
    finally:
        self._is_closed = True
    logger.info("Fluent server exited.")
```

Several things have changed. `_execute("/", "exit")` has become `self._sendExitRequest()`. The name now says what the call is for. `FluentServerShutdown("Session is already closed.")` has become `ServerAlreadyShutDown()`. The name now says what the condition means, and the string message is redundant — the type is the documentation. Most importantly, `except Exception` has become `except ServerDroppedConnectionOnExit`. The handler now catches only the specific, named condition it was designed for. Any other exception will propagate, which is correct behaviour. `finally` ensures `_is_closed` is set regardless of outcome, which prevents the unkillable-server bug.

But the comment is still there. That `# nosec B110` annotation is still telling us something we should not need to be told: that a connection drop is expected. This is a detail of the exit transaction — it belongs inside `_sendExitRequest`, not leaked into the method that calls it. The fix is to encapsulate it:

```python
def exit(self) -> None:
    if self._is_closed:
        raise ServerAlreadyShutDown()
    self._sendExitRequest()
    self._is_closed = True
    logger.info("Fluent server exited.")
```

`_sendExitRequest` absorbs the knowledge that a connection drop is expected and handles it internally. `exit` no longer needs to know about it. The comment is gone — not because we deleted it, but because the information it contained has been encoded into the structure of the code itself. This is the ideal outcome: intent expressed through names and structure rather than through annotations layered on top of unclear code.

Read this final version of `exit` from top to bottom:

1. If the session is already closed, raise an error that says so.
2. Send the exit request.
3. Mark the session as closed.
4. Log that the server exited.

Every line is at the same conceptual level: the level of *what is happening in a shutdown sequence*. There is no URL encoding, no HTTP status codes, no connection-drop mechanics. Those things exist, but they live at the level where they belong. Here, the reader can see version 1 and version 2 simultaneously — what was written and what was intended — and can therefore form an opinion about version 3.

---

## Summary

The Single Level of Abstraction Principle is not a rule about code organisation for its own sake. It is a rule about communication. Code is read far more often than it is written. Every time a developer reads a function, they are trying to reconstruct what the author intended, and every low-level detail that intrudes on a high-level narrative forces them to do that reconstruction work themselves.

The concrete costs are:

- **Readability**: a reader must induce intent rather than read it, which is slower and error-prone.
- **Reviewability**: logic buried inside compound expressions or broad exception handlers cannot be evaluated for correctness until it is first decoded.
- **Maintainability**: code changed without full understanding of intent produces bugs. Comments that attempted to compensate for the lack of clarity go stale.
- **Testability**: logic entangled with surrounding mechanics cannot be tested in isolation.
- **Safety**: low-level constructs like `except Exception` carry insufficient information to make correct high-level decisions, which leads directly to bugs.

The remedies are equally concrete: extract methods named after what they mean rather than what they do, name exceptions after the conditions they represent, and ensure that every line in a function speaks the same language as the lines around it.

When code is written at a consistent level of abstraction, intent becomes legible. And when intent is legible, correctness can be debated — which is, ultimately, the only way to know whether what was written is what should have been written.

"""