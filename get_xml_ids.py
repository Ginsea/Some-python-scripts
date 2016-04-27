#!/usr/bin/env python

'''
@Description This script can be used to extract ids which have hits in blast xml file
@Usage:
      python get_xml_ids.py --xml xmlfile --hits hitsids.txt --nohits nohitsids.txt
'''

import argparse
import os
import sys

def parse_args():
    parser = argparse.ArgumentParser(usage="%(prog)s[options]")
    parser.add_argument("--xml",help="Your xml file")
    parser.add_argument("--hits",help="A txt file contained ids with hits")
    parser.add_argument("--nohits",help="A txt file contained ids without hits")
    return parser.parse_args()

def get_ids(xml,hits,nohits):
    in_xml = open(xml,"r")
    xml_read = in_xml.read()
    xml_split = xml_read.split("<Iteration>")
    xml_len = len(xml_split)
    out1 = open(hits,"w")
    out2 = open(nohits,"w")
    for i in range(1,xml_len):
        if "No hits found" in xml_split[i]:
            out2.write("%s\n"%(xml_split[i].split("\n")[3].split(">")[1].split("<")[0].split()[0]))
        else:
            out1.write("%s\n"%(xml_split[i].split("\n")[3].split(">")[1].split("<")[0].split()[0]))

def main():
    args = parse_args()

    if args.xml == None or args.hits == None or args.nohits == None:
        os.system("python %s -h"%sys.argv[0])
        exit(1)

    get_ids(args.xml,args.hits,args.nohits)

if __name__ == "__main__":
    main()
