"""Module containing the meshing utility examples."""

meshing_utility_examples = {
    "add_labels_on_cell_zones": [
        'meshing_session.meshing_utilities.add_labels_on_cell_zones(cell_zone_name_list=["elbow-fluid"], label_name_list=["elbow-1"])',
        'meshing_session.meshing_utilities.add_labels_on_cell_zones(cell_zone_id_list=[87], label_name_list=["87-1"])',
        'meshing_session.meshing_utilities.add_labels_on_cell_zones(cell_zone_name_pattern="*", label_name_list=["cell-1"])',
    ],
    "add_labels_on_edge_zones": [
        'meshing_session.meshing_utilities.add_labels_on_edge_zones(edge_zone_name_list=["symmetry:xyplane:hot-inlet:elbow-fluid:feature.20", "hot-inlet:wall-inlet:elbow-fluid:feature.21"], label_name_list=["20-1", "21-1"])',
        'meshing_session.meshing_utilities.add_labels_on_edge_zones(edge_zone_id_list=[22, 23], label_name_list=["22-1", "23-1"])',
        'meshing_session.meshing_utilities.add_labels_on_edge_zones(edge_zone_name_pattern="cold-inlet*", label_name_list=["26-1"])',
    ],
    "add_labels_on_face_zones": [
        'meshing_session.meshing_utilities.add_labels_on_face_zones(face_zone_name_list=["wall-inlet", "wall-elbow"], label_name_list=["wall-inlet-1", "wall-elbow-1"])',
        'meshing_session.meshing_utilities.add_labels_on_face_zones(face_zone_id_list=[30, 31], label_name_list=["hot-inlet-1", "cold-inlet-1"])',
        'meshing_session.meshing_utilities.add_labels_on_face_zones(face_zone_name_pattern="out*", label_name_list=["outlet-1"])',
    ],
    "clean_face_zone_names": [
        "meshing_session.meshing_utilities.clean_face_zone_names()"
    ],
    "delete_all_sub_domains": [
        "meshing_session.meshing_utilities.delete_all_sub_domains()"
    ],
    "delete_empty_cell_zones": [
        "meshing_session.meshing_utilities.delete_empty_cell_zones(cell_zone_id_list=[87])",
        'meshing_session.meshing_utilities.delete_empty_cell_zones(cell_zone_name_list=["elbow.87"])',
        'meshing_session.meshing_utilities.delete_empty_cell_zones(cell_zone_name_pattern="*")',
    ],
    "delete_empty_edge_zones": [
        "meshing_session.meshing_utilities.delete_empty_edge_zones(edge_zone_id_list=[20, 25, 26])",
        'meshing_session.meshing_utilities.delete_empty_edge_zones("symmetry:xyplane:hot-inlet:elbow-fluid:feature.20", "hot-inlet:wall-inlet:elbow-fluid:feature.21")',
        'meshing_session.meshing_utilities.delete_empty_edge_zones(edge_zone_name_pattern="*")',
    ],
    "delete_empty_face_zones": [
        "meshing_session.meshing_utilities.delete_empty_face_zones(face_zone_id_list=[30, 31, 32])",
        'meshing_session.meshing_utilities.delete_empty_face_zones(face_zone_name_list=["wall-inlet", "wallfluid-new"])',
        'meshing_session.meshing_utilities.delete_empty_face_zones(face_zone_name_pattern="*")',
    ],
    "delete_empty_zones": [
        "meshing_session.meshing_utilities.delete_empty_zones(zone_id_list=[20, 32, 87])",
        'meshing_session.meshing_utilities.delete_empty_zones(zone_name_list=["hotfluid-new", "elbow.87"])',
        'meshing_session.meshing_utilities.delete_empty_zones(zone_name_pattern="*")',
    ],
    "delete_marked_faces_in_zones": [
        "meshing_session.meshing_utilities.delete_marked_faces_in_zones(face_zone_id_list=[30, 31, 32])",
        'meshing_session.meshing_utilities.delete_marked_faces_in_zones(face_zone_name_list=["wall-inlet", "wallfluid-new"])',
        'meshing_session.meshing_utilities.delete_marked_faces_in_zones(face_zone_name_pattern="*")',
    ],
    "merge_cell_zones": [
        "meshing_session.meshing_utilities.merge_cell_zones(cell_zone_id_list=[87])",
        'meshing_session.meshing_utilities.merge_cell_zones(cell_zone_name_list=["elbow-fluid"])',
        'meshing_session.meshing_utilities.merge_cell_zones(cell_zone_name_pattern="*")',
    ],
    "merge_cell_zones_with_same_prefix": [
        'meshing_session.meshing_utilities.merge_cell_zones_with_same_prefix(prefix="elbow")'
    ],
    "merge_cell_zones_with_same_suffix": [
        'meshing_session.meshing_utilities.merge_cell_zones_with_same_suffix(suffix="fluid")'
    ],
    "merge_face_zones": [
        "meshing_session.meshing_utilities.merge_face_zones(face_zone_id_list=[30, 31, 32])",
        'meshing_session.meshing_utilities.merge_face_zones(face_zone_name_pattern="wall*")',
    ],
    "merge_face_zones_of_type": [
        'meshing_session.meshing_utilities.merge_face_zones_of_type(face_zone_type="velocity-inlet", face_zone_name_pattern="*")'
    ],
    "merge_face_zones_with_same_prefix": [
        'meshing_session.meshing_utilities.merge_face_zones_with_same_prefix(prefix="elbow")'
    ],
    "remove_id_suffix_from_face_zones": [
        "meshing_session.meshing_utilities.remove_id_suffix_from_face_zones()"
    ],
    "remove_ids_from_zone_names": [
        "meshing_session.meshing_utilities.remove_ids_from_zone_names(zone_id_list=[30, 31, 32])"
    ],
    "remove_labels_on_cell_zones": [
        'meshing_session.meshing_utilities.remove_labels_on_cell_zones(cell_zone_name_list=["elbow-fluid"], label_name_list=["elbow-1"])',
        'meshing_session.meshing_utilities.remove_labels_on_cell_zones(cell_zone_id_list=[87], label_name_list=["87-1"])',
        'meshing_session.meshing_utilities.remove_labels_on_cell_zones(cell_zone_name_pattern="*", label_name_list=["cell-1"])',
    ],
    "remove_labels_on_edge_zones": [
        'meshing_session.meshing_utilities.remove_labels_on_edge_zones(edge_zone_name_list=["symmetry:xyplane:hot-inlet:elbow-fluid:feature.20"], label_name_list=["20-1"])',
        'meshing_session.meshing_utilities.remove_labels_on_edge_zones(edge_zone_id_list=[22], label_name_list=["22-1"])',
        'meshing_session.meshing_utilities.remove_labels_on_edge_zones(edge_zone_name_pattern="*", label_name_list=["26-1"])',
    ],
    "remove_labels_on_face_zones": [
        'meshing_session.meshing_utilities.remove_labels_on_face_zones(face_zone_name_list=["wall-inlet"], label_name_list=["wall-inlet-1"])',
        'meshing_session.meshing_utilities.remove_labels_on_face_zones(face_zone_id_list=[30], label_name_list=["hot-inlet-1"])',
        'meshing_session.meshing_utilities.remove_labels_on_face_zones(face_zone_name_pattern="*", label_name_list=["wall-elbow-1"])',
    ],
    "rename_edge_zone": [
        'meshing_session.meshing_utilities.rename_edge_zone(zone_id=20, new_name="symmetry:xyplane:hot-inlet:elbow-fluid:feature.20-new")'
    ],
    "rename_face_zone": [
        'meshing_session.meshing_utilities.rename_face_zone(zone_name="symmetry:xyplane:hot-inlet:elbow-fluid:feature.20-new", new_name="symmetry:xyplane:hot-inlet:elbow-fluid:feature.20")',
        'meshing_session.meshing_utilities.rename_face_zone(zone_id=32, new_name="outlet-32")',
        'meshing_session.meshing_utilities.rename_face_zone(zone_name="outlet-32", new_name="outlet")',
    ],
    "rename_face_zone_label": [
        'meshing_session.meshing_utilities.rename_face_zone_label(object_name="elbow-fluid-1", old_label_name="outlet", new_label_name="outlet-new")'
    ],
    "rename_object": [
        'meshing_session.meshing_utilities.rename_object(old_object_name="elbow-fluid", new_object_name="elbow-fluid-1")'
    ],
    "renumber_zone_ids": [
        "meshing_session.meshing_utilities.renumber_zone_ids(zone_id_list=[30, 31, 32], start_number=1)"
    ],
    "replace_cell_zone_suffix": [
        'meshing_session.meshing_utilities.replace_cell_zone_suffix(cell_zone_id_list=[87], old_suffix="fluid", new_suffix="fluid-new", merge=True)',
        'meshing_session.meshing_utilities.replace_cell_zone_suffix(cell_zone_name_list=["elbow-fluid-new"], old_suffix="fluid", new_suffix="fluid-new", merge=True)',
    ],
    "replace_edge_zone_suffix": [
        'meshing_session.meshing_utilities.replace_edge_zone_suffix(edge_zone_id_list=[20], old_suffix="fluid", new_suffix="fluid-new", merge=True)',
        'meshing_session.meshing_utilities.replace_edge_zone_suffix(edge_zone_name_list=["hot-inlet:wall-inlet:elbow-fluid:feature.21"], old_suffix="fluid", new_suffix="fluid-new", merge=True)',
    ],
    "replace_face_zone_suffix": [
        'meshing_session.meshing_utilities.replace_face_zone_suffix(face_zone_id_list=[30, 31, 32], separator="-suffix-", replace_with="-with-", merge=False)',
        'meshing_session.meshing_utilities.replace_face_zone_suffix(face_zone_name_list=["cold-inlet", "hot-inlet"], separator="-suffix-", replace_with="-with-", merge=False)',
    ],
    "replace_label_suffix": [
        'meshing_session.meshing_utilities.replace_label_suffix(object_name_list=["elbow-fluid-1"], separator="-", new_suffix="fluid-new")'
    ],
    "replace_object_suffix": [
        'meshing_session.meshing_utilities.replace_object_suffix(object_name_list=["elbow-fluid"], separator="-", new_suffix="fluid-new")'
    ],
    "set_number_of_parallel_compute_threads": [
        "meshing_session.meshing_utilities.set_number_of_parallel_compute_threads(nthreads=2)"
    ],
    "set_object_cell_zone_type": [
        'meshing_session.meshing_utilities.set_object_cell_zone_type(object_name="elbow-fluid", cell_zone_type="mixed")'
    ],
    "set_quality_measure": [
        'meshing_session.meshing_utilities.set_quality_measure(measure="Aspect Ratio")'
    ],
    "_cell_zones_labels_fdl": [
        "meshing_session.meshing_utilities._cell_zones_labels_fdl()"
    ],
    "_cell_zones_str_fdl": ["meshing_session.meshing_utilities._cell_zones_str_fdl()"],
    "_edge_zones_labels_fdl": [
        "meshing_session.meshing_utilities._edge_zones_labels_fdl()"
    ],
    "_edge_zones_str_fdl": ["meshing_session.meshing_utilities._edge_zones_str_fdl()"],
    "_face_zones_labels_fdl": [
        "meshing_session.meshing_utilities._face_zones_labels_fdl()"
    ],
    "_face_zones_str_fdl": ["meshing_session.meshing_utilities._face_zones_str_fdl()"],
    "_node_zones_labels_fdl": [
        "meshing_session.meshing_utilities._node_zones_labels_fdl()"
    ],
    "_node_zones_str_fdl": ["meshing_session.meshing_utilities._node_zones_str_fdl()"],
    "_object_names_str_fdl": [
        "meshing_session.meshing_utilities._object_names_str_fdl()"
    ],
    "_prism_cell_zones_labels_fdl": [
        "meshing_session.meshing_utilities._prism_cell_zones_labels_fdl()"
    ],
    "_prism_cell_zones_str_fdl": [
        "meshing_session.meshing_utilities._prism_cell_zones_str_fdl()"
    ],
    "_regions_str_fdl": ["meshing_session.meshing_utilities._regions_str_fdl()"],
    "_zone_types_fdl": ["meshing_session.meshing_utilities._zone_types_fdl()"],
    "boundary_zone_exists": [
        "meshing_session.meshing_utilities.boundary_zone_exists(zone_id=31)",
        'meshing_session.meshing_utilities.boundary_zone_exists(zone_name="wall-inlet")',
    ],
    "cell_zone_exists": [
        "meshing_session.meshing_utilities.cell_zone_exists(zone_id=87)",
        'meshing_session.meshing_utilities.cell_zone_exists(zone_name="elbow.87")',
    ],
    "convert_zone_ids_to_name_strings": [
        "meshing_session.meshing_utilities.convert_zone_ids_to_name_strings(zone_id_list=[32, 31])"
    ],
    "convert_zone_name_strings_to_ids": [
        'meshing_session.meshing_utilities.convert_zone_name_strings_to_ids(zone_name_list=["outlet", "cold-inlet"])'
    ],
    "copy_face_zone_labels": [
        "meshing_session.meshing_utilities.copy_face_zone_labels(from_face_zone_id=33, to_face_zone_id=34)"
    ],
    "count_marked_faces": [
        'meshing_session.meshing_utilities.count_marked_faces(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"])',
        'meshing_session.meshing_utilities.count_marked_faces(face_zone_name_pattern="*")',
    ],
    "create_boi_and_size_functions_from_refinement_regions": [
        'meshing_session.meshing_utilities.create_boi_and_size_functions_from_refinement_regions(region_type="hexcore", boi_prefix_string="wall", create_size_function=True)'
    ],
    "dump_face_zone_orientation_in_region": [
        'meshing_session.meshing_utilities.dump_face_zone_orientation_in_region(file_name="facezonetest.txt")'
    ],
    "fill_holes_in_face_zone_list": [
        "meshing_session.meshing_utilities.fill_holes_in_face_zone_list(face_zone_id_list=[30, 31, 32], max_hole_edges=2)",
        'meshing_session.meshing_utilities.fill_holes_in_face_zone_list(face_zone_name_list=["wall-inlet", "wallfluid-new"], max_hole_edges=2)',
        'meshing_session.meshing_utilities.fill_holes_in_face_zone_list(face_zone_name_pattern="wall*", max_hole_edges=2)',
    ],
    "get_adjacent_cell_zones_for_given_face_zones": [
        "meshing_session.meshing_utilities.get_adjacent_cell_zones_for_given_face_zones(face_zone_id_list=[29, 30, 31, 32, 33])",
        'meshing_session.meshing_utilities.get_adjacent_cell_zones_for_given_face_zones(face_zone_name_list=["outlet", "inlet", "wall", "internal"])',
        'meshing_session.meshing_utilities.get_adjacent_cell_zones_for_given_face_zones(face_zone_name_pattern="*")',
    ],
    "get_adjacent_face_zones_for_given_cell_zones": [
        "meshing_session.meshing_utilities.get_adjacent_face_zones_for_given_cell_zones(cell_zone_id_list=[87])",
        'meshing_session.meshing_utilities.get_adjacent_face_zones_for_given_cell_zones(cell_zone_name_list=["elbow-fluid"])',
        'meshing_session.meshing_utilities.get_adjacent_face_zones_for_given_cell_zones(cell_zone_name_pattern="*")',
    ],
    "get_adjacent_interior_and_boundary_face_zones_for_given_cell_zones": [
        "meshing_session.meshing_utilities.get_adjacent_interior_and_boundary_face_zones_for_given_cell_zones(cell_zone_id_list=[87])",
        'meshing_session.meshing_utilities.get_adjacent_interior_and_boundary_face_zones_for_given_cell_zones(cell_zone_name_list=["elbow-fluid"])',
        'meshing_session.meshing_utilities.get_adjacent_interior_and_boundary_face_zones_for_given_cell_zones(cell_zone_name_pattern="*")',
    ],
    "get_adjacent_zones_by_edge_connectivity": [
        "meshing_session.meshing_utilities.get_adjacent_zones_by_edge_connectivity(zone_id_list=[29, 30, 31, 32, 33])",
        'meshing_session.meshing_utilities.get_adjacent_zones_by_edge_connectivity(zone_name_list=["outlet", "inlet", "wall", "internal"])',
        'meshing_session.meshing_utilities.get_adjacent_zones_by_edge_connectivity(zone_name_pattern="*")',
    ],
    "get_adjacent_zones_by_node_connectivity": [
        "meshing_session.meshing_utilities.get_adjacent_zones_by_node_connectivity(zone_id_list=[29, 30, 31, 32, 33])",
        'meshing_session.meshing_utilities.get_adjacent_zones_by_node_connectivity(zone_name_list=["outlet", "inlet", "wall", "internal"])',
        'meshing_session.meshing_utilities.get_adjacent_zones_by_node_connectivity(zone_name_pattern="*")',
    ],
    "get_all_objects": ["meshing_session.meshing_utilities.get_all_objects()"],
    "get_average_bounding_box_center": [
        "meshing_session.meshing_utilities.get_average_bounding_box_center(face_zone_id_list=[30, 31, 32])"
    ],
    "get_baffles_for_face_zones": [
        "meshing_session.meshing_utilities.get_baffles_for_face_zones(face_zone_id_list=[29, 30, 31, 32, 33])"
    ],
    "get_bounding_box_of_zone_list": [
        "meshing_session.meshing_utilities.get_bounding_box_of_zone_list(zone_id_list=[26])"
    ],
    "get_cell_mesh_distribution": [
        'meshing_session.meshing_utilities.get_cell_mesh_distribution(cell_zone_id_list=[87], measure="Orthogonal Quality", partitions=2, range=[0.9, 1])',
        'meshing_session.meshing_utilities.get_cell_mesh_distribution(cell_zone_name_list=["elbow-fluid"], measure="Orthogonal Quality", partitions=2, range=[0.9, 1])',
        'meshing_session.meshing_utilities.get_cell_mesh_distribution(cell_zone_name_pattern="*", measure="Orthogonal Quality", partitions=2, range=[0.9, 1])',
    ],
    "get_cell_quality_limits": [
        'meshing_session.meshing_utilities.get_cell_quality_limits(cell_zone_id_list=[87], measure="Orthogonal Quality")',
        'meshing_session.meshing_utilities.get_cell_quality_limits(cell_zone_name_list=["elbow-fluid"], measure="Orthogonal Quality")',
        'meshing_session.meshing_utilities.get_cell_quality_limits(cell_zone_name_pattern="*", measure="Orthogonal Quality")',
    ],
    "get_cell_zone_count": [
        "meshing_session.meshing_utilities.get_cell_zone_count(cell_zone_id_list=[87])",
        'meshing_session.meshing_utilities.get_cell_zone_count(cell_zone_name_list=["elbow-fluid"])',
        'meshing_session.meshing_utilities.get_cell_zone_count(cell_zone_name_pattern="*")',
    ],
    "get_cell_zone_id_list_with_labels": [
        'meshing_session.meshing_utilities.get_cell_zone_id_list_with_labels(cell_zone_id_list=[87], label_name_list=["elbow-1"])',
        'meshing_session.meshing_utilities.get_cell_zone_id_list_with_labels(cell_zone_name_list=["elbow-fluid"], label_name_list=["elbow-1"])',
        'meshing_session.meshing_utilities.get_cell_zone_id_list_with_labels(cell_zone_name_pattern="*", label_name_list=["elbow-1"])',
    ],
    "get_cell_zone_shape": [
        "meshing_session.meshing_utilities.get_cell_zone_shape(cell_zone_id=87)"
    ],
    "get_cell_zone_volume": [
        "meshing_session.meshing_utilities.get_cell_zone_volume(cell_zone_id_list=[87])",
        'meshing_session.meshing_utilities.get_cell_zone_volume(cell_zone_name_list=["elbow-fluid"])',
        'meshing_session.meshing_utilities.get_cell_zone_volume(cell_zone_name_pattern="*")',
    ],
    "get_cell_zones": [
        'meshing_session.meshing_utilities.get_cell_zones(filter="*")',
        "meshing_session.meshing_utilities.get_cell_zones(maximum_entity_count=100)",
        "meshing_session.meshing_utilities.get_cell_zones(xyz_coordinates=[-7, -6, 0.4])",
    ],
    "get_edge_size_limits": [
        "meshing_session.meshing_utilities.get_edge_size_limits(face_zone_id_list=[30, 31, 32])",
        'meshing_session.meshing_utilities.get_edge_size_limits(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"])',
        'meshing_session.meshing_utilities.get_edge_size_limits(face_zone_name_pattern="*")',
    ],
    "get_edge_zone_id_list_with_labels": [
        'meshing_session.meshing_utilities.get_edge_zone_id_list_with_labels(edge_zone_id_list=[20, 21], label_name_list=["20-1", "21-1"])',
        'meshing_session.meshing_utilities.get_edge_zone_id_list_with_labels(edge_zone_name_list=["symmetry:xyplane:hot-inlet:elbow-fluid:feature.20", "hot-inlet:wall-inlet:elbow-fluid:feature.21"], label_name_list=["20-1", "21-1"])',
        'meshing_session.meshing_utilities.get_edge_zone_id_list_with_labels(edge_zone_name_pattern="*", label_name_list=["20-1", "21-1"])',
    ],
    "get_edge_zones": [
        'meshing_session.meshing_utilities.get_edge_zones(filter="*")',
        "meshing_session.meshing_utilities.get_edge_zones(maximum_entity_count=20, only_boundary=False)",
    ],
    "get_edge_zones_list": [
        'meshing_session.meshing_utilities.get_edge_zones_list(filter="*")'
    ],
    "get_edge_zones_of_object": [
        'meshing_session.meshing_utilities.get_edge_zones_of_object(objects=["elbow-fluid"])',
        'meshing_session.meshing_utilities.get_edge_zones_of_object(object_name="elbow-fluid")',
    ],
    "get_embedded_baffles": [
        "meshing_session.meshing_utilities.get_embedded_baffles()"
    ],
    "get_face_mesh_distribution": [
        'meshing_session.meshing_utilities.get_face_mesh_distribution(face_zone_id_list=[30, 31, 32], measure="Orthogonal Quality", partitions=2, range=[0.9, 1])',
        'meshing_session.meshing_utilities.get_face_mesh_distribution(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"], measure="Orthogonal Quality", partitions=2, range=[0.9, 1])',
        'meshing_session.meshing_utilities.get_face_mesh_distribution(face_zone_name_pattern="*", measure="Orthogonal Quality", partitions=2, range=[0.9, 1])',
    ],
    "get_face_quality_limits": [
        'meshing_session.meshing_utilities.get_face_quality_limits(face_zone_id_list=[30, 31, 32], measure="Orthogonal Quality")',
        'meshing_session.meshing_utilities.get_face_quality_limits(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"], measure="Orthogonal Quality")',
        'meshing_session.meshing_utilities.get_face_quality_limits(face_zone_name_pattern="*", measure="Orthogonal Quality")',
    ],
    "get_face_zone_area": [
        "meshing_session.meshing_utilities.get_face_zone_area(face_zone_id_list=[30, 31, 32])",
        'meshing_session.meshing_utilities.get_face_zone_area(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"])',
        'meshing_session.meshing_utilities.get_face_zone_area(face_zone_name_pattern="*")',
    ],
    "get_face_zone_count": [
        "meshing_session.meshing_utilities.get_face_zone_count(face_zone_id_list=[30, 31, 32])",
        'meshing_session.meshing_utilities.get_face_zone_count(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"])',
        'meshing_session.meshing_utilities.get_face_zone_count(face_zone_name_pattern="*")',
    ],
    "get_face_zone_id_list_with_labels": [
        'meshing_session.meshing_utilities.get_face_zone_id_list_with_labels(face_zone_id_list=[33, 34], label_name_list=["wall-inlet-1", "wall-elbow-1"])',
        'meshing_session.meshing_utilities.get_face_zone_id_list_with_labels(face_zone_name_list=["wall-inlet", "wall-elbow"], label_name_list=["wall-inlet-1", "wall-elbow-1"])',
        'meshing_session.meshing_utilities.get_face_zone_id_list_with_labels(face_zone_name_pattern="wall*", label_name_list=["wall-inlet-1", "wall-elbow-1"])',
    ],
    "get_face_zone_node_count": [
        "meshing_session.meshing_utilities.get_face_zone_node_count(face_zone_id=32)",
        'meshing_session.meshing_utilities.get_face_zone_node_count(face_zone_name="outlet")',
    ],
    "get_face_zones": [
        'meshing_session.meshing_utilities.get_face_zones(filter="*")',
        'meshing_session.meshing_utilities.get_face_zones(prism_control_name="*")',
        "meshing_session.meshing_utilities.get_face_zones(xyz_coordinates=[1.4, 1.4, 1.4])",
        "meshing_session.meshing_utilities.get_face_zones(maximum_entity_count=20, only_boundary=True)",
    ],
    "get_face_zones_by_zone_area": [
        "meshing_session.meshing_utilities.get_face_zones_by_zone_area(maximum_zone_area=100)",
        "meshing_session.meshing_utilities.get_face_zones_by_zone_area(minimum_zone_area=10)",
    ],
    "get_face_zones_of_object": [
        'meshing_session.meshing_utilities.get_face_zones_of_object(object_name="elbow-fluid", regions=["elbow-fluid"])',
        'meshing_session.meshing_utilities.get_face_zones_of_object(object_name="elbow-fluid", labels=["outlet"])',
        'meshing_session.meshing_utilities.get_face_zones_of_object(object_name="elbow-fluid", region_type="elbow-fluid")',
        'meshing_session.meshing_utilities.get_face_zones_of_object(object_name="elbow-fluid")',
        'meshing_session.meshing_utilities.get_face_zones_of_object(objects=["elbow-fluid"])',
    ],
    "get_face_zones_with_zone_specific_prisms_applied": [
        "meshing_session.meshing_utilities.get_face_zones_with_zone_specific_prisms_applied()"
    ],
    "get_free_faces_count": [
        "meshing_session.meshing_utilities.get_free_faces_count(face_zone_id_list=[30, 31, 32])",
        'meshing_session.meshing_utilities.get_free_faces_count(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"])',
        'meshing_session.meshing_utilities.get_free_faces_count(face_zone_name_pattern="*")',
    ],
    "get_interior_face_zones_for_given_cell_zones": [
        "meshing_session.meshing_utilities.get_interior_face_zones_for_given_cell_zones(cell_zone_id_list=[87])",
        'meshing_session.meshing_utilities.get_interior_face_zones_for_given_cell_zones(cell_zone_name_list=["elbow-fluid"])',
        'meshing_session.meshing_utilities.get_interior_face_zones_for_given_cell_zones(cell_zone_name_pattern="*")',
    ],
    "get_labels": [
        'meshing_session.meshing_utilities.get_labels(object_name="elbow-fluid")',
        'meshing_session.meshing_utilities.get_labels(object_name="elbow-fluid", filter="*")',
        'meshing_session.meshing_utilities.get_labels(object_name="elbow-fluid", label_name_pattern="*")',
    ],
    "get_labels_on_cell_zones": [
        "meshing_session.meshing_utilities.get_labels_on_cell_zones(cell_zone_id_list=[87])",
        'meshing_session.meshing_utilities.get_labels_on_cell_zones(cell_zone_name_list=["elbow-fluid"])',
        'meshing_session.meshing_utilities.get_labels_on_cell_zones(cell_zone_name_pattern="*")',
    ],
    "get_labels_on_edge_zones": [
        "meshing_session.meshing_utilities.get_labels_on_edge_zones(edge_zone_id_list=[22, 23])",
        'meshing_session.meshing_utilities.get_labels_on_edge_zones(edge_zone_name_list=["symmetry:xyplane:hot-inlet:elbow-fluid:feature.20", "hot-inlet:wall-inlet:elbow-fluid:feature.21"])',
        'meshing_session.meshing_utilities.get_labels_on_edge_zones(edge_zone_name_pattern="cold-inlet*")',
    ],
    "get_labels_on_face_zones": [
        "meshing_session.meshing_utilities.get_labels_on_face_zones(face_zone_id_list=[30, 31])",
        'meshing_session.meshing_utilities.get_labels_on_face_zones(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"])',
        'meshing_session.meshing_utilities.get_labels_on_face_zones(face_zone_name_pattern="out*")',
    ],
    "get_labels_on_face_zones_list": [
        "meshing_session.meshing_utilities.get_labels_on_face_zones_list(face_zone_id_list=[30, 31])"
    ],
    "get_maxsize_cell_zone_by_count": [
        "meshing_session.meshing_utilities.get_maxsize_cell_zone_by_count(zone_id_list=[87])",
        'meshing_session.meshing_utilities.get_maxsize_cell_zone_by_count(zone_name_list=["outlet", "inlet", "wall", "internal"])',
        'meshing_session.meshing_utilities.get_maxsize_cell_zone_by_count(zone_name_pattern="*")',
    ],
    "get_maxsize_cell_zone_by_volume": [
        "meshing_session.meshing_utilities.get_maxsize_cell_zone_by_volume(zone_id_list=[87])",
        'meshing_session.meshing_utilities.get_maxsize_cell_zone_by_volume(zone_name_list=["outlet", "inlet", "wall", "internal"])',
        'meshing_session.meshing_utilities.get_maxsize_cell_zone_by_volume(zone_name_pattern="*")',
    ],
    "get_minsize_face_zone_by_area": [
        "meshing_session.meshing_utilities.get_minsize_face_zone_by_area(zone_id_list=[29, 30, 31, 32, 33])",
        'meshing_session.meshing_utilities.get_minsize_face_zone_by_area(zone_name_list=["outlet", "inlet", "wall", "internal"])',
        'meshing_session.meshing_utilities.get_minsize_face_zone_by_area(zone_name_pattern="*")',
    ],
    "get_minsize_face_zone_by_count": [
        "meshing_session.meshing_utilities.get_minsize_face_zone_by_count(zone_id_list=[29, 30, 31, 32, 33])",
        'meshing_session.meshing_utilities.get_minsize_face_zone_by_count(zone_name_list=["outlet", "inlet", "wall", "internal"])',
        'meshing_session.meshing_utilities.get_minsize_face_zone_by_count(zone_name_pattern="*")',
    ],
    "get_multi_faces_count": [
        "meshing_session.meshing_utilities.get_multi_faces_count(face_zone_id_list=[30, 31, 32])",
        'meshing_session.meshing_utilities.get_multi_faces_count(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"])',
        'meshing_session.meshing_utilities.get_multi_faces_count(face_zone_name_pattern="*")',
    ],
    "get_node_zones": ['meshing_session.meshing_utilities.get_node_zones(filter="*")'],
    "get_objects": [
        'meshing_session.meshing_utilities.get_objects(type_name="mesh")',
        'meshing_session.meshing_utilities.get_objects(filter="*")',
    ],
    "get_overlapping_face_zones": [
        'meshing_session.meshing_utilities.get_overlapping_face_zones(face_zone_name_pattern="*", area_tolerance=0.01, distance_tolerance=0.01)'
    ],
    "get_pairs_of_overlapping_face_zones": [
        "meshing_session.meshing_utilities.get_pairs_of_overlapping_face_zones(face_zone_id_list=[29, 30, 31, 32, 33], join_tolerance=0.001, absolute_tolerance=True, join_angle=45)",
        'meshing_session.meshing_utilities.get_pairs_of_overlapping_face_zones(face_zone_name_list=["outlet", "inlet", "wall", "internal"], join_tolerance=0.001, absolute_tolerance=True, join_angle=45)',
        'meshing_session.meshing_utilities.get_pairs_of_overlapping_face_zones(face_zone_name_pattern="*", join_tolerance=0.001, absolute_tolerance=True, join_angle=45)',
    ],
    "get_prism_cell_zones": [
        "meshing_session.meshing_utilities.get_prism_cell_zones(zone_id_list=[87])",
        'meshing_session.meshing_utilities.get_prism_cell_zones(zone_name_list=["outlet", "inlet", "wall", "internal"])',
        'meshing_session.meshing_utilities.get_prism_cell_zones(zone_name_pattern="*")',
    ],
    "get_region_volume": [
        'meshing_session.meshing_utilities.get_region_volume(object_name="elbow-fluid", sorting_order="ascending")',
        'meshing_session.meshing_utilities.get_region_volume(object_name="elbow-fluid", region_name="elbow-fluid")',
    ],
    "get_regions": [
        'meshing_session.meshing_utilities.get_regions(object_name="elbow-fluid", region_name_pattern="*")',
        'meshing_session.meshing_utilities.get_regions(object_name="elbow-fluid", filter="*")',
        'meshing_session.meshing_utilities.get_regions(object_name="elbow-fluid")',
    ],
    "get_regions_of_face_zones": [
        "meshing_session.meshing_utilities.get_regions_of_face_zones(face_zone_id_list=[29, 30, 31, 32, 33])",
        'meshing_session.meshing_utilities.get_regions_of_face_zones(face_zone_name_list=["outlet", "inlet", "wall", "internal"])',
        'meshing_session.meshing_utilities.get_regions_of_face_zones(face_zone_name_pattern="*")',
    ],
    "get_shared_boundary_face_zones_for_given_cell_zones": [
        "meshing_session.meshing_utilities.get_shared_boundary_face_zones_for_given_cell_zones(cell_zone_id_list=[87])",
        'meshing_session.meshing_utilities.get_shared_boundary_face_zones_for_given_cell_zones(cell_zone_name_list=["elbow-fluid"])',
        'meshing_session.meshing_utilities.get_shared_boundary_face_zones_for_given_cell_zones(cell_zone_name_pattern="*")',
    ],
    "get_tet_cell_zones": [
        "meshing_session.meshing_utilities.get_tet_cell_zones(zone_id_list=[29, 30, 31, 32, 33])",
        'meshing_session.meshing_utilities.get_tet_cell_zones(zone_name_list=["outlet", "inlet", "wall", "internal"])',
        'meshing_session.meshing_utilities.get_tet_cell_zones(zone_name_pattern="*")',
    ],
    "get_unreferenced_cell_zones": [
        "meshing_session.meshing_utilities.get_unreferenced_cell_zones()",
        'meshing_session.meshing_utilities.get_unreferenced_cell_zones(filter="*")',
        'meshing_session.meshing_utilities.get_unreferenced_cell_zones(zone_name_pattern="*")',
    ],
    "get_unreferenced_edge_zones": [
        "meshing_session.meshing_utilities.get_unreferenced_edge_zones()",
        'meshing_session.meshing_utilities.get_unreferenced_edge_zones(filter="*")',
        'meshing_session.meshing_utilities.get_unreferenced_edge_zones(zone_name_pattern="*")',
    ],
    "get_unreferenced_face_zones": [
        "meshing_session.meshing_utilities.get_unreferenced_face_zones()",
        'meshing_session.meshing_utilities.get_unreferenced_face_zones(filter="*")',
        'meshing_session.meshing_utilities.get_unreferenced_face_zones(zone_name_pattern="*")',
    ],
    "get_wrapped_face_zones": [
        "meshing_session.meshing_utilities.get_wrapped_face_zones()"
    ],
    "get_zone_type": [
        "meshing_session.meshing_utilities.get_zone_type(zone_id=87)",
        'meshing_session.meshing_utilities.get_zone_type(zone_name="elbow-fluid")',
    ],
    "get_zones": [
        'meshing_session.meshing_utilities.get_zones(type_name="velocity-inlet")',
        'meshing_session.meshing_utilities.get_zones(group_name="inlet")',
    ],
    "get_zones_with_free_faces_for_given_face_zones": [
        "meshing_session.meshing_utilities.get_zones_with_free_faces_for_given_face_zones(face_zone_id_list=[29, 30, 31, 32, 33])",
        'meshing_session.meshing_utilities.get_zones_with_free_faces_for_given_face_zones(face_zone_name_list=["outlet", "inlet", "wall", "internal"])',
        'meshing_session.meshing_utilities.get_zones_with_free_faces_for_given_face_zones(face_zone_id_list=[face_zone_name_pattern="*"])',
    ],
    "get_zones_with_marked_faces_for_given_face_zones": [
        "meshing_session.meshing_utilities.get_zones_with_marked_faces_for_given_face_zones(face_zone_id_list=[29, 30, 31, 32, 33])",
        'meshing_session.meshing_utilities.get_zones_with_marked_faces_for_given_face_zones(face_zone_name_list=["outlet", "inlet", "wall", "internal"])',
        'meshing_session.meshing_utilities.get_zones_with_marked_faces_for_given_face_zones(face_zone_id_list=[face_zone_name_pattern="*"])',
    ],
    "get_zones_with_multi_faces_for_given_face_zones": [
        "meshing_session.meshing_utilities.get_zones_with_multi_faces_for_given_face_zones(face_zone_id_list=[29, 30, 31, 32, 33])",
        'meshing_session.meshing_utilities.get_zones_with_multi_faces_for_given_face_zones(face_zone_name_list=["outlet", "inlet", "wall", "internal"])',
        'meshing_session.meshing_utilities.get_zones_with_multi_faces_for_given_face_zones(face_zone_id_list=[face_zone_name_pattern="*"])',
    ],
    "interior_zone_exists": [
        "meshing_session.meshing_utilities.interior_zone_exists(zone_id=31)",
        'meshing_session.meshing_utilities.interior_zone_exists(zone_name="wall-inlet")',
    ],
    "mark_bad_quality_faces": [
        "meshing_session.meshing_utilities.mark_bad_quality_faces(face_zone_id_list=[30, 31, 32], quality_limit=0.5, number_of_rings=2)",
        'meshing_session.meshing_utilities.mark_bad_quality_faces(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"], quality_limit=0.5, number_of_rings=2)',
        'meshing_session.meshing_utilities.mark_bad_quality_faces(face_zone_name_pattern="*", quality_limit=0.5, number_of_rings=2)',
    ],
    "mark_duplicate_faces": [
        "meshing_session.meshing_utilities.mark_duplicate_faces(face_zone_id_list=[30, 31, 32])",
        'meshing_session.meshing_utilities.mark_duplicate_faces(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"])',
        'meshing_session.meshing_utilities.mark_duplicate_faces(face_zone_name_pattern="*")',
    ],
    "mark_face_strips_by_height_and_quality": [
        'meshing_session.meshing_utilities.mark_face_strips_by_height_and_quality(face_zone_id_list=[30, 31, 32], strip_type=2, strip_height=2, quality_measure="Size Change", quality_limit=0.5, feature_angle=40)',
        'meshing_session.meshing_utilities.mark_face_strips_by_height_and_quality(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"], strip_type=2, strip_height=2, quality_measure="Size Change", quality_limit=0.5, feature_angle=40)',
        'meshing_session.meshing_utilities.mark_face_strips_by_height_and_quality(face_zone_name_pattern="cold*", strip_type=2, strip_height=2, quality_measure="Size Change", quality_limit=0.5, feature_angle=40)',
    ],
    "mark_faces_by_quality": [
        'meshing_session.meshing_utilities.mark_faces_by_quality(face_zone_id_list=[30, 31, 32], quality_measure="Skewness", quality_limit=0.9, append_marking=False)',
        'meshing_session.meshing_utilities.mark_faces_by_quality(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"], quality_measure="Skewness", quality_limit=0.9, append_marking=False)',
        'meshing_session.meshing_utilities.mark_faces_by_quality(face_zone_name_pattern="*", quality_measure="Skewness", quality_limit=0.9, append_marking=False)',
    ],
    "mark_faces_deviating_from_size_field": [
        'meshing_session.meshing_utilities.mark_faces_deviating_from_size_field(face_zone_id_list=[30, 31, 32], min_size_factor=0.5, max_size_factor=1.1, size_factor_type_to_compare="geodesic")',
        'meshing_session.meshing_utilities.mark_faces_deviating_from_size_field(face_zone_name_list=["cold-inlet", "hot-inlet"] min_size_factor=0.5, max_size_factor=1.1, size_factor_type_to_compare="geodesic")',
        'meshing_session.meshing_utilities.mark_faces_deviating_from_size_field(face_zone_name_pattern="*", min_size_factor=0.5, max_size_factor=1.1, size_factor_type_to_compare="geodesic")',
    ],
    "mark_faces_in_self_proximity": [
        "meshing_session.meshing_utilities.mark_faces_in_self_proximity(face_zone_id_list=[30, 31, 32], relative_tolerance=True, tolerance=0.05, proximity_angle=40.5, ignore_orientation=False)",
        'meshing_session.meshing_utilities.mark_faces_in_self_proximity(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"], relative_tolerance=True, tolerance=0.05, proximity_angle=40.5, ignore_orientation=False)',
        'meshing_session.meshing_utilities.mark_faces_in_self_proximity(face_zone_name_pattern="*", relative_tolerance=True, tolerance=0.05, proximity_angle=40.5, ignore_orientation=False)',
    ],
    "mark_faces_using_node_degree": [
        "meshing_session.meshing_utilities.mark_faces_using_node_degree(face_zone_id_list=[30, 31, 32], node_degree_threshold=2)",
        'meshing_session.meshing_utilities.mark_faces_using_node_degree(face_zone_name_list=["cold-inlet", "hot-inlet"], node_degree_threshold=2)',
        'meshing_session.meshing_utilities.mark_faces_using_node_degree(face_zone_name_pattern="*", node_degree_threshold=2)',
    ],
    "mark_free_faces": [
        "meshing_session.meshing_utilities.mark_free_faces(face_zone_id_list=[30, 31, 32])",
        'meshing_session.meshing_utilities.mark_free_faces(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"])',
        'meshing_session.meshing_utilities.mark_free_faces(face_zone_name_pattern="*")',
    ],
    "mark_invalid_normals": [
        "meshing_session.meshing_utilities.mark_invalid_normals(face_zone_id_list=[30, 31, 32])",
        'meshing_session.meshing_utilities.mark_invalid_normals(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"])',
        'meshing_session.meshing_utilities.mark_invalid_normals(face_zone_name_pattern="*")',
    ],
    "mark_island_faces": [
        "meshing_session.meshing_utilities.mark_island_faces(face_zone_id_list=[30, 31, 32], island_face_count=5)",
        'meshing_session.meshing_utilities.mark_island_faces(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"], island_face_count=5)',
        'meshing_session.meshing_utilities.mark_island_faces(face_zone_name_pattern="cold*", island_face_count=5)',
    ],
    "mark_multi_faces": [
        "meshing_session.meshing_utilities.mark_multi_faces(face_zone_id_list=[30, 31, 32], fringe_length=5)",
        'meshing_session.meshing_utilities.mark_multi_faces(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"], fringe_length=5)',
        'meshing_session.meshing_utilities.mark_multi_faces(face_zone_name_pattern="cold*", fringe_length=5)',
    ],
    "mark_point_contacts": [
        "meshing_session.meshing_utilities.mark_point_contacts(face_zone_id_list=[30, 31, 32])",
        'meshing_session.meshing_utilities.mark_point_contacts(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"])',
        'meshing_session.meshing_utilities.mark_point_contacts(face_zone_name_pattern="cold*")',
    ],
    "mark_self_intersecting_faces": [
        "meshing_session.meshing_utilities.mark_self_intersecting_faces(face_zone_id_list=[30, 31, 32], mark_folded=True)",
        'meshing_session.meshing_utilities.mark_self_intersecting_faces(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"], mark_folded=True)',
        'meshing_session.meshing_utilities.mark_self_intersecting_faces(face_zone_name_pattern="cold*", mark_folded=True)',
    ],
    "mark_sliver_faces": [
        "meshing_session.meshing_utilities.mark_sliver_faces(face_zone_id_list=[30, 31, 32], max_height=2, skew_limit=0.2)",
        'meshing_session.meshing_utilities.mark_sliver_faces(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"], max_height=2, skew_limit=0.2)',
        'meshing_session.meshing_utilities.mark_sliver_faces(face_zone_name_pattern="cold*", max_height=2, skew_limit=0.2)',
    ],
    "mark_spikes": [
        "meshing_session.meshing_utilities.mark_spikes(face_zone_id_list=[30, 31, 32], spike_angle=40.5)",
        'meshing_session.meshing_utilities.mark_spikes(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"], spike_angle=40.5)',
        'meshing_session.meshing_utilities.mark_spikes(face_zone_name_pattern="cold*", spike_angle=40.5)',
    ],
    "mark_steps": [
        "meshing_session.meshing_utilities.mark_steps(face_zone_id_list=[30, 31, 32], step_angle=40.5, step_width=3.3)",
        'meshing_session.meshing_utilities.mark_steps(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"], step_angle=40.5, step_width=3.3)',
        'meshing_session.meshing_utilities.mark_steps(face_zone_name_pattern="cold*", step_angle=40.5, step_width=3.3)',
    ],
    "mesh_check": [
        'meshing_session.meshing_utilities.mesh_check(type_name="face-children", edge_zone_id_list=[22, 23], face_zone_id_list=[30, 31, 32], cell_zone_id_list=[87])',
        'meshing_session.meshing_utilities.mesh_check(type_name="nodes-per-cell", edge_zone_name_pattern="cold-inlet*", face_zone_id_list=[30, 31, 32], cell_zone_id_list=[87])',
        'meshing_session.meshing_utilities.mesh_check(type_name="volume-statistics", edge_zone_id_list=[22, 23], face_zone_name_pattern="*", cell_zone_id_list=[87])',
        'meshing_session.meshing_utilities.mesh_check(type_name="nodes-per-cell", edge_zone_name_pattern="cold-inlet*", face_zone_name_pattern="*", cell_zone_id_list=[87])',
        'meshing_session.meshing_utilities.mesh_check(type_name="face-children", edge_zone_id_list=[22, 23], face_zone_id_list=[30, 31, 32], cell_zone_name_pattern="*")',
        'meshing_session.meshing_utilities.mesh_check(type_name="volume-statistics", edge_zone_name_pattern="cold-inlet*", face_zone_name_pattern="*", cell_zone_name_pattern="*")',
    ],
    "mesh_exists": ["meshing_session.meshing_utilities.mesh_exists()"],
    "print_worst_quality_cell": [
        'meshing_session.meshing_utilities.print_worst_quality_cell(cell_zone_id_list=[87], measure="Orthogonal Quality")',
        'meshing_session.meshing_utilities.print_worst_quality_cell(cell_zone_name_list=["elbow-fluid"], measure="Orthogonal Quality")',
        'meshing_session.meshing_utilities.print_worst_quality_cell(cell_zone_name_pattern="*", measure="Orthogonal Quality")',
    ],
    "project_zone_on_plane": [
        "meshing_session.meshing_utilities.project_zone_on_plane(zone_id=87, plane=[[1, 0, 0], [0, 1, 0], [0, 0, 1]])"
    ],
    "refine_marked_faces_in_zones": [
        "meshing_session.meshing_utilities.refine_marked_faces_in_zones(face_zone_id_list=[30, 31, 32])",
        'meshing_session.meshing_utilities.refine_marked_faces_in_zones(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"])',
        'meshing_session.meshing_utilities.refine_marked_faces_in_zones(face_zone_name_pattern="cold*")',
    ],
    "scale_cell_zones_around_pivot": [
        "meshing_session.meshing_utilities.scale_cell_zones_around_pivot(cell_zone_id_list=[87], scale=[1.1, 1.2, 1.3], pivot=[1.1482939720153809, -2.2965879440307617, 0.7345014897547645], use_bbox_center=True)",
        'meshing_session.meshing_utilities.scale_cell_zones_around_pivot(cell_zone_name_list=["elbow-fluid"], scale=[1.1, 1.2, 1.3], pivot=[1.1482939720153809, -2.2965879440307617, 0.7345014897547645], use_bbox_center=True)',
        'meshing_session.meshing_utilities.scale_cell_zones_around_pivot(cell_zone_name_pattern="*", scale=[1.1, 1.2, 1.3], pivot=[1.1482939720153809, -2.2965879440307617, 0.7345014897547645], use_bbox_center=True)',
    ],
    "scale_face_zones_around_pivot": [
        "meshing_session.meshing_utilities.scale_face_zones_around_pivot(face_zone_id_list=[30, 31, 32], scale=[1.1, 1.2, 1.3], pivot=[1.1482939720153809, -2.2965879440307617, 0.7345014897547645], use_bbox_center=True)",
        'meshing_session.meshing_utilities.scale_face_zones_around_pivot(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"], scale=[1.1, 1.2, 1.3], pivot=[1.1482939720153809, -2.2965879440307617, 0.7345014897547645], use_bbox_center=True)',
        'meshing_session.meshing_utilities.scale_face_zones_around_pivot(face_zone_name_pattern="*", scale=[1.1, 1.2, 1.3], pivot=[1.1482939720153809, -2.2965879440307617, 0.7345014897547645], use_bbox_center=True)',
    ],
    "separate_cell_zone_layers_by_face_zone_using_id": [
        "meshing_session.meshing_utilities.separate_cell_zone_layers_by_face_zone_using_id(cell_zone_id=87, face_zone_id_list=[30, 31, 32], nlayers=2)",
        'meshing_session.meshing_utilities.separate_cell_zone_layers_by_face_zone_using_id(cell_zone_id=87, face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"], nlayers=2)',
        'meshing_session.meshing_utilities.separate_cell_zone_layers_by_face_zone_using_id(cell_zone_id=87, face_zone_name_pattern="*", nlayers=2)',
    ],
    "separate_cell_zone_layers_by_face_zone_using_name": [
        'meshing_session.meshing_utilities.separate_cell_zone_layers_by_face_zone_using_name(cell_zone_name="elbow-fluid", face_zone_id_list=[30, 31, 32], nlayers=2)',
        'meshing_session.meshing_utilities.separate_cell_zone_layers_by_face_zone_using_name(cell_zone_name="elbow-fluid", face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"], nlayers=2)',
        'meshing_session.meshing_utilities.separate_cell_zone_layers_by_face_zone_using_name(cell_zone_name="elbow-fluid", face_zone_name_pattern="*", nlayers=2)',
    ],
    "separate_face_zones_by_cell_neighbor": [
        "meshing_session.meshing_utilities.separate_face_zones_by_cell_neighbor(face_zone_id_list=[30, 31, 32])",
        'meshing_session.meshing_utilities.separate_face_zones_by_cell_neighbor(face_zone_name_list=["cold-inlet", "hot-inlet", "outlet"])',
        'meshing_session.meshing_utilities.separate_face_zones_by_cell_neighbor(face_zone_name_pattern="cold*")',
    ],
    "unpreserve_cell_zones": [
        "meshing_session.meshing_utilities.unpreserve_cell_zones(cell_zone_id_list=[87])",
        'meshing_session.meshing_utilities.unpreserve_cell_zones(cell_zone_name_list=["elbow-fluid"])',
        'meshing_session.meshing_utilities.unpreserve_cell_zones(cell_zone_name_pattern="*")',
    ],
}
