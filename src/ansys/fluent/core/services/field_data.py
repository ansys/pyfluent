# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
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

"""Wrappers over FieldData gRPC service of Fluent."""
from dataclasses import dataclass, field
from enum import Enum
from functools import reduce
import logging
import time
from typing import Callable, Dict, List, Tuple
import warnings
import weakref

import grpc
import numpy as np

from ansys.api.fluent.v0 import field_data_pb2 as FieldDataProtoModule
from ansys.api.fluent.v0 import field_data_pb2_grpc as FieldGrpcModule
from ansys.fluent.core.exceptions import DisallowedValuesError
from ansys.fluent.core.field_data_interfaces import (
    BaseFieldDataSource,
    BaseFieldInfo,
    FieldDataSource,
    FieldTransaction,
    PathlinesFieldDataRequest,
    ScalarFieldDataRequest,
    SurfaceDataType,
    SurfaceFieldDataRequest,
    VectorFieldDataRequest,
    _AllowedScalarFieldNames,
    _AllowedSurfaceIDs,
    _AllowedSurfaceNames,
    _AllowedVectorFieldNames,
    _ReturnFieldData,
)
from ansys.fluent.core.pyfluent_warnings import PyFluentDeprecationWarning
from ansys.fluent.core.services.interceptors import (
    BatchInterceptor,
    ErrorStateInterceptor,
    GrpcErrorInterceptor,
    TracingInterceptor,
)
from ansys.fluent.core.services.streaming import StreamingService
from ansys.fluent.core.utils.deprecate import deprecate_argument, deprecate_arguments

logger = logging.getLogger("pyfluent.field_data")


def override_help_text(func, func_to_be_wrapped):
    """Override function help text."""
    if func_to_be_wrapped.__doc__:
        func.__doc__ = "\n" + func_to_be_wrapped.__doc__
    func.__name__ = func_to_be_wrapped.__qualname__
    return func


class FieldDataService(StreamingService):
    """FieldData service of Fluent."""

    def __init__(
        self, channel: grpc.Channel, metadata: List[Tuple[str, str]], fluent_error_state
    ):
        """__init__ method of FieldDataService class."""
        intercept_channel = grpc.intercept_channel(
            channel,
            GrpcErrorInterceptor(),
            ErrorStateInterceptor(fluent_error_state),
            TracingInterceptor(),
            BatchInterceptor(),
        )
        super().__init__(
            stub=FieldGrpcModule.FieldDataStub(intercept_channel), metadata=metadata
        )

    def get_scalar_field_range(self, request):
        """GetRange RPC of FieldData service."""
        return self._stub.GetRange(request, metadata=self._metadata)

    def get_scalar_fields_info(self, request):
        """GetFieldsInfo RPC of FieldData service."""
        return self._stub.GetFieldsInfo(request, metadata=self._metadata)

    def get_vector_fields_info(self, request):
        """GetVectorFieldsInfo RPC of FieldData service."""
        return self._stub.GetVectorFieldsInfo(request, metadata=self._metadata)

    def get_surfaces_info(self, request):
        """GetSurfacesInfo RPC of FieldData service."""
        return self._stub.GetSurfacesInfo(request, metadata=self._metadata)

    def get_fields(self, request):
        """GetFields RPC of FieldData service.

        Raises
        ------
        RuntimeError
            If an empty chunk encountered during field extraction.
        """
        chunk_iterator = self._stub.GetFields(request, metadata=self._metadata)
        if not chunk_iterator.is_active():
            raise RuntimeError(
                "Unexpectedly encountered empty chunk during field extraction."
            )
        return chunk_iterator

    def get_solver_mesh_nodes_float(
        self, request: FieldDataProtoModule.GetSolverMeshNodesRequest
    ):
        """GetSolverMeshNodesFloat RPC of FieldData service."""
        responses = self._stub.GetSolverMeshNodesFloat(request, metadata=self._metadata)
        nested_nodes = []
        for response in responses:
            nested_nodes.append(response.nodes)
        return nested_nodes

    def get_solver_mesh_nodes_double(
        self, request: FieldDataProtoModule.GetSolverMeshNodesRequest
    ):
        """GetSolverMeshNodesDouble RPC of FieldData service."""
        responses = self._stub.GetSolverMeshNodesDouble(
            request, metadata=self._metadata
        )
        nested_nodes = []
        for response in responses:
            nested_nodes.append(response.nodes)
        return nested_nodes

    def get_solver_mesh_elements(
        self, request: FieldDataProtoModule.GetSolverMeshElementsRequest
    ):
        """GetSolverMeshElements RPC of FieldData service."""
        responses = self._stub.GetSolverMeshElements(request, metadata=self._metadata)
        elementss = []
        for response in responses:
            elementss.append(response.elements)
        return elementss


