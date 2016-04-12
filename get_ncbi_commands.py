#!/usr/bin/env python

'''
@Description This script can be used to produce command file for NCBIWWW blasting
'''

import os
import os.path
import argparse

def parse_args():
    parser = argparse.ArgumentParser(usage="%(prog)s[options]")
    parser.add_argument("--path",help="The path for ncbiRemoteblast.py")
    return parser.parse_args()

def get_file(path):
    rootdir = os.getcwd()
    splitdir = "%s/split"%rootdir
    out = open("commands.txt","w")
    for parent, dirnames, filenames in os.walk(splitdir):
        for filename in filenames:
            if filename[-2:] == "fa":
                out.write("python %s --fasta %s/%s --type prot\n"%(path,splitdir,filename))

def main():
    argese = parse_args()
    get_file(argese.path)

if __name__ == "__main__":
    main()
