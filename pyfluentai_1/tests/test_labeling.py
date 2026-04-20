from pyfluentai.labeling import build_relation_edges, parse_rst_sections

SAMPLE_RST = """.. _ref_launch:

Launching Fluent
================

See :ref:`ref_installation` and :py:func:`launch_fluent <ansys.fluent.core.launch_fluent>`.

.. note::
   A note block.

Setup
-----

.. toctree::
   :maxdepth: 1

   getting_started/installation

Use :doc:`getting_started/installation`.
"""


def test_parse_rst_sections_extracts_section_metadata():
    records = parse_rst_sections(SAMPLE_RST, "getting_started/installation.rst")

    assert len(records) == 2
    assert records[0].section_title == "Launching Fluent"
    assert records[0].heading_path == ["Launching Fluent"]
    assert records[0].anchor_ids == ["ref_launch"]
    assert records[0].directives == ["note"]
    assert {ref["role"] for ref in records[0].explicit_refs} == {"ref", "py:func"}

    assert records[1].section_title == "Setup"
    assert records[1].heading_path == ["Launching Fluent", "Setup"]
    assert records[1].toctree_entries == ["getting_started/installation"]
    assert records[1].content_type == "getting_started"


def test_build_relation_edges_preserves_reference_targets():
    records = parse_rst_sections(SAMPLE_RST, "getting_started/installation.rst")
    edges = build_relation_edges(records)

    relation_types = {edge.relation_type for edge in edges}
    target_ids = {edge.target_id for edge in edges}

    assert "defines_anchor" in relation_types
    assert "references" in relation_types
    assert "api_symbol_ref" in relation_types
    assert "contains" in relation_types
    assert "anchor:ref_launch" in target_ids
    assert "anchor:ref_installation" in target_ids
    assert "entity:ansys.fluent.core.launch_fluent" in target_ids
    assert "doc:getting_started/installation" in target_ids