class FieldInfo(BaseFieldInfo):
    """Provides access to Fluent field information.

    Methods
    -------
    get_scalar_field_range(field: str, node_value: bool, surface_ids: List[int])
    -> List[float]
        Get the range (minimum and maximum values) of the field.

    get_scalar_fields_info(self) -> dict
        Get fields information (field name, domain, and section).

    get_vector_fields_info(self) -> dict
        Get vector fields information.

    get_surfaces_info(self) -> dict
        Get surfaces information (surface name, ID, and type).
    """

    def __init__(
        self,
        service: FieldDataService,
        is_data_valid: Callable[[], bool],
    ):
        """__init__ method of FieldInfo class."""
        self._service = service
        self._is_data_valid = is_data_valid

    def get_scalar_field_range(
        self, field: str, node_value: bool = False, surface_ids: List[int] = None
    ) -> List[float]:
        """Get the range (minimum and maximum values) of the field.

        Parameters
        ----------
        field: str
            Field name
        node_value: bool
        surface_ids : List[int], optional
            List of surface IDS for the surface data.

        Returns
        -------
        List[float]
        """
        if not surface_ids:
            surface_ids = []
        request = FieldDataProtoModule.GetRangeRequest()
        request.fieldName = field
        request.nodeValue = node_value
        request.surfaceid.extend(
            [FieldDataProtoModule.SurfaceId(id=int(id)) for id in surface_ids]
        )
        response = self._service.get_scalar_field_range(request)
        return [response.minimum, response.maximum]

    def get_scalar_fields_info(self) -> Dict[str, Dict]:
        """Get fields information (field name, domain, and section).

        Returns
        -------
        Dict
        """
        request = FieldDataProtoModule.GetFieldsInfoRequest()
        response = self._service.get_scalar_fields_info(request)
        return {
            field_info.solverName: {
                "display_name": field_info.displayName,
                "section": field_info.section,
                "domain": field_info.domain,
                "quantity_name": field_info.quantity_name,
            }
            for field_info in response.fieldInfo
        }

    def get_vector_fields_info(self) -> Dict[str, Dict]:
        """Get vector fields information (vector components).

        Returns
        -------
        Dict
        """
        request = FieldDataProtoModule.GetVectorFieldsInfoRequest()
        response = self._service.get_vector_fields_info(request)
        return {
            vector_field_info.displayName: {
                "x-component": vector_field_info.xComponent,
                "y-component": vector_field_info.yComponent,
                "z-component": vector_field_info.zComponent,
            }
            for vector_field_info in response.vectorFieldInfo
        }

    def get_surfaces_info(self) -> Dict[str, Dict]:
        """Get surfaces information (surface name, ID, and type).

        Returns
        -------
        Dict
        """
        request = FieldDataProtoModule.GetSurfacesInfoResponse()
        response = self._service.get_surfaces_info(request)
        info = {
            surface_info.surfaceName: {
                "surface_id": [surf.id for surf in surface_info.surfaceId],
                "zone_id": surface_info.zoneId.id,
                "zone_type": surface_info.zoneType,
                "type": surface_info.type,
            }
            for surface_info in response.surfaceInfo
        }
        return info

    def validate_scalar_fields(self, field_name: str):
        """Validate scalar fields."""
        _AllowedScalarFieldNames(
            self._is_data_valid, info=self.get_scalar_fields_info()
        ).valid_name(field_name)

    def validate_vector_fields(self, field_name: str):
        """Validate vector fields."""
        _AllowedVectorFieldNames(
            self._is_data_valid, info=self.get_vector_fields_info()
        ).valid_name(field_name)

    def validate_surfaces(self, surfaces: List[str]):
        """Validate surfaces."""
        for surface in surfaces:
            _AllowedSurfaceNames(info=self.get_surfaces_info()).valid_name(surface)


class _FieldMethod:
    class _Arg:
        def __init__(self, accessor):
            self._accessor = accessor

        def allowed_values(self):
            """Returns set of allowed values."""
            return sorted(self._accessor())

    def __init__(self, field_data_accessor, args_allowed_values_accessors):
        self._field_data_accessor = field_data_accessor
        for arg_name, accessor in args_allowed_values_accessors.items():
            setattr(self, arg_name, _FieldMethod._Arg(accessor))

    def __call__(self, *args, **kwargs):
        return self._field_data_accessor(*args, **kwargs)


def _data_type_convertor(args_dict):
    d_type_list = []
    d_type_map = {
        "provide_vertices": SurfaceDataType.Vertices,
        "provide_faces": SurfaceDataType.FacesConnectivity,
        "provide_faces_centroid": SurfaceDataType.FacesCentroid,
        "provide_faces_normal": SurfaceDataType.FacesNormal,
    }
    for key, val in d_type_map.items():
        if args_dict.get(key):
            d_type_list.append(val)
        args_dict.pop(key, None)
    if args_dict.get("data_types") is None:
        args_dict["data_types"] = d_type_list
    return args_dict


class _FetchFieldData:

    @staticmethod
    def _surface_data(
        data_types: List[SurfaceDataType] | List[str],
        surface_ids: List[int],
        overset_mesh: bool | None = False,
    ):
        return [
            FieldDataProtoModule.SurfaceRequest(
                surfaceId=surface_id,
                oversetMesh=overset_mesh,
                provideFaces=SurfaceDataType.FacesConnectivity in data_types,
                provideVertices=SurfaceDataType.Vertices in data_types,
                provideFacesCentroid=SurfaceDataType.FacesCentroid in data_types,
                provideFacesNormal=SurfaceDataType.FacesNormal in data_types,
            )
            for surface_id in surface_ids
        ]

    @staticmethod
    def _scalar_data(
        field_name: str,
        surface_ids: List[int],
        node_value: bool,
        boundary_value: bool,
    ):
        return [
            FieldDataProtoModule.ScalarFieldRequest(
                surfaceId=surface_id,
                scalarFieldName=field_name,
                dataLocation=(
                    FieldDataProtoModule.DataLocation.Nodes
                    if node_value
                    else FieldDataProtoModule.DataLocation.Elements
                ),
                provideBoundaryValues=boundary_value,
            )
            for surface_id in surface_ids
        ]

    @staticmethod
    def _vector_data(
        field_name: str,
        surface_ids: List[int],
    ):
        return [
            FieldDataProtoModule.VectorFieldRequest(
                surfaceId=surface_id, vectorFieldName=field_name
            )
            for surface_id in surface_ids
        ]

    @staticmethod
    def _pathlines_data(
        field_name: str,
        surface_ids: List[int],
        **kwargs,
    ):
        return [
            FieldDataProtoModule.PathlinesFieldRequest(
                surfaceId=surface_id,
                field=field_name,
                **kwargs,
            )
            for surface_id in surface_ids
        ]


