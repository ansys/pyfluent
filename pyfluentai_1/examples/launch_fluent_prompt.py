import os

from llama_index.core import (
    Settings,
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

PERSIST_DIR = "./pyfluent_index"

# Set up local embedding model
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

if os.path.exists(PERSIST_DIR):
    print("Loading index from disk...")
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)
else:
    print("Building index from scratch...")
    documents = SimpleDirectoryReader(
        input_dir="../docsource",
        recursive=True,
        required_exts=[".rst"],
        exclude=[
            "changelog.rst",
            "contributing_contents.rst",
            "sg_execution_times.rst",
            "index.rst",
            "*_contents.rst",
        ],
    ).load_data()

    splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)
    nodes = splitter.get_nodes_from_documents(documents)

    MIN_CHARS = 300
    file_total_chars = {}
    for node in nodes:
        fname = node.metadata["file_name"]
        file_total_chars[fname] = file_total_chars.get(fname, 0) + len(node.text)

    stub_files = {fname for fname, total in file_total_chars.items() if total < 1000}

    filtered_nodes = [
        node
        for node in nodes
        if len(node.text) >= MIN_CHARS or node.metadata["file_name"] in stub_files
    ]

    index = VectorStoreIndex(filtered_nodes)
    index.storage_context.persist(persist_dir=PERSIST_DIR)
    print(f"Index built and saved to {PERSIST_DIR}")

retriever = index.as_retriever(similarity_top_k=5)

# Quick sanity check
test_query = "How do I launch Fluent?"
results = retriever.retrieve(test_query)

print(f"\nQuery: {test_query}")
print(f"Retrieved {len(results)} nodes:\n")
for i, node in enumerate(results):
    print(f"  {i+1}. {node.metadata['file_name']} (score: {node.score:.4f})")
    print(f"     {node.text[:150].strip()}...")
    print()
