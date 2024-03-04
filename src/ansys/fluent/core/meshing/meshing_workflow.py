"""Meshing workflow specialization of the Workflow module that wraps and extends the
core functionality."""

from __future__ import annotations

from typing import Optional

from ansys.fluent.core.services.datamodel_se import PyMenuGeneric
from ansys.fluent.core.workflow import ClassicWorkflow, Workflow


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


class MeshingWorkflow(Workflow):
    """Provides meshing specialization of the workflow wrapper that extends the core
    functionality in an object-oriented manner."""

    def __init__(
        self,
        workflow: PyMenuGeneric,
        meshing: PyMenuGeneric,
    ) -> None:
        """Initialize MeshingWorkflow.

        Parameters
        ----------
        workflow : PyMenuGeneric
            Underlying workflow object.
        meshing : PyMenuGeneric
            The meshing object.
        """
        super().__init__(workflow=workflow, command_source=meshing)


class WatertightMeshingWorkflow(MeshingWorkflow):
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
        self._meshing = meshing

    def reinitialize(self) -> None:
        """Initialize a watertight workflow."""
        self._new_workflow(name="Watertight Geometry")

    def __getattribute__(self, item: str):
        if (
            item != "reinitialize"
            and not item.startswith("_")
            and not self._meshing.GlobalSettings.EnableCleanCAD()
        ):
            raise RuntimeError(
                "'Watertight' objects are inaccessible from 'Fault-tolerant' workflow."
            )
        return super().__getattribute__(item)


class FaultTolerantMeshingWorkflow(MeshingWorkflow):
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
        self._meshing = meshing
        self._part_management = part_management
        self._pm_file_management = pm_file_management

    def reinitialize(self):
        """Initialize a fault-tolerant workflow."""
        self._new_workflow("Fault-tolerant Meshing")

    def __getattribute__(self, item):
        if (
            item != "reinitialize"
            and not item.startswith("_")
            and not self._meshing.GlobalSettings.EnableComplexMeshing()
        ):
            raise RuntimeError(
                "'Fault-tolerant' objects are inaccessible from 'Watertight' workflow."
            )
        return super().__getattribute__(item)

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