class BaseFieldData:
    """The base field data interface."""

    def __init__(
        self,
        data: Dict,
        field_info,
        allowed_surface_names,
        allowed_scalar_field_names,
    ):
        """__init__ method of BaseFieldData class."""
        self.data = data
        self._field_info = field_info
        self._allowed_surface_names = allowed_surface_names
        self._allowed_scalar_field_names = allowed_scalar_field_names
        self._returned_data = _ReturnFieldData()
        self._deprecated_flag = False

    def get_surface_ids(self, surfaces: List[str | int]) -> List[int]:
        """Get a list of surface ids based on surfaces provided as inputs."""
        return _get_surface_ids(
            field_info=self._field_info,
            allowed_surface_names=self._allowed_surface_names,
            surfaces=surfaces,
        )

    def _get_scalar_field_data(
        self,
        **kwargs,
    ) -> Dict[int | str, np.array]:
        scalar_field_data = self.data[
            (
                ("type", "scalar-field"),
                ("dataLocation", 0 if kwargs.get("node_value") else 1),
                ("boundaryValues", kwargs.get("boundary_value")),
            )
        ]
        return self._returned_data._scalar_data(
            kwargs.get("field_name"),
            kwargs.get("surfaces"),
            self.get_surface_ids(kwargs.get("surfaces")),
            scalar_field_data,
        )

    def _get_surface_data(
        self,
        **kwargs,
    ) -> Dict[int | str, Dict[SurfaceDataType, np.array | List[np.array]]]:
        surface_data = self.data[(("type", "surface-data"),)]
        return self._returned_data._surface_data(
            kwargs.get("data_types"),
            kwargs.get("surfaces"),
            self.get_surface_ids(kwargs.get("surfaces")),
            surface_data,
        )

    def _get_vector_field_data(
        self,
        **kwargs,
    ) -> Dict[int | str, np.array]:
        vector_field_data = self.data[(("type", "vector-field"),)]
        return self._returned_data._vector_data(
            kwargs.get("field_name"),
            kwargs.get("surfaces"),
            self.get_surface_ids(kwargs.get("surfaces")),
            vector_field_data,
        )

    def _get_pathlines_field_data(
        self,
        **kwargs,
    ) -> Dict:
        if kwargs.get("zones") is None:
            zones = []
        del zones
        pathlines_data = self.data[
            (("type", "pathlines-field"), ("field", kwargs.get("field_name")))
        ]
        return self._returned_data._pathlines_data(
            kwargs.get("field_name"),
            kwargs.get("surfaces"),
            self.get_surface_ids(kwargs.get("surfaces")),
            pathlines_data,
        )

    def get_field_data(
        self,
        obj: (
            SurfaceFieldDataRequest
            | ScalarFieldDataRequest
            | VectorFieldDataRequest
            | PathlinesFieldDataRequest
        ),
    ) -> Dict[int | str, Dict | np.array]:
        """Get the surface, scalar, vector or path-lines field data on a surface."""
        if isinstance(obj, SurfaceFieldDataRequest):
            return self._get_surface_data(**obj._asdict())
        elif isinstance(obj, ScalarFieldDataRequest):
            return self._get_scalar_field_data(**obj._asdict())
        elif isinstance(obj, VectorFieldDataRequest):
            return self._get_vector_field_data(**obj._asdict())
        elif isinstance(obj, PathlinesFieldDataRequest):
            return self._get_pathlines_field_data(**obj._asdict())


class TransactionFieldData(BaseFieldData, BaseFieldDataSource):
    """Provides access to Fluent field data on surfaces collected via transactions."""

    def __init__(
        self,
        data: Dict,
        field_info,
        allowed_surface_names,
        allowed_scalar_field_names,
    ):
        """__init__ method of TransactionFieldData class."""
        super().__init__(
            data, field_info, allowed_surface_names, allowed_scalar_field_names
        )

    def __len__(self):
        return len(self.data)

    def __call__(self):
        return self.data


