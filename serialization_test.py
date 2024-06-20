from rdflib import Graph
from yarspglib.serializer.YARSpgSerializer import YARSpgSerializer

graph = Graph()



def execute_code():
    graph.parse("input\\wikidata_10mln.nt", format="nt")
    serializer = YARSpgSerializer(graph)
    with open("input\\wikidata_10mln.yarspg", "wb") as f:
        serializer.serialize(f)


execute_code()
