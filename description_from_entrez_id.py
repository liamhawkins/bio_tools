from Bio import Entrez
from argparse import ArgumentParser

parser = ArgumentParser(description='Query NCBI Entrez database with entrez IDs for protein descriptions')
parser.add_argument('-i', '--input', dest='input_file', required=True, help='input file containing one entrez ID per line', metavar='FILE')
parser.add_argument('-o', '--ouput', dest='output_file', required=True, help='output file (.csv)', metavar='FILE')
parser.add_argument('-e', '--email', dest='email', required=True, help='Email address to identify yourself to NCBI', metavar='EMAIL')

args = parser.parse_args()

input_file = args.input_file
output_file = args.output_file
Entrez.email = args.email

with open(input_file) as f:
    ids = f.read().splitlines()

handle = Entrez.esummary(db='protein', id=ids, retmode='xml')
records = list(Entrez.parse(handle))

with open(output_file, 'w') as f:
    for entrez_id, record in zip([ids, records]):
        f.write(str(entrez_id) + ',' + record['Title'] + '\n')
