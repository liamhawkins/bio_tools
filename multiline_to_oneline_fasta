#!/bin/bash
# Converts multiline FASTA (FASTA with line breaks in sequences) to FASTA with oneline sequences
# Usage: ./multiline_to_oneline_fasta.sh <INPUT.FASTA> > <OUTPUT.FASTA>

awk '/^>/ { print (NR==1 ? "" : RS) $0; next } { printf "%s", $0 } END { printf RS }' $1

