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
        "*_contents.rst"]
).load_data()

# Parse documents into nodes
splitter = SentenceSplitter(
    chunk_size=512,
    chunk_overlap=50
)

nodes = splitter.get_nodes_from_documents(documents)

print(f"Total nodes: {len(nodes)}")
print(f"\nFirst node ID: {nodes[0].node_id}")
print(f"First node metadata: {nodes[0].metadata}")
print(f"First node text:\n{nodes[0].text}")

for i, node in enumerate(nodes):
    print(f"{i:3d} | {node.metadata['file_name']:40s} | {len(node.text):5d} chars")
    
#for i in [55, 115, 142, 143]:
#    print(f"\n--- Node {i} ({nodes[i].metadata['file_name']}) ---")
#    print(nodes[i].text)
    
# Filter out orphaned fragments but keep intentionally small docs
MIN_CHARS = 300

# Files where ALL nodes are small (genuine stubs worth keeping)
file_total_chars = {}
for node in nodes:
    fname = node.metadata['file_name']
    file_total_chars[fname] = file_total_chars.get(fname, 0) + len(node.text)

stub_files = {fname for fname, total in file_total_chars.items() if total < 1000}

filtered_nodes = [
    node for node in nodes
    if len(node.text) >= MIN_CHARS or node.metadata['file_name'] in stub_files
]


other_nodes = [
    node for node in nodes
    if len(node.text) < MIN_CHARS and node.metadata['file_name'] not in stub_files
]

retained_files = {node.metadata['file_name'] for node in filtered_nodes}

print(f"Nodes after filtering: {len(filtered_nodes)}")
print(f"Stub files retained: {stub_files}")
print(f"Dropped {len(nodes) - len(filtered_nodes)} orphaned fragment nodes")
print(f"Small nodes dropped from files: {[node.metadata['file_name'] for node in other_nodes]}")
print(f"Files still represented: {sorted(retained_files)}")
