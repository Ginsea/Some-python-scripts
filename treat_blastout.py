#!/usr/bin/env python
#coding=UTF-8

import argparse
import os
import sys
import time
global rd
rd = os.getcwd()

def ltime():
    return time.strftime("%H:%M:%S",time.localtime(time.time()))

def opt():
    args = argparse.ArgumentParser(usage="%(prog)s[options]")
    args.add_argument("--out1",help="The first blast out file with format 6, Pacbio")
    args.add_argument("--out2",help="The second blast out file with format 6, Annot")
    args.add_argument("--com",help="The comparison file ")
    return args.parse_args()

def load_outfmt(out):
    sys.stdout.write("[{0}] Load file {1}\n".format(ltime(),os.path.basename(out)))
    tmpdir = {}
    for line in open(out,"r"):
        ele = line.strip().split("\t")
        if ele[0] not in tmpdir.keys():
            tmpdir[ele[0]] = {}
            tmpdir[ele[0]]["identity"] = float(ele[2])
            tmpdir[ele[0]]["score"] = float(ele[-1])
            tmpdir[ele[0]]["query"] = ele[1]
    sys.stdout.write("[{0}] Load file {1} successfully\n".format(ltime(),os.path.basename(out)))
    return tmpdir

def load_com(com):
    sys.stdout.write("[{0}] Load file {1}\n".format(ltime(),os.path.basename(com)))
    tmpdir = {}
    for line in open(com,"r"):
        if "double" in line.strip():
            ele = line.strip().split("\t")
            ids = ele[0].strip().split(",")[0]
            tmpdir[ids]={}
            tmpdir[ids]["pac"] = ele[-3].strip().split(",")
            tmpdir[ids]["ann"] = list(x.rstrip("-TA") for x in ele[-1].strip().split(","))
    sys.stdout.write("[{0}] Load file{1} successfully\n".format(ltime(), os.path.basename(com)))
    return tmpdir

def noloci(ou1,ou2):
    try:
        os.stat("{0}/tmp/noloci".format(rd))
    except:
        os.makedirs("{0}/tmp/noloci".format(rd))
    pacdir = load_outfmt(ou1)
    anndir = load_outfmt(ou2)
    sys.stdout.write("[{0}] Write information to noloci.txt\n".format(ltime()))
    out1 = open("{0}/tmp/noloci/H1_I.txt".format(rd),"w")
    H1I = 0
    out2 = open("{0}/tmp/noloci/E1_I.txt".format(rd),"w")
    E1I = 0
    out3 = open("{0}/tmp/noloci/L1_I.txt".format(rd),"w")
    L1I = 0
    out4 = open("{0}/tmp/noloci/H1_S.txt".format(rd),"w")
    H1S = 0
    out5 = open("{0}/tmp/noloci/E1_S.txt".format(rd),"w")
    E1S = 0
    out6 = open("{0}/tmp/noloci/L1_S.txt".format(rd),"w")
    L1S = 0

    for keys in pacdir.keys():
        if keys in anndir.keys():
            pac_i = pacdir[keys]["identity"]
            ann_i = anndir[keys]["identity"]
            pac_gene = pacdir[keys]["query"]
            pac_s = pacdir[keys]["score"]
            ann_s = anndir[keys]["score"]
            ann_gene = anndir[keys]["query"]
            if pac_i/ann_i > 1:
                out1.write("{0}\t{1}\t{2}\n".format(keys,pac_gene,ann_gene))
                H1I += 1
            elif pac_i/ann_i == 1:
                out2.write("{0}\t{1}\t{2}\n".format(keys, pac_gene, ann_gene))
                E1I += 1
            elif pac_i/ann_i < 1:
                out3.write("{0}\t{1}\t{2}\n".format(keys, pac_gene, ann_gene))
                L1I += 1

            if pac_s/ann_s > 1:
                out4.write("{0}\t{1}\t{2}\n".format(keys, pac_gene, ann_gene))
                H1S += 1
            elif pac_s/ann_s == 1:
                out5.write("{0}\t{1}\t{2}\n".format(keys, pac_gene, ann_gene))
                E1S += 1
            elif pac_s/ann_s < 1:
                out6.write("{0}\t{1}\t{2}\n".format(keys, pac_gene, ann_gene))
                L1S += 1

    out7 = open("{0}/tmp/noloci/noloci_identity.txt".format(rd),"w")
    out7.write("NCBI\tpac_i\tann_i\tclass_i\n")
    out8 = open("{0}/tmp/noloci/noloci_score.txt".format(rd),"w")
    out8.write("NCBI\tpac_s\tann_s\tclass_s\n")

    for keys in pacdir.keys():
        if keys in anndir.keys():
            pac_i = pacdir[keys]["identity"]
            ann_i = anndir[keys]["identity"]
            pac_gene = pacdir[keys]["query"]
            pac_s = pacdir[keys]["score"]
            ann_s = anndir[keys]["score"]
            ann_gene = anndir[keys]["query"]
            if pac_i/ann_i > 1:
                out7.write("{0}\t{1}\t{2}\tH1({3})\n".format(keys,pac_i,ann_i,H1I))
            elif pac_i/ann_i == 1:
                out7.write("{0}\t{1}\t{2}\tE1({3})\n".format(keys, pac_i, ann_i, E1I))
            elif pac_i/ann_i < 1:
                out7.write("{0}\t{1}\t{2}\tL1({3})\n".format(keys, pac_i, ann_i, L1I))

            if pac_s/ann_s > 1:
                out8.write("{0}\t{1}\t{2}\tH1({3})\n".format(keys, pac_s, ann_s, H1S))
            elif pac_s/ann_s == 1:
                out8.write("{0}\t{1}\t{2}\tE1({3})\n".format(keys, pac_s, ann_s, E1S))
            elif pac_s/ann_s < 1:
                out8.write("{0}\t{1}\t{2}\tL1({3})\n".format(keys, pac_s, ann_s, L1S))

