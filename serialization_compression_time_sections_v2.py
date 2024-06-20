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
    return gzip.compress(data, compresslevel=9)


def compress_with_brotli(data: bytes) -> bytes:
    return brotli.compress(data, quality=9)


def compress_with_zstd(data: bytes) -> bytes:
    return zstd.ZstdCompressor(level=19).compress(data)


def compress_with_snappy(data: bytes) -> bytes:
    return snappy.compress(data)


def measure_time(func, *args) -> float:
    start_time = timeit.default_timer()
    result = func(*args)
    end_time = timeit.default_timer()
    return end_time - start_time, result


def write_to_file(data: bytes, output_file: str):
    with open(output_file, "wb") as f:
        f.write(data)


compression_methods = ["gzip", "brotli", "zstd", "snappy"]
input_file = f"input//wikidata_1.5mln.nt"
temp_file = f"input//wikidata_1.5mln.yarspg"


serialize_time, _ = measure_time(serialize_rdf_to_yarspg, input_file, temp_file)
print(f"Czas serializacji (w sekundach): {serialize_time}")

nodes_section, edges_section = split_yarspg(temp_file)

for compression_method in compression_methods:
    nodes_output_file = f"input//wikidata_1.5mln_nodes.{compression_method[:2]}"
    edges_output_file = f"input//wikidata_1.5mln_edges.{compression_method[:2]}"

    nodes_compression_times = []
    edges_compression_times = []

    for _ in range(2):
        if compression_method == "gzip":
            nodes_compressed_time, nodes_compressed = measure_time(compress_data,
                                                                   "\n".join(nodes_section).encode('utf-8'),
                                                                   compress_with_gzip)
            edges_compressed_time, edges_compressed = measure_time(compress_data,
                                                                   "\n".join(edges_section).encode('utf-8'),
                                                                   compress_with_gzip)
        elif compression_method == "brotli":
            nodes_compressed_time, nodes_compressed = measure_time(compress_data,
                                                                   "\n".join(nodes_section).encode('utf-8'),
                                                                   compress_with_brotli)
            edges_compressed_time, edges_compressed = measure_time(compress_data,
                                                                   "\n".join(edges_section).encode('utf-8'),
                                                                   compress_with_brotli)
        elif compression_method == "zstd":
            nodes_compressed_time, nodes_compressed = measure_time(compress_data,
                                                                   "\n".join(nodes_section).encode('utf-8'),
                                                                   compress_with_zstd)
            edges_compressed_time, edges_compressed = measure_time(compress_data,
                                                                   "\n".join(edges_section).encode('utf-8'),
                                                                   compress_with_zstd)
        elif compression_method == "snappy":
            nodes_compressed_time, nodes_compressed = measure_time(compress_data,
                                                                   "\n".join(nodes_section).encode('utf-8'),
                                                                   compress_with_snappy)
            edges_compressed_time, edges_compressed = measure_time(compress_data,
                                                                   "\n".join(edges_section).encode('utf-8'),
                                                                   compress_with_snappy)
        else:
            raise ValueError(f"Unknown compression method: {compression_method}")

        nodes_compression_times.append(nodes_compressed_time)
        edges_compression_times.append(edges_compressed_time)

        write_to_file(nodes_compressed, nodes_output_file)
        write_to_file(edges_compressed, edges_output_file)

    print(f"Czasy kompresji węzłów {compression_method} (w sekundach): {nodes_compression_times}")
    print(f"Czasy kompresji krawędzi {compression_method} (w sekundach): {edges_compression_times}")

    avg_nodes_compression_time = sum(nodes_compression_times) / len(nodes_compression_times)
    avg_edges_compression_time = sum(edges_compression_times) / len(edges_compression_times)

    print(f"Średni czas kompresji węzłów {compression_method} (w sekundach): {avg_nodes_compression_time}")
    print(f"Średni czas kompresji krawędzi {compression_method} (w sekundach): {avg_edges_compression_time}")

    print(f"Suma dla {compression_method}:", (avg_edges_compression_time + avg_edges_compression_time) )