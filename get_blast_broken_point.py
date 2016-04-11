#!/usr/bin/env python
'''
@Description This script can be used to get no blast ids if your analysis stopped accidently
@Author This script was developed by Ginsea Chen (ginseachen@hotmail.com) in CATAS
@Usage python get_blast_broken_point.py --fasta test.fa --xml blast.xml
'''
import argparse
from Bio import SeqIO

def parse_args():
    parser = argparse.ArgumentParser(usage="%(prog)s[options]")
    parser.add_argument("--fasta",default="test.fa",help="Your fasta file which used to run blast")
    parser.add_argument("--xml",default="blast.xml",help="blast outfile with xml format")
    return parser.parse_args()

def get_last_ids(xml):
    infile = open(xml,"r")
    inline = infile.read()
    ml = inline.split("<Iteration>")
    fl = len(ml)
    return [ml[fl - 1].split("\n")[3].split(">")[1].split("<")[0].split()[0]]

def get_finished_ids(xml):
    ids = []
    last_ids = get_last_ids(xml)
    for line in open(xml,"r"):
        if "<Iteration_query-def>" in line:
            sids = line.split(">")[1].split("<")[0].split()[0]
            if sids not in last_ids:
                ids.append(sids)
    return ids

def get_retain_fasta(xml, fasta):
    out = open("%s.retain"%fasta,"w")
    finished_ids = get_finished_ids(xml)
    for seqs in SeqIO.parse(fasta,"fasta"):
        if str(seqs.id) not in finished_ids:
            out.write(">%s\n%s\n"%(str(seqs.id),str(seqs.seq)))
    return out

def main():
    parser = parse_args()
    get_last_ids(parser.xml)
    get_finished_ids(parser.xml)
    get_retain_fasta(parser.xml,parser.fasta)

if __name__ == "__main__":
    main()
