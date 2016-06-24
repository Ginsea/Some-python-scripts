#!/usr/bin/python
'''
count_database_annotation.py
Ginsea Chen (chenzx@biobreeding.com.cn)
This script can be used to count database annotation results (nr, cog, kegg, go, pfam)
and then draw venn diagram
Usage:
    python count_database_annotation.py --nr nr.annot --cog cog.annot, --kegg kegg.annot --go go.annot, --pfam pfam.annot
'''
import argparse
import os,sys

def parse_args():
    parser = argparse.ArgumentParser(usage="%s(prog)s[options]")
    parser.add_argument("--nr",help="Nr database annotation results")
    parser.add_argument("--cog",help="COG database annotation results")
    parser.add_argument("--kegg",help="KEGG database annotation results")
    parser.add_argument("--go",help="Go database annotation results")
    parser.add_argument("--pfam",help="pfam database annotation results")
    return parser.parse_args()

def read_nr(nr):
    '''
    :param nr: nr database annotation results
    :return: A tuple which contained seqs ids annotated in nr database
    '''
    nr_ids = [] # this tuple contained ids which annotated in nr database, nr database is non-redundant protein database

    for line in open(nr,"r"):
        if line[0] != "#":
            elements = line.strip().split()
            ids = elements[0].strip()
            if ids not in nr_ids:
                nr_ids.append(ids)
    return nr_ids

def read_cog(cog):
    '''
    :param cog: cog database annotation results
    :return: A tuple which contained seqs ids annotated in cog database
    '''
    cog_ids = [] # this tuple contained ids which annotated in cog database,

    for line in open(cog,"r"):
        if line[0] != "#":
            elements = line.strip().split()
            ids = elements[0].strip()
            if ids not in cog_ids:
                cog_ids.append(ids)
    return cog_ids

def read_kegg(kegg):
    '''
    :param kegg:kegg annotation results
    :return: A tuple which contained seq ids annotated in kegg database
    '''
    kegg_ids = [] # This tuple contained ids which annotated in kegg database

    for line in open(kegg,"r"):
        if line[0] != "#":
            elements = line.strip().split()
            ids = elements[0].strip()
            if ids not in kegg_ids:
                kegg_ids.append(ids)
    return kegg_ids

def read_go(go):
    '''
    :param go: Go database annotation results
    :return: A tuple which contained ids annotated in go database
    '''
    go_ids = [] # This tuple contained ids which annotated in Go database

    for line in open(go,"r"):
        if line[0] != "#":
            elements = line.strip().split()
            ids = elements[0].strip()
            if ids not in go_ids:
                go_ids.append(ids)
    return go_ids

def read_pfam(pfam):
    '''
    :param pfam: pfam database annotation results
    :return: A tuple which contained ids annotated in pfam database
    '''
    pfam_ids = [] #This tuple contained ids which annotated in pfam database

    for line in open(pfam,"r"):
        if line[0] != "#":
            elements = line.strip().split()
            ids = elements[0]
            if ids not in pfam_ids:
                pfam_ids.append(ids)
    return pfam_ids

def write_R_code(nr,cog,kegg,go,pfam):
    set_nr = set(read_nr(nr))
    set_cog = set(read_cog(cog))
    set_kegg = set(read_kegg(kegg))
    set_go = set(read_go(go))
    set_pfam = set(read_pfam(pfam))
    area1 = len(set_nr)
    area2 = len(set_cog)
    area3 = len(set_kegg)
    area4 = len(set_go)
    area5 = len(set_pfam)
    n12 = len(set_nr&set_cog)
    n13 = len(set_nr&set_kegg)
    n14 = len(set_nr&set_go)
    n15 = len(set_nr&set_pfam)
    n23 = len(set_cog&set_kegg)
    n24 = len(set_cog&set_go)
    n25 = len(set_cog&set_pfam)
    n34 = len(set_kegg&set_go)
    n35 = len(set_kegg&set_pfam)
    n45 = len(set_go&set_pfam)
    n123 = len(set_nr&set_cog&set_kegg)
    n124 = len(set_nr&set_cog&set_go)
    n125 = len(set_nr&set_cog&set_pfam)
    n134 = len(set_nr&set_kegg&set_go)
    n135 = len(set_nr&set_kegg&set_pfam)
    n145 = len(set_nr&set_go&set_pfam)
    n234 = len(set_cog&set_kegg&set_go)
    n235 = len(set_cog&set_kegg&set_pfam)
    n245 = len(set_cog&set_go&set_pfam)
    n345 = len(set_kegg&set_go&set_pfam)
    n1234 = len(set_nr&set_cog&set_kegg&set_go)
    n1345 = len(set_nr&set_kegg&set_go&set_pfam)
    n2345 = len(set_cog&set_kegg&set_go&set_pfam)
    n12345 = len(set_nr&set_cog&set_kegg&set_go&set_pfam)
    R_code = open("5Venn.r","w")
    R_code.write("library('VennDiagram')\n"
                 "venn.plot <- draw.quintuple.venn("
                 "area1 = %d,"
                 "area2 = %d,"
                 "area3 = %d,"
                 "area4 = %d,"
                 "area5 = %d,"
                 "n12 = %d,"
                 "n13 = %d,"
                 "n14 = %d,"
                 "n15 = %d,"
                 "n23 = %d,"
                 "n24 = %d,"
                 "n25 = %d,"
                 "n34 = %d,"
                 "n35 = %d,"
                 "n45 = %d,"
                 "n123 = %d,"
                 "n124 = %d,"
                 "n125 = %d,"
                 "n134 = %d,"
                 "n135 = %d,"
                 "n145 = %d,"
                 "n234 = %d,"
                 "n235 = %d,"
                 "n245 = %d,"
                 "n345 = %d,"
                 "n1234 = %d,"
                 "n1345 = %d,"
                 "n2345 = %d,"
                 "n12345 = %d,"
                 "category = c('NR','COG','KEGG','GO','PFAM'),"
                 "fill = c('dodgerblue','goldenrod1','darkorange1','seagreen3','orchid3'),"
                 "cat.col = c('dodgerblue','goldenrod1','darkorange1','seagreen3','orchid3'),"
                 "cat.cex = 2,"
                 "margin = 0.05,"
                 "ind = TRUE);\n"
                 "tiff(filename='Anno_5venn.tiff',compression = 'lzw');\n"
                 "grid.draw(venn.plot);\n"
                 "dev.off();")

def get_venn(venn):
    os.system("R -e 'source('%d')'"%venn)

def main():
    pargs = parse_args()

    if pargs.nr == "None" or pargs.cog == "None" or pargs.kegg == "None" or pargs.go == "None" or pargs.pfam == "None":
        os.system("python %s -h"%sys.argv[0])
        exit(1)

    nr = pargs.nr
    cog = pargs.cog
    kegg = pargs.kegg
    go = pargs.go
    pfam = pargs.pfam

    write_R_code(nr=nr,cog=cog,kegg=kegg,go=go,pfam=pfam)

    venn = "5Venn.r"
    get_venn(venn=venn)

if __name__ == '__main__':
    main()
