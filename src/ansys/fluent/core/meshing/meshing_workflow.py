"""Meshing workflow specialization of the Workflow module that wraps and extends the
core functionality."""


from __future__ import annotations

from typing import Optional

import ansys.fluent.core.launcher as launcher
from ansys.fluent.core.services.datamodel_se import PyMenuGeneric
from ansys.fluent.core.workflow import ClassicWorkflow, EnhancedWorkflow


class ClassicMeshingWorkflow(ClassicWorkflow):
    """Provides meshing specialization of the workflow wrapper."""

    def __init__(
        self,
        workflow: PyMenuGeneric,
        meshing: PyMenuGeneric,
    ) -> None:
        """Initialize ClassicMeshingWorkflow.

        Parameters
        ----------
        workflow : PyMenuGeneric
            Underlying workflow object.
        meshing : PyMenuGeneric
            Meshing object.
        """
        super().__init__(workflow=workflow, command_source=meshing)


class EnhancedMeshingWorkflow(EnhancedWorkflow):
    """Provides meshing specialization of the workflow wrapper that extends the core
    functionality in an object-oriented manner."""

    def __init__(
        self,
        workflow: PyMenuGeneric,
        meshing: PyMenuGeneric,
    ) -> None:
        """Initialize EnhancedMeshingWorkflow.

        Parameters
        ----------
        workflow : PyMenuGeneric
            Underlying workflow object.
        meshing : PyMenuGeneric
            The meshing object.
        """
        super().__init__(workflow=workflow, command_source=meshing)

    @staticmethod
    def pyfluent_launch_code(is_ftm, **launch_args):
        if "dynamic_interface" in launch_args:
            del launch_args["dynamic_interface"]
        if "session" in launch_args:
            session = launch_args["session"]
        else:
            args = dict(mode=launcher.launcher_utils.FluentMode.PURE_MESHING_MODE)
            args.update(launch_args)
            try:
                session = launcher.launcher.launch_fluent(**args)
            except Exception:
                args["mode"] = launcher.launcher_utils.FluentMode.MESHING_MODE
                session = launcher.launcher.launch_fluent(**args)
        if is_ftm:
            return session.fault_tolerant()
        else:
            return session.watertight()


class WatertightMeshingWorkflow(EnhancedMeshingWorkflow):
    """Provides watertight meshing specialization of the workflow wrapper."""

    def __init__(self, workflow: PyMenuGeneric, meshing: PyMenuGeneric) -> None:
        """Initialize WatertightMeshingWorkflow.

        Parameters
        ----------
        workflow : PyMenuGeneric
            The underlying workflow object.
        meshing : PyMenuGeneric
            The meshing object.
        """
        super().__init__(workflow=workflow, meshing=meshing)

    def reinitialize(self) -> None:
        """Initialize a watertight workflow."""
        self._new_workflow(name="Watertight Geometry")


class FaultTolerantMeshingWorkflow(EnhancedMeshingWorkflow):
    """Provides fault-tolerant meshing specialization of the workflow wrapper."""

    def __init__(
        self,
        workflow: PyMenuGeneric,
        meshing: PyMenuGeneric,
        part_management: PyMenuGeneric,
        pm_file_management: PyMenuGeneric,
    ) -> None:
        """Initialize FaultTolerantMeshingWorkflow.

        Parameters
        ----------
        workflow : PyMenuGeneric
            The underlying workflow object.
        meshing : PyMenuGeneric
            The meshing object.
        part_management : PyMenuGeneric
            The part-management object.
        pm_file_management : PyMenuGeneric
            The part-management file-management object.
        """
        super().__init__(workflow=workflow, meshing=meshing)
        self._part_management = part_management
        self._pm_file_management = pm_file_management

    def reinitialize(self):
        """Initialize a fault-tolerant workflow."""
        self._new_workflow("Fault-tolerant Meshing")

    @property
    def part_management(self) -> Optional[PyMenuGeneric]:
        """Access part-management in fault-tolerant mode.

        Returns
        -------
        Optional[PyMenuGeneric]
            Part-management.
        """
        return self._part_management

    @property
    def pm_file_management(self):
        """Access the part-management file-management object in fault-tolerant mode.

        Returns
        -------
        Optional[PyMenuGeneric]
            Part-management file-management object .
        """
        return self._pm_file_management
