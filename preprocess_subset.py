import re

def preprocess_nt_file(input_file: str, output_file: str) -> None:
    date_pattern1 = re.compile(r'"-\d{4}-\d{2}-\d{2}T00:00:00Z"\^\^<http://www.w3.org/2001/XMLSchema#dateTime>')
    date_pattern2 = re.compile(r'"-\d{5,}-\d{2}-\d{2}T00:00:00Z"\^\^<http://www.w3.org/2001/XMLSchema#dateTime>')
    date_pattern3 = re.compile(r'"-\d{4}-\d{2}-\d{2}T00:00:00Z"\^\^xsd:dateTime')
    date_pattern4 = re.compile(r'"-\d{5,}-\d{2}-\d{2}T00:00:00Z"\^\^xsd:dateTime')

    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            if not date_pattern1.search(line) and not date_pattern2.search(line) and not date_pattern3.search(line) and not date_pattern4.search(line):
                outfile.write(line)

input_file = "input//yago_15mln.ttl"
preprocessed_file = "input//yago_15mln_processed.ttl"

preprocess_nt_file(input_file, preprocessed_file)
