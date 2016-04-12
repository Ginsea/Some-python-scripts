#!/usr/bin/env python

'''
@Description This script can be used to get command line file for exonerate software, and then you can run it in multiple threads
@Author This script was developed by Ginsea Chen (ginseachen@hotmail.com) of CATAS
@Usage python %[prog]s --query query.fa --taget target.fa --num [NUM] --out commands.txt
'''
import argparse

def parse_args():
    parser = argparse.ArgumentParser(usage="%(prog)s[options]")
    parser.add_argument("--query",default="query.fa",help="The query file")
    parser.add_argument("--target",default="target.fa",help="The target file")
    parser.add_argument("--num", default=100, type=int,help="how many parts you want to split")
    parser.add_argument("--out", default="command.txt",help="outfile")
    return parser.parse_args()

def main():
    argse = parse_args()
    out = open(argse.out,"w")
    for i in range(1,(int(argse.num) + 1)):
        out.write("exonerate --model protein2genome -q %s -t %s --showtargetgff T --showalignment F --showvulgar F --showcigar F --ryo F --targetchunkid %d --targetchunktotal %d > %s_%d.exonerate\n"%(argse.query,argse.target,i,int(argse.num),argse.query.split(".")[0],i))

if __name__ == "__main__":
    main()
