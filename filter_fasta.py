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
args = parser.parse_args()

input_fasta = list(SeqIO.parse(args.INPUT_FASTA, "fasta"))

with open(args.FILTER_FILE, "r") as f:
    goi = sorted(f.read().split('\n'))

goi_records = []
print('Filtering...')
matches = 0
for gene in goi:
    for record in input_fasta:
        if gene == record.id[:len(gene)]:
            matches += 1
            goi_records.append(record)
            break

print('\nDone!\nMatches:{}\nNo Matches:{}'.format(matches, len(goi)-matches))

SeqIO.write(goi_records, args.OUTPUT_FASTA, "fasta")

