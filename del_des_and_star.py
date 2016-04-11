#!/usr/bin/env python
#@Description this script can be used to delete description of seqs in fasta file
#Need biopython
#Usage python treat_fasta.py fastafile

from Bio import SeqIO
import sys

try:
    sys.argv[1]
except IndexError:
    print "Please input a fasta file"
    exit(1)

out = open("%s.s.fa"%sys.argv[1].split(".")[0],"w")

for seqs in SeqIO.parse(sys.argv[1],"fasta"):
    if "*" == str(seqs.seq)[-1]:
        out.write(">%s\n%s\n"%(str(seqs.id),str(seqs.seq)[:-1]))
    elif "*" != str(seqs.seq)[-1]:
        out.write(">%s\n%s\n"%(str(seqs.id),str(seqs.seq)))
out.close()
