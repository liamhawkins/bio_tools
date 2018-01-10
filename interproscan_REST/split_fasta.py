#!/usr/bin/env python3

#=====================================================#
# Script for exploding FASTA files into individual
# FASTA files
#
# Author: Terry Mun <hello@terrymun.com>
# Date: November 9, 2016
#=====================================================#

# Load libraries
import os, sys, time, re
from Bio import SeqIO

# File path
currentDir = os.path.dirname(os.path.realpath(__file__))

# Configuration
minSeqLength = 80

# Start reading/writing
with \
open(currentDir + '/badRecords.txt', 'w') as badRecordsFile, \
open(currentDir + '/correctedRecords.txt', 'w') as correctedRecordsFile, \
open(currentDir + '/shortRecords.txt', 'w') as shortRecordsFile, \
open(currentDir + '/<INSERT_FASTA_FILE_HERE>', 'r') as fasta:

  count = 0
  records = {'corrected': [], 'bad': [], 'tooShort': []}

  # Make output directory if not present
  if not os.path.exists(currentDir + '/seqs'):
    os.makedirs(currentDir + '/seqs')

  # Iterate through all records
  for record in SeqIO.parse(fasta, 'fasta'):

    count += 1

    # Only process if sequence is longer than 80 amino acids
    if len(str(record.seq)) >= minSeqLength:

      if re.match(r'(.*)\*$', str(record.seq)):
        records['corrected'].append(record.id)
        correctedRecordsFile.write(record.id+'\n')

      sequence = re.sub(r'(.*)\*$', r'\1', str(record.seq))

      if '*' in sequence:
        records['bad'].append(record.id)
        badRecordsFile.write(record.id+'\n')
        print(str(record.id) + ' Warning: Entry contains non-trailing stop codon.')

      else:
        with open(currentDir + '/seqs/' + record.id + '.fa', 'w') as entry:
          entry.write('>'+str(record.id)+'\n')
          entry.write(sequence+'\n')


      if count%1000 == 0:
        print('Records processed: '+str(count))

    else:
      records['tooShort'].append(record.id)
      shortRecordsFile.write(record.id+'\n')
      print(str(record.id) + ' Warning: Entry is shorter than minimum sequence length of '+str(minSeqLength))
    
  print('====================================')
  print('End of file')
  print('====================================')
  print('Total records processed: '+str(count))
  print('Corrected records (all is good): '+str(len(records['corrected'])))
  print('Problematic records (requires attention): '+str(len(records['bad'])))
  print('Short records (not written): '+str(len(records['tooShort'])))
  print('====================================')
