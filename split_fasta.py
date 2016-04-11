#!/usr/bin/env python

'''
This script can be used to split a large fasta to multiple files averagely
Usgae python split_fasta_vaeragely.py --fasta fasta.fa --num [NUM]
'''

from Bio import SeqIO
import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser(usage="%(prog)s[options]")
    parser.add_argument("--fasta",default="fasta.fa",help="Your fasta file")
    parser.add_argument("--num",default=100, type=int,help="number of seqs contained in each files")
    return parser.parse_args()

def create_dir():
    try:
        os.stat("split")
    except:
        os.mkdir("split")

def main():
    agrse = parse_args()
    create_dir()
    seqs_fa = dict()
    for seqs in SeqIO.parse(agrse.fasta,"fasta"):
        seqs_fa[str(seqs.id)] = str(seqs.seq)
    i = len(seqs_fa)
    seqs_id = seqs_fa.keys()
    num = int(agrse.num)
    nf = i / num
    x = 1
    
    if i%num == 0:
        while x <= nf:
            out = open("split/%s_%d.fa"%(agrse.fasta.split(".")[0],x),"w")
            if x < nf:
                for y in range(num*(x - 1), num*x):
                    out.write(">%s\n%s\n"%(seqs_id[y],seqs_fa.get(seqs_id[y])))
            elif x == nf:
                for y in range(num*(x - 1), num*x + 1):
                    out.write(">%s\n%s\n"%(seqs_id[y],seqs_fa.get(seqs_id[y])))
            x += 1

    elif i%num != 0:
        while x <= nf + 1:
            out = open("split/%s_%d.fa"%(agrse.fasta.split(".")[0],x),"w")
            if x < nf + 1:
                for y in range(num*(x - 1), num*x):
                    out.write(">%s\n%s\n"%(seqs_id[y],seqs_fa.get(seqs_id[y])))
            elif x == nf + 1:
                for y in range(num*(x - 1),i):
                    out.write(">%s\n%s\n"%(seqs_id[y],seqs_fa.get(seqs_id[y])))
            x += 1

if __name__ == "__main__":
    main()
