#!/usr/bin/env python
'''
@Descriptions This script can be used to produce EVM weights file
@Author This script was developed by Ginsea Chen of CATAS (ginseachen@hotmail.com)
@Usage: --denovo The absolute path of folder contained all gff3 files from de novo prediction
        --protein The absolute path of folder contained all gff3 files from protein alignment
        --transcript The absolute path of folder contained all gff3 files from transcript alignment
'''

import os,os.path
import argparse
import sys

def parse_args():
    parser = argparse.ArgumentParser(usage="%(prog)s[options]")
    parser.add_argument("--denovo",help="The AP of de novo file")
    parser.add_argument("--protein",help="The AP of protein file")
    parser.add_argument("--transcript",help="The AP of transcript file")
    return parser.parse_args()

def get_label(path,gff3):
    infile = open("%s%s"%(path,gff3),"r")
    i = 1
    label = ""
    while i:
        line = infile.readline()
        if "#" in line or len(line.split()) < 8:
            pass
        else:
            label += line.split()[1]
            i = i - 1
    return label


def de_novo(denovo,out):
    for p1s, d1s, f1s in os.walk(denovo):
        for f1 in f1s:
            if f1[-4:] == "gff3":
                weights = raw_input("\nIf %s is your target file, enter the weights value, else enter pass:"%f1)
                if weights == "pass":
                    pass
                else:
                    out.write("ABINITIO_PREDICTION\t%s\t%d\n"%(str(get_label(denovo,f1)),int(weights)))

def protein(pro,out):
    for p1s, d1s, f1s in os.walk(pro):
        for f1 in f1s:
            if f1[-4:] == "gff3":
                weights = raw_input("\nIf %s is your target file, enter the weights value, else enter pass:"%f1)
                if weights == "pass":
                    pass
                else:
                    out.write("PROTEIN\t%s\t%d\n"%(str(get_label(pro,f1)),int(weights)))

def transcript(transcript,out):
    for p1s, d1s, f1s in os.walk(transcript):
        for f1 in f1s:
            if f1[-4:] == "gff3":
                weights = raw_input("\nIf %s is your target file, enter the weights value, else enter pass:"%f1)
                if weights == "pass":
                    pass
                else:
                    out.write("TRANSCRIPT\t%s\t%d\n"%(str(get_label(transcript,f1)),int(weights)))

def main():
    agrse = parse_args()

    if agrse.denovo == None or agrse.protein == None or agrse.transcript == None:
        os.system("python %s -h"%sys.argv[0])
        exit(1)

    out = open("weights.txt","w")
    de_novo(agrse.denovo,out)
    protein(agrse.protein,out)
    transcript(agrse.transcript,out)

if __name__ == "__main__":
    main()