class Transaction(FieldTransaction):
    """Populates Fluent field data on surfaces."""

    def __init__(
        self,
        service: FieldDataService,
        field_info: FieldInfo,
        allowed_surface_ids,
        allowed_surface_names,
        allowed_scalar_field_names,
        allowed_vector_field_names,
    ):
        """__init__ method of Transaction class."""
        self._service = service
        self._field_info = field_info
        self._fields_request = get_fields_request()

        self._allowed_surface_names = allowed_surface_names
        self._allowed_scalar_field_names = allowed_scalar_field_names
        self._allowed_vector_field_names = allowed_vector_field_names

        surface_args = dict(
            surface_ids=allowed_surface_ids,
            surface_names=self._allowed_surface_names,
        )
        scalar_field_args = {
            **dict(field_name=self._allowed_scalar_field_names),
            **surface_args,
        }
        self.add_scalar_fields_request = override_help_text(
            _FieldMethod(
                field_data_accessor=self.add_scalar_fields_request,
                args_allowed_values_accessors=scalar_field_args,
            ),
            self.add_scalar_fields_request,
        )
        self.add_vector_fields_request = override_help_text(
            _FieldMethod(
                field_data_accessor=self.add_vector_fields_request,
                args_allowed_values_accessors={
                    **dict(field_name=self._allowed_vector_field_names),
                    **surface_args,
                },
            ),
            self.add_vector_fields_request,
        )
        self.add_surfaces_request = override_help_text(
            _FieldMethod(
                field_data_accessor=self.add_surfaces_request,
                args_allowed_values_accessors=surface_args,
            ),
            self.add_surfaces_request,
        )
        self.add_pathlines_fields_request = override_help_text(
            _FieldMethod(
                field_data_accessor=self.add_pathlines_fields_request,
                args_allowed_values_accessors=scalar_field_args,
            ),
            self.add_pathlines_fields_request,
        )

        self._fetched_data = _FetchFieldData()
        self._pathline_field_data = []
        self._cache_requests = []

    def get_surface_ids(self, surfaces: List[str | int]) -> List[int]:
        """Get a list of surface ids based on surfaces provided as inputs."""
        return _get_surface_ids(
            field_info=self._field_info,
            allowed_surface_names=self._allowed_surface_names,
            surfaces=surfaces,
        )

    def _add_surfaces_request(self, **kwargs) -> None:
        updated_data_types = []
        for d_type in kwargs.get("data_types"):
            if isinstance(d_type, str):
                updated_data_types.append(SurfaceDataType(d_type))
            else:
                updated_data_types.append(d_type)
        data_types = updated_data_types
        self._fields_request.surfaceRequest.extend(
            self._fetched_data._surface_data(
                data_types,
                kwargs.get("surfaces"),
                kwargs.get("overset_mesh"),
            )
        )

    def _add_scalar_fields_request(self, **kwargs) -> None:
        self._fields_request.scalarFieldRequest.extend(
            self._fetched_data._scalar_data(
                self._allowed_scalar_field_names.valid_name(kwargs.get("field_name")),
                kwargs.get("surfaces"),
                kwargs.get("node_value"),
                kwargs.get("boundary_value"),
            )
        )

    def _add_vector_fields_request(self, **kwargs) -> None:
        self._fields_request.vectorFieldRequest.extend(
            self._fetched_data._vector_data(
                self._allowed_vector_field_names.valid_name(kwargs.get("field_name")),
                kwargs.get("surfaces"),
            )
        )

    def _add_pathlines_fields_request(
        self,
        **kwargs,
    ) -> None:
        if kwargs.get("zones") is None:
            zones = []
        field_name = self._allowed_scalar_field_names.valid_name(
            kwargs.get("field_name")
        )
        if field_name in self._pathline_field_data:
            raise ValueError("For 'path-lines' `field_name` should be unique.")
        else:
            self._pathline_field_data.append(field_name)
        self._fields_request.pathlinesFieldRequest.extend(
            self._fetched_data._pathlines_data(
                field_name,
                kwargs.get("surfaces"),
                additionalField=kwargs.get("additional_field_name"),
                provideParticleTimeField=kwargs.get("provide_particle_time_field"),
                dataLocation=(
                    FieldDataProtoModule.DataLocation.Nodes
                    if kwargs.get("node_value")
                    else FieldDataProtoModule.DataLocation.Elements
                ),
                steps=kwargs.get("steps"),
                stepSize=kwargs.get("step_size"),
                skip=kwargs.get("skip"),
                reverse=kwargs.get("reverse"),
                accuracyControlOn=kwargs.get("accuracy_control_on"),
                tolerance=kwargs.get("tolerance"),
                coarsen=kwargs.get("coarsen"),
                velocityDomain=kwargs.get("velocity_domain"),
                zones=zones,
            )
        )

    @deprecate_argument(
        old_arg="surface_names",
        new_arg="surfaces",
        converter=lambda old_arg_val: old_arg_val or [],
    )
    @deprecate_argument(
        old_arg="surface_ids",
        new_arg="surfaces",
        converter=lambda old_arg_val: old_arg_val or [],
    )
    @deprecate_arguments(converter=_data_type_convertor)
    def add_surfaces_request(
        self,
        data_types: List[SurfaceDataType] | List[str],
        surfaces: List[int | str],
        overset_mesh: bool | None = False,
    ) -> None:
        """Add request to get surface data (vertices, face connectivity, centroids, and
        normals)."""
        warnings.warn(
            "'add_surfaces_request' is deprecated, use 'add_requests' instead",
            PyFluentDeprecationWarning,
        )
        self._add_surfaces_request(
            data_types=data_types,
            surfaces=self.get_surface_ids(surfaces),
            overset_mesh=overset_mesh,
        )

    @deprecate_argument(
        old_arg="surface_names",
        new_arg="surfaces",
        converter=lambda old_arg_val: old_arg_val or [],
    )
    @deprecate_argument(
        old_arg="surface_ids",
        new_arg="surfaces",
        converter=lambda old_arg_val: old_arg_val or [],
    )
    def add_scalar_fields_request(
        self,
        field_name: str,
        surfaces: List[int | str],
        node_value: bool | None = True,
        boundary_value: bool | None = True,
    ) -> None:
        """Add request to get scalar field data on surfaces."""
        warnings.warn(
            "'add_scalar_fields_request' is deprecated, use 'add_requests' instead",
            PyFluentDeprecationWarning,
        )
        self._add_scalar_fields_request(
            field_name=field_name,
            surfaces=self.get_surface_ids(surfaces),
            node_value=node_value,
            boundary_value=boundary_value,
        )

    @deprecate_argument(
        old_arg="surface_names",
        new_arg="surfaces",
        converter=lambda old_arg_val: old_arg_val or [],
    )
    @deprecate_argument(
        old_arg="surface_ids",
        new_arg="surfaces",
        converter=lambda old_arg_val: old_arg_val or [],
    )
    def add_vector_fields_request(
        self,
        field_name: str,
        surfaces: List[int | str],
    ) -> None:
        """Add request to get vector field data on surfaces."""
        warnings.warn(
            "'add_vector_fields_request' is deprecated, use 'add_requests' instead",
            PyFluentDeprecationWarning,
        )
        self._add_vector_fields_request(
            field_name=field_name, surfaces=self.get_surface_ids(surfaces)
        )

    @deprecate_argument(
        old_arg="surface_names",
        new_arg="surfaces",
        converter=lambda old_arg_val: old_arg_val or [],
    )
    @deprecate_argument(
        old_arg="surface_ids",
        new_arg="surfaces",
        converter=lambda old_arg_val: old_arg_val or [],
    )
    def add_pathlines_fields_request(
        self,
        field_name: str,
        surfaces: List[int | str],
        additional_field_name: str = "",
        provide_particle_time_field: bool | None = False,
        node_value: bool | None = True,
        steps: int | None = 500,
        step_size: float | None = 500,
        skip: int | None = 0,
        reverse: bool | None = False,
        accuracy_control_on: bool | None = False,
        tolerance: float | None = 0.001,
        coarsen: int | None = 1,
        velocity_domain: str | None = "all-phases",
        zones: list | None = None,
    ) -> None:
        """Add request to get path-lines field on surfaces."""
        warnings.warn(
            "'add_pathlines_fields_request' is deprecated, use 'add_requests' instead",
            PyFluentDeprecationWarning,
        )
        self._add_pathlines_fields_request(
            field_name=field_name,
            surfaces=self.get_surface_ids(surfaces),
            additional_field_name=additional_field_name,
            provide_particle_time_field=provide_particle_time_field,
            node_value=node_value,
            steps=steps,
            step_size=step_size,
            skip=skip,
            reverse=reverse,
            accuracy_control_on=accuracy_control_on,
            tolerance=tolerance,
            coarsen=coarsen,
            velocity_domain=velocity_domain,
            zones=zones,
        )

    def add_requests(
        self,
        obj: (
            SurfaceFieldDataRequest
            | ScalarFieldDataRequest
            | VectorFieldDataRequest
            | PathlinesFieldDataRequest
        ),
        *args: SurfaceFieldDataRequest
        | ScalarFieldDataRequest
        | VectorFieldDataRequest
        | PathlinesFieldDataRequest,
    ):
        """
        Add field data requests for surfaces, scalars, vectors, or pathlines.

        This method allows users to specify multiple field data requests, which will
        later be processed when retrieving responses.
        """
        for req in (obj,) + args:
            req = req._replace(surfaces=self.get_surface_ids(req.surfaces))
            if req in self._cache_requests:
                warnings.warn(f"{req._asdict()} is duplicate and being ignored.")
                continue
            elif isinstance(req, SurfaceFieldDataRequest):
                self._add_surfaces_request(
                    data_types=req.data_types,
                    surfaces=req.surfaces,
                    overset_mesh=req.overset_mesh,
                )
            elif isinstance(req, ScalarFieldDataRequest):
                self._add_scalar_fields_request(
                    field_name=req.field_name,
                    surfaces=req.surfaces,
                    node_value=req.node_value,
                    boundary_value=req.boundary_value,
                )
            elif isinstance(req, VectorFieldDataRequest):
                self._add_vector_fields_request(
                    field_name=req.field_name,
                    surfaces=req.surfaces,
                )
            elif isinstance(req, PathlinesFieldDataRequest):
                self._add_pathlines_fields_request(
                    field_name=req.field_name,
                    surfaces=req.surfaces,
                    additional_field_name=req.additional_field_name,
                    provide_particle_time_field=req.provide_particle_time_field,
                    node_value=req.node_value,
                    steps=req.steps,
                    step_size=req.step_size,
                    skip=req.skip,
                    reverse=req.reverse,
                    accuracy_control_on=req.accuracy_control_on,
                    tolerance=req.tolerance,
                    coarsen=req.coarsen,
                    velocity_domain=req.velocity_domain,
                    zones=req.zones,
                )
            self._cache_requests.append(req)
        return self

    def get_fields(self) -> TransactionFieldData:
        """Get data for previously added requests."""
        warnings.warn(
            "'get_fields' is deprecated, use 'get_response' instead",
            PyFluentDeprecationWarning,
        )
        return self.get_response()

    def get_response(self) -> TransactionFieldData:
        """Get data for previously added requests.

        Returns
        -------
        Dict[int, Dict[int, Dict[str, np.array]]]
            Data is returned as dictionary of dictionaries in the following structure:
            tag int | Tuple-> surface_id [int] -> field_name [str] -> field_data[np.array]

            The tag is a tuple for Fluent 2023 R1 or later.
        """
        return TransactionFieldData(
            ChunkParser().extract_fields(
                self._service.get_fields(self._fields_request)
            ),
            self._field_info,
            self._allowed_surface_names,
            self._allowed_scalar_field_names,
        )

    def __call__(self):
        self.get_response()


