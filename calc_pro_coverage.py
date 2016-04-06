#!/usr/bin/env python

'''
@Description This script can be used to get protein coverage based on blast+ outfile (outfmt 6)
protein coverage is the highest percentage of protein aligned to the best of homologs
@Author This script is developed by Ginsea Chen of CATAS (ginseachen@hotmail.com)
@Usage: python calc_prot_coverage.py --blast blast.outfmt6 --fasta target.fasta --out out.tab
'''
import argparse
from Bio import SeqIO

def parse_args():
    parser = argparse.ArgumentParser(usage="%(prog)s[options]")
    parser.add_argument("--blast", default="blast.outfmt6", help="blast out file with outfmt 6 format")
    parser.add_argument("--fasta", default="target.fa", help="target file with fasta format")
    parser.add_argument("--out", default="protein.coverage.tab", help="a txt file contained ids and corresponding protein covergae values")
    return parser.parse_args()

def get_identity(infile):
    identity=dict()
    for line in open(infile,"r"):
        if line.strip().split()[0] not in identity.keys():
            identity[line.strip().split()[0]] = line.strip().split()[2]
        else:
            continue
    return identity

def get_align_len(infile):
    align_len = dict()
    for line in open(infile,"r"):
        if line.strip().split()[0] not in align_len.keys():
            align_len[line.strip().split()[0]] = line.strip().split()[3]
        else:
            continue
    return align_len

def get_best_homo(infile):
    best_homo = dict()
    for line in open(infile,'r'):
        if line.strip().split()[0] not in best_homo:
            best_homo[line.strip().split()[0]] = line.strip().split()[1]
        else:
            continue
    return best_homo

def get_seq_len(fasta):
    seqs_len = dict()
    for seqs in SeqIO.parse(fasta,"fasta"):
        if "*" in seqs.seq:
            seqs_len[seqs.id] = str(len(seqs.seq) - 1)
        elif "*" not in seqs.seq:
            seqs_len[seqs.id] = str(len(seqs.seq))
    return seqs_len

def main():
    args = parse_args()
    out = open(args.out,"w")
    identity = get_identity(args.blast)
    align_len = get_align_len(args.blast)
    best_homo = get_best_homo(args.blast)
    seqs_len = get_seq_len(args.fasta)
    for query in identity:
        x = float(identity.get(query))
        y = float(align_len.get(query))
        a = best_homo.get(query)
        z = float(seqs_len.get(a))
        protein_coverage = x*y/(z*100)
        out.write("%s\t%f\n"%(query,protein_coverage))

if __name__ == "__main__":
    main()
