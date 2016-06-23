#!/usr/local/bin/python3


import sys
import os
from Bio import SeqIO
import re

def options():
    try:
        sys.argv[1] or sys.argv[2] or sys.argv[3] or sys.argv[4] or sys.argv[5]
    except:
        print("Usage:\n\tpython %s config pfam1 pfam2,ath_fa kiwi_fa\n"
              "\tconfig: The file contained ath gene name and gene ids\n"
              "\tpfam1: The file of pfam results for ath seqs\n"
              "\tpfam2: The file of pfam results for kiwi seqs\n"
              "\tath_fa: The fasta file which contained ath peptide seqs\n"
              "\tkiwi_fa: The fasta file which contained kiwi peptide seqs\n"%sys.argv[0])
        exit(1)

def read_pfam(pfam_results):
    '''
    :param pfam_results: The output file of pfamscan.pl for reference seqs of thaliana
    :return: Two direcontary
    '''
    spi = {} #seq ids vs pfam ids
    spn = {} # seq ids vs pfam name

    for line in open(pfam_results,"r"):
        if line[0] != "#" and len(line)>20:
            elements = line.split()
            seq_ids = elements[0].upper()
            pfam_ids = elements[5]
            pfam_name = elements[6]

            try:
                spi[seq_ids].append(pfam_ids)
            except:
                spi[seq_ids] = [pfam_ids]

            try:
                spn[seq_ids].append[pfam_name]
            except:
                spn[seq_ids] = [pfam_name]
    return spi,spn

def read_config(config,pfam_results):
    '''
    :param config:config file which contained gene name and gene ids
    :return: a direcontary which contained gene name and corresponding pfam domain ids
    '''
    config_dir = {}
    gngi = {} #keys: ath gene name; items: ath gene ids
    spi = read_pfam(pfam_results)[0]

    for l1 in open(config,"r"):
        elements = l1.split("\t")
        gene_name = elements[0]

        if "." in elements[1]:
            gene_ids = elements[1]
        else:
            gene_ids = "%s.1"%elements[1]

        try:
            try:
                config_dir[gene_name].append(spi[gene_ids.upper()])
            except:
                config_dir[gene_name] = [spi[gene_ids.upper()]]
        except:
            continue

        try:
            gngi[gene_name].append(gene_ids.upper())
        except:
            gngi[gene_name] = [gene_ids.upper()]

    gnpn = {} # gene name vs pfam ids

    for keys in config_dir.keys():
        for tu in config_dir[keys]:
            for ids in tu:
                gnpn[keys] = ids

    return gnpn,gngi

def read_pfam1(pfam2):
    '''
    :param pfam2: pfam result of kiwi peptide
    :param pfam: pfam results of reference seqs of ath
    :return: a dir which contained gene name, gene id and pfam id
    '''

    kpi = {} # kiwi_pfam_ids

    for line in open(pfam2):
        if line[0] != "#" and len(line) > 20:
            elements = line.split()
            kiwi_ids = elements[0]
            pfam_ids = elements[5]

            try:
                kpi[pfam_ids].append(kiwi_ids)
            except:
                kpi[pfam_ids] = [kiwi_ids]


    return kpi

def read_fasta(ath,kiwi):
    ath_dir = {}
    kiwi_dir = {}

    for seqs in SeqIO.parse(ath,"fasta"):
        try:
            ids = re.search(r"AT[A-Z0-9a-z]+.[0-9]",str(seqs.id).upper()).group()
        except:
            ids = "%s.1"%re.search(r"AT[A-Z0-9a-z]+",str(seqs.id).upper()).group()

        ath_dir[ids] = str(seqs.seq)

    for seqs in SeqIO.parse(kiwi,"fasta"):
        kiwi_dir[str(seqs.id)] = str(seqs.seq)
    return ath_dir,kiwi_dir



def main():
    options()
    config = sys.argv[1] # config file which contained
    pfam_ath = sys.argv[2] # pfam results file of some ath seqs, this seqs used as reference for kiwi peptide searching
    pfam_kiwi = sys.argv[3] #pfam results file of all kiwi peptide seqs,
    ath_fa = sys.argv[4] # fasta file of thaliana (peptide)
    kiwi_fa = sys.argv[5] #fasta file of kiwifruit (peptide)
    spi = read_pfam(pfam_ath)[0] # The dictionary which contained thaliana ids (keys) and corresponding pfam ids (items)
    spn = read_pfam(pfam_ath)[1] # The dictionary which contained thaliana ids (keys) and corresponding pfam name (items)
    gnpn = read_config(config,pfam_ath)[0] # The dictionary which contained gene name (keys) and pfam ids (items)
    gngi = read_config(config,pfam_ath)[1] # The dictionary which contained gene name (keys) and gene ids (items)
    kpi = read_pfam1(pfam_kiwi) #  The didtionary which contained pfam ids (keys) and corresponding kiwi_ids (items)
    ath_fasta_dir = read_fasta(ath_fa,kiwi_fa)[0]
    kiwi_fasta_dir = read_fasta(ath_fa,kiwi_fa)[1]
    out1 = open("results.tab","w")

    for keys in gngi.keys():
        out1.write("%s\n"%keys)
        out2 = open("%s.fa"%"_".join(keys.split()),"r")
        for ids in gngi[keys]:
            out1.write("\t%s\n"%ids)
            out2.write(">%s\n%s\n"%(ids,ath_fasta_dir[ids]))
            for pfam_ids in spi[ids]:
                for kiwi_ids in kpi[pfam_ids]:
                    out1.write("\t\t%s\n"%kiwi_ids)
                    out2.write(">%s\n%s\n"%(kiwi_ids,kiwi_fasta_dir[kiwi_ids]))

if __name__ == '__main__':
    main()