class _FieldDataConstants:
    """Defines constants for Fluent field data."""

    # data mapping
    proto_field_type_to_np_data_type = {
        FieldDataProtoModule.FieldType.INT_ARRAY: np.int32,
        FieldDataProtoModule.FieldType.LONG_ARRAY: np.int64,
        FieldDataProtoModule.FieldType.FLOAT_ARRAY: np.float32,
        FieldDataProtoModule.FieldType.DOUBLE_ARRAY: np.float64,
    }
    np_data_type_to_proto_field_type = {
        np.int32: FieldDataProtoModule.FieldType.INT_ARRAY,
        np.int64: FieldDataProtoModule.FieldType.LONG_ARRAY,
        np.float32: FieldDataProtoModule.FieldType.FLOAT_ARRAY,
        np.float64: FieldDataProtoModule.FieldType.DOUBLE_ARRAY,
    }
    chunk_size = 256 * 1024
    bytes_stream = True
    payloadTags = {
        FieldDataProtoModule.PayloadTag.OVERSET_MESH: 1,
        FieldDataProtoModule.PayloadTag.ELEMENT_LOCATION: 2,
        FieldDataProtoModule.PayloadTag.NODE_LOCATION: 4,
        FieldDataProtoModule.PayloadTag.BOUNDARY_VALUES: 8,
    }


def _get_surface_ids(
    field_info: FieldInfo,
    allowed_surface_names,
    surfaces: List[int | str],
) -> List[int]:
    """Get surface IDs based on surface names or IDs.

    Parameters
    ----------
    surfaces : List[int] | List[str]
        List of surface IDs or surface names.

    Returns
    -------
    List[int]
    """
    surface_ids = []
    for surf in surfaces:
        if isinstance(surf, str):
            surface_ids.extend(
                field_info.get_surfaces_info()[allowed_surface_names.valid_name(surf)][
                    "surface_id"
                ]
            )
        else:
            allowed_surf_ids = _AllowedSurfaceIDs(field_info)()
            if surf in allowed_surf_ids:
                surface_ids.append(surf)
            else:
                raise DisallowedValuesError("surface", surf, allowed_surf_ids)
    return surface_ids


def get_fields_request():
    """Populates a new field request."""
    return FieldDataProtoModule.GetFieldsRequest(
        provideBytesStream=_FieldDataConstants.bytes_stream,
        chunkSize=_FieldDataConstants.chunk_size,
    )


