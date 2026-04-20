from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter

# Load the RST docs
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

print(f"Loaded {len(documents)} documents")
print(f"\nFirst document metadata:\n{documents[0].metadata}")
print(f"\nFirst document text snippet:\n{documents[0].text[:500]}")

for doc in documents:
    print(doc.metadata["file_name"])
