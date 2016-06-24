#!/usr/bin/python

'''
@Description This script can be used to combine results of CNCI, CPC and PFAM, then produce Venn diagram;
@Author Ginsea Chen (chenzx@biobreeding.com.cn)
Usage:
    python get_lncRNA.py --cpc cpc results --cnci cnci results --pfam pfam_results --fasta fasta file
'''

import argparse
import os,sys
from Bio import SeqIO
from matplotlib_venn import venn3

def parse_args():
    parser = argparse.ArgumentParser(usage="%(prog)s[options]")
    parser.add_argument("--cpc" or "-cpc",help="cpc results")
    parser.add_argument("--pfam" or "-pfam",help="pfam searching results")
    parser.add_argument("--cnci" or "-cnci",help="cnci results")
    parser.add_argument("--fasta" or "-fasta",help="target fasta file")
    return parser.parse_args()

def test_options():
    pargs=parse_args()
    if pargs.cpc == "None" or pargs.pfam == "None" or pargs.cnci == "None" or pargs.fasta == "None":
        os.system("python %s -h"%sys.argv[0])
        exit(1)

def read_cpc(cpc):
    '''
    :param cpc: cpc results (a tab file produced by cpc software)
    :return: two tuples, one contained all nocoding ids and another all coding ids
    '''
    cpc_c = [] #tuple contained all coding ids
    cpc_n = [] #tuple contained all nocoding ids

    for line in open(cpc,"r"): #read cpc results
        elements = line.strip().split() # split the lines
        ids = elements[0] # seq ids label
        noc = elements[2] # coding or nocoding (noc) label
        if noc == "noncoding":
            cpc_n.append(ids)
        else:
            cpc_c.append(ids)
    return cpc_c,cpc_n

def read_cnci(cnci):
    '''
    :param cnci: cnci result file (a tab file produced by cnci software, always named as CNCI.index
    in work dictionary of CNCI software)
    :return: two tuples ,one contained all nocoding ids and another all coding ids
    '''
    cnci_c = [] #tuple contained all coding ids
    cnci_n = [] #tuple contained all noncoding ids

    for line in open(cnci,"r"):
        elements = line.strip().split()
        ids = elements[0]
        noc = elements[1]
        if ids != "Transcript":
            if noc == "coding":
                cnci_c.append(ids)
            elif noc == "noncoding":
                cnci_n.append(ids)
    return cnci_c,cnci_n

def read_pfam(pfam,fasta):
    '''
    :param pfam:pfam result (a tab split file which produced from pfamscan.pl searching)
    :param fasta: target fasta file
    :return: two tuples, one contained all seqs which have domain prediction, and another seqs stored in another tuple
    '''
    all_ids = [] # a tuple contained all ids get from fasta file;
    id_seq = {} # a dictionart contained ids (keys) and seqs (items);
    for seqs in SeqIO.parse(fasta,"fasta"):
        ids = str(seqs.id)
        all_ids.append(ids)
        id_seq[ids] = str(seqs.seq)

    pfam_ids = [] # a tuple contained all ids which have domain annotation
    for line in open(pfam):
        if line[0] != "#" and len(line) > 30:
            elements = line.strip().split()
            ids = elements[0]
            if ids not in pfam_ids:
                pfam_ids.append(ids)

    np_ids = [] #a tuple contained all seqs which have no domain annotation
    for ids in all_ids:
        if ids not in pfam_ids:
            np_ids.append(ids)
    return pfam_ids,np_ids,all_ids,id_seq

def draw_venn(cpc,cnci,fasta,pfam):
    cpc_n = set(read_cpc(cpc)[1])
    cnci_n = set(read_cnci(cnci)[1])
    pfam_n = set(read_pfam(pfam,fasta)[1])
    venn3([cpc_n,cnci_n,pfam_n],("cpc","cnci","pfam"))
    plt.show()

def main():
    pargs = parse_args()
    test_options()

    cpc = pargs.cpc
    cnci = pargs.cnci
    pfam = pargs.pfam
    fasta = pargs.fasta

    cpc_n = read_cpc(cpc)[1]
    cnci_n = read_cnci(cnci)[1]
    pfam_n = read_pfam(pfam,fasta)[1]
    fasta_all = read_pfam(pfam,fasta)[2]
    id_seq = read_pfam(pfam,fasta)[3]

    common_set = set(cpc_n)&set(cnci_n)&set(pfam_n)

    out1 = open("lncRNA.count","r")
    out1.write("Total\tcpc\tcnci\tpfam\n%d\t%d\t%d\t%d\n"%(len(common_set),len(cpc_n),len(cnci_n),len(pfam_n)))

    out2 = open("lncRNA.fasta","r")
    for ids in common_set:
        out2.write(">%s\n%s\n"%(ids,id_seq[ids]))

if __name__ == '__main__':
    main()