def loci(ou1,ou2,com):
    try:
        os.stat("{0}/tmp/loci".format(rd))
    except:
        os.makedirs("{0}/tmp/loci".format(rd))

    out1 = open("{0}/tmp/loci/loci_H1I.txt".format(rd),"w")
    H1I = 0
    out2 = open("{0}/tmp/loci/loci_E1I.txt".format(rd),"w")
    E1I = 0
    out3 = open("{0}/tmp/loci/loci_L1I.txt".format(rd),"w")
    L1I = 0
    out4 = open("{0}/tmp/loci/loci_H1S.txt".format(rd),"w")
    H1S = 0
    out5 = open("{0}/tmp/loci/loci_E1S.txt".format(rd),"w")
    E1S = 0
    out6 = open("{0}/tmp/loci/loci_L1S.txt".format(rd),"w")
    L1S = 0
    out7 = open("{0}/tmp/loci/loci_identity.txt".format(rd),"w")
    out7.write("NCBI\tPD\tGD\tClass\n")
    out8 = open("{0}/tmp/loci/loci_score.txt".format(rd),"w")
    out8.write("NCBI\tPD\tGD\tClass\n")

    pacdir = load_outfmt(ou1)
    anndir = load_outfmt(ou2)
    comdir = load_com(com)

    for keys in comdir.keys():
 #       print(comdir[keys]["pac"])
 #       print(comdir[keys]["ann"].rstrip("-TA"))
        try:
#            print(pacdir[keys]["query"])
#            print(anndir[keys]["query"])
            if pacdir[keys]["query"] in comdir[keys]["pac"] and anndir[keys]["query"] in comdir[keys]["ann"]:
                pacs = pacdir[keys]["score"]
                anns = anndir[keys]["score"]
                paci = pacdir[keys]["identity"]
                anni = anndir[keys]["identity"]
                if paci/anni > 1:
                    out1.write("{0}\t{1}\t{2}\t{3}\n".format(keys,anndir[keys]["query"],pacdir[keys]["query"],paci/anni))
                    H1I += 1
                elif paci/anni == 1:
                    out2.write("{0}\t{1}\t{2}\t{3}\n".format(keys,anndir[keys]["query"],pacdir[keys]["query"],paci/anni))
                    E1I += 1
                elif paci/anni < 1:
                    out3.write("{0}\t{1}\t{2}\t{3}\n".format(keys,anndir[keys]["query"],pacdir[keys]["query"],paci/anni))
                    L1I += 1

                if pacs/anns > 1:
                    out4.write("{0}\t{1}\t{2}\t{3}\n".format(keys,anndir[keys]["query"],pacdir[keys]["query"],pacs/anns))
                    H1S += 1
                elif pacs/anns == 1:
                    out5.write("{0}\t{1}\t{2}\t{3}\n".format(keys,anndir[keys]["query"],pacdir[keys]["query"],pacs/anns))
                    E1S += 1
                elif pacs/anns < 1:
                    out6.write("{0}\t{1}\t{2}\t{3}\n".format(keys,anndir[keys]["query"],pacdir[keys]["query"],pacs/anns))
                    L1S += 1
        except KeyError:
            print(keys)

    for keys in comdir.keys():
        try:
            if pacdir[keys]["query"] in comdir[keys]["pac"] and anndir[keys]["query"] in comdir[keys]["ann"]:
                pacs = pacdir[keys]["score"]
                anns = anndir[keys]["score"]
                paci = pacdir[keys]["identity"]
                anni = anndir[keys]["identity"]
                if paci / anni > 1:
                    out7.write("{0}\t{1}\t{2}\tH1({3})\n".format(keys,paci,anni,H1I))
                elif paci / anni == 1:
                    out7.write("{0}\t{1}\t{2}\tE1({3})\n".format(keys, paci, anni, E1I))
                elif paci / anni < 1:
                    out7.write("{0}\t{1}\t{2}\tL1({3})\n".format(keys, paci, anni, L1I))

                if pacs / anns > 1:
                    out8.write("{0}\t{1}\t{2}\tH1({3})\n".format(keys, pacs, anns, H1S))
                elif pacs / anns == 1:
                    out8.write("{0}\t{1}\t{2}\tE1({3})\n".format(keys, pacs, anns, E1S))
                elif pacs / anns < 1:
                    out8.write("{0}\t{1}\t{2}\tL1({3})\n".format(keys, pacs, anns, L1S))
        except KeyError:
            continue

