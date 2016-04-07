#!/usr/bin/env python

'''
@Description This script can be used to calculate protein coverage based on blast outfile
@Protein coverage is the highest percentage of protein coverage, which can be calculated through (identity_value * alignment_length) / (target_seqs_len * 100)
@Usage: python calc_prot_cov.py --fasta target.fa --blast blast.outfmt6 --out prot_cov.tab
'''
from Bio import SeqIO
import argparse

def parse_args():
    parser = argparse.ArgumentParser(usage="%(prog)s[options]")
    parser.add_argument("--fasta", default="target.fa", help="blast database file")
    parser.add_argument("--blast", default="blast.outfmt6", help="blast outfile with outfmt6 format")
    parser.add_argument("--out", default="prot_cov.tab", help="outfile with TAB")
    return parser.parse_args()


def get_len(fastafile):
    seqs_len = dict()
    for seqs in SeqIO.parse(fastafile,"fasta"):
        if "*" in str(seqs.seq):
            lg = len(str(seqs.seq)) - 1
            seqs_len[str(seqs.id)] = lg
        else:
            lg = len(str(seqs.seq))
            seqs_len[str(seqs.id)] = lg
    return seqs_len

def get_pc(blastfile, fastafile):
    tp = dict()
    tl = get_len(fastafile)
    for line in open(blastfile,"r"):
        qi = line.strip().split()[0]
        ti = line.strip().split()[1]
        idv = float(line.strip().split()[2])
        al = float(line.strip().split()[3])
        pc = (idv * al) / (tl.get(ti) * 100)
        try:
            tp[qi].append(pc)
        except KeyError:
            tp[qi] = [pc]
    return tp

def main():
    args = parse_args()
    out = open(args.out,"w")
    pd = get_pc(args.blast, args.fasta)
    for query in pd:
        out.write("%s\t%f\n"%(query,float(max((pd[query])))))

if __name__ == "__main__":
    main()