class ChunkParser:
    """Class for parsing field data stream received from Fluent.

    Parameters
    ----------
    callbacks_provider : object
    The object which can register and unregister callbacks.
    It provides callbacks, which are triggered with following arguments:
        zone_id : int

        field_name : str

        field : numpy array
    """

    def __init__(self, callbacks_provider: object = None):
        """__init__ method of ChunkParser class."""
        self._callbacks_provider = callbacks_provider

    def extract_fields(self, chunk_iterator) -> Dict[int, Dict[str, np.array]]:
        """Extracts field data received from Fluent.

        if callbacks_provider is set then callbacks are triggered with extracted data.
        """

        def _get_tag_for_surface_request():
            return (("type", "surface-data"),)

        def _get_tag_for_vector_field_request():
            return (("type", "vector-field"),)

        def _get_tag_for_scalar_field_request(scalar_field_request):
            return (
                ("type", "scalar-field"),
                ("dataLocation", scalar_field_request.dataLocation),
                ("boundaryValues", scalar_field_request.provideBoundaryValues),
            )

        def _get_tag_for_pathlines_field_request(pathlines_field_request):
            return (
                ("type", "pathlines-field"),
                ("field", pathlines_field_request.field),
            )

        def _extract_field(field_datatype, field_size, chunk_iterator):
            field_arr = np.empty(field_size, dtype=field_datatype)
            field_datatype_item_size = np.dtype(field_datatype).itemsize
            index = 0
            for chunk in chunk_iterator:
                if chunk.bytePayload:
                    count = min(
                        len(chunk.bytePayload) // field_datatype_item_size,
                        field_size - index,
                    )
                    field_arr[index : index + count] = np.frombuffer(
                        chunk.bytePayload, field_datatype, count=count
                    )
                    index += count
                    if index == field_size:
                        return field_arr
                else:
                    payload = (
                        chunk.floatPayload.payload
                        or chunk.intPayload.payload
                        or chunk.doublePayload.payload
                        or chunk.longPayload.payload
                    )
                    count = len(payload)
                    field_arr[index : index + count] = np.fromiter(
                        payload, dtype=field_datatype
                    )
                    index += count
                    if index == field_size:
                        return field_arr

        fields_data = {}
        for chunk in chunk_iterator:
            payload_info = chunk.payloadInfo
            surface_id = payload_info.surfaceId
            field_request_info = payload_info.fieldRequestInfo
            request_type = field_request_info.WhichOneof("request")
            if request_type is not None:
                payload_tag_id = (
                    _get_tag_for_surface_request()
                    if request_type == "surfaceRequest"
                    else (
                        _get_tag_for_scalar_field_request(
                            field_request_info.scalarFieldRequest
                        )
                        if request_type == "scalarFieldRequest"
                        else (
                            _get_tag_for_vector_field_request()
                            if request_type == "vectorFieldRequest"
                            else (
                                _get_tag_for_pathlines_field_request(
                                    field_request_info.pathlinesFieldRequest
                                )
                                if request_type == "pathlinesFieldRequest"
                                else None
                            )
                        )
                    )
                )
            else:
                if self._callbacks_provider is None:
                    payload_tag_id = reduce(
                        lambda x, y: x | y,
                        [
                            _FieldDataConstants.payloadTags[tag]
                            for tag in payload_info.payloadTag
                        ]
                        or [0],
                    )
                else:
                    payload_tag_id = None
            field = None
            if payload_tag_id is not None:
                field = _extract_field(
                    _FieldDataConstants.proto_field_type_to_np_data_type[
                        payload_info.fieldType
                    ],
                    payload_info.fieldSize,
                    chunk_iterator,
                )

            if self._callbacks_provider is not None:
                for callback_data in self._callbacks_provider.callbacks():
                    callback, args, kwargs = callback_data
                    # print('cb', surface_id, payload_info.fieldName)
                    callback(surface_id, payload_info.fieldName, field, *args, **kwargs)
            else:
                payload_data = fields_data.get(payload_tag_id)
                if not payload_data:
                    payload_data = fields_data[payload_tag_id] = {}
                surface_data = payload_data.get(surface_id)
                if surface_data:
                    if payload_info.fieldName in surface_data:
                        surface_data.update(
                            {
                                payload_info.fieldName: np.concatenate(
                                    (surface_data[payload_info.fieldName], field)
                                )
                            }
                        )
                    else:
                        surface_data.update({payload_info.fieldName: field})
                else:
                    payload_data[surface_id] = {payload_info.fieldName: field}
        return fields_data


# Root domain id in Fluent.
ROOT_DOMAIN_ID = 1


class ZoneType(Enum):
    """Zone types for mesh."""

    CELL = 1
    FACE = 2


@dataclass
class ZoneInfo:
    """Zone information for mesh.

    Attributes
    ----------
    _id : int
        Zone ID.
    name : str
        Name of the zone.
    zone_type : ZoneType
        Type of the zone for mesh.
    """

    _id: int
    name: str
    zone_type: ZoneType


@dataclass
class Node:
    """Node class for mesh.

    Attributes
    ----------
    x : float
        x-coordinate of the node.
    y : float
        y-coordinate of the node.
    z : float
        z-coordinate of the node.
    """

    _id: int
    x: float
    y: float
    z: float


class CellElementType(Enum):
    """Element types for a cell element."""

    # 3 nodes, 3 faces
    TRIANGLE = 1
    # 4 nodes, 4 faces
    TETRAHEDRON = 2
    # 4 nodes, 4 faces
    QUADRILATERAL = 3
    # 8 nodes, 6 faces
    HEXAHEDRON = 4
    # 5 nodes, 5 faces
    PYRAMID = 5
    # 6 nodes, 5 faces
    WEDGE = 6
    # Arbitrary number of nodes and faces
    POLYHEDRON = 7
    # 2 nodes, 1 face (only in 2D)
    GHOST = 8
    # 10 nodes, 4 faces
    QUADRATIC_TETRAHEDRON = 9
    # 20 nodes, 6 faces
    QUADRATIC_HEXAHEDRON = 10
    # 13 nodes, 5 faces
    QUADRATIC_PYRAMID = 11
    # 15 nodes, 5 faces
    QUADRATIC_WEDGE = 12


@dataclass
class Facet:
    """Facet class within a mesh element.

    Attributes
    ----------
    node_indices : list[int]
        0-based node indices of the facet.
    """

    node_indices: list[int]


@dataclass
class Element:
    """Element class for mesh.

    Attributes
    ----------
    element_type : CellElementType
        Element type of the element.
    node_indices : list[int]
        0-based node indices of the element. Populated for standard elements.
    facets : list[Facet]
        List of facets of the element. Populated for polyhedral elements.
    """

    _id: int
    element_type: CellElementType
    node_indices: list[int] = field(default_factory=list)
    facets: list[Facet] = field(default_factory=list)


@dataclass
class Mesh:
    """Mesh class for Fluent field data.

    Attributes
    ----------
    nodes : list[Node]
        List of nodes in the mesh.
    elements : list[Element]
        List of elements in the mesh.
    """

    nodes: list[Node]
    elements: list[Element]


