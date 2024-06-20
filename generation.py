import random
import argparse

def generate_rdf(num_triples, format, output_file):
    ns = "https://w3id.org/MON/person.owl#"
    nodes = [f"https://example.org/N{i+1}" for i in range(num_triples // 2)]

    triples = []
    for _ in range(num_triples):
        subject = nodes[random.randint(0, len(nodes) - 1)]
        predicate = f"{ns}friendOf"
        obj = nodes[random.randint(0, len(nodes) - 1)]
        while subject == obj:
            obj = nodes[random.randint(0, len(nodes) - 1)]
        triples.append((subject, predicate, obj))

    with open(output_file, 'w', encoding='utf-8') as f:
        if format == 'nt':
            for subject, predicate, obj in triples:
                f.write(f"<{subject}> <{predicate}> <{obj}> .\n")

def main():
    parser = argparse.ArgumentParser(description='Generate synthetic RDF data.')
    parser.add_argument('num_triples', type=int, help='Number of RDF triples to generate')
    parser.add_argument('--format', type=str, choices=['nt', 'ttl'], default='nt', help='Output format: nt for N-Triples, ttl for Turtle')
    parser.add_argument('--output', type=str, required=True, help='Output file name')
    args = parser.parse_args()

    generate_rdf(args.num_triples, args.format, args.output)
    print(f"RDF data has been written to {args.output}")

if __name__ == "__main__":
    main()
