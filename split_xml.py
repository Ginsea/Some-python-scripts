#!/usr/bin/env python
'''
@Description This script can be used to split large xml file of blast
@Author This script is developed by Ginsea Chen (ginseachen@hotmail.com) in CATAS
@Usage python split_xml.py --xml blast.xml --num [NUM]
'''
import os
import argparse
import os.path

def parse_args():
    parser = argparse.ArgumentParser(usage="%(prog)s[options]")
    parser.add_argument("--xml",default="blast.xml",help="Your blast output file with xml format (outfmt 5)")
    parser.add_argument("--num",default=1000, type=int,help="how many seqs in a split file")
    return parser.parse_args()

def split_xml(xml,num):
    fp = open(xml)
    inf = fp.read()
    ml = inf.split("<Iteration>")
    y = len(ml) / int(num)
    os.system("mkdir split")
    i = 1
    while i <= y:
        if i < y:
            out = open("split/%s.xml"%i,"w")
            out.write("%s"%ml[0].rstrip())
            for x in range(int(num)*(i-1),int(num)*i):
                out.write("\n<Iteration>\n%s"%ml[x+1].strip())
            out.write("\n</BlastOutput_iterations>\n")
            out.write("</BlastOutput>")
        elif i == y:
            out = open("split/%s.xml"%i,"w")
            out.write("%s\n"%ml[0].rstrip())
            for x in range(int(num)*(i - 1),len(ml) - 1):
                out.write("\n<Iteration>\n%s\n"%ml[x+1].strip())
        i += 1

def main():
    argser = parse_args()
    split_xml(argser.xml,int(argser.num))

if __name__ == "__main__":
    main()
