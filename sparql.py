from SPARQLWrapper import SPARQLWrapper, TURTLE
import rdflib
import time

def fetch_and_save_dbpedia_data(output_file, batch_size=10000, total_rows=10000000, max_retries=5):
    sparql_endpoint = "https://dbpedia.org/sparql"
    offset = 0

    while offset < total_rows:
        g = rdflib.Graph()
        query = f"""
            CONSTRUCT {{
                ?subject ?predicate ?object .
            }}
            WHERE {{
                ?subject ?predicate ?object .
            }}
            LIMIT {batch_size}
            OFFSET {offset}
        """
        sparql = SPARQLWrapper(sparql_endpoint)
        sparql.setQuery(query)
        sparql.setReturnFormat(TURTLE)

        retries = 0
        while retries < max_retries:
            try:
                results = sparql.query().convert()
                g.parse(data=results, format='turtle')
                break
            except Exception as e:
                print(f"Error fetching data at offset {offset}: {e}")
                retries += 1
                if retries >= max_retries:
                    print(f"Max retries reached at offset {offset}. Stopping.")
                    return
                time.sleep(5)

        if retries < max_retries:
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(g.serialize(format='nt'))
            offset += batch_size
            print(f"Fetched {offset} rows")
        else:
            print(f"Skipping offset {offset} after {max_retries} retries.")
            offset += batch_size

output_file = 'dbpedia_large_dataset.nt'

fetch_and_save_dbpedia_data(output_file, batch_size=10000, total_rows=10000000)
