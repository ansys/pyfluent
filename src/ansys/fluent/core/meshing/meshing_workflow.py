"""Meshing workflow specialization of the Workflow module that wraps and extends the
core functionality."""


from __future__ import annotations

from typing import Optional

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

    def watertight(self, dynamic_interface: bool) -> None:
        """Initialize a watertight workflow.

        Parameters
        ----------
        dynamic_interface : bool
            Flag to expose object-oriented behaviour.
        """

        self._new_workflow(
            name="Watertight Geometry", dynamic_interface=dynamic_interface
        )


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

    def fault_tolerant(self, dynamic_interface: bool):
        """Initialize a fault-tolerant workflow.

        Parameters
        ----------
        dynamic_interface : bool
            Flag to expose object-oriented behaviour.
        """
        self._new_workflow(
            "Fault-tolerant Meshing", dynamic_interface=dynamic_interface
        )

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
