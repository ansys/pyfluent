
from typing import Dict, List, Optional

def fake_extract_field_data_from_object(obj):
  class FieldData:
    def get_scalar_field(
        self,
        surface_ids: List[int],
        scalar_field: str,
        node_value: Optional[bool] = True,
        boundary_value: Optional[bool] = False,
    ) -> Dict[int, Dict]:
        from numpy import array, float32
        with open("field_data_dump.txt", "r") as file1:
            return eval(file1.read())
    def get_vector_field(
        self,
        surface_ids: List[int],
        vector_field: Optional[str] = "velocity",
        scalar_field: Optional[str] = "",
        node_value: Optional[bool] = False,
    ) -> Dict[int, Dict]:
      return {}
  return FieldData()

def fake_extract_field_info_from_object(obj):
  class FieldInfo:
    def get_range(
        self, field: str, node_value: bool = False, surface_ids: List[int] = []
    ) -> List[float]:
        return [0.0,0.0]
    def get_fields_info(self) -> dict:
        return {"Temperature": {"solver_name":"temperature"}}
    def get_vector_fields_info(self) -> dict:
        return {}
    def get_surfaces_info(self) -> dict:
        return {
                "plane-1":{"surface_id": [7], "zone_id": -1}, 
                "symmetry":{"surface_id": [4], "zone_id": 4}
                }
  return FieldInfo()
  

from ansys.fluent.core import meta
meta.extract_field_data_from_object = fake_extract_field_data_from_object
meta.extract_field_info_from_object = fake_extract_field_info_from_object

import ansys.fluent.post.pyvista as pv

graphics_session1 = pv.Graphics(None)
contour1 = graphics_session1.Contours["contour-1"]
contour1.field = "temperature"
contour1.surfaces_list = ['symmetry']
contour1.display("plotter-1")