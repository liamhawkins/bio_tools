#!/bin/bash
# Takes list of UNIPROT accession IDs and downloads sequences in FASTA format from UNIPROT
# Usage: ./fasta_from_uniprot.sh <ACCESSION_LIST.txt>

sort $1 | uniq | cut -d ';' -f 1 | tr -d '\r' > uniq_ids.temp
mkdir -p ./uniprot_fastas
while read line; do
	wget -O ./uniprot_fastas/$line.fasta www.uniprot.org/uniprot/$line.fasta
done < uniq_ids.temp

rm ./uniq_ids.temp
