import socket


def get_free_port() -> int:
    """Identifies a free port to which a new socket connection can be
    established.

    Returns
    -------
    int
        port number
    """
    sock = socket.socket()
    sock.bind(("", 0))
    return sock.getsockname()[1]