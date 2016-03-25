#!/usr/bin/env python
__DESCRIPTION__="""
Calculate the frequency of any number of nucleotide pairs.
python Code_freq.py --in in_fastafile --num numbers
"""

from itertools import product
import argparse

def parse_args():
    parser = argparse.ArgumentParser(usage="%(prog)s [options]")
    parser.add_argument("--infile",default="test.fa",help="Your fasta file")
    parser.add_argument("num",nargs="+", default=3,type=int,help="numbers")
    return parser.parse_args()

def read_fasta(infile):
    name = None
    for line in open(infile,"r"):
        if line[0] == ">":
            if name:
                yield(name, seq)
            name = line[1:]
            seq = ""
        else:
            seq += line
    yield (name,seq)

def codes(repeat):
    return [''.join(x) for x in product("ATCG",repeat=repeat)]

def main():
    args=parse_args()
    out = open('%s.codes' % args.num[0], "w")
    for code in codes(repeat=int(args.num[0])):
        y = 0
        for seqs in read_fasta(args.infile):
            if code in seqs[1]:
                y +=1
        out.write("%s\t%d\n"%(code,y))

if __name__=="__main__":
    main()
