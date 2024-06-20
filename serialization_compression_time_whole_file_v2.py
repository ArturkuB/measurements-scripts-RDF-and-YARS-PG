import timeit
import gzip
import brotli
import zstandard as zstd
import snappy
from rdflib import Graph
from yarspglib.serializer.YARSpgSerializer import YARSpgSerializer

graph = Graph()


def serialize_rdf_to_yarspg(input_file: str, output_file: str) -> None:
    graph.parse(input_file, format="nt")
    serializer = YARSpgSerializer(graph)
    with open(output_file, "wb") as f:
        serializer.serialize(f)


def compress_file(input_file: str, output_file: str, compress_func) -> None:
    with open(input_file, "rb") as f_in:
        data = f_in.read()
        compressed_data = compress_func(data)
        with open(output_file, "wb") as f_out:
            f_out.write(compressed_data)


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
    func(*args)
    end_time = timeit.default_timer()
    return end_time - start_time


input_file = "input//wikidata_1.5mln.nt"
output_yarspg_file = "input//wikidata_1.5mln_before_compression.yarspg"
compression_methods = ["gzip", "brotli", "zstd", "snappy"]

serialize_time = measure_time(serialize_rdf_to_yarspg, input_file, output_yarspg_file)
print(f"Czas serializacji (w sekundach): {serialize_time}")

for compression_method in compression_methods:
    compress_times = []
    for _ in range(2):
        compressed_file = f"input//wikidata_1.5mln.yarspg.{compression_method[:2]}"
        if compression_method == "gzip":
            compress_time = measure_time(compress_file, output_yarspg_file, compressed_file, compress_with_gzip)
        elif compression_method == "brotli":
            compress_time = measure_time(compress_file, output_yarspg_file, compressed_file, compress_with_brotli)
        elif compression_method == "zstd":
            compress_time = measure_time(compress_file, output_yarspg_file, compressed_file, compress_with_zstd)
        elif compression_method == "snappy":
            compress_time = measure_time(compress_file, output_yarspg_file, compressed_file, compress_with_snappy)
        else:
            raise ValueError(f"Unknown compression method: {compression_method}")

        compress_times.append(compress_time)

    print(f"Czasy kompresji {compression_method} (w sekundach): {compress_times}")

    average_compress_time = sum(compress_times) / len(compress_times)
    print(f"Średni czas kompresji {compression_method} (w sekundach): {average_compress_time}")