#!/usr/bin/env python
"""
This script can be used to delete abbre of species in fasta ids
These abbre usually splited by "|" with seqs ids, just like ">abbre|seqsids"
"""
from Bio import SeqIO
import sys

try:
    sys.argv[1]
except IndexError:
    print "Usage: python del_abbre.py fastafile"
    exit(1)

out = open("%s.fa"%sys.argv[1].split(".")[0].lower(),"w")
for seqs in SeqIO.parse(sys.argv[1],"fasta"):
    out.write(">%s\n%s\n"%(str(seqs.id).split("|")[1],str(seqs.seq)))
out.close()
