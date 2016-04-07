#!/usr/bin/env python

'''
@Description This script can be used to filter gene models produced by PASA. The threshold is :
protein coverage >= 0.5; Cscore >= 0.5; The coverage of TE =< 0.3
protein coverage is the highest percentage of protein aligned to the best of homologs;
Cscore is a protein BLASTP score ratio to MBH (mutual best hit) BLASTP score;
The coverage of TE is the coverage of TE-associated domains which introduced in book "Origin and evolution of eukaryotic gene sequences derived from transposable elements"
@Need: pfam_scan.pl; HMMER; blast.py (which can be used to calculate cscore) of github (https://github.com/tanghaibao/jcvi/tree/master/formats)
@Usage: python Filter_gene_models.py --pfam pfam.out --cscore fasta.cscore --blastp fasta.outfmt6 --fasta target.fa --query query.fa
'''

from Bio import SeqIO
import argparse

def parse_args():
    argser = argparse.ArgumentParser(usage="%(prog)s[options]")
    argser.add_argument("--pfam", default="pfam.out", help="This is the outfile of pfam_scan.pl")
    argser.add_argument("--cscore",default="fasta.cscore", help="This is the outfile of blast.py of Dr. Tang")
    argser.add_argument("--blastp", default="fasta.outfmt6", help="This the tabluar(outfmt6) outfile of blastp ")
    argser.add_argument("--target", default="target.fa", help="This is the proteomes which used in gene models prediction")
    argser.add_argument("--query", default="query.fa",help="This is the gene models of your species")
    return argser.parse_args()

## Get a dictionary which key is seqs.id and value is seqs.seq
def get_query_seqs(query_fa):
    query_seqs = dict()
    for seqs in SeqIO.parse(query_fa,'fasta'):
        query_seqs[str(seqs.id)] = str(seqs.seq)
    return query_seqs

## Get ids which cscore higher than 0.5 ##
def treat_cscore(infile):
    retain_cscore_ids = []
    cd = dict()
    for line in open(infile,"r"):
        query, target, cscore = line.strip().split()
        try:
            cd[query].append(cscore)
        except KeyError:
            cd[query] = [cscore]

    for query in cd:
        if float(max(cd[query])) >= 0.5:
            retain_cscore_ids.append(query)
    return retain_cscore_ids

## Filer seqs with TE-associated domains (higher than 0.3)
def get_len(fasta):
    seqs_len = dict()
    for seqs in SeqIO.parse(fasta,"fasta"):
        if "*" in str(seqs.seq):
            seqs_len[str(seqs.id)] = len(str(seqs.seq)) - 1
        else:
            seqs_len[str(seqs.id)] = len(str(seqs.seq))
    return seqs_len

def get_TE_ids(TE_ids):
    TE = []
    for line in open(TE_ids,"r"):
        if "#" not in line:
            TE.append(line)
    return TE

def get_domain(pfam):
    pfam_ids = dict()
    for line in open(pfam,"r"):
        if "#" not in line and len(line.strip().split()) == 15:
            try:
                pfam_ids[line.strip().split()[0]].append(line.strip().split()[5])
            except KeyError:
                pfam_ids[line.strip().split()[0]] = [str(line).strip().split()]
    return pfam_ids

def filter_TEs(fasta, pfam, TE_ids):

    seqslen = get_len(fasta)
    TE = get_TE_ids(TE_ids)
    TI = []

    for line in open(pfam,"r"):
        if "#" not in line and len(line.strip().split()) == 15:
            ids = line.strip().split()[0]
            start = int(line.strip().split()[1])
            end = int(line.strip().split()[2])
            hmm = line.strip().split()[5]
            if hmm.split(".")[0] in TE:
                per = (float(end) - float(start) + float(1)) / float(seqslen.get(ids))
                if per >= 0.3:
                    TI.append(ids)
    set1 = set(TI)
    set2 = set(seqslen.keys())
    set3 = set2 - set1
    return set3

## Filter seqs with protein coverage higher than 0.5
def get_pc(blast, fasta):
    tp = dict()
    tl = get_len(fasta)
    bpc = []
    for line in open(blast,"r"):
        qi = line.strip().split()[0]
        ti = line.strip().split()[1]
        idv = float(line.strip().split()[2])
        al = float(line.strip().split()[3])
        pc = (idv * al) / (tl.get(ti) * 100)
        try:
            tp[qi].append(pc)
        except KeyError:
            tp[qi] = [pc]

    for query in tp:
        if float(max(tp[query])) >= 0.5:
           bpc.append(query)
    return bpc

def main():
    agser = parse_args()
    out = open("TN90.F.fa","w")
    cscore = set(treat_cscore(agser.cscore))
    pc = set(get_pc(agser.blastp, agser.target))
    TE = filter_TEs(agser.query, agser.pfam, "TE-associated-domains.ids")
    query = get_query_seqs(agser.query)
    for ids in cscore|pc|TE:
        out.write(">%s\n%s\n"%(ids,query.get(ids)))

if __name__ == "__main__":
    main()
