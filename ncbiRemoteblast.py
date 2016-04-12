#!/usr/bin/env python

'''
@Description This script can be used to run blast through internet
@Author This script was developed by Ginsea Chen (ginseachen@hotmail.com) in CATAS
'''
from Bio.Blast import NCBIWWW
from Bio import SeqIO
from time import clock
import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser(usage="%(prog)s[options]")
    parser.add_argument("--fasta",default="test.fa",help="Your fasta file")
    parser.add_argument("--type",default="prot",help="Your seqs type: prot or nucl")
    return parser.parse_args()

def create_dir():
    try:
        os.stat("split_xml")
    except OSError:
        os.mkdir("split_xml")

def run_blast(fasta,type):
    if type == "prot":
        for seqs in SeqIO.parse(fasta,"fasta"):
            clock()
            out = open("split_xml/%s.xml"%str(seqs.id),"w")
            ncbi = NCBIWWW.qblast(program="blastp",database="nr",sequence=str(seqs.seq),format_type="XML",ncbi_gi=str(seqs.id), alignments=20,word_size=3)
            out.write(ncbi.read())
            print "%s\t%f"%(str(seqs.id),float(clock()))
    elif type == "nucl":
        for seqs in SeqIO.parse(fasta,"fasta"):
            clock()
            out = open("split_xml/%s.xml"%str(seqs.id),"w")
            ncbi = NCBIWWW.qblast(program="blastp",database="nr",sequence=str(seqs.seq),format_type="XML",ncbi_gi=str(seqs.id), alignments=20,word_size=3)
            out.write(ncbi.read())
            print "%s\t%f"%(str(seqs.id),float(clock()))

def main():
    argser = parse_args()
    if argser.type not in ["prot","nucl"]:
        print "You should type 'prot' or 'nucl'"
        exit(1)

    create_dir()
    run_blast(argser.fasta,argser.type)

if __name__ == "__main__":
    main()
