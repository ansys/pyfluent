"""Transport-neutral step snapshots and pluggable result externalizers."""

from .model import StepSnapshot
from .store import SnapshotStore
from .grpc_transport import GrpcExternalizer, GrpcSnapshotServer
from .visualization import LiveSnapshotPlotter, plot_latest_snapshot, plot_snapshot
from .strategies import (
    AsyncFileExternalizer,
    ExternalizationMetrics,
    SharedFolderExternalizer,
    SharedFolderPoller,
    StepSnapshotObserver,
    SynchronousFileExternalizer,
    create_step_observer,
)

__all__ = [
    "AsyncFileExternalizer",
    "ExternalizationMetrics",
    "GrpcExternalizer",
    "GrpcSnapshotServer",
    "LiveSnapshotPlotter",
    "SharedFolderExternalizer",
    "SharedFolderPoller",
    "SnapshotStore",
    "StepSnapshot",
    "StepSnapshotObserver",
    "SynchronousFileExternalizer",
    "create_step_observer",
    "plot_latest_snapshot",
    "plot_snapshot",
]
