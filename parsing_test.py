from yarspglib.parser.YARSpgProcessor import YARSpgProcessor

with open("input//wikidata_10mln.yarspg", "r", encoding="utf8") as file:
    yarspg_data = file.read()

def execute_code():
    processor = YARSpgProcessor()
    processor.process_YARSpg(yarspg_data)
    processor.graph.serialize(format='turtle')


execute_code()
