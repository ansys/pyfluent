"""Run the independent shared-folder snapshot consumer.

Example:
    python examples/poll_shared_snapshots.py --shared results/poc/shared \
        --destination results/poc/snapshots
"""

from __future__ import annotations

import argparse
from pathlib import Path
import threading

from fvm.externalization import SharedFolderPoller


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Poll a shared snapshot directory and externalize new steps."
    )
    parser.add_argument("--shared", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--interval", type=float, default=1.0)
    arguments = parser.parse_args()
    if arguments.interval <= 0.0:
        parser.error("--interval must be positive")

    poller = SharedFolderPoller(arguments.shared, arguments.destination)
    stop = threading.Event()
    try:
        poller.run(arguments.interval, stop)
    except KeyboardInterrupt:
        stop.set()
        poller.poll_once()
    print(
        f"Externalized {poller.snapshots} snapshots "
        f"({poller.bytes_written} bytes)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
