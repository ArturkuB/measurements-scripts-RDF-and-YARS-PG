import timeit
import gzip
import brotli
import zstandard as zstd
import snappy
from yarspglib.parser.YARSpgProcessor import YARSpgProcessor

def decompress_file(input_file: str, output_file: str, decompress_func) -> None:
    with open(input_file, "rb") as f_in:
        compressed_data = f_in.read()
        decompressed_data = decompress_func(compressed_data)
        with open(output_file, "wb") as f_out:
            f_out.write(decompressed_data)

def decompress_with_gzip(data: bytes) -> bytes:
    return gzip.decompress(data)

def decompress_with_brotli(data: bytes) -> bytes:
    return brotli.decompress(data)

def decompress_with_zstd(data: bytes) -> bytes:
    return zstd.ZstdDecompressor().decompress(data)

def decompress_with_snappy(data: bytes) -> bytes:
    return snappy.decompress(data)

def parse_yarspg(input_file: str, output_file: str) -> None:
    with open(input_file, "r", encoding="utf8") as file:
        yarspg_data = file.read()
    processor = YARSpgProcessor()
    processor.process_YARSpg(yarspg_data)
    with open(output_file, "wb") as f:
        processor.graph.serialize(f, format='nt', encoding="utf-8")

def combine_sections(nodes_file: str, edges_file: str, combined_file: str) -> None:
    with open(combined_file, "w", encoding="utf-8") as f_out:
        with open(nodes_file, "r", encoding="utf-8") as nodes_in:
            f_out.write("# Nodes\n")
            f_out.write(nodes_in.read())
        f_out.write("\n# Edges\n")
        with open(edges_file, "r", encoding="utf-8") as edges_in:
            f_out.write(edges_in.read())

def measure_time(func, *args) -> float:
    start_time = timeit.default_timer()
    func(*args)
    end_time = timeit.default_timer()
    return end_time - start_time

compression_methods = ["gzip", "brotli", "zstd", "snappy"]
nodes_compressed_files = {method: f"input//wikidata_1.5mln_nodes.{method[:2]}" for method in compression_methods}
edges_compressed_files = {method: f"input//wikidata_1.5mln_edges.{method[:2]}" for method in compression_methods}
decompressed_nodes_file = f"input//wikidata_1.5mln_nodes.yarspg"
decompressed_edges_file = f"input//wikidata_1.5mln_edges.yarspg"
combined_file = f"input//wikidata_1.5mln_combined.yarspg"
output_file = f"input//wikidata_1.5mln_sections.nt"

decompress_times = {method: [] for method in compression_methods}

for compression_method in compression_methods:
    for _ in range(5):
        if compression_method == "gzip":
            decompress_time_nodes = measure_time(decompress_file, nodes_compressed_files[compression_method], decompressed_nodes_file, decompress_with_gzip)
            decompress_time_edges = measure_time(decompress_file, edges_compressed_files[compression_method], decompressed_edges_file, decompress_with_gzip)
        elif compression_method == "brotli":
            decompress_time_nodes = measure_time(decompress_file, nodes_compressed_files[compression_method], decompressed_nodes_file, decompress_with_brotli)
            decompress_time_edges = measure_time(decompress_file, edges_compressed_files[compression_method], decompressed_edges_file, decompress_with_brotli)
        elif compression_method == "zstd":
            decompress_time_nodes = measure_time(decompress_file, nodes_compressed_files[compression_method], decompressed_nodes_file, decompress_with_zstd)
            decompress_time_edges = measure_time(decompress_file, edges_compressed_files[compression_method], decompressed_edges_file, decompress_with_zstd)
        elif compression_method == "snappy":
            decompress_time_nodes = measure_time(decompress_file, nodes_compressed_files[compression_method], decompressed_nodes_file, decompress_with_snappy)
            decompress_time_edges = measure_time(decompress_file, edges_compressed_files[compression_method], decompressed_edges_file, decompress_with_snappy)
        else:
            raise ValueError(f"Unknown compression method: {compression_method}")

        total_decompress_time = decompress_time_nodes + decompress_time_edges
        decompress_times[compression_method].append(total_decompress_time)

average_decompress_times = {method: sum(times) / len(times) for method, times in decompress_times.items()}

for method, times in decompress_times.items():
    print(f"Czasy dekompresji {method}: {times}")
    print(f"Średni czas dekompresji {method} (w sekundach): {average_decompress_times[method]}")

combine_sections(decompressed_nodes_file, decompressed_edges_file, combined_file)

parse_time = measure_time(parse_yarspg, combined_file, output_file)
print(f"Czas parsowania (w sekundach): {parse_time}")

for method, avg_decompress_time in average_decompress_times.items():
    total_time = avg_decompress_time + parse_time
    print(f"Czas dekompresji {method} i potem parsowania (w sekundach): {total_time}")