class LiveFieldData(BaseFieldData, FieldDataSource):
    """Provides access to Fluent field data on surfaces."""

    def __init__(
        self,
        service: FieldDataService,
        field_info: FieldInfo,
        is_data_valid: Callable[[], bool],
        scheme_eval=None,
        get_zones_info: weakref.WeakMethod[Callable[[], list[ZoneInfo]]] | None = None,
    ):
        """__init__ method of FieldData class."""
        self._service = service
        self._field_info = field_info
        self.is_data_valid = is_data_valid
        self.scheme_eval = scheme_eval
        self.get_zones_info = lambda: get_zones_info()()

        self._allowed_surface_names = _AllowedSurfaceNames(field_info)

        self._allowed_surface_ids = _AllowedSurfaceIDs(field_info)

        self._allowed_scalar_field_names = _AllowedScalarFieldNames(
            is_data_valid, field_info
        )

        self._allowed_vector_field_names = _AllowedVectorFieldNames(
            is_data_valid, field_info
        )
        super().__init__(
            {},
            self._field_info,
            self._allowed_surface_names,
            self._allowed_scalar_field_names,
        )

        surface_args = dict(
            surface_ids=self._allowed_surface_ids,
            surface_name=self._allowed_surface_names,
        )
        scalar_field_args = {
            **dict(field_name=self._allowed_scalar_field_names),
            **surface_args,
        }
        self.get_scalar_field_data = override_help_text(
            _FieldMethod(
                field_data_accessor=self.get_scalar_field_data,
                args_allowed_values_accessors=scalar_field_args,
            ),
            self.get_scalar_field_data,
        )
        self.get_vector_field_data = override_help_text(
            _FieldMethod(
                field_data_accessor=self.get_vector_field_data,
                args_allowed_values_accessors={
                    **dict(field_name=self._allowed_vector_field_names),
                    **surface_args,
                },
            ),
            self.get_vector_field_data,
        )
        self.get_surface_data = override_help_text(
            _FieldMethod(
                field_data_accessor=self.get_surface_data,
                args_allowed_values_accessors=surface_args,
            ),
            self.get_surface_data,
        )
        self.get_pathlines_field_data = override_help_text(
            _FieldMethod(
                field_data_accessor=self.get_pathlines_field_data,
                args_allowed_values_accessors=scalar_field_args,
            ),
            self.get_pathlines_field_data,
        )
        self._returned_data = _ReturnFieldData()
        self._fetched_data = _FetchFieldData()

    def new_transaction(self):
        """Create a new field transaction."""
        return Transaction(
            self._service,
            self._field_info,
            self._allowed_surface_ids,
            self._allowed_surface_names,
            self._allowed_scalar_field_names,
            self._allowed_vector_field_names,
        )

    def _get_scalar_field_data(self, **kwargs):
        surfaces = kwargs.get("surfaces")
        surface_ids = self.get_surface_ids(surfaces)
        fields_request = get_fields_request()
        fields_request.scalarFieldRequest.extend(
            self._fetched_data._scalar_data(
                self._allowed_scalar_field_names.valid_name(kwargs.get("field_name")),
                self.get_surface_ids(surfaces),
                kwargs.get("node_value"),
                kwargs.get("boundary_value"),
            )
        )
        fields = ChunkParser().extract_fields(self._service.get_fields(fields_request))
        scalar_field_data = next(iter(fields.values()))
        return self._returned_data._scalar_data(
            kwargs.get("field_name"), surfaces, surface_ids, scalar_field_data
        )

    def _get_surface_data(
        self,
        **kwargs,
    ) -> Dict[int | str, Dict[SurfaceDataType, np.array | List[np.array]]]:
        surface_ids = self.get_surface_ids(kwargs.get("surfaces"))
        fields_request = get_fields_request()
        fields_request.surfaceRequest.extend(
            self._fetched_data._surface_data(
                kwargs.get("data_types"),
                surface_ids,
                kwargs.get("overset_mesh"),
            )
        )
        fields = ChunkParser().extract_fields(self._service.get_fields(fields_request))
        surface_data = next(iter(fields.values()))
        if self._deprecated_flag:
            self._deprecated_flag = False
            return self._returned_data._surface_data(
                kwargs.get("data_types"),
                kwargs.get("surfaces"),
                surface_ids,
                surface_data,
                deprecated_flag=True,
            )

        return self._returned_data._surface_data(
            kwargs.get("data_types"), kwargs.get("surfaces"), surface_ids, surface_data
        )

    def _get_vector_field_data(
        self,
        **kwargs,
    ) -> Dict[int | str, np.array]:
        surface_ids = self.get_surface_ids(kwargs.get("surfaces"))
        for surface_id in surface_ids:
            self.scheme_eval.string_eval(f"(surface? {surface_id})")
        fields_request = get_fields_request()
        fields_request.vectorFieldRequest.extend(
            self._fetched_data._vector_data(
                self._allowed_vector_field_names.valid_name(kwargs.get("field_name")),
                surface_ids,
            )
        )
        fields = ChunkParser().extract_fields(self._service.get_fields(fields_request))
        vector_field_data = next(iter(fields.values()))

        return self._returned_data._vector_data(
            kwargs.get("field_name"),
            kwargs.get("surfaces"),
            surface_ids,
            vector_field_data,
        )

    def _get_pathlines_field_data(
        self,
        **kwargs,
    ) -> Dict:
        if kwargs.get("zones") is None:
            zones = []
        surface_ids = self.get_surface_ids(kwargs.get("surfaces"))
        fields_request = get_fields_request()
        fields_request.pathlinesFieldRequest.extend(
            self._fetched_data._pathlines_data(
                self._allowed_scalar_field_names.valid_name(kwargs.get("field_name")),
                surface_ids,
                additionalField=kwargs.get("additional_field_name"),
                provideParticleTimeField=kwargs.get("provide_particle_time_field"),
                dataLocation=(
                    FieldDataProtoModule.DataLocation.Nodes
                    if kwargs.get("node_value")
                    else FieldDataProtoModule.DataLocation.Elements
                ),
                steps=kwargs.get("steps"),
                stepSize=kwargs.get("step_size"),
                skip=kwargs.get("skip"),
                reverse=kwargs.get("reverse"),
                accuracyControlOn=kwargs.get("accuracy_control_on"),
                tolerance=kwargs.get("tolerance"),
                coarsen=kwargs.get("coarsen"),
                velocityDomain=kwargs.get("velocity_domain"),
                zones=zones,
            )
        )
        fields = ChunkParser().extract_fields(self._service.get_fields(fields_request))
        pathlines_data = next(iter(fields.values()))

        if self._deprecated_flag:
            self._deprecated_flag = False
            return self._returned_data._pathlines_data(
                kwargs.get("field_name"),
                kwargs.get("surfaces"),
                surface_ids,
                pathlines_data,
                deprecated_flag=True,
            )

        return self._returned_data._pathlines_data(
            kwargs.get("field_name"),
            kwargs.get("surfaces"),
            surface_ids,
            pathlines_data,
        )

    def get_scalar_field_data(
        self,
        field_name: str,
        surfaces: List[int | str],
        node_value: bool | None = True,
        boundary_value: bool | None = True,
    ) -> Dict[int | str, np.array]:
        """Get scalar field data on a surface."""
        warnings.warn(
            "'get_scalar_field_data' is deprecated, use 'get_field_data' instead",
            PyFluentDeprecationWarning,
        )
        return self._get_scalar_field_data(
            field_name=field_name,
            surfaces=surfaces,
            node_value=node_value,
            boundary_value=boundary_value,
        )

    def get_surface_data(
        self,
        data_types: List[SurfaceDataType],
        surfaces: List[int | str],
        overset_mesh: bool | None = False,
    ) -> Dict[int | str, Dict[SurfaceDataType, np.array | List[np.array]]]:
        """Get surface data (vertices, faces connectivity, centroids, and normals)."""
        warnings.warn(
            "'get_surface_data' is deprecated, use 'get_field_data' instead",
            PyFluentDeprecationWarning,
        )
        self._deprecated_flag = True
        return self._get_surface_data(
            data_types=data_types, surfaces=surfaces, overset_mesh=overset_mesh
        )

    def get_vector_field_data(
        self,
        field_name: str,
        surfaces: List[int | str],
    ) -> Dict[int | str, np.array]:
        """Get vector field data on a surface."""
        warnings.warn(
            "'get_vector_field_data' is deprecated, use 'get_field_data' instead",
            PyFluentDeprecationWarning,
        )
        return self._get_vector_field_data(
            field_name=field_name,
            surfaces=surfaces,
        )

    def get_pathlines_field_data(
        self,
        field_name: str,
        surfaces: List[int | str],
        additional_field_name: str = "",
        provide_particle_time_field: bool | None = False,
        node_value: bool | None = True,
        steps: int | None = 500,
        step_size: float | None = 500,
        skip: int | None = 0,
        reverse: bool | None = False,
        accuracy_control_on: bool | None = False,
        tolerance: float | None = 0.001,
        coarsen: int | None = 1,
        velocity_domain: str | None = "all-phases",
        zones: list | None = None,
    ) -> Dict:
        """Get the pathlines field data on a surface."""
        warnings.warn(
            "'get_pathlines_field_data' is deprecated, use 'get_field_data' instead",
            PyFluentDeprecationWarning,
        )
        self._deprecated_flag = True
        return self._get_pathlines_field_data(
            field_name=field_name,
            surfaces=surfaces,
            additional_field_name=additional_field_name,
            provide_particle_time_field=provide_particle_time_field,
            node_value=node_value,
            steps=steps,
            step_size=step_size,
            skip=skip,
            reverse=reverse,
            accuracy_control_on=accuracy_control_on,
            tolerance=tolerance,
            coarsen=coarsen,
            velocity_domain=velocity_domain,
            zones=zones,
        )

    def get_mesh(self, zone: str | int) -> Mesh:
        """Get mesh for a zone.

        Parameters
        ----------
        zone : str | int
            Zone name or id. Currently, only cell zones are supported.

        Returns
        -------
        Mesh
            Mesh object containing nodes and elements.

        Raises
        ------
        ValueError
            If the zone is not found.
        NotImplementedError
            If a face zone is provided.
        """
        zone_info = None
        for zone_info in self.get_zones_info():
            if zone_info.name == zone or zone_info._id == zone:
                break
        if zone_info is None:
            raise ValueError(f"Zone {zone} not found.")
        if zone_info.zone_type == ZoneType.FACE:
            raise NotImplementedError("Face zone mesh is not supported.")

        # Mesh data is retrieved from the root domain in Fluent
        logger.info(f"Getting nodes data for zone {zone_info._id}")
        start_time = time.time()
        nodes_request = FieldDataProtoModule.GetSolverMeshNodesRequest(
            domain_id=ROOT_DOMAIN_ID, thread_id=zone_info._id
        )
        # TODO: Add precision query in AppUtilities service
        is_double_precision = self.scheme_eval.scheme_eval("(rp-double?)")
        if is_double_precision:
            nested_nodes = self._service.get_solver_mesh_nodes_double(nodes_request)
        else:
            nested_nodes = self._service.get_solver_mesh_nodes_float(nodes_request)
        logger.info(f"Nodes data received in {time.time() - start_time} seconds")
        logger.info(f"Getting elements for zone {zone_info._id}")
        start_time = time.time()
        elements_request = FieldDataProtoModule.GetSolverMeshElementsRequest(
            domain_id=ROOT_DOMAIN_ID, thread_id=zone_info._id
        )
        elementss_pb = self._service.get_solver_mesh_elements(elements_request)
        logger.info(f"Elements data received in {time.time() - start_time} seconds")
        logger.info("Constructing nodes structure in PyFluent")
        start_time = time.time()
        node_count = sum(len(nodes) for nodes in nested_nodes)
        nodes = np.empty(node_count, dtype=Node)
        node_index_by_id = {}
        i = 0
        for nodes_pb in nested_nodes:
            for node_pb in nodes_pb:
                nodes[i] = Node(_id=node_pb.id, x=node_pb.x, y=node_pb.y, z=node_pb.z)
                node_index_by_id[node_pb.id] = i
                i += 1
        logger.info(
            f"Nodes structure constructed in {time.time() - start_time} seconds"
        )
        logger.info("Constructing elements structure in PyFluent")
        start_time = time.time()
        element_count = sum(len(elements) for elements in elementss_pb)
        elements = np.empty(element_count, dtype=Element)
        i = 0
        for elements_pb in elementss_pb:
            for element_pb in elements_pb:
                element_type = CellElementType(element_pb.element_type)
                if element_type == CellElementType.POLYHEDRON:
                    facets = []
                    for facet_pb in element_pb.facets:
                        facet = Facet(
                            node_indices=[node_index_by_id[id] for id in facet_pb.node]
                        )
                        facets.append(facet)
                    element = Element(
                        _id=element_pb.id,
                        element_type=element_type,
                        facets=facets,
                    )
                else:
                    element = Element(
                        _id=element_pb.id,
                        element_type=element_type,
                        node_indices=[
                            node_index_by_id[id] for id in element_pb.node_ids
                        ],
                    )
                elements[i] = element
                i += 1
        logger.info(
            f"Elements structure constructed in {time.time() - start_time} seconds"
        )
        logger.info("Returning mesh")
        return Mesh(nodes=nodes, elements=elements)
