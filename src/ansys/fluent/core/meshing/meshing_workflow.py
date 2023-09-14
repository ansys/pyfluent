"""Meshing workflow specialization of the Workflow module that wraps and extends the core functionality."""


from __future__ import annotations

from typing import Optional

from ansys.fluent.core.workflow import WorkflowWrapper


class MeshingWorkflow(WorkflowWrapper):
    """Meshing specialization of the WorkflowWrapper that extends the core functionality."""

    def __init__(
        self,
        workflow: PyMenuGeneric,
        meshing: PyMenuGeneric,
        part_management: PyMenuGeneric,
        pm_file_management: PyMenuGeneric,
    ) -> None:
        """Initialize MeshingWorkflow.

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
        super().__init__(workflow=workflow, command_source=meshing)
        self._is_ftm = False
        self._part_management = part_management
        self._pm_file_management = pm_file_management

    def watertight(self, dynamic_interface: bool) -> None:
        """Initialize a watertight workflow.

        Parameters
        ----------
        dynamic_interface : bool
            xxx
        """

        self._new_workflow(
            name="Watertight Geometry", dynamic_interface=dynamic_interface
        )
        self._is_ftm = False

    def fault_tolerant(self, dynamic_interface: bool):
        """Initialize a fault-tolerant workflow.

        Parameters
        ----------
        dynamic_interface : bool
            xxx
        """
        self._new_workflow(
            "Fault-tolerant Meshing", dynamic_interface=dynamic_interface
        )
        self._is_ftm = True

    @property
    def part_management(self) -> Optional[PyMenuGeneric]:
        """Access part-management in fault-tolerant mode.

        Returns
        -------
        Optional[PyMenuGeneric]
            Part-management.
        """
        if self._is_ftm:
            return self._part_management

    @property
    def pm_file_management(self):
        """Access the part-management file-management object in fault-tolerant mode.

        Returns
        -------
        Optional[PyMenuGeneric]
            Part-management file-management object .
        """
        if self._is_ftm:
            return self._pm_file_management
