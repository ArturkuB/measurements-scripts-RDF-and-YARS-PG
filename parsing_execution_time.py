import timeit

from yarspglib.parser.YARSpgProcessor import YARSpgProcessor

with open("input//wikidata_10mln.yarspg", "r", encoding="utf8") as file:
    yarspg_data = file.read()

def execute_code():
    processor = YARSpgProcessor()
    processor.process_YARSpg(yarspg_data)
    processor.graph.serialize(format='nt')

repeat_count = 1
execution_times = []

for _ in range(repeat_count):
    start_time = timeit.default_timer()
    execute_code()
    end_time = timeit.default_timer()
    execution_times.append(end_time - start_time)

average_execution_time = sum(execution_times) / len(execution_times)

print("Czasy wykonania (w sekundach):", execution_times)
print("Średni czas wykonania (w sekundach):", average_execution_time)
