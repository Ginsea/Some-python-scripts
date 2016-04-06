#/usr/bin/env python
'''
@Author This script was developed by Ginsea Chen in CATAS (ginseachen@hotmail.com)
@Description You can delete sequences which contained more than thirty percent TE-related domains coverage
@The TE-ralated domains were obtained from paper: Evaluating the protein coding potential of exonized transposable element sequences.
@Usage: python filter-TE-domains.py --fasta test.fa --infile test.pfam -TE TE-associated-domains.ids
'''
import argparse
from Bio import SeqIO

def args_parse():
    parser = argparse.ArgumentParser(usage="%(prog)s[options]")
    parser.add_argument("--fasta", help="fasta file")
    parser.add_argument("--infile",help="pfam searching outfile")
    parser.add_argument("--TE",help="A file contained 124 TE-associated domains")
    return parser.parse_args()

def get_len(fasta):
    seqs_len = dict()
    for seqs in SeqIO.parse(fasta,'fasta'):
        seqs_len[str(seqs.id)] = len(str(seqs.seq))
    return seqs_len

def get_seqs(fasta):
    fasta_seqs = dict()
    for seqs in SeqIO.parse(fasta,"fasta"):
        fasta_seqs[str(seqs.id)] = str(seqs.seq)
    return fasta_seqs

def get_TE_ids(infile):
    TE = []
    for line in open(infile,"r"):
        if "#" not in line:
            TE.append(line.strip())
    return TE

def get_pfam(pfam):
    pfam_ids = dict()
    for line in open(pfam,"r"):
        if "#" not in line and len(line.strip().split()) == 15:
            try:
                pfam_ids[line.strip().split()[0]].append(line.strip().split()[5])
            except KeyError:
                pfam_ids[line.strip().split()[0]] = [line.strip().split()[5]]
    return pfam_ids


def main():
    args = args_parse()
    out1 = open("%s.TE.fa"%str(args.fasta).split(".")[0],"w")
    out2 = open("%s.CON.fa"%str(args.fasta).split(".")[0],"w")
    seqslen = get_len(args.fasta)
    seqs = get_seqs(args.fasta)
    TE = get_TE_ids(args.TE)
    pfam_ids = get_pfam(args.infile)
    TE_ids = []

    for line in open(args.infile,"r"):
        if "#" not in line and len(line.strip().split()) == 15 :
            ids = line.strip().split()[0]
            start = int(line.strip().split()[1])
            end = int(line.strip().split()[2])
            hmm = line.strip().split()[5]

            if hmm.split(".")[0] in TE:
                per = (float(end)-float(start)+float(1))/float(seqslen.get(ids))
                if per >= float(0.3):
                    TE_ids.append(ids)
                    out1.write(">%s\t%f\n%s\n"%(ids,per,seqs.get(ids)))
    set1 = set(TE_ids)
    set2 = set(seqs.keys())
    for retain_ids in set2 - set1:
        try:
            out2.write(">%s\t%s\n%s\n"%(retain_ids,pfam_ids[retain_ids],seqs.get(retain_ids)))
        except KeyError:
            out2.write(">%s\tNon-domains\n%s\n"%(retain_ids,seqs.get(retain_ids)))

if __name__=="__main__":
    main()
