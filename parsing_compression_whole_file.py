import timeit
import gzip
import brotli
import zstandard as zstd
import snappy
from yarspglib.parser.YARSpgProcessor import YARSpgProcessor

def decompress_file(input_file: str, output_file: str, decompress_func) -> None:
    with open(input_file, "rb") as f_in:
        compressed_data = f_in.read()
        data = decompress_func(compressed_data)
        with open(output_file, "wb") as f_out:
            f_out.write(data)

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

def measure_time(func, *args) -> float:
    start_time = timeit.default_timer()
    func(*args)
    end_time = timeit.default_timer()
    return end_time - start_time

compression_methods = ["gzip", "brotli", "zstd", "snappy"]
compressed_files = {method: f"input//wikidata_1.5mln.yarspg.{method[:2]}" for method in compression_methods}
decompressed_file = f"input//wikidata_1.5mln_decompressed.yarspg"
output_file = f"input//wikidata_1.5mln_wholefile.nt"

decompress_times = {method: [] for method in compression_methods}

for compression_method in compression_methods:
    for _ in range(5):
        if compression_method == "gzip":
            decompress_time = measure_time(decompress_file, compressed_files[compression_method], decompressed_file, decompress_with_gzip)
        elif compression_method == "brotli":
            decompress_time = measure_time(decompress_file, compressed_files[compression_method], decompressed_file, decompress_with_brotli)
        elif compression_method == "zstd":
            decompress_time = measure_time(decompress_file, compressed_files[compression_method], decompressed_file, decompress_with_zstd)
        elif compression_method == "snappy":
            decompress_time = measure_time(decompress_file, compressed_files[compression_method], decompressed_file, decompress_with_snappy)
        else:
            raise ValueError(f"Unknown compression method: {compression_method}")

        decompress_times[compression_method].append(decompress_time)

for method, times in decompress_times.items():
    print(f"Czasy dekompresji {method}: {times}")
    average_time = sum(times) / len(times)
    print(f"Średni czas dekompresji {method} (w sekundach): {average_time}")

parse_time = measure_time(parse_yarspg, decompressed_file, output_file)
print(f"Czas parsowania (w sekundach): {parse_time}")

for method, times in decompress_times.items():
    average_time = sum(times) / len(times)
    total_time = average_time + parse_time
    print(f"Czas dekompresji {method} i potem parsowania (w sekundach): {total_time}")