def draw_point():
    try:
        os.stat("{0}/tmp/rscript".format(rd))
    except:
        os.mkdir("{0}/tmp/rscript".format(rd))
    
    try:
        os.stat("{0}/tmp/fig".format(rd))
    except:
        os.mkdir("{0}/tmp/fig".format(rd))

    out1 = open("{0}/tmp/rscript/noloci_i.r".format(rd),"w")
    out2 = open("{0}/tmp/rscript/noloci_s.r".format(rd),"w")
    out3 = open("{0}/tmp/rscript/loci_i.r".format(rd),"w")
    out4 = open("{0}/tmp/rscript/loci_s.r".format(rd),"w")
    out1.write("library(ggplot2);\n"
               "data <- read.table('{0}/tmp/noloci/noloci_identity.txt',header = TRUE, sep='\t');\n"
               "connames(data) <- c('NCBI','PD','GD','Class');\n"
               "p <- ggplot(data,aes(x=GD,y=PD)) + aes(shape=Class) + geom_point(aes(colour=Class)) + theme_bw();\n"
               "q <- p + theme(axis.title.x = element_text(size=18,colour = 'black'),axis.title.y = element_text(size=18,colour = 'black'),axis.text.x = element_text(size=18,colour = 'black',angle = 45, vjust = 0.5, hjust = 0.5),axis.text.y = element_text(size=18,colour = 'black'),legend.title=element_text(colour = 'black',size = 18),legend.text = element_text(color = 'black',size=18));\n"
               "q + guides(fill=guide_legend(title = NULL));\n"
               "ggsave('{0}/tmp/noloci/fig/noloci_i.png',width = 4.5,height = 5.5)".format(rd))
    os1 = os.system("Rscript {0}/tmp/rscript/noloci_i.r".format(rd))
    if os1:
        exit("[{0}] Please Check noloci_i.r\n".format(ltime()))
    else:
        sys.stdout.write("[{0}] Draw figure noloci_i.png successfully\n".format(ltime()))
        
    out2.write("library(ggplot2);\n"
           "data <- read.table('{0}/tmp/noloci/noloci_score.txt',header = TRUE, sep='\t');\n"
           "connames(data) <- c('NCBI','PD','GD','Class');\n"
           "p <- ggplot(data,aes(x=GD,y=PD)) + aes(shape=Class) + geom_point(aes(colour=Class)) + theme_bw();\n"
           "q <- p + theme(axis.title.x = element_text(size=18,colour = 'black'),axis.title.y = element_text(size=18,colour = 'black'),axis.text.x = element_text(size=18,colour = 'black',angle = 45, vjust = 0.5, hjust = 0.5),axis.text.y = element_text(size=18,colour = 'black'),legend.title=element_text(colour = 'black',size = 18),legend.text = element_text(color = 'black',size=18));\n"
           "q + guides(fill=guide_legend(title = NULL));\n"
           "ggsave('{0}/tmp/noloci/fig/noloci_s.png',width = 4.5,height = 5.5)".format(rd))
    os2 = os.system("Rscript {0}/tmp/rscript/noloci_s.r".format(rd))
    if os2:
        exit("[{0}] Please Check noloci_s.r\n".format(ltime()))
    else:
        sys.stdout.write("[{0}] Draw figure noloci_s.png successfully\n".format(ltime()))

    out3.write("library(ggplot2);\n"
           "data <- read.table('{0}/tmp/noloci/loci_identity.txt',header = TRUE, sep='\t');\n"
           "connames(data) <- c('NCBI','PD','GD','Class');\n"
           "p <- ggplot(data,aes(x=GD,y=PD)) + aes(shape=Class) + geom_point(aes(colour=Class)) + theme_bw();\n"
           "q <- p + theme(axis.title.x = element_text(size=18,colour = 'black'),axis.title.y = element_text(size=18,colour = 'black'),axis.text.x = element_text(size=18,colour = 'black',angle = 45, vjust = 0.5, hjust = 0.5),axis.text.y = element_text(size=18,colour = 'black'),legend.title=element_text(colour = 'black',size = 18),legend.text = element_text(color = 'black',size=18));\n"
           "q + guides(fill=guide_legend(title = NULL));\n"
           "ggsave('{0}/tmp/noloci/fig/loci_i.png',width = 4.5,height = 5.5)".format(rd))
    os3 = os.system("Rscript {0}/tmp/rscript/loci_i.r".format(rd))
    if os3:
        exit("[{0}] Please Check loci_i.r\n".format(ltime()))
    else:
        sys.stdout.write("[{0}] Draw figure loci_i.png successfully\n".format(ltime()))
    
    out4.write("library(ggplot2);\n"
           "data <- read.table('{0}/tmp/noloci/loci_score.txt',header = TRUE, sep='\t');\n"
           "connames(data) <- c('NCBI','PD','GD','Class');\n"
           "p <- ggplot(data,aes(x=GD,y=PD)) + aes(shape=Class) + geom_point(aes(colour=Class)) + theme_bw();\n"
           "q <- p + theme(axis.title.x = element_text(size=18,colour = 'black'),axis.title.y = element_text(size=18,colour = 'black'),axis.text.x = element_text(size=18,colour = 'black',angle = 45, vjust = 0.5, hjust = 0.5),axis.text.y = element_text(size=18,colour = 'black'),legend.title=element_text(colour = 'black',size = 18),legend.text = element_text(color = 'black',size=18));\n"
           "q + guides(fill=guide_legend(title = NULL));\n"
           "ggsave('{0}/tmp/noloci/fig/loci_s.png',width = 4.5,height = 5.5)".format(rd))
    os4 = os.system("Rscript {0}/tmp/rscript/loci_s.r".format(rd))
    if os4:
        exit("[{0}] Please Check loci_s.r\n".format(ltime()))
    else:
        sys.stdout.write("[{0}] Draw figure loci_s.png successfully\n".format(ltime()))

def main():
    args = opt()
    if args.out1 == None or args.out2 == None or args.com == None:
        os.system("python {0} -h".format(sys.argv[0]))
        exit("[{0}]Error:Incomplete Options\n".format(ltime()))

    pac = args.out1
    ann = args.out2
    com = args.com
    noloci(pac,ann)
    loci(pac,ann,com)
    draw_point()

if __name__ == '__main__':
    main()
