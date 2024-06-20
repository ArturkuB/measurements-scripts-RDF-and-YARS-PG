import rdflib

def turtle_to_ntriples(input_file, output_file):
    g = rdflib.Graph()

    g.parse(input_file, format='turtle')

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(g.serialize(format='nt'))


input_file = 'input//yago_10mln.ttl'
output_file = 'input//yago_10mln.nt'

turtle_to_ntriples(input_file, output_file)
