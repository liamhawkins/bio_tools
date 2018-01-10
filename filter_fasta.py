#!/usr/bin/env python3

from Bio import SeqIO
from argparse import ArgumentParser

parser = ArgumentParser(description="Filters fasta files")
parser.add_argument('-i', '--input', dest='INPUT_FASTA', required=True,
                    help='input fasta file to be filtered', metavar='FILE')
parser.add_argument('-f', '--filter', dest='FILTER_FILE', required=True,
                    help='file containing GOIs corresponding to \
                            FASTA IDs in the input_fasta file', metavar='FILE')
parser.add_argument('-o', '--output', dest='OUTPUT_FASTA', required=True,
                    help='output fasta file containing filtered \
                            results', metavar='FILE')
parser.add_argument('-r', '--reverse', action='store_true',
                    help='Perform reverse filter')
args = parser.parse_args()

input_fasta = list(SeqIO.parse(args.INPUT_FASTA, "fasta"))
input_dict = {record.id:record for record in input_fasta}
input_len = len(input_dict)

#with open(args.FILTER_FILE, "r") as f:
#    goi = sorted(f.read().split('\n'))
goi = open(args.FILTER_FILE).readlines()
goi = [line[:-1] for line in goi]

goi_records = []
print('Filtering...\n')
matches = 0

for gene in goi:
    if gene in input_dict:
        matches += 1
        if args.reverse:
            del input_dict[gene]
        else:
            goi_records.append(input_dict[gene])


print('Input:{}\nFilter:{}'.format(input_len, len(goi)))
print('Matches:{}\nNo Matches:{}'.format(matches, len(goi)-matches))

if args.reverse:
    goi_records = input_dict.values()

print("Records written: {}".format(len(goi_records)))
SeqIO.write(goi_records, args.OUTPUT_FASTA, "fasta")

