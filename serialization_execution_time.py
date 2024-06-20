from rdflib import Graph
from yarspglib.serializer.YARSpgSerializer import YARSpgSerializer
import timeit

graph = Graph()



def execute_code():
    graph.parse("input//sample100k.nt", format="nt")
    serializer = YARSpgSerializer(graph)
    with open("..//input//sample100k.yarspg", "wb") as f:
        serializer.serialize(f)

repeat_count = 1
execution_times = []

for _ in range(repeat_count):
    start_time = timeit.default_timer()
    graph = Graph()
    execute_code()
    end_time = timeit.default_timer()
    execution_times.append(end_time - start_time)

average_execution_time = sum(execution_times) / len(execution_times)

print("Czasy wykonania (w sekundach):", execution_times)
print("Średni czas wykonania (w sekundach):", average_execution_time)
