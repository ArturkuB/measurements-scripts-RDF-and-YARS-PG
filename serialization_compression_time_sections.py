import timeit
import gzip
import brotli
import zstandard as zstd
import snappy
from rdflib import Graph
from yarspglib.serializer.YARSpgSerializer import YARSpgSerializer

graph = Graph()

def serialize_rdf_to_yarspg(input_file: str, temp_file: str) -> None:
    graph.parse(input_file, format="nt")
    serializer = YARSpgSerializer(graph)
    with open(temp_file, "wb") as f:
        serializer.serialize(f)

def split_yarspg(temp_file: str):
    with open(temp_file, "r", encoding="utf-8") as file:
        nodes_section = []
        edges_section = []
        section = None

        for line in file:
            line_lower = line.lower()
            if line_lower.startswith("#nodes") or line_lower.startswith("# nodes") or line_lower.startswith("#nodes") or line_lower.startswith("# nodes") or line_lower.startswith("%nodes") or line_lower.startswith("% nodes"):
                section = "nodes"
            elif line_lower.startswith("#edges") or line_lower.startswith("# edges") or line_lower.startswith("#edges") or line_lower.startswith("# edges") or line_lower.startswith("%edges") or line_lower.startswith("% edges"):
                section = "edges"
            elif section == "nodes":
                nodes_section.append(line)
            elif section == "edges":
                edges_section.append(line)
    return nodes_section, edges_section

def compress_data(data: bytes, compress_func) -> bytes:
    return compress_func(data)

def compress_with_gzip(data: bytes) -> bytes:
    return gzip.compress(data)

def compress_with_brotli(data: bytes) -> bytes:
    return brotli.compress(data)

def compress_with_zstd(data: bytes) -> bytes:
    return zstd.ZstdCompressor().compress(data)

def compress_with_snappy(data: bytes) -> bytes:
    return snappy.compress(data)

def measure_time(func, *args) -> float:
    start_time = timeit.default_timer()
    func(*args)
    end_time = timeit.default_timer()
    return end_time - start_time

def write_combined_file(nodes_data: bytes, edges_data: bytes, output_file: str):
    with open(output_file, "wb") as f:
        f.write(b"# Nodes\n")
        f.write(nodes_data)
        f.write(b"\n# Edges\n")
        f.write(edges_data)

testset = "hdo"
compression_method = "gzip"
input_file = f"input\\{testset}.nt"
temp_file = f"input\\{testset}_sections.yarspg"
output_file = f"input\\{testset}.yarspg.sections.{compression_method[:2]}"

serialize_time = measure_time(serialize_rdf_to_yarspg, input_file, temp_file)
print(f"Czas serializacji (w sekundach): {serialize_time}")

nodes_section, edges_section = split_yarspg(temp_file)

if compression_method == "gzip":
    nodes_compressed = compress_data("\n".join(nodes_section).encode('utf-8'), compress_with_gzip)
    edges_compressed = compress_data("\n".join(edges_section).encode('utf-8'), compress_with_gzip)
elif compression_method == "brotli":
    nodes_compressed = compress_data("\n".join(nodes_section).encode('utf-8'), compress_with_brotli)
    edges_compressed = compress_data("\n".join(edges_section).encode('utf-8'), compress_with_brotli)
elif compression_method == "zstd":
    nodes_compressed = compress_data("\n".join(nodes_section).encode('utf-8'), compress_with_zstd)
    edges_compressed = compress_data("\n".join(edges_section).encode('utf-8'), compress_with_zstd)
elif compression_method == "snappy":
    nodes_compressed = compress_data("\n".join(nodes_section).encode('utf-8'), compress_with_snappy)
    edges_compressed = compress_data("\n".join(edges_section).encode('utf-8'), compress_with_snappy)
else:
    raise ValueError(f"Unknown compression method: {compression_method}")

combine_time = measure_time(write_combined_file, nodes_compressed, edges_compressed, output_file)

print(f"Czas kompresji {compression_method} (w sekundach): {combine_time}")
print(f"Czas serializacji i potem kompresji w {compression_method} (w sekundach): {serialize_time + combine_time}")
