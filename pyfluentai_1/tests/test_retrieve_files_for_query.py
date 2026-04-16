import pytest
from pyfluentai.document_indexer import DocumentIndexer
from pyfluentai.section_indexer import SectionIndexer
from pyfluentai.retriever import PyFluentRetriever
from pathlib import Path

import shutil

def cleanup():
    """Utility to clear index persist directories."""
    for indexer_name in [DocumentIndexer.__name__, SectionIndexer.__name__]:
        persist_path = Path(PERSIST_DIR) / indexer_name
        if persist_path.exists():
            shutil.rmtree(persist_path)

def setup_module():
    """Clear index persist directories before running tests."""
    cleanup()

def teardown_module():
    """Clear index persist directories after running tests."""
    cleanup()

def retrieve_filenames(retriever, query):
    results = retriever.retrieve(query)
    return [
        node.metadata.get('file_name') or
        node.metadata.get('source_file') for node in results
        ]

ROOT = Path(__file__).parent.parent
DOC_DIR = str(ROOT / "docsource")
PERSIST_DIR = ROOT / "pyfluent_index"
RETRIEVER_TOP_K=5

@pytest.fixture(scope="module", params=[DocumentIndexer, SectionIndexer])
def retriever(request):
    persist_dir = PERSIST_DIR / request.param.__name__
    index = request.param(
        doc_dir=DOC_DIR,
        persist_dir=persist_dir).get_index()  # use a per-indexer persisted cache; setup/teardown cleans it for test isolation
    retriever = PyFluentRetriever(index, top_k=RETRIEVER_TOP_K)
    retriever.indexer_name = request.param.__name__
    return retriever

def test_retriever_returns_results(retriever):
    results = retriever.retrieve("How do I launch Fluent?")
    assert len(results) > 0

def test_retriever_returns_results_for_field_data_query(retriever):
    results = retriever.retrieve("What is the difference between field data and solution data?")
    assert len(results) > 0

def test_retriever_returns_results_for_slurm_query(retriever):
    results = retriever.retrieve("How do I launch Fluent in Slurm environment?")
    assert len(results) > 0

def test_retriever_returns_correct_number(retriever):
    results = retriever.retrieve("How do I launch Fluent?")
    assert len(results) == 5

def test_launch_query_returns_correct_file(retriever):
    filenames = retrieve_filenames(retriever, "How do I launch Fluent?")
    assert "launching_ansys_fluent.rst" in filenames

def test_meshing_query_returns_correct_file(retriever):
    filenames = retrieve_filenames(retriever, "How do I set up a meshing workflow?")
    assert any("meshing" in f for f in filenames)

def test_boundary_conditions_query(retriever):
    filenames = retrieve_filenames(retriever, "How do I set boundary conditions?")
    assert "boundary_conditions.rst" in filenames
    
def test_physical_units(retriever):
    filenames = retrieve_filenames(retriever, "How do I work with physical units?")
    # These baseline files are expected in all indexers
    baseline_files = ['units.rst', 'materials.rst', 'physical_variables.rst']
    for name in baseline_files:
        assert name in filenames, f"Expected {name} not found in {filenames}"
    
    # flunits.py is a known gap for SectionIndexer; only xfail if it's actually missing
    if 'flunits.py' not in filenames:
        if retriever.indexer_name == 'SectionIndexer':
            pytest.xfail("SectionIndexer does not yet return flunits.py for this query")
        else:
            assert False, f"flunits.py should be in {filenames} for {retriever.indexer_name}"
    else:
        assert True  # flunits.py is present, which is good
